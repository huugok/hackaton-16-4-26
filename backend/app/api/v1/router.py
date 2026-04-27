from fastapi import APIRouter
from app.api.v1.endpoints import assessments, doctor, users

api_router = APIRouter

api_router.include_router(
    assessments.router,
    prefix="/assessments",
    tags= [assessments]
)