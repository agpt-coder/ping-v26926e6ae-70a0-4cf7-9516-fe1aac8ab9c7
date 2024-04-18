from datetime import datetime
from typing import List

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class Message(BaseModel):
    """
    Model representing a message sent or received by the user.
    """

    id: str
    createdAt: datetime
    content: str
    response: str


class UserDetailResponse(BaseModel):
    """
    Response model containing detailed information about a user including related data like messages and roles.
    """

    id: str
    username: str
    createdAt: datetime
    updatedAt: datetime
    role: prisma.enums.UserRole
    Messages: List[Message]


async def getUserDetails(userId: str) -> UserDetailResponse:
    """
    Fetches detailed information about a specific user using their unique userID. Useful for detailed user profile views and audit purposes.

    Args:
        userId (str): Unique identifier for the user. Used to fetch detailed profile data.

    Returns:
        UserDetailResponse: Response model containing detailed information about a user including related data like messages and roles.
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"id": userId}, include={"Messages": True}
    )
    if not user:
        raise ValueError(f"No user found with ID {userId}")
    messages = [
        Message(
            id=msg.id,
            createdAt=msg.createdAt,
            content=msg.content,
            response=msg.response,
        )
        for msg in user.Messages
    ]
    details = UserDetailResponse(
        id=user.id,
        username=user.username,
        createdAt=user.createdAt,
        updatedAt=user.updatedAt,
        role=user.role.name,
        Messages=messages,
    )
    return details
