from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session

from app.db.session import get_session
from app.models.inventory import Host
from app.schemas.inventory import HostCreate, HostRead, HostUpdate, HostWithDetails
from app.services.host_service import HostService

router = APIRouter()


@router.post("/", response_model=HostRead, status_code=status.HTTP_201_CREATED)
def create_host(host: HostCreate, session: Session = Depends(get_session)):
    # Corrigido para usar hostname em vez de name
    db_host = HostService.get_by_hostname(session, hostname=host.hostname)
    if db_host:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Host com o hostname '{host.hostname}' já existe"
        )
    return HostService.create(session=session, host_create=host)


@router.get("/", response_model=List[HostRead])
def read_hosts(
    skip: int = 0,
    limit: int = 100,
    group_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    if group_id:
        hosts = HostService.get_by_group(
            session=session, group_id=group_id, skip=skip, limit=limit)
    else:
        hosts = HostService.get_all(session=session, skip=skip, limit=limit)
    return hosts


@router.get("/{host_id}", response_model=HostWithDetails)
def read_host(host_id: int, session: Session = Depends(get_session)):
    db_host = HostService.get_by_id(session=session, host_id=host_id)
    if db_host is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Host com ID {host_id} não encontrado"
        )
    return db_host


@router.put("/{host_id}", response_model=HostRead)
def update_host(
    host_id: int,
    host: HostUpdate,
    session: Session = Depends(get_session)
):
    db_host = HostService.update(
        session=session, host_id=host_id, host_update=host)
    if db_host is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Host com ID {host_id} não encontrado"
        )
    return db_host


@router.delete("/{host_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_host(host_id: int, session: Session = Depends(get_session)):
    success = HostService.delete(session=session, host_id=host_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Host com ID {host_id} não encontrado"
        )
    return None
