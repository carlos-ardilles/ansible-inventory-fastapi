from typing import Dict, Any
from sqlmodel import Session, select

from app.models.inventory import Group, Host, GroupVar, HostVar, HostGroupLink


class InventoryService:
    @staticmethod
    def export_ansible_inventory(session: Session) -> Dict[str, Any]:
        # Buscar todos os grupos
        statement = select(Group)
        groups = session.exec(statement).all()

        inventory = {}

        # Para cada grupo, adicionar ao inventário
        for group in groups:
            group_name = group.name

            # Inicializar grupo no inventário
            if group_name not in inventory:
                inventory[group_name] = {
                    "hosts": {},
                    "vars": {},
                    "children": []
                }

            # Adicionar variáveis do grupo
            for var in group.variables:
                inventory[group_name]["vars"][var.var_name] = var.var_value

            # Adicionar hosts do grupo
            for host in group.hosts:
                host_name = host.hostname

                # Adicionar o host ao grupo
                inventory[group_name]["hosts"][host_name] = {
                    "ansible_host": host.ansible_host
                }

                # Adicionar variáveis do host
                for var in host.variables:
                    inventory[group_name]["hosts"][host_name][var.var_name] = var.var_value

        # Adicionar hosts sem grupo
        # Subconsulta para obter IDs de hosts que têm grupos
        host_ids_in_groups = select(HostGroupLink.host_id)

        # Consulta para encontrar hosts que não estão na subconsulta (hosts sem grupos)
        statement = select(Host).where(~Host.id.in_(host_ids_in_groups))
        ungrouped_hosts = session.exec(statement).all()

        if ungrouped_hosts:
            if "ungrouped" not in inventory:
                inventory["ungrouped"] = {
                    "hosts": {},
                    "vars": {}
                }

            for host in ungrouped_hosts:
                host_name = host.hostname

                # Adicionar o host aos ungrouped
                inventory["ungrouped"]["hosts"][host_name] = {
                    "ansible_host": host.ansible_host
                }

                # Adicionar variáveis do host
                for var in host.variables:
                    inventory["ungrouped"]["hosts"][host_name][var.var_name] = var.var_value

        return {
            "all": {
                "children": list(inventory.keys())
            },
            **inventory
        }
