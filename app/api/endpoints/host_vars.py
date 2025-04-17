from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db.session import get_session
from app.models.inventory import HostVar
from app.schemas.inventory import HostVarCreate, HostVarRead, HostVarUpdate
from app.services.host_var_service import HostVarService
from app.services.host_service import HostService

router = APIRouter()

@router.post("/", response_model=HostVarRead, status_code=status.HTTP_201_CREATED)
def create_host_var(host_var: HostVarCreate, session: Session = Depends(get_session)):
    # Verificar se o host existe
    db_host = HostService.get_by_id(session, host_id=host_var.host_id)
    if not db_host:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Host com ID {host_var.host_id} não encontrado"
        )

    # Verificar se já existe uma variável com a mesma chave para este host
    existing_var = HostVarService.get_by_key_and_host(
        session=session, key=host_var.key, host_id=host_var.host_id
    )
    if existing_var:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Variável com a chave '{host_var.key}' já existe para este host"
        )

    return HostVarService.create(session=session, host_var_create=host_var)


@router.get("/host/{host_id}", response_model=List[HostVarRead])
def read_host_vars_by_host(host_id: int, session: Session = Depends(get_session)):
    # Verificar se o host existe
    db_host = HostService.get_by_id(session, host_id=host_id)
    if not db_host:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Host com ID {host_id} não encontrado"
        )

    return HostVarService.get_all_by_host(session=session, host_id=host_id)


@router.get("/{var_id}", response_model=HostVarRead)
def read_host_var(var_id: int, session: Session = Depends(get_session)):
    db_var = HostVarService.get_by_id(session=session, var_id=var_id)
    if not db_var:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Variável com ID {var_id} não encontrada"
        )
    return db_var


@router.put("/{var_id}", response_model=HostVarRead)
def update_host_var(var_id: int, var_update: HostVarUpdate, session: Session = Depends(get_session)):
    db_var = HostVarService.update(session=session, var_id=var_id, var_update=var_update)
    if not db_var:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Variável com ID {var_id} não encontrada"
        )
    return db_var


@router.delete("/{var_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_host_var(var_id: int, session: Session = Depends(get_session)):
    success = HostVarService.delete(session=session, var_id=var_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Variável com ID {var_id} não encontrada"
        )
    return None