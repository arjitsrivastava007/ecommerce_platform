from fastapi import APIRouter, Depends
from app.api.v1.controller import ecommerce_controller
from app.middlewares.authentication import auth_middleware

api_router = APIRouter()

api_router.include_router(
    ecommerce_controller.router,
    prefix="/ecommerce",
    tags=["Ecommerce"],
    dependencies=[Depends(auth_middleware)]
)
