from datetime import datetime

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UserDetailsResponse(BaseModel):
    """
    Response model encapsulating full user details from the /users/{userId} endpoint.
    """

    id: str
    username: str
    createdAt: datetime
    updatedAt: datetime
    role: prisma.enums.UserRole
    status: str


async def GetUserDetails(userId: str) -> UserDetailsResponse:
    """
    Fetches details of a specific user by user ID. The response includes full user details like name, email, role, and status.

    Args:
    userId (str): The unique identifier for a prisma.models.User.

    Returns:
    UserDetailsResponse: Response model encapsulating full user details from the /users/{userId} endpoint.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if user is None:
        raise ValueError(f"prisma.models.User with ID {userId} not found")
    response = UserDetailsResponse(
        id=user.id,
        username=user.username,
        createdAt=user.createdAt,
        updatedAt=user.updatedAt,
        role=user.role,
        status="Active" if user.updatedAt > user.createdAt else "Inactive",
    )
    return response
