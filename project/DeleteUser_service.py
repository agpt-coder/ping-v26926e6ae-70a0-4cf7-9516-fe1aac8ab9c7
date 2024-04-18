import prisma
import prisma.models
from pydantic import BaseModel


class DeleteUserResponse(BaseModel):
    """
    Response model to confirm the deletion of a user. It provides a message stating the outcome of the operation.
    """

    message: str


async def DeleteUser(userId: str) -> DeleteUserResponse:
    """
    Deletes a specific user using the user ID. Success response confirms the deletion of the user.

    Args:
        userId (str): The unique identifier of the user to be deleted.

    Returns:
        DeleteUserResponse: Response model to confirm the deletion of a user. It provides a message stating the outcome of the operation.
    """
    user = await prisma.models.User.prisma().delete(where={"id": userId})
    if user:
        return DeleteUserResponse(
            message=f"User with ID {userId} was successfully deleted."
        )
    else:
        return DeleteUserResponse(
            message=f"User with ID {userId} not found or could not be deleted."
        )
