import prisma
import prisma.models
from pydantic import BaseModel


class PingResponse(BaseModel):
    """
    Provides the modified response prefixed with 'pong: ' after the message passes the security checks.
    """

    response_message: str


async def verify_security_module_enabled() -> bool:
    """
    Verifies if the security module is enabled.

    Returns:
        bool: True if the security module is enabled, False otherwise.
    """
    enabled = await prisma.models.Module.prisma().find_first(
        where={"name": "SECURITY", "enabled": True}
    )
    return enabled is not None


async def is_authorized_to_ping(user_id: str) -> bool:
    """
    Check if the user is authorized to use the ping service by checking user's role associated with the security module.

    Args:
        user_id (str): The user's unique identifier.

    Returns:
        bool: True if the user is authorized, False otherwise.
    """
    authorized = await prisma.models.ModuleRole.prisma().find_first(
        where={"role": "API_USER", "Module": {"name": "SECURITY", "enabled": True}}
    )
    return authorized is not None


async def SendPing(user_message: str) -> PingResponse:
    """
    Receives a user message and replies with 'pong: [user_message]'. It ensures the message is authentic by
    verifying with the Security Module.

    Args:
    user_message (str): The message sent by the user to the server.

    Returns:
    PingResponse: Provides the modified response prefixed with 'pong: ' after the message passes the security checks.
    """
    security_config = await verify_security_module_enabled()
    if not security_config:
        raise ValueError("Security module is not enabled.")
    new_message = f"pong: {user_message}"
    return PingResponse(response_message=new_message)
