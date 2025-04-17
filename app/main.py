from fastapi import FastAPI, APIRouter, Depends
from sqlmodel import SQLModel

from app.core.config import settings
from app.core.auth import get_current_user, User, has_role
from app.db.session import engine
from app.api.endpoints import groups, hosts, group_vars, host_vars, inventory, auth

# Criar as tabelas no banco de dados
def create_tables():
    SQLModel.metadata.create_all(engine)

# Inicializar a aplicação FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url=f"/api/openapi.json"
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
api_router.include_router(group_vars.router, prefix="/group-vars", tags=["group-vars"])
api_router.include_router(host_vars.router, prefix="/host-vars", tags=["host-vars"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])

# Adicionar o prefixo global da API
app.include_router(api_router, prefix=f"/api/{settings.API_VERSION}")

@app.get("/", include_in_schema=False)
def root():
    return {"message": f"Bem-vindo à {settings.PROJECT_NAME}! Use /api/docs para acessar a documentação."}

# Evento de inicialização
@app.on_event("startup")
async def startup_event():
    create_tables()