from pydantic import BaseModel, EmailStr
from typing import Optional, List

class LoginRequest(BaseModel):
    """Esquema para solicitação de login"""
    username: str
    password: str

class Token(BaseModel):
    """Esquema para resposta de token"""
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    refresh_expires_in: Optional[int] = None

class UserInfo(BaseModel):
    """Esquema para informações do usuário"""
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    roles: List[str] = []