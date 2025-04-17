from typing import List, Optional
from sqlmodel import Session, select

from app.models.inventory import GroupVar
from app.schemas.inventory import GroupVarCreate, GroupVarUpdate

class GroupVarService:
    @staticmethod
    def create(session: Session, group_var_create: GroupVarCreate) -> GroupVar:
        group_var = GroupVar.from_orm(group_var_create)
        session.add(group_var)
        session.commit()
        session.refresh(group_var)
        return group_var

    @staticmethod
    def get_by_id(session: Session, var_id: int) -> Optional[GroupVar]:
        return session.get(GroupVar, var_id)

    @staticmethod
    def get_by_key_and_group(session: Session, key: str, group_id: int) -> Optional[GroupVar]:
        statement = select(GroupVar).where(
            GroupVar.key == key,
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

        var_data = var_update.dict(exclude_unset=True)
        for key, value in var_data.items():
            setattr(db_var, key, value)

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