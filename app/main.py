from fastapi import FastAPI, APIRouter, Depends
from sqlmodel import SQLModel
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.auth import get_current_user, User, has_role
from app.db.session import engine
from app.api.endpoints import groups, hosts, group_vars, host_vars, inventory, auth

# Criar as tabelas no banco de dados


def create_tables():
    SQLModel.metadata.create_all(engine)

# Definir o contexto lifespan para substituir on_event


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código executado na inicialização (substitui @app.on_event("startup"))
    create_tables()
    yield
    # Código executado no encerramento (substitui @app.on_event("shutdown"))
    # Coloque aqui qualquer limpeza necessária

# Inicializar a aplicação FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url=f"/api/openapi.json",
    lifespan=lifespan
)

# Configurar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    # Permitir todas as origens em desenvolvimento. Em produção, especifique as origens permitidas.
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos
    allow_headers=["*"],  # Permitir todos os headers
)

# Agrupar as rotas sob um prefixo comum
api_router = APIRouter()

# Endpoint para obter informações do usuário autenticado


@api_router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Retorna informações sobre o usuário autenticado."""
    return current_user

# Registrar os endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(hosts.router, prefix="/hosts", tags=["hosts"])
api_router.include_router(
    group_vars.router, prefix="/group-vars", tags=["group-vars"])
api_router.include_router(
    host_vars.router, prefix="/host-vars", tags=["host-vars"])
api_router.include_router(
    inventory.router, prefix="/inventory", tags=["inventory"])

# Adicionar o prefixo global da API
app.include_router(api_router, prefix=f"/api/{settings.API_VERSION}")


@app.get("/", include_in_schema=False)
def root():
    return {"message": f"Bem-vindo à {settings.PROJECT_NAME}! Use /api/docs para acessar a documentação."}

# Removido o on_event("startup") depreciado - substituído pelo lifespan acima
