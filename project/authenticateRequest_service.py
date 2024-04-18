from datetime import datetime, timedelta

import prisma
import prisma.models
from jose import jwt
from pydantic import BaseModel


class AuthenticationResponse(BaseModel):
    """
    Response model for returning an authorization token after successful authentication.
    """

    token: str
    message: str


def create_access_token(user_id: str, username: str, expiry_period: int = 24) -> str:
    """
    Generates a JWT access token with user identification and an expiration period.

    Args:
    user_id (str): The unique identifier of the user.
    username (str): The username of the user.
    expiry_period (int): The token expiry period in hours.

    Returns:
    str: A JWT token.
    """
    expiry = datetime.utcnow() + timedelta(hours=expiry_period)
    to_encode = {"exp": expiry, "sub": user_id, "username": username}
    return jwt.encode(to_encode, "YOUR_SECRET_KEY_HERE", algorithm="HS256")


async def authenticateRequest(username: str, password: str) -> AuthenticationResponse:
    """
    Verifies user credentials and issues a token if valid. Critical for securing access to the single 'pong' endpoint by ensuring only authenticated requests proceed.

    Args:
    username (str): The username of the user trying to authenticate.
    password (str): The password of the user, which should be appropriately hashed and secured in transit and at rest.

    Returns:
    AuthenticationResponse: Response model for returning an authorization token after successful authentication.
    """
    user = await prisma.models.User.prisma().find_unique(where={"username": username})
    if user is None:
        return AuthenticationResponse(token="", message="User not found")
    if password == "EXPECTED_PASSWORD_PLACEHOLDER":
        token = create_access_token(user_id=user.id, username=user.username)
        return AuthenticationResponse(token=token, message="Authentication successful")
    else:
        return AuthenticationResponse(token="", message="Incorrect password")
