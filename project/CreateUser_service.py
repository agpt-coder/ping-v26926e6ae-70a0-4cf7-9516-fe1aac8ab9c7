import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    """
    Response model indicating the successful creation of a user.
    """

    confirmation_message: str


async def CreateUser(name: str, email: str, password: str) -> CreateUserResponse:
    """
    Creates a new user by taking user details. It requires name, email, and password as input. The response includes the confirmation of user creation.

    Args:
        name (str): The full name of the user.
        email (str): The email address of the user, which will be used as the login username.
        password (str): The account password for the user, which will be encrypted and stored securely.

    Returns:
        CreateUserResponse: Response model indicating the successful creation of a user.
    """
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    user = await prisma.models.User.prisma().create(
        data={"username": email, "password": hashed_password}
    )
    return CreateUserResponse(
        confirmation_message=f"User {name} has been successfully created with ID {user.id}."
    )
