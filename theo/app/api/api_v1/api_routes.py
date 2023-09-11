from app.api.api_v1.endpoints import login, logout, users, technologies, items

from fastapi.routing import APIRouter

api_router = APIRouter()

api_router.include_router(router=login.router, tags=["Login"])
api_router.include_router(router=logout.router, tags=["Logout"])

api_router.include_router(router=users.router, tags=["Users"], prefix="/users")
api_router.include_router(
    router=technologies.router, tags=["Technologies"], prefix="/technologies"
)
api_router.include_router(
    router=items.router, tags=["Items"], prefix="/items"
)
