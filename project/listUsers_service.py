from datetime import datetime
from typing import List, Optional

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


class GetUsersResponse(BaseModel):
    """
    Response model returning the list of all users, wrapped in a standard response structure.
    """

    users: List[User]


async def listUsers(
    page: Optional[int] = None, limit: Optional[int] = None
) -> GetUsersResponse:
    """
    Retrieves a list of all users in the system. Accessible by administrators for monitoring and management purposes.

    Args:
        page (Optional[int]): The page number for pagination. Starts from 1.
        limit (Optional[int]): The number of items per page. Default is set to a reasonable number like 10.

    Returns:
        GetUsersResponse: Response model returning the list of all users, wrapped in a standard response structure.
    """
    if limit is None:
        limit = 10
    if page is None:
        page = 1
    skip = (page - 1) * limit
    users = await prisma.models.User.prisma().find_many(skip=skip, take=limit)
    response = GetUsersResponse(users=users)
    return response
