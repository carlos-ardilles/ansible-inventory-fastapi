from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session

from app.db.session import get_session
from app.models.inventory import Group
from app.schemas.inventory import GroupCreate, GroupRead, GroupUpdate, GroupWithDetails
from app.services.group_service import GroupService

router = APIRouter()

@router.post("/", response_model=GroupRead, status_code=status.HTTP_201_CREATED)
def create_group(group: GroupCreate, session: Session = Depends(get_session)):
    db_group = GroupService.get_by_name(session, name=group.name)
    if db_group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Grupo com o nome '{group.name}' já existe"
        )
    return GroupService.create(session=session, group_create=group)


@router.get("/", response_model=List[GroupRead])
def read_groups(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    groups = GroupService.get_all(session=session, skip=skip, limit=limit)
    return groups


@router.get("/{group_id}", response_model=GroupWithDetails)
def read_group(group_id: int, session: Session = Depends(get_session)):
    db_group = GroupService.get_by_id(session=session, group_id=group_id)
    if db_group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Grupo com ID {group_id} não encontrado"
        )
    return db_group


@router.put("/{group_id}", response_model=GroupRead)
def update_group(
    group_id: int,
    group: GroupUpdate,
    session: Session = Depends(get_session)
):
    db_group = GroupService.update(session=session, group_id=group_id, group_update=group)
    if db_group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Grupo com ID {group_id} não encontrado"
        )
    return db_group


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, session: Session = Depends(get_session)):
    success = GroupService.delete(session=session, group_id=group_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Grupo com ID {group_id} não encontrado"
        )
    return None