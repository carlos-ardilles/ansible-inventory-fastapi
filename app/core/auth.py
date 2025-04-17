from typing import Dict, List, Optional
import time
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
import requests
from pydantic import BaseModel

from app.core.config import settings

# Modelo para representar o usuário autenticado
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    roles: List[str] = []

# OAuth2 scheme usado para extrair o token da requisição
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"
)

# Cache para armazenar temporariamente a chave pública do Keycloak
keycloak_public_key = None
keycloak_public_key_expiry = 0
KEY_CACHE_TTL = 24 * 3600  # 24 horas

def get_keycloak_public_key() -> str:
    """Obtém a chave pública do Keycloak para validação de tokens."""
    global keycloak_public_key, keycloak_public_key_expiry

    current_time = time.time()
    if keycloak_public_key and current_time < keycloak_public_key_expiry:
        return keycloak_public_key

    # Obter a chave pública do Keycloak
    cert_endpoint = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}"
    response = requests.get(
        cert_endpoint,
        verify=settings.KEYCLOAK_SSL_VERIFY
    )
    response.raise_for_status()
    jwks = response.json()

    # Extrair a chave pública
    keycloak_public_key = f"-----BEGIN PUBLIC KEY-----\n{jwks['public_key']}\n-----END PUBLIC KEY-----"
    keycloak_public_key_expiry = current_time + KEY_CACHE_TTL

    return keycloak_public_key

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Valida o token JWT e extrai as informações do usuário.
    Será usado como dependência em endpoints protegidos.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Obter a chave pública para validação
        public_key = get_keycloak_public_key()

        # Verificar e decodificar o token JWT
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience="account",
            options={"verify_signature": True}
        )

        username: str = payload.get("preferred_username")
        if username is None:
            raise credentials_exception

        # Extrair os papéis/roles
        realm_access = payload.get("realm_access", {})
        roles = realm_access.get("roles", [])

        # Criar o objeto de usuário
        user = User(
            username=username,
            email=payload.get("email"),
            full_name=payload.get("name"),
            roles=roles
        )

        return user
    except JWTError:
        raise credentials_exception
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar autenticação: {str(e)}"
        )

def has_role(required_roles: List[str]):
    """
    Verificador de papel (role) a ser usado com Depends.
    Exemplo: @app.get("/admin", dependencies=[Depends(has_role(["admin"]))])
    """
    async def role_checker(user: User = Depends(get_current_user)):
        for role in required_roles:
            if role in user.roles:
                return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão insuficiente"
        )
    return role_checker