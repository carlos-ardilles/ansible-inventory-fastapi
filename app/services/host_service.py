from typing import List, Optional
from sqlmodel import Session, select

from app.models.inventory import Host
from app.schemas.inventory import HostCreate, HostUpdate

class HostService:
    @staticmethod
    def create(session: Session, host_create: HostCreate) -> Host:
        host = Host.from_orm(host_create)
        session.add(host)
        session.commit()
        session.refresh(host)
        return host

    @staticmethod
    def get_by_id(session: Session, host_id: int) -> Optional[Host]:
        return session.get(Host, host_id)

    @staticmethod
    def get_by_name(session: Session, name: str) -> Optional[Host]:
        statement = select(Host).where(Host.name == name)
        result = session.exec(statement).first()
        return result

    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 100) -> List[Host]:
        statement = select(Host).offset(skip).limit(limit)
        return session.exec(statement).all()

    @staticmethod
    def get_by_group(session: Session, group_id: int, skip: int = 0, limit: int = 100) -> List[Host]:
        statement = select(Host).where(Host.group_id == group_id).offset(skip).limit(limit)
        return session.exec(statement).all()

    @staticmethod
    def update(session: Session, host_id: int, host_update: HostUpdate) -> Optional[Host]:
        db_host = session.get(Host, host_id)
        if not db_host:
            return None

        host_data = host_update.dict(exclude_unset=True)
        for key, value in host_data.items():
            setattr(db_host, key, value)

        session.add(db_host)
        session.commit()
        session.refresh(db_host)
        return db_host

    @staticmethod
    def delete(session: Session, host_id: int) -> bool:
        db_host = session.get(Host, host_id)
        if not db_host:
            return False

        session.delete(db_host)
        session.commit()
        return True