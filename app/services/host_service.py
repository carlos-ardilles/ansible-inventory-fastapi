from typing import List, Optional
from datetime import datetime
from sqlmodel import Session, select, or_

from app.models.inventory import Host, Group, HostGroupLink
from app.schemas.inventory import HostCreate, HostUpdate


class HostService:
    @staticmethod
    def create(session: Session, host_create: HostCreate) -> Host:
        # Extrair group_ids do objeto de criação antes de criar o host
        group_ids = None
        if hasattr(host_create, 'group_ids'):
            group_ids = host_create.model_dump().pop('group_ids', None)

        # Criar o objeto host sem os group_ids
        host_data = host_create.model_dump(
            exclude={"group_ids"} if hasattr(host_create, 'group_ids') else {})
        host = Host(**host_data)

        # Definir timestamps
        host.created_at = datetime.now()
        host.updated_at = datetime.now()

        session.add(host)
        session.flush()  # Para obter o ID antes de commit

        # Associar aos grupos se group_ids foram fornecidos
        if group_ids:
            for group_id in group_ids:
                host_group_link = HostGroupLink(
                    host_id=host.id, group_id=group_id)
                session.add(host_group_link)

        session.commit()
        session.refresh(host)
        return host

    @staticmethod
    def get_by_id(session: Session, host_id: int) -> Optional[Host]:
        return session.get(Host, host_id)

    @staticmethod
    def get_by_hostname(session: Session, hostname: str) -> Optional[Host]:
        statement = select(Host).where(Host.hostname == hostname)
        result = session.exec(statement).first()
        return result

    @staticmethod
    def get_all(session: Session, skip: int = 0, limit: int = 100) -> List[Host]:
        statement = select(Host).offset(skip).limit(limit)
        return session.exec(statement).all()

    @staticmethod
    def get_by_group(session: Session, group_id: int, skip: int = 0, limit: int = 100) -> List[Host]:
        # Buscar todos os hosts associados a um grupo específico
        statement = (
            select(Host)
            .join(HostGroupLink, Host.id == HostGroupLink.host_id)
            .where(HostGroupLink.group_id == group_id)
            .offset(skip)
            .limit(limit)
        )
        return session.exec(statement).all()

    @staticmethod
    def get_by_ansible_connection(session: Session, connection_type: str, skip: int = 0, limit: int = 100) -> List[Host]:
        statement = (
            select(Host)
            .where(Host.ansible_connection == connection_type)
            .offset(skip)
            .limit(limit)
        )
        return session.exec(statement).all()

    @staticmethod
    def search_hosts(session: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[Host]:
        # Buscar hosts por hostname ou ansible_host
        statement = (
            select(Host)
            .where(
                or_(
                    Host.hostname.contains(search_term),
                    Host.ansible_host.contains(search_term),
                    Host.ansible_user.contains(search_term)
                )
            )
            .offset(skip)
            .limit(limit)
        )
        return session.exec(statement).all()

    @staticmethod
    def update(session: Session, host_id: int, host_update: HostUpdate) -> Optional[Host]:
        db_host = session.get(Host, host_id)
        if not db_host:
            return None

        # Extrair group_ids se existirem
        group_ids = None
        if hasattr(host_update, 'group_ids'):
            group_ids = host_update.model_dump().pop('group_ids', None)

        # Atualizar os campos do host
        host_data = host_update.model_dump(exclude={"group_ids"} if hasattr(
            host_update, 'group_ids') else {}, exclude_unset=True)
        for key, value in host_data.items():
            setattr(db_host, key, value)

        # Atualizar timestamp
        db_host.updated_at = datetime.now()

        # Atualizar associações de grupo se fornecidas
        if group_ids is not None:
            # Remover associações existentes
            session.exec(
                select(HostGroupLink).where(HostGroupLink.host_id == host_id)
            ).delete()
            session.flush()

            # Adicionar novas associações
            for group_id in group_ids:
                host_group_link = HostGroupLink(
                    host_id=host_id, group_id=group_id)
                session.add(host_group_link)

        session.add(db_host)
        session.commit()
        session.refresh(db_host)
        return db_host

    @staticmethod
    def delete(session: Session, host_id: int) -> bool:
        db_host = session.get(Host, host_id)
        if not db_host:
            return False

        # Excluir variáveis associadas
        for var in db_host.variables:
            session.delete(var)

        # Excluir associações de grupo
        session.exec(
            select(HostGroupLink).where(HostGroupLink.host_id == host_id)
        ).delete()

        # Finalmente excluir o host
        session.delete(db_host)
        session.commit()
        return True

    @staticmethod
    def add_to_group(session: Session, host_id: int, group_id: int) -> bool:
        # Verificar se o host e grupo existem
        host = session.get(Host, host_id)
        group = session.get(Group, group_id)
        if not host or not group:
            return False

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
    def remove_from_group(session: Session, host_id: int, group_id: int) -> bool:
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
