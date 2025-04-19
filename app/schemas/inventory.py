from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel

from app.models.inventory import GroupBase, HostBase, GroupVarBase, HostVarBase

# Esquemas para criar e atualizar entidades


class GroupCreate(GroupBase):
    pass


class GroupUpdate(SQLModel):
    name: Optional[str] = None    
    parent_group_id: Optional[int] = None


class HostCreate(HostBase):
    # Adicionando campo para associar a grupos na criação
    group_ids: Optional[List[int]] = None


class HostUpdate(SQLModel):
    hostname: Optional[str] = None
    ansible_host: Optional[str] = None
    ansible_port: Optional[int] = None
    ansible_user: Optional[str] = None
    ansible_connection: Optional[str] = None
    # Adicionando campo para atualizar associação com grupos
    group_ids: Optional[List[int]] = None


class GroupVarCreate(GroupVarBase):
    pass


class GroupVarUpdate(SQLModel):
    var_name: Optional[str] = None
    var_value: Optional[str] = None
    is_encrypted: Optional[bool] = None


class HostVarCreate(HostVarBase):
    pass


class HostVarUpdate(SQLModel):
    var_name: Optional[str] = None
    var_value: Optional[str] = None
    is_encrypted: Optional[bool] = None

# Esquema para associar hosts a grupos


class HostGroupAssociation(SQLModel):
    host_id: int
    group_id: int

# Esquemas para respostas


class GroupRead(GroupBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class HostRead(HostBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class GroupVarRead(GroupVarBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class HostVarRead(HostVarBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# Esquemas para respostas incluindo relacionamentos


class GroupWithDetails(GroupRead):
    hosts: List[HostRead] = []
    variables: List[GroupVarRead] = []
    parent: Optional[GroupRead] = None
    children: List["GroupWithDetails"] = []


class HostWithDetails(HostRead):
    groups: List[GroupRead] = []
    variables: List[HostVarRead] = []

# Esquema para exportação de inventário no formato Ansible


class AnsibleInventory(SQLModel):
    groups: dict
