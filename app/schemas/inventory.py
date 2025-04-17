from typing import List, Optional
from sqlmodel import SQLModel

from app.models.inventory import GroupBase, HostBase, GroupVarBase, HostVarBase

# Esquemas para criar e atualizar entidades

class GroupCreate(GroupBase):
    pass

class GroupUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None

class HostCreate(HostBase):
    pass

class HostUpdate(SQLModel):
    name: Optional[str] = None
    ip_address: Optional[str] = None
    description: Optional[str] = None
    group_id: Optional[int] = None

class GroupVarCreate(GroupVarBase):
    pass

class GroupVarUpdate(SQLModel):
    key: Optional[str] = None
    value: Optional[str] = None

class HostVarCreate(HostVarBase):
    pass

class HostVarUpdate(SQLModel):
    key: Optional[str] = None
    value: Optional[str] = None

# Esquemas para respostas

class GroupRead(GroupBase):
    id: int

class HostRead(HostBase):
    id: int

class GroupVarRead(GroupVarBase):
    id: int

class HostVarRead(HostVarBase):
    id: int

# Esquemas para respostas incluindo relacionamentos

class GroupWithDetails(GroupRead):
    hosts: List[HostRead] = []
    variables: List[GroupVarRead] = []

class HostWithDetails(HostRead):
    variables: List[HostVarRead] = []

# Esquema para exportação de inventário no formato Ansible
class AnsibleInventory(SQLModel):
    groups: dict