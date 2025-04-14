from fastapi import APIRouter, Depends, HTTPException
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
