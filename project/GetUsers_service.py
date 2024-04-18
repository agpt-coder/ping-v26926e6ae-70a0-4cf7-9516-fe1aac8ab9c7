from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UserInfo(BaseModel):
    """
    The basic user information including ID, username, and email.
    """

    id: str
    username: str
    email: str


class UsersListResponse(BaseModel):
    """
    This response model returns a paginated list of users including their ID, username, and email. It wraps the results in a pagination structure.
    """

    users: List[UserInfo]
    total: int
    page: int
    limit: int


async def GetUsers(
    page: Optional[int] = None, limit: Optional[int] = None
) -> UsersListResponse:
    """
    Retrieves a list of all users with pagination support. Each user's ID, username, and email are listed.

    Args:
        page (Optional[int]): The page number for pagination, starts from 1.
        limit (Optional[int]): The number of items per page. Default is 10 if not specified.

    Returns:
        UsersListResponse: This response model returns a paginated list of users including their ID, username, and email.
    """
    if page is None:
        page = 1
    if limit is None:
        limit = 10
    skip = (page - 1) * limit
    users_query = await prisma.models.User.prisma().find_many(
        skip=skip, take=limit, order={"createdAt": "asc"}
    )
    users_info = [
        UserInfo(id=user.id, username=user.username, email=user.email)
        for user in users_query
    ]  # TODO(autogpt): Cannot access attribute "email" for class "User"
    #     Attribute "email" is unknown. reportAttributeAccessIssue
    total_users = await prisma.models.User.prisma().count()
    return UsersListResponse(
        users=users_info, total=total_users, page=page, limit=limit
    )
