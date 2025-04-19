from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select

from app.models.inventory import GroupVar
from app.schemas.inventory import GroupVarCreate, GroupVarUpdate


class GroupVarService:
    @staticmethod
    def create(session: Session, group_var_create: GroupVarCreate) -> GroupVar:
        # Criar uma nova variável de grupo
        group_var_data = group_var_create.model_dump()
        group_var = GroupVar(**group_var_data)

        # Definir timestamps
        group_var.created_at = datetime.now()
        group_var.updated_at = datetime.now()

        session.add(group_var)
        session.commit()
        session.refresh(group_var)
        return group_var

    @staticmethod
    def get_by_id(session: Session, var_id: int) -> Optional[GroupVar]:
        return session.get(GroupVar, var_id)

    @staticmethod
    def get_by_name_and_group(session: Session, var_name: str, group_id: int) -> Optional[GroupVar]:
        statement = select(GroupVar).where(
            GroupVar.var_name == var_name,
            GroupVar.group_id == group_id
        )
        return session.exec(statement).first()

    @staticmethod
    def get_all_by_group(session: Session, group_id: int) -> List[GroupVar]:
        statement = select(GroupVar).where(GroupVar.group_id == group_id)
        return session.exec(statement).all()

    @staticmethod
    def update(session: Session, var_id: int, var_update: GroupVarUpdate) -> Optional[GroupVar]:
        db_var = session.get(GroupVar, var_id)
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
        db_var = session.get(GroupVar, var_id)
        if not db_var:
            return False

        session.delete(db_var)
        session.commit()
        return True

    @staticmethod
    def set_encrypted(session: Session, var_id: int, is_encrypted: bool) -> Optional[GroupVar]:
        """Definir o status de criptografia de uma variável"""
        db_var = session.get(GroupVar, var_id)
        if not db_var:
            return None

        db_var.is_encrypted = is_encrypted
        db_var.updated_at = datetime.now()

        session.add(db_var)
        session.commit()
        session.refresh(db_var)
        return db_var
