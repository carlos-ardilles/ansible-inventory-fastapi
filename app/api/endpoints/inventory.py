from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.services.inventory_service import InventoryService
from app.core.auth import get_current_user, User, has_role

router = APIRouter()

@router.get("/ansible-format")
def get_ansible_inventory(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Exporta o inventário no formato utilizado pelo Ansible.
    Este formato é compatível com inventários dinâmicos do Ansible.
    Requer autenticação.
    """
    return InventoryService.export_ansible_inventory(session=session)


@router.get("/ansible-format-admin", dependencies=[Depends(has_role(["admin"]))])
def get_ansible_inventory_admin(
    session: Session = Depends(get_session)
):
    """
    Endpoint que requer papel de admin.
    Exporta o inventário no formato utilizado pelo Ansible.
    """
    return InventoryService.export_ansible_inventory(session=session)