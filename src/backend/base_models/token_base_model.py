from pydantic import BaseModel

class Token(BaseModel):
    accessToken: str
    tokenType: str

class TokenData(BaseModel):
    userName: str | None = None