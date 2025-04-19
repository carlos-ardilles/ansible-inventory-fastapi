import os
import pytest
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app
from app.db.session import get_session
from app.models.inventory import Group, Host, GroupVar, HostVar, HostGroupLink

# Criar um banco de dados SQLite em arquivo para testes
TEST_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={
                            "check_same_thread": False})

# Criar tabelas antes dos testes


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Configura o banco de dados de teste antes dos testes e limpa depois."""
    # Criar tabelas
    SQLModel.metadata.create_all(test_engine)
    yield
    # Limpar após os testes
    if os.path.exists("./test.db"):
        os.unlink("./test.db")


@pytest.fixture(autouse=True, scope="function")
def clean_tables():
    """Limpar todas as tabelas antes de cada teste."""
    with Session(test_engine) as session:
        # Usar text() para declarações SQL literais
        session.exec(text("DELETE FROM host_group_membership"))
        session.exec(text("DELETE FROM group_vars"))
        session.exec(text("DELETE FROM host_vars"))
        session.exec(text("DELETE FROM hosts"))
        session.exec(text("DELETE FROM groups"))
        session.commit()
    yield


@pytest.fixture(name="session")
def session_fixture():
    """Fixture que fornece uma sessão de banco de dados de teste."""
    with Session(test_engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Fixture que fornece um cliente de teste para a API FastAPI."""
    def get_session_override():
        return session

    # Sobrescrever a dependência de sessão durante os testes
    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as client:
        yield client

    # Limpar sobrescritas após o teste
    app.dependency_overrides = {}


@pytest.fixture(name="test_data")
def test_data_fixture(session: Session):
    """Fixture que carrega dados de teste no banco de dados."""
    # Criar grupos
    group1 = Group(name="webservers")
    group2 = Group(name="dbservers")
    session.add(group1)
    session.add(group2)
    session.commit()
    session.refresh(group1)
    session.refresh(group2)

    # Criar hosts
    host1 = Host(
        hostname="web1",
        ansible_host="192.168.1.10",
        ansible_port=22,
        ansible_user="admin",
        ansible_connection="ssh"
    )
    host2 = Host(
        hostname="web2",
        ansible_host="192.168.1.11",
        ansible_port=22,
        ansible_user="admin",
        ansible_connection="ssh"
    )
    host3 = Host(
        hostname="db1",
        ansible_host="192.168.1.20",
        ansible_port=22,
        ansible_user="dbadmin",
        ansible_connection="ssh"
    )
    session.add(host1)
    session.add(host2)
    session.add(host3)
    session.commit()
    session.refresh(host1)
    session.refresh(host2)
    session.refresh(host3)

    # Criar relações entre hosts e grupos
    host_group1 = HostGroupLink(host_id=host1.id, group_id=group1.id)
    host_group2 = HostGroupLink(host_id=host2.id, group_id=group1.id)
    host_group3 = HostGroupLink(host_id=host3.id, group_id=group2.id)
    session.add(host_group1)
    session.add(host_group2)
    session.add(host_group3)
    session.commit()

    # Criar variáveis de grupo
    group_var1 = GroupVar(var_name="ansible_user",
                          var_value="admin", group_id=group1.id)
    group_var2 = GroupVar(var_name="http_port",
                          var_value="80", group_id=group1.id)
    group_var3 = GroupVar(var_name="ansible_user",
                          var_value="dbadmin", group_id=group2.id)
    session.add(group_var1)
    session.add(group_var2)
    session.add(group_var3)
    session.commit()

    # Criar variáveis de host
    host_var1 = HostVar(var_name="ansible_host",
                        var_value="192.168.1.10", host_id=host1.id)
    host_var2 = HostVar(var_name="http_port",
                        var_value="8080", host_id=host1.id)
    session.add(host_var1)
    session.add(host_var2)
    session.commit()

    return {
        "groups": [group1, group2],
        "hosts": [host1, host2, host3],
        "group_vars": [group_var1, group_var2, group_var3],
        "host_vars": [host_var1, host_var2]
    }

# Mock para autenticação durante os testes


@pytest.fixture(name="mock_auth")
def mock_auth_fixture():
    """Cria um mock para autenticação durante os testes."""
    from app.core.auth import get_current_user, User

    async def mock_get_current_user():
        return User(
            username="testuser",
            email="test@example.com",
            full_name="Test User",
            roles=["admin"]
        )

    # Sobrescrever a função de autenticação com um mock
    original_dependency = app.dependency_overrides.get(get_current_user)
    app.dependency_overrides[get_current_user] = mock_get_current_user

    yield

    # Restaurar a dependência original, se existia alguma
    if original_dependency:
        app.dependency_overrides[get_current_user] = original_dependency
    else:
        if get_current_user in app.dependency_overrides:
            del app.dependency_overrides[get_current_user]
