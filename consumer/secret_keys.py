from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class SecretKeys(BaseSettings):
    REGION_NAME: str = ""
    AWS_SQS_VIDEO_PROCESSING: str = ""
    
