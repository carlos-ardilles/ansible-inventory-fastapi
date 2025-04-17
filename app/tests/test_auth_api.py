import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from sqlmodel import Session

from app.schemas.auth import LoginRequest, Token, UserInfo


def test_login_success(client: TestClient, session: Session):
    """
    Testa o login bem-sucedido que deve retornar um token.
    Usa um mock para a chamada ao Keycloak.
    """
    # Mock da resposta do Keycloak
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "access_token": "mock-access-token",
        "token_type": "Bearer",
        "refresh_token": "mock-refresh-token",
        "expires_in": 300,
        "refresh_expires_in": 1800
    }

    with patch("requests.post", return_value=mock_response):
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "testuser", "password": "testpassword"}
        )

        # Verificar resposta
        assert response.status_code == 200
        token_data = response.json()
        assert "access_token" in token_data
        assert token_data["access_token"] == "mock-access-token"
        assert token_data["token_type"] == "Bearer"
        assert token_data["refresh_token"] == "mock-refresh-token"


def test_login_failure(client: TestClient, session: Session):
    """
    Testa o login com credenciais inválidas.
    Usa um mock para a chamada ao Keycloak.
    """
    # Mock da resposta do Keycloak para credenciais inválidas
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.json.return_value = {
        "error": "invalid_grant",
        "error_description": "Credenciais inválidas"
    }

    with patch("requests.post", return_value=mock_response):
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "wronguser", "password": "wrongpassword"}
        )

        # Verificar resposta
        assert response.status_code == 401
        assert "detail" in response.json()


def test_refresh_token_success(client: TestClient, session: Session):
    """
    Testa a renovação bem-sucedida de um token.
    Usa um mock para a chamada ao Keycloak.
    """
    # Mock da resposta do Keycloak
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "access_token": "new-mock-access-token",
        "token_type": "Bearer",
        "refresh_token": "new-mock-refresh-token",
        "expires_in": 300
    }

    with patch("requests.post", return_value=mock_response):
        response = client.post(
            "/api/v1/auth/refresh",
            params={"refresh_token": "old-refresh-token"}
        )

        # Verificar resposta
        assert response.status_code == 200
        token_data = response.json()
        assert "access_token" in token_data
        assert token_data["access_token"] == "new-mock-access-token"


def test_refresh_token_failure(client: TestClient, session: Session):
    """
    Testa a renovação de token com refresh token inválido.
    Usa um mock para a chamada ao Keycloak.
    """
    # Mock da resposta do Keycloak para refresh token inválido
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {
        "error": "invalid_grant",
        "error_description": "Token de atualização inválido ou expirado"
    }

    with patch("requests.post", return_value=mock_response):
        response = client.post(
            "/api/v1/auth/refresh",
            params={"refresh_token": "invalid-refresh-token"}
        )

        # Verificar resposta
        assert response.status_code == 401
        assert "detail" in response.json()


def test_user_info_endpoint(client: TestClient, mock_auth):
    """
    Testa o endpoint para obter informações do usuário autenticado.
    """
    response = client.get("/api/v1/auth/me")

    # Verificar resposta
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["username"] == "testuser"
    assert "roles" in user_data