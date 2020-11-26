from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security

router = APIRouter()


@router.post("/", response_model=schemas.AuthToken, status_code=status.HTTP_201_CREATED)
def login(
    loginUser: schemas.UserLogin,
    db: Session = Depends(deps.get_db),
    Authorize: AuthJWT = Depends(),
):
    """
    Login user.
    """
    user = crud.user.authenticate(
        db, email=loginUser.email, password=loginUser.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    # subject identifier for who this token is for example id or username from database
    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_refresh_token(subject=user.email)
    return schemas.AuthToken(
        jwt=access_token, refresh_token=refresh_token, user_id=user.email
    )


@router.post("/refresh", response_model=schemas.AuthToken)
def refresh(refresh_token: schemas.AuthTokenRefresh, Authorize: AuthJWT = Depends()):
    """
    Refesh JWT Token
    """
    # Had to use private function because AuthJWT does not
    # allow to use refresh header from request body
    Authorize._verify_jwt_in_request(
        token=refresh_token,
        type_token="refresh",
        token_from="header",
    )
    current_user = Authorize._verified_token(refresh_token)["sub"]
    new_access_token = Authorize.create_access_token(subject=current_user)

    return schemas.AuthToken(jwt=new_access_token)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    refresh_token: schemas.AuthTokenRefresh,
    Authorize: AuthJWT = Depends(),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Logout current user.
    """
    security.add_to_deny(AuthJWT)
    security.add_to_deny(AuthJWT, refresh_token)
    return Response(status_code=status.HTTP_204_NO_CONTENT.value)
