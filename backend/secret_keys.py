from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class SecretKeys(BaseSettings):
    COGNITO_CLIENT_ID: str = ""
    COGNITO_CLIENT_SECRET: str = ""
    REGION_NAME: str = ""
    POSTGRES_DB_URL: str = ""
    AWS_RAW_VIDEOS_BUCKET: str = ""
    AWS_VIDEO_THUMBNAIL_BUCKET: str = ""
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    REDIS_DB_HOST: str = ""
    REDIS_DB_PORT: int = 0
    REDIS_DB_PASSWORD: str = ""
    
    
