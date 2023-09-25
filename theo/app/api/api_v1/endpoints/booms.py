from typing import List
import os
from shortuuid import uuid
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status, Depends, BackgroundTasks, UploadFile, File
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from app.api import deps, schemas, crud, models
from app.core import s3
from app.core.utility import create_image
from app.core.config import settings

router = APIRouter()
prefix = "/users/{user_id}/cribblies/{cribbly_id}/crabbles/{crabble_id}"


@router.get("/booms", status_code=status.HTTP_200_OK, response_model=List[schemas.Boom])
def get_booms(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> List[schemas.Boom]:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User have not enough permissions",
        )
    booms = crud.boom.get_multi(db=session, skip=skip, limit=limit)
    return booms


@router.post(
    prefix + "/booms",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Boom,
)
async def create_boom(
    *,
    name: str,
    body: str,
    crabble_id: int,
    image: UploadFile = File(""),
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_user),
    background_tacks: BackgroundTasks,
) -> schemas.Boom:
    crabble = crud.crabble.get(db=session, id=crabble_id)
    if not crabble:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Crabble not found"
        )
    if not current_user.is_superuser or current_user.id != crabble.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User have not enough permissions",
        )
    try:
        filename = f"{uuid()}_{crabble_id}_boom"
        if not image:
            filename += ".png"
            image_file = create_image(caption=name)
        else:
            suffix = os.path.splitext(image.filename)[1]
            filename += suffix
            image_file = image.file

        image_path = f"{settings.AWS_BUCKET_FOLDER}/{current_user.id}/{crabble.cribbly_id}/{crabble_id}/{filename}"
        background_tacks.add_task(s3.upload_obj, image_file, image_path)
        boom_in = schemas.CrabbleCreate(name=name, body=body, image=image_path)
        boom = crud.boom.create_with_crabble(
            session, obj_in=boom_in, crabble_id=crabble_id, owner_id=current_user.id
        )
        return boom
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This boom already exists",
        )


@router.get(
    prefix + "/booms",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Boom],
)
def get_booms(
    crabble_id: int,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    crabble = crud.crabble.get(session, id=crabble_id)
    if not crabble:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Crabble not found"
        )
    if not current_user.is_superuser or current_user.id != crabble.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can get only your own booms",
        )
    booms = crud.boom.get_multi_by_crabble(
        session, crabble_id=crabble_id, skip=skip, limit=limit
    )
    return booms


@router.get(
    prefix + "/booms/{boom_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Boom,
)
def retrieve_boom(
    *,
    boom_id: int,
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> schemas.Boom:
    boom = crud.boom.get(db=session, id=boom_id)
    if not boom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Boom not found"
        )
    if not current_user.is_superuser or current_user.id != boom.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can get only your own boom",
        )
    return boom


@router.put(
    prefix + "/booms/{boom_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Boom,
)
def update_boom(
    *,
    name: str,
    body: str,
    boom_id: int,
    image: UploadFile = File(""),
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_user),
    background_tasks: BackgroundTasks,
) -> schemas.Boom:
    boom = crud.boom.get(db=session, id=boom_id)
    if not boom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Boom not found"
        )
    if not current_user.is_superuser or current_user.id != boom.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can update your own boom"
        )
    try:
        image_path = boom.image
        if image:
            background_tasks.add_task(s3.remove_obj, image_path)
            suffix = os.path.splitext(image.filename)[1]
            filename = f"{uuid()}_{boom.crabble_id}{suffix}"
            image_path = image_path.replace(image_path.split("/")[-1], filename)
            background_tasks.add_task(s3.upload_obj, image.file, image_path)

        boom_in = schemas.BoomUpdate(name=name, body=body, image=image_path)
        updated_boom = crud.boom.update(session, db_obj=boom, obj_in=boom_in)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This boom name already exists",
        )
    return updated_boom


@router.delete(prefix + "/booms/{boom_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_boom(
    *,
    boom_id: int,
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_user),
    background_tasks: BackgroundTasks,
) -> None:
    boom = crud.booms.get(session, id=boom_id)
    if not boom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Boom not found"
        )
    if not current_user.is_superuser or current_user.id != boom.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You can remove you own boom"
        )
    background_tasks.add_task(s3.remove_obj, boom.image)
    crud.boom.remove(db=session, id=boom_id)
