from pydantic import BaseModel

from typing import Optional


# Model for JWT authentification
class AuthTokenBase(BaseModel):
    jwt: Optional[str] = None
    refresh_token: Optional[str] = None
    user_id: Optional[str] = None


class AuthToken(AuthTokenBase):
    jwt: str


class AuthTokenRefresh(AuthTokenBase):
    refresh_token: str
