from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, ideas, index, users

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/access-tokens",
    tags=["access-tokens"],
)

api_router.include_router(ideas.router, prefix="/ideas", tags=["ideas"])

api_router.include_router(users.router, tags=["users"])

api_router.include_router(
    index.router,
    tags=["index"],
)
