from fastapi import APIRouter

from app.backend.schemas.auth_schema import AuthRequest
from app.backend.schemas.auth_schema import AuthResponse
from app.backend.services.login import login as _login

router = APIRouter()


@router.post("/login", response_model=AuthResponse)
async def login(request: AuthRequest):
    return await _login(request)
