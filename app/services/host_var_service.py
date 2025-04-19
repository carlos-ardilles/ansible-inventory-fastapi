from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select

from app.models.inventory import HostVar
from app.schemas.inventory import HostVarCreate, HostVarUpdate


class HostVarService:
    @staticmethod
    def create(session: Session, host_var_create: HostVarCreate) -> HostVar:
        # Criar variável de host
        host_var_data = host_var_create.model_dump()
        host_var = HostVar(**host_var_data)

        # Definir timestamps
        host_var.created_at = datetime.now()
        host_var.updated_at = datetime.now()

        session.add(host_var)
        session.commit()
        session.refresh(host_var)
        return host_var

    @staticmethod
    def get_by_id(session: Session, var_id: int) -> Optional[HostVar]:
        return session.get(HostVar, var_id)

    @staticmethod
    def get_by_name_and_host(session: Session, var_name: str, host_id: int) -> Optional[HostVar]:
        statement = select(HostVar).where(
            HostVar.var_name == var_name,
            HostVar.host_id == host_id
        )
        return session.exec(statement).first()

    @staticmethod
    def get_all_by_host(session: Session, host_id: int) -> List[HostVar]:
        statement = select(HostVar).where(HostVar.host_id == host_id)
        return session.exec(statement).all()

    @staticmethod
    def update(session: Session, var_id: int, var_update: HostVarUpdate) -> Optional[HostVar]:
        db_var = session.get(HostVar, var_id)
        if not db_var:
            return None

        var_data = var_update.model_dump(exclude_unset=True)
        for key, value in var_data.items():
            setattr(db_var, key, value)

        # Atualizar timestamp
        db_var.updated_at = datetime.now()

        session.add(db_var)
        session.commit()
        session.refresh(db_var)
        return db_var

    @staticmethod
    def delete(session: Session, var_id: int) -> bool:
        db_var = session.get(HostVar, var_id)
        if not db_var:
            return False

        session.delete(db_var)
        session.commit()
        return True

    @staticmethod
    def set_encrypted(session: Session, var_id: int, is_encrypted: bool) -> Optional[HostVar]:
        """Definir o status de criptografia de uma variável"""
        db_var = session.get(HostVar, var_id)
        if not db_var:
            return None

        db_var.is_encrypted = is_encrypted
        db_var.updated_at = datetime.now()

        session.add(db_var)
        session.commit()
        session.refresh(db_var)
        return db_var
