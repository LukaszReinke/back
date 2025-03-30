from contextlib import asynccontextmanager

import services as svc
import controllers as ctrl
import routers

from app_exceptions.exception_handler import (
    generate_error_responses,
    register_all_errors,
)

from authentication import PasswordManager, jwt_manager

from fastapi import APIRouter, FastAPI, HTTPException, status, Body
from fastapi.middleware.cors import CORSMiddleware
from app_exceptions import errors

from models.base import create_engine, init_db


test_router = APIRouter()
password_manager = PasswordManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_engine()
    await init_db()

    yield


app = FastAPI(debug=True, lifespan=lifespan)
register_all_errors(app)

app.include_router(routers.contest_router)
app.include_router(routers.events_router)
app.include_router(routers.users_router)
app.include_router(routers.profile_router)
app.include_router(routers.organizer_router)
app.include_router(routers.workshop_router)


origins = [
    "http://localhost:3001",
    # Add more origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/login",
    response_model=ctrl.LoginResponse,
    responses=generate_error_responses(),
)
async def login(data: ctrl.LoginRequest = Body()):
    user = await svc.UserService.get_user_by_email(data.email)
    print(user.__dict__, user.role)

    if user is None or not password_manager.verify_password(
        data.password, str(user.hashed_password)
    ):
        raise errors.InvalidCredentials

    if user.is_initial_password is True:
        reset_token = jwt_manager.create_access_token(str(user.email), None, 5)

        return ctrl.LoginResponse(
            access_token=reset_token,
            token_type="bearer",
            user=user,
            message="Change your password first",
        )

    access_token: str = jwt_manager.create_access_token(
        str(user.email),
        str(user.role),
    )

    return ctrl.LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=user,
    )


@app.post("/refresh")
async def refresh_token(response: ctrl.RefreshTokenRequest = Body()):
    payload = jwt_manager.get_payload(response.refresh_token)
    email: str | None = payload.get("email", None)

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user = await svc.UserService.get_user_by_email(email)

    new_access_token = jwt_manager.create_access_token(str(user.email))

    return {"access_token": new_access_token, "token_type": "bearer"}
