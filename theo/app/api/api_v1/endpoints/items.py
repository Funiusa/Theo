from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status, Depends
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from app.api import deps, schemas, crud

router = APIRouter(
    dependencies=[Depends(deps.get_current_active_user)]
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Item])
def get_items(
        skip: int = 0,
        limit: int = 100,
        session: Session = Depends(deps.get_session),
) -> List[schemas.Technology]:
    items = crud.item.get_multi(db=session, skip=skip, limit=limit)
    return items


@router.get(
    "/{item_id}", status_code=status.HTTP_200_OK, response_model=schemas.Item
)
def retrieve_item(
        *, item_id: int, session: Session = Depends(deps.get_session),
) -> schemas.Item:
    item = crud.item.get(db=session, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return item


@router.put("/{item_id}", status_code=status.HTTP_200_OK, response_model=schemas.Item)
def update_item(
        *,
        item_id: int,
        item_in: schemas.ItemUpdate,
        session: Session = Depends(deps.get_session),
) -> schemas.Item:
    item = crud.item.get(db=session, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    try:
        updated_item = crud.item.update(
            session, db_obj=item, obj_in=item_in
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="This item name already exists"
        )
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item(
        *,
        item_id: int,
        session: Session = Depends(deps.get_session),
) -> None:
    item = crud.item.get(session, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    crud.item.remove(db=session, id=item_id)
