import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session


def test_create_group(client: TestClient, mock_auth):
    """Testa a criação de um grupo via API."""
    response = client.post(
        "/api/v1/groups/",
        json={"name": "test_group_api"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test_group_api"
    assert "id" in data


def test_get_all_groups(client: TestClient, test_data, mock_auth):
    """Testa a listagem de grupos via API."""
    response = client.get("/api/v1/groups/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {group["name"] for group in data} == {"webservers", "dbservers"}


def test_get_group_by_id(client: TestClient, test_data, mock_auth):
    """Testa a obtenção de um grupo específico via API."""
    group_id = test_data["groups"][0].id
    response = client.get(f"/api/v1/groups/{group_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "webservers"
    assert "hosts" in data
    assert "variables" in data


def test_update_group(client: TestClient, test_data, mock_auth):
    """Testa a atualização de um grupo via API."""
    group_id = test_data["groups"][0].id
    response = client.put(
        f"/api/v1/groups/{group_id}"

    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "webservers"  # Não alterado


def test_delete_group(client: TestClient, test_data, mock_auth):
    """Testa a exclusão de um grupo via API."""
    group_id = test_data["groups"][1].id
    response = client.delete(f"/api/v1/groups/{group_id}")
    assert response.status_code == 204

    # Verificar se o grupo realmente foi excluído
    response = client.get(f"/api/v1/groups/{group_id}")
    assert response.status_code == 404
