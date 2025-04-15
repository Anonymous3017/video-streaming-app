import json
from db.models.video import ProcessingStatus, Video, VisibilityStatus
from fastapi import APIRouter, Depends, HTTPException
from db.db import get_db
from db.middleware.auth_middleware import get_current_user
from sqlalchemy.orm import Session
from sqlalchemy import or_
from db.redis_db import redis_client


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
    cache_key = f"video:{video_id}"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        print("Cache hit")
        print(cached_data)
        return json.loads(cached_data)
    video = (
        db.query(Video)
        .filter(
            Video.id == video_id,
            Video.is_processing == ProcessingStatus.COMPLETED,
            or_(
                Video.visibility == VisibilityStatus.PUBLIC,
                Video.visibility == VisibilityStatus.UNLISTED,
            ),
        )
        .first()
    )

    redis_client.setex(
        cache_key,
        3600,
        json.dumps(video.to_dict()),
    )
    return video
