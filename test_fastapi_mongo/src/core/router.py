from fastapi import APIRouter

from api import employee


api_router = APIRouter()


api_router.include_router(employee.router, prefix='/api/employee', tags=['employee'])
