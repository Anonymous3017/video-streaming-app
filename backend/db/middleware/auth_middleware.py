import logging
from fastapi import HTTPException, Cookie
import boto3
from secret_keys import SecretKeys

cognito_client = boto3.client("cognito-idp", region_name=SecretKeys().REGION_NAME)

# def _get_user_from_cognito(access_token: str):
#     try:
#         user_res = cognito_client.get_user(
#             AccessToken=access_token
#         )

#         return user_res
#     except Exception as e:
#         raise HTTPException (500, "Error fetching user")

def _get_user_from_cognito(access_token: str):
    try:
        user_res = cognito_client.get_user(AccessToken=access_token)
        return {
            attr["Name"]: attr["Value"] for attr in user_res.get("UserAttributes", [])
        }
    except cognito_client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except cognito_client.exceptions.UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logging.error(f"Error fetching user from Cognito: {e}")
        raise HTTPException(status_code=500, detail="Error fetching user")
    
def get_current_user(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(401, "User not logged in!")
    
    print(access_token)
    user = _get_user_from_cognito(access_token)
    return user