import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Ansible Inventory API")
    API_VERSION: str = os.getenv("API_VERSION", "v1")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Configuração de banco de dados
    DATABASE_TYPE: str = os.getenv("DATABASE_TYPE", "sqlite")

    # URL do banco de dados com fallback para SQLite se não configurado
    @property
    def DATABASE_URL(self) -> str:
        if self.DATABASE_TYPE.lower() == "postgresql":
            return os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ansible_inventory")
        else:
            return os.getenv("DATABASE_URL_SQLITE", "sqlite:///./ansible_inventory.db")

    # Configurações do Keycloak
    KEYCLOAK_SERVER_URL: str = os.getenv("KEYCLOAK_SERVER_URL", "http://localhost:8080/auth")
    KEYCLOAK_REALM: str = os.getenv("KEYCLOAK_REALM", "your-realm")
    KEYCLOAK_CLIENT_ID: str = os.getenv("KEYCLOAK_CLIENT_ID", "your-client-id")
    KEYCLOAK_CLIENT_SECRET: str = os.getenv("KEYCLOAK_CLIENT_SECRET", "your-client-secret")
    KEYCLOAK_SSL_VERIFY: bool = os.getenv("KEYCLOAK_SSL_VERIFY", "False").lower() == "true"

settings = Settings()