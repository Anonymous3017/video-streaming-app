from db.models.video import ProcessingStatus, Video, VisibilityStatus
from fastapi import APIRouter, Depends, HTTPException
from db.db import get_db
from db.middleware.auth_middleware import get_current_user
from sqlalchemy.orm import Session
from sqlalchemy import or_


router = APIRouter()


@router.get("/all")
def get_all_videos(
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    all_videos = (
        db.query(Video)
        .filter(
            Video.is_processing == ProcessingStatus.COMPLETED,
            Video.visibility == VisibilityStatus.PUBLIC,
        )
        .all()
    )
    return all_videos


@router.get("/")
def get_video_info(
    video_id: str,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    video = (
        db.query(Video)
        .filter(
            Video.id == video_id,
            # Video.is_processing == ProcessingStatus.COMPLETED,
            or_(
                Video.visibility == VisibilityStatus.PUBLIC,
                Video.visibility == VisibilityStatus.UNLISTED,
            ),
        )
        .first()
    )
    return video
