from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db.session import get_session
from app.models.inventory import GroupVar
from app.schemas.inventory import GroupVarCreate, GroupVarRead, GroupVarUpdate
from app.services.group_var_service import GroupVarService
from app.services.group_service import GroupService

router = APIRouter()

@router.post("/", response_model=GroupVarRead, status_code=status.HTTP_201_CREATED)
def create_group_var(group_var: GroupVarCreate, session: Session = Depends(get_session)):
    # Verificar se o grupo existe
    db_group = GroupService.get_by_id(session, group_id=group_var.group_id)
    if not db_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Grupo com ID {group_var.group_id} não encontrado"
        )

    # Verificar se já existe uma variável com a mesma chave para este grupo
    existing_var = GroupVarService.get_by_key_and_group(
        session=session, key=group_var.key, group_id=group_var.group_id
    )
    if existing_var:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Variável com a chave '{group_var.key}' já existe para este grupo"
        )

    return GroupVarService.create(session=session, group_var_create=group_var)


@router.get("/group/{group_id}", response_model=List[GroupVarRead])
def read_group_vars_by_group(group_id: int, session: Session = Depends(get_session)):
    # Verificar se o grupo existe
    db_group = GroupService.get_by_id(session, group_id=group_id)
    if not db_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Grupo com ID {group_id} não encontrado"
        )

    return GroupVarService.get_all_by_group(session=session, group_id=group_id)


@router.get("/{var_id}", response_model=GroupVarRead)
def read_group_var(var_id: int, session: Session = Depends(get_session)):
    db_var = GroupVarService.get_by_id(session=session, var_id=var_id)
    if not db_var:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Variável com ID {var_id} não encontrada"
        )
    return db_var


@router.put("/{var_id}", response_model=GroupVarRead)
def update_group_var(var_id: int, var_update: GroupVarUpdate, session: Session = Depends(get_session)):
    db_var = GroupVarService.update(session=session, var_id=var_id, var_update=var_update)
    if not db_var:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Variável com ID {var_id} não encontrada"
        )
    return db_var


@router.delete("/{var_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group_var(var_id: int, session: Session = Depends(get_session)):
    success = GroupVarService.delete(session=session, var_id=var_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Variável com ID {var_id} não encontrada"
        )
    return None