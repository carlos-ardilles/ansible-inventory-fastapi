from typing import List, Optional
from sqlmodel import Session, select

from app.models.inventory import Group
from app.schemas.inventory import GroupCreate, GroupUpdate

class GroupService:
    @staticmethod
    def create(session: Session, group_create: GroupCreate) -> Group:
        # Atualizar para usar model_validate ao invés de from_orm (que está depreciado)
        group = Group.model_validate(group_create.model_dump())
        session.add(group)
        session.commit()
        session.refresh(group)
        return group

    @staticmethod
    def get_by_id(session: Session, group_id: int) -> Optional[Group]:
        return session.get(Group, group_id)

    @staticmethod
    def get_by_name(session: Session, name: str) -> Optional[Group]:
        statement = select(Group).where(Group.name == name)
        result = session.exec(statement).first()
        return result

    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 100) -> List[Group]:
        statement = select(Group).offset(skip).limit(limit)
        return session.exec(statement).all()

    @staticmethod
    def update(session: Session, group_id: int, group_update: GroupUpdate) -> Optional[Group]:
        db_group = session.get(Group, group_id)
        if not db_group:
            return None

        # Atualizado para usar model_dump ao invés de dict (que está depreciado)
        group_data = group_update.model_dump(exclude_unset=True)
        for key, value in group_data.items():
            setattr(db_group, key, value)

        session.add(db_group)
        session.commit()
        session.refresh(db_group)
        return db_group

    @staticmethod
    def delete(session: Session, group_id: int) -> bool:
        db_group = session.get(Group, group_id)
        if not db_group:
            return False

        # Excluir primeiro todas as variáveis de grupo associadas
        for var in db_group.variables:
            session.delete(var)

        # Atualizar todos os hosts associados para não ter grupo (NÃO EXCLUIR os hosts)
        for host in db_group.hosts:
            host.group_id = None
            session.add(host)

        # Agora é seguro excluir o grupo
        session.delete(db_group)
        session.commit()
        return True