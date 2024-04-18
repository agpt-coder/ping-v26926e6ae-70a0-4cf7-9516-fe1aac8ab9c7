from pydantic import BaseModel


class PingResponse(BaseModel):
    """
    Provides the modified response prefixed with 'pong: ' after the message passes the security checks.
    """

    response_message: str


def ping(user_message: str) -> PingResponse:
    """
    Receives a message and responds with 'pong:' followed by the same message. The route verifies authentication token validity before processing to ensure security.

    Args:
        user_message (str): The message sent by the user to the server.

    Returns:
        PingResponse: Provides the modified response prefixed with 'pong: ' after the message passes the security checks.
    """
    response_msg = f"pong: {user_message}"
    return PingResponse(response_message=response_msg)
