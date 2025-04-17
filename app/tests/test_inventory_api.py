import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

def test_get_ansible_inventory_authenticated(client: TestClient, test_data, mock_auth):
    """Testa o acesso ao endpoint de inventário com autenticação."""
    response = client.get("/api/v1/inventory/ansible-format")
    assert response.status_code == 200
    data = response.json()

    # Verificar a estrutura do inventário
    assert "all" in data
    assert "children" in data["all"]

    # Verificar se os grupos estão presentes
    assert "webservers" in data
    assert "dbservers" in data

    # Verificar se os hosts estão presentes nos grupos corretos
    assert "web1" in data["webservers"]["hosts"]
    assert "web2" in data["webservers"]["hosts"]
    assert "db1" in data["dbservers"]["hosts"]

    # Verificar variáveis
    assert data["webservers"]["vars"]["ansible_user"] == "admin"
    assert data["webservers"]["vars"]["http_port"] == "80"

    # Verificar informações do host
    assert data["webservers"]["hosts"]["web1"]["ansible_host"] == "192.168.1.10"

def test_get_ansible_inventory_admin_role(client: TestClient, test_data, mock_auth):
    """Testa o acesso ao endpoint de inventário que requer papel de admin."""
    response = client.get("/api/v1/inventory/ansible-format-admin")
    assert response.status_code == 200  # O mock tem o papel 'admin'

    # O resultado deve ser o mesmo do endpoint normal
    data = response.json()
    assert "all" in data
    assert "webservers" in data
    assert "dbservers" in data

def test_user_info_endpoint(client: TestClient, mock_auth):
    """Testa o endpoint /me que retorna as informações do usuário autenticado."""
    response = client.get("/api/v1/me")
    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "admin" in data["roles"]