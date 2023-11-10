from pydantic import BaseModel


class UserModel(BaseModel):
    phone: str
    address: str
