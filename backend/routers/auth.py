from helper.auth_helper import get_secret_hash
from pydantic_models.auth_models import SignupRequest
from fastapi import APIRouter
import boto3
from secret_keys import SecretKeys

router = APIRouter()
sectet_keys = SecretKeys()

COGNITO_CLIENT_ID = sectet_keys.COGNITO_CLIENT_ID
COGNITO_CLIENT_SECRET = sectet_keys.COGNITO_CLIENT_SECRET
REGION_NAME = sectet_keys.REGION_NAME


cognito_client = boto3.client("cognito-idp", region_name="ap-south-1")

@router.post("/signup")
def signup_user(data: SignupRequest):

    secret_hash = get_secret_hash(data.email, COGNITO_CLIENT_ID, COGNITO_CLIENT_SECRET)

    cognito_response = cognito_client.sign_up(
        ClientId=COGNITO_CLIENT_ID,
        Username=data.email,
        Password=data.password,
        SecretHash=secret_hash,
        UserAttributes=[
            {"Name": "email", "Value": data.email},
            {"Name": "name", "Value": data.name},
        ],
        
    )
    return {"msg": "User signed up successfully, Please Verify your email if required "}