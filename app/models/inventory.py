from typing import List, Optional, Set
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

# Tabela de relacionamento muitos-para-muitos entre hosts e groups


class HostGroupLink(SQLModel, table=True):
    __tablename__ = "host_group_membership"

    host_id: int = Field(foreign_key="hosts.id", primary_key=True)
    group_id: int = Field(foreign_key="groups.id", primary_key=True)


class GroupBase(SQLModel):
    name: str = Field(index=True)
    parent_group_id: Optional[int] = Field(
        default=None, foreign_key="groups.id")


class Group(GroupBase, table=True):
    __tablename__ = "groups"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)

    # Relacionamentos
    hosts: List["Host"] = Relationship(
        back_populates="groups",
        link_model=HostGroupLink
    )
    variables: List["GroupVar"] = Relationship(back_populates="group")
    # Auto-relacionamento para grupos pais/filhos
    parent: Optional["Group"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Group.id"}
    )
    children: List["Group"] = Relationship(
        back_populates="parent"
    )


class HostBase(SQLModel):
    hostname: str = Field(index=True)
    ansible_host: Optional[str] = Field(default=None)
    ansible_port: int = Field(default=22)
    ansible_user: Optional[str] = Field(default=None, max_length=100)
    ansible_connection: Optional[str] = Field(default="ssh", max_length=50)


class Host(HostBase, table=True):
    __tablename__ = "hosts"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)

    # Relacionamentos
    groups: List[Group] = Relationship(
        back_populates="hosts",
        link_model=HostGroupLink
    )
    variables: List["HostVar"] = Relationship(back_populates="host")


class GroupVarBase(SQLModel):
    var_name: str = Field(index=True)
    var_value: str
    is_encrypted: bool = Field(default=False)
    group_id: int = Field(foreign_key="groups.id")


class GroupVar(GroupVarBase, table=True):
    __tablename__ = "group_vars"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)

    # Relacionamento
    group: Group = Relationship(back_populates="variables")


class HostVarBase(SQLModel):
    var_name: str = Field(index=True)
    var_value: str
    is_encrypted: bool = Field(default=False)
    host_id: int = Field(foreign_key="hosts.id")


class HostVar(HostVarBase, table=True):
    __tablename__ = "host_vars"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)

    # Relacionamento
    host: Host = Relationship(back_populates="variables")
