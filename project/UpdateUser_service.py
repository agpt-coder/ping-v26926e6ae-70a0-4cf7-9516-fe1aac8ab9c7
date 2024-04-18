from datetime import datetime
from enum import Enum

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class User(BaseModel):
    """
    Represents a user entity as persisted in the database.
    """

    id: str
    createdAt: datetime
    updatedAt: datetime
    username: str
    role: prisma.enums.UserRole


class UpdateUserDetailsResponse(BaseModel):
    """
    Model representing the response after successfully updating a user's details.
    """

    success: bool
    updatedUser: User


class UserRole(Enum):
    API_USER: str = "API_USER"
    SYSTEM_ADMIN: str = "SYSTEM_ADMIN"


async def UpdateUser(
    userId: str, name: str, email: str, role: prisma.enums.UserRole
) -> UpdateUserDetailsResponse:
    """
    Updates a user's details. Acceptable fields for update are name, email, and role. The endpoint requires the user ID of the user whose details need to be updated.

    Args:
    userId (str): The unique identifier of the user whose details are to be updated.
    name (str): The new name to update for the user.
    email (str): The new email to update for the user.
    role (prisma.enums.UserRole): The new role to assign to the user, which must be either 'API_USER' or 'SYSTEM_ADMIN'.

    Returns:
    UpdateUserDetailsResponse: Model representing the response after successfully updating a user's details.
    """
    user = await prisma.models.User.prisma().update(
        where={"id": userId}, data={"username": name, "email": email, "role": str(role)}
    )
    updated_user_model = User(
        id=user.id,
        createdAt=user.createdAt,
        updatedAt=user.updatedAt,
        username=user.username,
        role=prisma.enums.UserRole[user.role],
    )
    response = UpdateUserDetailsResponse(success=True, updatedUser=updated_user_model)
    return response
