import logging
from contextlib import asynccontextmanager
from typing import Optional

import prisma
import prisma.enums
import project.authenticateRequest_service
import project.CreateUser_service
import project.createUser_service
import project.DeleteUser_service
import project.deleteUser_service
import project.GetUserDetails_service
import project.getUserDetails_service
import project.GetUsers_service
import project.listUsers_service
import project.ping_service
import project.SendPing_service
import project.UpdateUser_service
import project.updateUser_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Ping v2",
    lifespan=lifespan,
    description="single endpoint server that just replies with the pong: and the users message",
)


@app.post("/ping", response_model=project.ping_service.PingResponse)
async def api_post_ping(
    user_message: str,
) -> project.ping_service.PingResponse | Response:
    """
    Receives a message and responds with 'pong:' followed by the same message. The route verifies authentication token validity before processing to ensure security.
    """
    try:
        res = project.ping_service.ping(user_message)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/users/{userId}", response_model=project.deleteUser_service.DeleteUserResponse
)
async def api_delete_deleteUser(
    userId: str,
) -> project.deleteUser_service.DeleteUserResponse | Response:
    """
    Removes a user from the system using their userID. Helps in cleaning up records and managing user lifecycle.
    """
    try:
        res = await project.deleteUser_service.deleteUser(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/users/{userId}", response_model=project.DeleteUser_service.DeleteUserResponse
)
async def api_delete_DeleteUser(
    userId: str,
) -> project.DeleteUser_service.DeleteUserResponse | Response:
    """
    Deletes a specific user using the user ID. Success response confirms the deletion of the user.
    """
    try:
        res = await project.DeleteUser_service.DeleteUser(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users", response_model=project.CreateUser_service.CreateUserResponse)
async def api_post_CreateUser(
    name: str, email: str, password: str
) -> project.CreateUser_service.CreateUserResponse | Response:
    """
    Creates a new user by taking user details. It requires name, email, and password as input. The response includes the confirmation of user creation.
    """
    try:
        res = await project.CreateUser_service.CreateUser(name, email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/ping", response_model=project.SendPing_service.PingResponse)
async def api_post_SendPing(
    user_message: str,
) -> project.SendPing_service.PingResponse | Response:
    """
    Receives a user message and replies with 'pong: [user_message]'. It ensures the message is authentic by verifying with the Security Module.
    """
    try:
        res = await project.SendPing_service.SendPing(user_message)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/users/{userId}", response_model=project.updateUser_service.UpdateUserResponse
)
async def api_put_updateUser(
    userId: str, username: str, role: prisma.enums.UserRole
) -> project.updateUser_service.UpdateUserResponse | Response:
    """
    Updates existing user details. Requires complete user information in the payload. Employed by administrators to maintain up-to-date records.
    """
    try:
        res = await project.updateUser_service.updateUser(userId, username, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users", response_model=project.createUser_service.CreateUserResponse)
async def api_post_createUser(
    name: str, email: str, password: str
) -> project.createUser_service.CreateUserResponse | Response:
    """
    Creates a new user record. Expects user details in the request body and returns the created user's details. Used by administrators to add users to the system.
    """
    try:
        res = await project.createUser_service.createUser(name, email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/users", response_model=project.listUsers_service.GetUsersResponse)
async def api_get_listUsers(
    page: Optional[int], limit: Optional[int]
) -> project.listUsers_service.GetUsersResponse | Response:
    """
    Retrieves a list of all users in the system. Accessible by administrators for monitoring and management purposes.
    """
    try:
        res = await project.listUsers_service.listUsers(page, limit)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/users/{userId}", response_model=project.GetUserDetails_service.UserDetailsResponse
)
async def api_get_GetUserDetails(
    userId: str,
) -> project.GetUserDetails_service.UserDetailsResponse | Response:
    """
    Fetches details of a specific user by user ID. The response includes full user details like name, email, role, and status.
    """
    try:
        res = await project.GetUserDetails_service.GetUserDetails(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/users/{userId}", response_model=project.getUserDetails_service.UserDetailResponse
)
async def api_get_getUserDetails(
    userId: str,
) -> project.getUserDetails_service.UserDetailResponse | Response:
    """
    Fetches detailed information about a specific user using their unique userID. Useful for detailed user profile views and audit purposes.
    """
    try:
        res = await project.getUserDetails_service.getUserDetails(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/authenticate",
    response_model=project.authenticateRequest_service.AuthenticationResponse,
)
async def api_post_authenticateRequest(
    username: str, password: str
) -> project.authenticateRequest_service.AuthenticationResponse | Response:
    """
    Verifies user credentials and issues a token if valid. Critical for securing access to the single 'pong' endpoint by ensuring only authenticated requests proceed.
    """
    try:
        res = await project.authenticateRequest_service.authenticateRequest(
            username, password
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/users/{userId}",
    response_model=project.UpdateUser_service.UpdateUserDetailsResponse,
)
async def api_put_UpdateUser(
    userId: str, name: str, email: str, role: prisma.enums.UserRole
) -> project.UpdateUser_service.UpdateUserDetailsResponse | Response:
    """
    Updates a user's details. Acceptable fields for update are name, email, and role. The endpoint requires the user ID of the user whose details need to be updated.
    """
    try:
        res = await project.UpdateUser_service.UpdateUser(userId, name, email, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/users", response_model=project.GetUsers_service.UsersListResponse)
async def api_get_GetUsers(
    page: Optional[int], limit: Optional[int]
) -> project.GetUsers_service.UsersListResponse | Response:
    """
    Retrieves a list of all users. This endpoint provides paginated user data. Each user's ID, name, and email are listed.
    """
    try:
        res = await project.GetUsers_service.GetUsers(page, limit)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
