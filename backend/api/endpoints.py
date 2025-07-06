from fastapi import APIRouter

from backend.internal.oauth.router import router as oauth_router
from backend.internal.pipeline.router import router as pipeline_router
from backend.internal.user.router import router as user_router

from backend.utils.routes import use_route_names_as_operation_ids


router = APIRouter(prefix="/api", tags=["api"])

router.include_router(oauth_router, prefix="/oauth", tags=["oauth"])
router.include_router(user_router, prefix="/user", tags=["user"])
router.include_router(pipeline_router, prefix="/pipeline", tags=["pipeline"])

use_route_names_as_operation_ids(router)