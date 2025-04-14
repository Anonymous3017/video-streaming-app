from db.models.video import Video
from fastapi import APIRouter, Depends, HTTPException
from pydantic_models.upload_models import UploadMetadata
from sqlalchemy.orm import Session
from db.db import get_db
from db.middleware.auth_middleware import get_current_user
from secret_keys import SecretKeys
import boto3
import uuid

secret_keys = SecretKeys()

router = APIRouter()

s3_client = boto3.client(
    "s3",
    region_name=secret_keys.REGION_NAME,
)


@router.get("/url")
def get_presigned_url(user=Depends(get_current_user)):
    try:
        video_id = f"videos/{user['sub']}/{uuid.uuid4()}"
        print(video_id)
        response = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": secret_keys.AWS_RAW_VIDEOS_BUCKET,
                "Key": video_id,
                "ContentType": "video/mp4",
            },
        )
        print(response)
        return {
            "url": response,
            "video_id": video_id,
        }
    # print the exception
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate presigned URL: {e}",
        ) from e


@router.get("/url/thumbnail")
def get_presigned_url_thumbnail(user=Depends(get_current_user)):
    try:
        thumbnail_id = f"{user['sub']}/{uuid.uuid4()}"
        print(thumbnail_id)
        response = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": secret_keys.AWS_VIDEO_THUMBNAIL_BUCKET,
                "Key": thumbnail_id,
                "ContentType": "image/*",
            },
        )
        print(response)
        return {
            "url": response,
            "thumbnail_id": thumbnail_id,
        }
    # print the exception
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate presigned URL: {e}",
        ) from e


@router.post("/metadata")
def upload_metadata(
    metadata: UploadMetadata,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_video = Video(
        id=metadata.video_id,
        title=metadata.title,
        description=metadata.description,
        video_s3_key=metadata.video_s3_key,
        visibility=metadata.visibility,
        user_id=user["sub"],
    )

    db.add(new_video)
    db.commit()
    db.refresh(new_video)
    return new_video
