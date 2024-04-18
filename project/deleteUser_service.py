import prisma
import prisma.models
from pydantic import BaseModel


class DeleteUserResponse(BaseModel):
    """
    Response model to confirm the deletion of a user. It provides a message stating the outcome of the operation.
    """

    message: str


async def deleteUser(userId: str) -> DeleteUserResponse:
    """
    Removes a user from the system using their userID. Helps in cleaning up records and managing user lifecycle.

    Args:
    userId (str): The unique identifier of the user to be deleted.

    Returns:
    DeleteUserResponse: Response model to confirm the deletion of a user. It provides a message stating the outcome of the operation.
    """
    user = await prisma.models.User.prisma().delete(where={"id": userId})
    if user:
        response = DeleteUserResponse(
            message="prisma.models.User successfully deleted."
        )
    else:
        response = DeleteUserResponse(message="prisma.models.User not found.")
    return response
