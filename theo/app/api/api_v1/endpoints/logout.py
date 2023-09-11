from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from fastapi import Depends, status, responses, Request
from sqlalchemy.orm import Session
from app.api.deps import get_session, oauth2schema, get_current_user
from app.api import crud, models, schemas
import jwt
from app.core.config import settings
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/logout")
async def logout(response: JSONResponse):
    response.delete_cookie(key="access_token")
    return {"message": "User logout"}
