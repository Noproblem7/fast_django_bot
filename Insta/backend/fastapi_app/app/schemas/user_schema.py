from pydantic import BaseModel
from typing import Optional


class Settings(BaseModel):
    authjwt_secret_key: str = "6db1eb12dd8469ca955e631258c2e27876f9c81a1d898c98e993e8e9128bdd26"


class UserRegisterSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]
    email: Optional[str]


class UserLoginSchema(BaseModel):
    username_or_email: Optional[str]
    password: Optional[str]


