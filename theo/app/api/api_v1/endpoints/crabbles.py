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
from app.core.config import settings
from app.core.utility import create_image

router = APIRouter()
prefix = "/users/{user_id}/cribblies/{cribbly_id}"


@router.get(
    "/crabbles", status_code=status.HTTP_200_OK, response_model=List[schemas.Crabble]
)
def get_crabbles(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> List[schemas.Cribbly]:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User have not enough permissions",
        )

    crabble = crud.crabble.get_multi(db=session, skip=skip, limit=limit)
    return crabble


@router.post(
    f"{prefix}/crabbles",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Crabble,
)
async def create_crabble(
    *,
    name: str,
    body: str,
    cribbly_id: int,
    image: UploadFile = File(""),
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_user),
    background_tacks: BackgroundTasks,
) -> schemas.Crabble:
    cribbly = crud.cribbly.get(db=session, id=cribbly_id)
    if not cribbly:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cribbly not found"
        )
    if not current_user.is_superuser or current_user.id != cribbly.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can create crabbly from your own cribbly",
        )
    try:
        filename = f"{uuid()}_{cribbly_id}_crabble"
        if not image:
            filename += ".png"
            image_file = create_image(caption=name)
        else:
            suffix = os.path.splitext(image.filename)[1]
            filename += suffix
            image_file = image.file

        upload_path = (
            f"{settings.AWS_BUCKET_FOLDER}/{current_user.id}/{cribbly_id}/{filename}"
        )
        background_tacks.add_task(s3.upload_obj, image_file, upload_path)
        crabble_in = schemas.CrabbleCreate(name=name, body=body, image=upload_path)
        crabble = crud.crabble.create_with_cribbly(
            session, obj_in=crabble_in, cribbly_id=cribbly_id, owner_id=current_user.id
        )
        return crabble
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This crabble already exists",
        )


@router.get(
    prefix + "/crabbles",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Crabble],
)
def get_crabbles(
    cribbly_id: int,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    cribbly = crud.cribbly.get(session, id=cribbly_id)
    if not cribbly:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cribbly not found"
        )
    if not current_user.is_superuser or current_user.id != cribbly.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can get only your own crabbles",
        )
    crabbles = crud.crabble.get_multi_by_cribbly(
        session, cribbly_id=cribbly_id, skip=skip, limit=limit
    )
    return crabbles


@router.get(
    prefix + "/crabbles/{crabble_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Crabble,
)
def retrieve_crabble(
    *,
    crabble_id: int,
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> schemas.Crabble:
    crabble = crud.crabble.get(db=session, id=crabble_id)
    if not crabble:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Crabble not found"
        )
    if not current_user.is_superuser or current_user.id != crabble.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can retrieve only your own crabble",
        )
    return crabble


@router.put(
    prefix + "/crabbles/{crabble_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Crabble,
)
def update_crabble(
    *,
    crabble_id: int,
    name: str,
    body: str,
    image: UploadFile = File(""),
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_user),
    background_tasks: BackgroundTasks,
) -> schemas.Crabble:
    crabble = crud.crabble.get(db=session, id=crabble_id)
    if not crabble:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Crabble not found"
        )
    if not current_user.is_superuser or current_user.id != crabble.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can update only your own crabble",
        )
    try:
        image_path = crabble.image
        if image:
            background_tasks.add_task(s3.remove_obj, image_path)
            suffix = os.path.splitext(image.filename)[1]
            filename = f"{uuid()}_{crabble.cribbly_id}_clabble{suffix}"
            image_path = image_path.replace(image_path.split("/")[-1], filename)
            background_tasks.add_task(s3.upload_obj, image.file, image_path)

        crabble_in = schemas.CrabbleUpdate(name=name, body=body, image=image_path)
        updated_crabble = crud.crabble.update(
            session, db_obj=crabble, obj_in=crabble_in
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This crabble name already exists",
        )
    return updated_crabble


@router.delete(
    prefix + "/crabbles/{crabble_id}", status_code=status.HTTP_204_NO_CONTENT
)
def remove_crabble(
    *,
    crabble_id: int,
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_user),
    background_tasks: BackgroundTasks,
) -> None:
    crabble = crud.crabble.get(session, id=crabble_id)
    if not crabble:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Crabble not found"
        )
    if not current_user.is_superuser or current_user.id != crabble.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User have not enough permissions",
        )
    background_tasks.add_task(s3.remove_obj, crabble.image)
    crud.crabble.remove(db=session, id=crabble_id)
