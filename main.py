#TODO: Use real Database if arc.dev team wants me to.


from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, status
from fastapi.responses import Response, HTMLResponse
from fastapi.requests import Request

from pydantic import BaseModel, validator

from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from functools import reduce

from libs.utils import gravatar

from passlib.context import CryptContext


app = FastAPI()

#for this basic example I use a "mock" database from python dicts
sql_mock = {"users": {}, "ideas": {}, "tokens": {}}

### START DATA MODELS ###


# Settings for this APP
class Settings(BaseModel):
    authjwt_secret_key: str = "b890b9f1a3398db80e7aac74fd5e2fd8b57087dd5020c46530f3bda784a8eda6"
    authjwt_access_token_expires: int = 60 * 10

    authjwt_header_name: str = "X-Access-Token"
    authjwt_header_type: str = None

    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}

    TestLKSADk: str = ""


#Model for JWT authentification
class AuthToken(BaseModel):
    jwt: str
    refresh_token: str
    user_id: str


#Model for user posted Idea inherited by IdeaIn
class IdeaIn(BaseModel):
    content: str
    impact: int
    ease: int
    confidence: int

    @validator('impact', 'ease', 'confidence')
    def max_value_10(cls, value: int):
        if value > 10 or value < 1:
            raise ValueError('must be between 1 and 10 included')
        return value


#Model for Idea saved in DB ()
class Idea(IdeaIn):
    id: UUID
    average_score: float
    created_at: int


class UserLogin(BaseModel):
    email: str
    password: str


class RefreshToken(BaseModel):
    refresh_token: str


#Model for User
class User(BaseModel):
    email: str
    name: str
    password: str
    avatar_url: Optional[str] = gravatar.default
    refresh_token: Optional[str] = None

    @validator('password')
    def must_be_long(cls, pw: str):
        assert len(pw) >= 8, 'Password must be at least 8 characters long'
        return pw

    @validator('password')
    def must_have_capital(cls, pw: str):
        assert reduce(
            lambda a, b: a or b,
            [char.isupper() for char in pw
             ]), 'Password must contain at least one uppercase character'
        return pw

    @validator('password')
    def must_have_lower(cls, pw: str):
        assert reduce(
            lambda a, b: a or b,
            [char.islower() for char in pw
             ]), 'Password must contain at least one lowercase character'
        return pw

    @validator('password')
    def must_have_numeric(cls, pw: str):
        assert reduce(
            lambda a, b: a or b,
            [char.isnumeric() for char in pw
             ]), 'Password must contain at least one numeric character'
        return pw


### END DATA MODELS ###


### START AUTH FUNCTIONS ###
# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code,
                        content={"detail": exc.message})


def return_current_user(Authorize: AuthJWT):
    Authorize.jwt_required()
    current_user_email = Authorize.get_jwt_subject()
    user = sql_mock["users"][current_user_email]
    if user is None:
        print("!!!!!! USER NOT FOUND !!!!!!")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Token user mismatch")

    return user



# A storage engine to save revoked tokens. in production,
# you can use Redis for storage system
denylist = set()


# For this example, we are just checking if the tokens jti
# (unique identifier) is in the denylist set. This could
# be made more complex, for example storing the token in Redis
# with the value true if revoked and false if not revoked
@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    if isinstance(decrypted_token, str):
        return decrypted_token in denylist
    jti = decrypted_token['jti']
    return jti in denylist


### END AUTH FUNCTIONS ###

### START PASSWORD FUNCTIONS ###

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

### END PASSWORD FUNCTIONS ###

### START TOKEN ENDPOINTS ####
#refesh JWT Token
@app.post("/access-tokens/refresh")
def refresh(refresh_token: RefreshToken, Authorize: AuthJWT = Depends()):
    #Authorize.jwt_refresh_token_required()

    user_with_refresh_token: User = next(
        filter(lambda user: user.refresh_token == refresh_token,
               sql_mock["users"].values()), None)

    if user_with_refresh_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Bad refresh token")

    new_access_token = Authorize.create_access_token(
        subject=user_with_refresh_token.email)
    return {
        "jwt": new_access_token
    }  #AuthToken(jwt=new_access_token, refresh_token=refresh_token, user_id=current_user_email)


#login User
@app.post("/access-tokens", status_code=status.HTTP_201_CREATED)
def login(user: UserLogin, Authorize: AuthJWT = Depends()):
    if user.email not in sql_mock["users"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Bad username or password")

    DbUser = sql_mock["users"][user.email]
    if not verify_password(user.password, DbUser.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Bad username or password")

    # subject identifier for who this token is for example id or username from database
    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_refresh_token(subject=user.email)

    DbUser.refresh_token = refresh_token

    return AuthToken(jwt=access_token,
                     refresh_token=refresh_token,
                     user_id=user.email)


# logout user
@app.delete("/access-tokens", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    refresh_token: RefreshToken,
    Authorize: AuthJWT = Depends(),
    #current_user: User = Depends(get_current_user)
):
    current_user = get_current_user(Authorize)
    #Authorize.jwt_refresh_token_required()

    jti = Authorize.get_raw_jwt()['jti']
    denylist.add(jti)
    denylist.add(refresh_token)

    sql_mock["users"][current_user.email].refresh_token = None
    return Response(status_code=status.HTTP_204_NO_CONTENT.value)


### END TOKEN ENDPOINTS ###


### START USER ENDPOINTS ###
# create new  user
@app.post("/users", status_code=status.HTTP_201_CREATED)
def signup(user: User, Authorize: AuthJWT = Depends()):

    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_refresh_token(subject=user.email)

    user.refresh_token = refresh_token
    user.avatar_url = gravatar.genAvatar(user.email)
    user.password = get_password_hash(user.password)

    sql_mock["users"][user.email] = user
    sql_mock["ideas"][user.email] = {}

    token = AuthToken(jwt=access_token,
                      refresh_token=refresh_token,
                      user_id=user.email)

    #sql_mock["tokens"][token.jwt] = token

    return token


# get current user info
@app.get("/me", response_model=User)
def get_current_user(
        #current_user: User = Depends(get_current_user)
        Authorize: AuthJWT = Depends()) -> User:
    current_user = return_current_user(Authorize)
    return current_user

    # logic get user from header token


### END USER ENDPOINTS ###

### START IDEA ENDPOINTS ###


#create new idea
@app.post("/ideas", response_model=Idea, status_code=status.HTTP_201_CREATED)
async def post_idea(
    idea: IdeaIn,
    #current_user: User = Depends(get_current_user),
    Authorize: AuthJWT = Depends()
) -> Idea:
    newIdea = Idea.parse_obj({
        **idea.dict(), "id":
        uuid4(),
        "created_at":
        datetime.now().timestamp(),
        "average_score": (idea.confidence + idea.ease + idea.impact) / 3
    })

    current_user = return_current_user(Authorize)
    sql_mock["ideas"][current_user.email][newIdea.id] = newIdea
    return newIdea


#delete idea
@app.delete("/ideas/{id}", status_code=status.HTTP_201_CREATED)
def delete_idea(id: str,
                Authorize: AuthJWT = Depends()
                #current_user: User = Depends(get_current_user)
                ):
    current_user = return_current_user(Authorize)
    del sql_mock["ideas"][current_user.email][UUID(id)]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#edit existing idea
@app.put("/ideas/{id}", response_model=Idea)
def update_idea(
    id: str,
    idea: IdeaIn,
    Authorize: AuthJWT = Depends()
    #current_user: User = Depends(get_current_user)
) -> Idea:
    uuid = UUID(id)
    current_user = return_current_user(Authorize)

    if uuid not in sql_mock["ideas"][current_user.email]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Idea not found")

    oldIdea = sql_mock["ideas"][current_user.email][uuid]
    sql_mock["ideas"][current_user.email][UUID(id)] = Idea.parse_obj({
        **oldIdea.dict(),
        **idea.dict(), "average_score":
        (idea.confidence + idea.ease + idea.impact) / 3
    })
    return sql_mock["ideas"][current_user.email][UUID(id)]


# get paginated list of ideas‚
@app.get("/ideas", response_model=List[Idea])
def get_ideas(
    page: Optional[int] = 1,
    #current_user: User = Depends(get_current_user)
    Authorize: AuthJWT = Depends()
) -> List[Idea]:
    current_user = return_current_user(Authorize)
    return list(sql_mock["ideas"][current_user.email].values())[(page - 1) *
                                                                10:page * 10]

@app.get("/", response_class=HTMLResponse)
def welcome():
    return """
    <html>
        <head>
            <title>arc.dev intro | Sakander Zirai | @suioni</title>
        </head>
        <body>
            <h1>arc.dev Intro Challenge</h1>
            <p>Welcome to the arc dev challange solution of Sakander Zirai <a href="https://arc.dev/@SuiOni">arc.dev/@SuiOni</a> </p> 
            <p>Go to <a href="./docs">docs</a> to see Swagger API Documentation</p>
            <p>Backend is written in Python3 with the FastAPI Framework</p>
            <p>Get the source code from GitHub</p>
        </body>
    </html>
    """


### END IDEA ENDPOINTS ###

#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)