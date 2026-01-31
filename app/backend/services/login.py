from app.backend.schemas.auth_schema import AuthRequest
from app.backend.schemas.auth_schema import AuthResponse


async def login(request: AuthRequest):
    user = request.id
    return AuthResponse(**user.dict())
