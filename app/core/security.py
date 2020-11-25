from fastapi.requests import Request
from fastapi.responses import JSONResponse

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from passlib.context import CryptContext

from app.main import app
from app.core import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# A storage engine to save revoked tokens.
denylist = set()


# Callback to get your configuration
@AuthJWT.load_config
def get_config():
    return settings


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code,
                        content={"detail": exc.message})


# We are just checking if the tokens jti
# (unique identifier) is in the denylist set.
@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    if isinstance(decrypted_token, str):
        return decrypted_token in denylist
    jti = decrypted_token['jti']
    return jti in denylist


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def add_to_deny(Authorize: AuthJWT, token: str = None):
    jti = Authorize.get_raw_jwt(token)['jti']
    denylist.add(jti)
