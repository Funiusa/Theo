import os.path
from shortuuid import uuid
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status, Depends, UploadFile, File, BackgroundTasks
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from app.api import deps, schemas, crud, models
from app.core.config import settings
from app.core import s3
from app.core.utility import create_image

# router = APIRouter(dependencies=[Depends(deps.get_current_active_user)])


router = APIRouter()


@router.get(
    "/cribblies", status_code=status.HTTP_200_OK, response_model=List[schemas.Cribbly]
)
async def get_cribblies(
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

    cribbly = crud.cribbly.get_multi(db=session, skip=skip, limit=limit)
    return cribbly


@router.post(
    "/users/{user_id}/cribblies",
    status_code=status.HTTP_201_CREATED,
)
async def create_cribbly(
    *,
    title: str,
    description: str,
    image: UploadFile = File(""),
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_user),
    background_tacks: BackgroundTasks,
) -> schemas.Cribbly:
    try:
        filename = f"{uuid()}"
        if not image:
            filename += f"_crib.png"
            image_file = create_image(caption=title)
        else:
            suffix = os.path.splitext(image.filename)[1]
            filename += f"_clib{suffix}"
            image_file = image.file
        image_path = f"{settings.AWS_BUCKET_FOLDER}/{current_user.id}/{filename}"

        background_tacks.add_task(s3.upload_obj, image_file, image_path)

        cribbly_in = schemas.CribblyCreate(
            title=title, description=description, image=image_path
        )

        cribbly = crud.cribbly.create_with_owner(
            db=session, obj_in=cribbly_in, owner_id=current_user.id
        )
        return cribbly

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This cribbly already exists",
        )


@router.get(
    "/users/{user_id}/cribblies",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Cribbly],
)
async def get_cribblies(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> List[schemas.Cribbly]:
    cribblies = crud.cribbly.get_multi_by_owner(
        db=session, owner_id=current_user.id, skip=skip, limit=limit
    )
    return cribblies


@router.get(
    "/users/{user_id}/cribblies/{cribbly_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Cribbly,
)
def retrieve_cribbly(
    *,
    cribbly_id: int,
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> schemas.Cribbly:
    cribbly = crud.cribbly.get(session, id=cribbly_id)
    if not cribbly:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cribbly not found"
        )
    if not current_user.is_superuser or current_user.id != cribbly.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User have not enough permissions",
        )
    return cribbly


@router.put(
    "/users/{user_id}/cribblies/{cribbly_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Cribbly,
)
def update_cribbly(
    *,
    cribbly_id: int,
    title: str,
    description: str,
    image: UploadFile = File(""),
    session: Session = Depends(deps.get_session),
    current_user: models.User = Depends(deps.get_current_active_user),
    background_tasks: BackgroundTasks,
) -> schemas.Cribbly:
    cribbly = crud.cribbly.get(db=session, id=cribbly_id)
    if not cribbly:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cribbly not found"
        )
    if not current_user.is_superuser or current_user.id != cribbly.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User have not enough permissions",
        )
    try:
        image_path = cribbly.image
        if image:
            background_tasks.add_task(s3.remove_obj, image_path)
            suffix = os.path.splitext(image.filename)[1]
            filename = f"{uuid()}_clib{suffix}"
            image_path = f"{settings.AWS_BUCKET_FOLDER}/{current_user.id}/{filename}"
            background_tasks.add_task(s3.upload_obj, image.file, image_path)

        cribbly_in = schemas.CribblyUpdate(
            title=title, description=description, image=image_path
        )
        updated_cribbly = crud.cribbly.update(
            session, db_obj=cribbly, obj_in=cribbly_in
        )
        return updated_cribbly
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This cribbly already exists",
        )


@router.delete(
    "/users/{user_id}/cribblies/{cribbly_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_cribbly(
    *,
    cribbly_id: int,
    session: Session = Depends(deps.get_session),
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> None:
    cribbly = crud.cribbly.get(session, id=cribbly_id)
    if not cribbly:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cribbly not found"
        )
    if not current_user.is_superuser or current_user.id != cribbly.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User have not enough permissions",
        )
    background_tasks.add_task(s3.remove_obj, cribbly.image)
    background_tasks.add_task(
        s3.remove_folder, f"{settings.AWS_BUCKET_FOLDER}/{cribbly_id}/"
    )
    crud.cribbly.remove(db=session, id=cribbly_id)
