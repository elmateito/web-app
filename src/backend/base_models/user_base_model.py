from pydantic import BaseModel, Field

class UserBase(BaseModel):
    userName: str = Field(min_length=4, max_length=16)
    userEmail: str = Field(min_length=4, max_length=32)
    userPassword: str = Field(min_length=1)
    userPasswordConfirm: str = Field(min_length=1)

class UserBaseLogin(BaseModel):
    userName: str = Field(min_length=4, max_length=16)
    userPassword: str = Field(min_length=1)

class UserExistsDb(UserBase):
    hashedPassword: str = Field(min_length=8)