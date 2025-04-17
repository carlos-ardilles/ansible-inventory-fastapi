from fastapi import APIRouter, Depends, HTTPException, status
import requests
from app.core.config import settings
from app.schemas.auth import LoginRequest, Token, UserInfo
from app.core.auth import get_current_user, User

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(login_request: LoginRequest):
    """
    Endpoint para autenticação de usuários.
    Envia as credenciais para o Keycloak e retorna o token.
    """
    keycloak_token_url = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"

    # Dados para enviar ao Keycloak
    data = {
        "client_id": settings.KEYCLOAK_CLIENT_ID,
        "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
        "grant_type": "password",
        "username": login_request.username,
        "password": login_request.password
    }

    try:
        response = requests.post(
            keycloak_token_url,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            verify=settings.KEYCLOAK_SSL_VERIFY
        )

        if response.status_code == 200:
            # Retornar o token e informações relacionadas
            token_data = response.json()
            return Token(
                access_token=token_data["access_token"],
                token_type=token_data["token_type"],
                refresh_token=token_data.get("refresh_token"),
                expires_in=token_data.get("expires_in"),
                refresh_expires_in=token_data.get("refresh_expires_in")
            )
        else:
            # Tratar erro de autenticação
            detail = "Credenciais inválidas"
            try:
                error_data = response.json()
                if "error_description" in error_data:
                    detail = error_data["error_description"]
            except:
                pass

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=detail
            )

    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erro ao comunicar com o servidor de autenticação: {str(e)}"
        )

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    """
    Endpoint para atualizar um token expirado usando refresh_token.
    """
    keycloak_token_url = f"{settings.KEYCLOAK_SERVER_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"

    # Dados para enviar ao Keycloak
    data = {
        "client_id": settings.KEYCLOAK_CLIENT_ID,
        "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    try:
        response = requests.post(
            keycloak_token_url,
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            verify=settings.KEYCLOAK_SSL_VERIFY
        )

        if response.status_code == 200:
            # Retornar o novo token
            token_data = response.json()
            return Token(
                access_token=token_data["access_token"],
                token_type=token_data["token_type"],
                refresh_token=token_data.get("refresh_token"),
                expires_in=token_data.get("expires_in"),
                refresh_expires_in=token_data.get("refresh_expires_in")
            )
        else:
            # Tratar erro de refresh
            detail = "Não foi possível atualizar o token"
            try:
                error_data = response.json()
                if "error_description" in error_data:
                    detail = error_data["error_description"]
            except:
                pass

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=detail
            )

    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erro ao comunicar com o servidor de autenticação: {str(e)}"
        )

@router.get("/me", response_model=UserInfo)
async def get_user_info(user: User = Depends(get_current_user)):
    """
    Endpoint para obter informações do usuário autenticado.
    """
    return UserInfo(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        roles=user.roles
    )