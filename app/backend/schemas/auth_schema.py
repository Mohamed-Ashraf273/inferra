from pydantic import BaseModel


class AuthRequest(BaseModel):
    id: str
    username: str
    full_name: str
    disabled: bool


class AuthResponse(BaseModel):
    username: str
    full_name: str
    disabled: bool
