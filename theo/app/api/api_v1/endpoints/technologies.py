from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status, Depends, Body, Form
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from app.api import deps, schemas, crud, models

router = APIRouter(
    dependencies=[Depends(deps.get_current_active_user)]
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Technology])
def get_technology(
        skip: int = 0,
        limit: int = 100,
        session: Session = Depends(deps.get_session),
) -> List[schemas.Technology]:
    technologies = crud.technology.get_multi(db=session, skip=skip, limit=limit)
    return technologies


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Technology)
async def create_technology(
        *,
        technology: schemas.TechnologyCreate,
        session: Session = Depends(deps.get_session),
) -> schemas.Technology:
    try:
        technology = crud.technology.create(session, obj_in=technology)
        return technology
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This technology already exists"
        )


@router.put(
    "/{technology_id}", status_code=status.HTTP_200_OK, response_model=schemas.Technology
)
def update_technology(
        *,
        technology_id: int,
        technology_in: schemas.TechnologyUpdate,
        session: Session = Depends(deps.get_session),
) -> schemas.Technology:
    technology = crud.technology.get(db=session, id=technology_id)
    if not technology:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Technology not found"
        )
    try:
        updated_technology = crud.technology.update(
            session, db_obj=technology, obj_in=technology_in
        )
        return updated_technology
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This technology already exists"
        )


@router.get(
    "/{technology_id}", status_code=status.HTTP_200_OK, response_model=schemas.Technology
)
def retrieve_technology(
        *,
        technology_id: int,
        session: Session = Depends(deps.get_session),
) -> schemas.Technology:
    technology = crud.technology.get(session, id=technology_id)
    if not technology:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Technology not found"
        )
    return technology


@router.delete("/{technology_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_technology(
        *,
        technology_id: int,
        session: Session = Depends(deps.get_session),
) -> None:
    technology = crud.technology.get(session, id=technology_id)
    if not technology:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Technology not found"
        )
    crud.technology.remove(db=session, id=technology_id)


@router.get(
    "/{technology_id}/items", status_code=status.HTTP_200_OK,
    response_model=List[schemas.Item]
)
def get_technology_items(
        technology_id: int,
        skip: int = 0,
        limit: int = 100,
        session: Session = Depends(deps.get_session),
):
    technology = crud.technology.get(session, id=technology_id)
    if not technology:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Technology not found"
        )
    items = crud.item.get_multi_by_technology(
        session, technology_id=technology_id, skip=skip, limit=limit
    )
    return items


@router.post("/{technology_id}/items", status_code=status.HTTP_201_CREATED,
             response_model=schemas.Item)
async def create_technology_item(
        *,
        technology_id: int,
        item_in: schemas.ItemCreate,
        session: Session = Depends(deps.get_session),
) -> schemas.Item:
    technology = crud.technology.get(db=session, id=technology_id)
    if not technology:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Technology not found"
        )
    try:
        item = crud.item.create_with_technology(
            session, obj_in=item_in, technology_id=technology_id
        )
        return item
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This technology already exists"
        )
