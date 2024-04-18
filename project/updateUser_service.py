from enum import Enum

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateUserResponse(BaseModel):
    """
    Response indicating success or failure of the update operation on the specified user.
    """

    success: bool
    message: str


class UserRole(Enum):
    API_USER: str = "API_USER"
    SYSTEM_ADMIN: str = "SYSTEM_ADMIN"


async def updateUser(userId: str, username: str, role: UserRole) -> UpdateUserResponse:
    """
    Updates existing user details. Requires complete user information in the payload. Employed by administrators to maintain up-to-date records.

    Args:
    userId (str): The unique identifier of the User to update. Extracted from the path variable.
    username (str): The new username to update the user with.
    role (UserRole): Defines the user's role after the update. It must align with defined user roles.

    Returns:
    UpdateUserResponse: Response indicating success or failure of the update operation on the specified user.

    Example:
        updateUser('123e4567-e89b-12d3-a456-426614174000', 'newUsername', UserRole.SYSTEM_ADMIN)
        > UpdateUserResponse(success=True, message='User updated successfully.')
    """
    existing_user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if not existing_user:
        return UpdateUserResponse(success=False, message="User not found.")
    user_with_same_username = await prisma.models.User.prisma().find_unique(
        where={"username": username}
    )
    if user_with_same_username and user_with_same_username.id != userId:
        return UpdateUserResponse(success=False, message="Username already in use.")
    try:
        await prisma.models.User.prisma().update(
            where={"id": userId}, data={"username": username, "role": role}
        )
        return UpdateUserResponse(success=True, message="User updated successfully.")
    except Exception as e:
        return UpdateUserResponse(
            success=False, message="Failed to update user: " + str(e)
        )
