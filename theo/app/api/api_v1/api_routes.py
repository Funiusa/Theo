from app.api.api_v1.endpoints import login, logout, users, cribblies, crabbles, booms

from fastapi.routing import APIRouter

api_router = APIRouter()

api_router.include_router(router=login.router, tags=["Login"])
api_router.include_router(router=logout.router, tags=["Logout"])

api_router.include_router(router=users.router, tags=["Users"], prefix="/users")
api_router.include_router(router=cribblies.router, tags=["Cribbly"])
api_router.include_router(router=crabbles.router, tags=["Crabble"])
api_router.include_router(router=booms.router, tags=["Booms"])
