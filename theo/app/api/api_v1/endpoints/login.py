from datetime import timedelta
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from fastapi import Depends, status
from sqlalchemy.orm import Session
from app.api import schemas
from app.api.deps import get_session
from app.core.config import settings
from app.core import security, celery
from app.api import crud

router = APIRouter()


@router.post("/login/", response_model=schemas.Token)
async def login_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_session),
):
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid username or password",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await security.create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    return {"token_type": "bearer", "access_token": access_token}
