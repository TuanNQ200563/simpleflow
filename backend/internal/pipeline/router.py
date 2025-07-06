import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.models.pipeline import Pipeline
from backend.middleware.auth import require_access_token
from backend.middleware.db import get_master_db


router = APIRouter()


@router.get("/", response_model=list[Pipeline])
def get_pipelines(db: Session = Depends(get_master_db), user: User = Depends(require_access_token)):
    try:
        query = select(Pipeline).where(Pipeline.user_id == user.id)
        result = db.execute(query).scalars().all()
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/", response_model=Pipeline)
def create_pipeline(pipeline: Pipeline, db: Session = Depends(get_master_db), user: User = Depends(require_access_token)):
    try:
        pipeline.user_id = user.id
        db.add(pipeline)
        db.commit()
        db.refresh(pipeline)
        return pipeline
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

   
@router.get("/{id}", response_model=Pipeline)
def get_pipeline(id: str, db: Session = Depends(get_master_db), user: User = Depends(require_access_token)):
    try:
        pipeline_id = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid pipeline ID format")

    try:
        query = select(Pipeline).where(Pipeline.id == pipeline_id, Pipeline.user_id == user.id)
        result = db.execute(query).scalars().first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pipeline not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))