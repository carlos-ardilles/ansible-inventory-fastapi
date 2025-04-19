from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select

from app.models.inventory import Group, HostGroupLink
from app.schemas.inventory import GroupCreate, GroupUpdate


class GroupService:
    @staticmethod
    def create(session: Session, group_create: GroupCreate) -> Group:
        # Criar o grupo
        group_data = group_create.model_dump()
        group = Group(**group_data)

        # Definir timestamps
        group.created_at = datetime.now()
        group.updated_at = datetime.now()

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
    def get_children(session: Session, parent_id: int) -> List[Group]:
        statement = select(Group).where(Group.parent_group_id == parent_id)
        return session.exec(statement).all()

    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 100) -> List[Group]:
        statement = select(Group).offset(skip).limit(limit)
        return session.exec(statement).all()

    @staticmethod
    def get_top_level_groups(session: Session, skip: int = 0, limit: int = 100) -> List[Group]:
        """Obter apenas os grupos de nível superior (sem pai)"""
        statement = select(Group).where(
            Group.parent_group_id == None).offset(skip).limit(limit)
        return session.exec(statement).all()

    @staticmethod
    def update(session: Session, group_id: int, group_update: GroupUpdate) -> Optional[Group]:
        db_group = session.get(Group, group_id)
        if not db_group:
            return None

        # Atualizar os campos do grupo
        group_data = group_update.model_dump(exclude_unset=True)
        for key, value in group_data.items():
            setattr(db_group, key, value)

        # Atualizar timestamp
        db_group.updated_at = datetime.now()

        session.add(db_group)
        session.commit()
        session.refresh(db_group)
        return db_group

    @staticmethod
    def delete(session: Session, group_id: int) -> bool:
        db_group = session.get(Group, group_id)
        if not db_group:
            return False

        # Verificar se há grupos filhos e mover para o mesmo nível ou para o pai do grupo atual
        child_groups = session.exec(select(Group).where(
            Group.parent_group_id == group_id)).all()
        for child in child_groups:
            # Move para o mesmo nível ou para None
            child.parent_group_id = db_group.parent_group_id
            session.add(child)

        # Excluir variáveis de grupo associadas
        for var in db_group.variables:
            session.delete(var)

        # Excluir associações de host-grupo, não os hosts em si
        host_group_links = session.exec(
            select(HostGroupLink).where(HostGroupLink.group_id == group_id)
        ).all()
        for link in host_group_links:
            session.delete(link)

        # Agora é seguro excluir o grupo
        session.delete(db_group)
        session.commit()
        return True

    @staticmethod
    def add_host(session: Session, group_id: int, host_id: int) -> bool:
        # Verificar se a associação já existe
        existing = session.exec(
            select(HostGroupLink)
            .where(HostGroupLink.host_id == host_id, HostGroupLink.group_id == group_id)
        ).first()

        if existing:
            return True  # Já existe

        # Criar nova associação
        link = HostGroupLink(host_id=host_id, group_id=group_id)
        session.add(link)
        session.commit()
        return True

    @staticmethod
    def remove_host(session: Session, group_id: int, host_id: int) -> bool:
        # Verificar se a associação existe e excluí-la
        result = session.exec(
            select(HostGroupLink)
            .where(HostGroupLink.host_id == host_id, HostGroupLink.group_id == group_id)
        ).first()

        if not result:
            return False

        session.delete(result)
        session.commit()
        return True

    @staticmethod
    def get_hosts(session: Session, group_id: int, skip: int = 0, limit: int = 100) -> List:
        """Obter todos os hosts associados a este grupo"""
        # Esta consulta usa o relacionamento muitos-para-muitos através da tabela de link
        from app.models.inventory import Host
        statement = (
            select(Host)
            .join(HostGroupLink, Host.id == HostGroupLink.host_id)
            .where(HostGroupLink.group_id == group_id)
            .offset(skip)
            .limit(limit)
        )
        return session.exec(statement).all()
