import bcrypt
import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    """
    Response model indicating the successful creation of a user.
    """

    confirmation_message: str


async def createUser(name: str, email: str, password: str) -> CreateUserResponse:
    """
    Creates a new user record. Expects user details in the request body and returns the created user's details. Used by administrators to add users to the system.

    Args:
        name (str): The full name of the user.
        email (str): The email address of the user, which will be used as the login username.
        password (str): The account password for the user, which will be encrypted and stored securely.

    Returns:
        CreateUserResponse: Response model indicating the successful creation of a user.

    Example:
        createUser("John Doe", "john.doe@example.com", "securepassword123")
        > CreateUserResponse(confirmation_message="User John Doe created successfully.")
    """
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    new_user = await prisma.models.User.prisma().create(
        data={
            "username": email,
            "password": hashed_password.decode("utf-8"),
            "role": prisma.enums.UserRole.API_USER,
        }
    )
    response = CreateUserResponse(
        confirmation_message=f"User {name} created successfully."
    )
    return response
