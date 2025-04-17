from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class GroupBase(SQLModel):
    name: str = Field(index=True)
    description: Optional[str] = None


class Group(GroupBase, table=True):
    __tablename__ = "groups"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relacionamentos
    hosts: List["Host"] = Relationship(back_populates="group")
    variables: List["GroupVar"] = Relationship(back_populates="group")


class HostBase(SQLModel):
    name: str = Field(index=True)
    ip_address: str
    description: Optional[str] = None
    group_id: Optional[int] = Field(default=None, foreign_key="groups.id")


class Host(HostBase, table=True):
    __tablename__ = "hosts"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relacionamentos
    group: Optional[Group] = Relationship(back_populates="hosts")
    variables: List["HostVar"] = Relationship(back_populates="host")


class GroupVarBase(SQLModel):
    key: str = Field(index=True)
    value: str
    group_id: int = Field(foreign_key="groups.id")


class GroupVar(GroupVarBase, table=True):
    __tablename__ = "group_vars"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relacionamento
    group: Group = Relationship(back_populates="variables")


class HostVarBase(SQLModel):
    key: str = Field(index=True)
    value: str
    host_id: int = Field(foreign_key="hosts.id")


class HostVar(HostVarBase, table=True):
    __tablename__ = "host_vars"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Relacionamento
    host: Host = Relationship(back_populates="variables")