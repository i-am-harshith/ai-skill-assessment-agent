from fastapi import APIRouter

from app.api.routes_catalog import router as catalog_router
from app.api.routes_workflow import router as workflow_router

api_router = APIRouter()
api_router.include_router(catalog_router, tags=["catalog"])
api_router.include_router(workflow_router, tags=["workflow"])
