import pytest
from sqlmodel import Session

from app.services.group_service import GroupService
from app.schemas.inventory import GroupCreate, GroupUpdate
from app.models.inventory import Group

def test_create_group(session: Session):
    """Testa a criação de um grupo via serviço."""
    group_data = GroupCreate(name="test_group", description="Test group description")
    group = GroupService.create(session=session, group_create=group_data)

    assert group.id is not None
    assert group.name == "test_group"
    assert group.description == "Test group description"

def test_get_by_id(session: Session, test_data):
    """Testa a obtenção de um grupo pelo ID."""
    group_id = test_data["groups"][0].id
    group = GroupService.get_by_id(session=session, group_id=group_id)

    assert group is not None
    assert group.id == group_id
    assert group.name == "webservers"

def test_get_by_name(session: Session, test_data):
    """Testa a obtenção de um grupo pelo nome."""
    group = GroupService.get_by_name(session=session, name="webservers")

    assert group is not None
    assert group.name == "webservers"

def test_get_all(session: Session, test_data):
    """Testa a obtenção de todos os grupos."""
    # Use a contagem exata de grupos criados no teste de dados
    groups = GroupService.get_all(session=session)

    assert len(groups) == len(test_data["groups"])
    group_names = {g.name for g in groups}
    assert "webservers" in group_names
    assert "dbservers" in group_names

def test_update(session: Session, test_data):
    """Testa a atualização de um grupo."""
    group_id = test_data["groups"][0].id
    update_data = GroupUpdate(description="Updated description")

    updated_group = GroupService.update(session=session, group_id=group_id, group_update=update_data)

    assert updated_group is not None
    assert updated_group.description == "Updated description"
    assert updated_group.name == "webservers"  # Não alterado

def test_delete(session: Session, test_data):
    """Testa a exclusão de um grupo."""
    group_id = test_data["groups"][1].id

    # Confirmar que o grupo existe antes
    assert GroupService.get_by_id(session=session, group_id=group_id) is not None

    # Excluir o grupo
    success = GroupService.delete(session=session, group_id=group_id)
    assert success is True

    # Confirmar que foi excluído
    assert GroupService.get_by_id(session=session, group_id=group_id) is None