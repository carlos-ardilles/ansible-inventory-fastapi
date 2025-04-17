from sqlmodel import Session, SQLModel, create_engine
import logging

from app.core.config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Opções de conexão específicas para PostgreSQL
connect_args = {}
if settings.DATABASE_TYPE.lower() == "postgresql":
    # Adicionar opções específicas para PostgreSQL se necessário
    logger.info(f"Configurando conexão para PostgreSQL: {settings.DATABASE_URL}")
else:
    # SQLite precisa desta configuração para suportar múltiplas threads
    connect_args = {"check_same_thread": False}
    logger.info(f"Configurando conexão para SQLite: {settings.DATABASE_URL}")

# Criar engine do banco de dados
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args=connect_args
)

def get_session():
    with Session(engine) as session:
        yield session