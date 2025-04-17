# Ansible Inventory API

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)

Uma API REST moderna para gerenciar inventários Ansible, construída com FastAPI e SQLModel. Perfeita para equipes que precisam gerenciar seus recursos Ansible através de uma interface programática ou web.

## 🚀 Recursos

- **Gerenciamento completo de Grupos e Hosts**: Crie, leia, atualize e exclua grupos e hosts
- **Gerenciamento de variáveis**: Configure variáveis para grupos e hosts individuais
- **Exportação de inventário**: Gere inventários em formato compatível com Ansible
- **Autenticação segura**: Integração com Keycloak via OAuth 2.0
- **API RESTful documentada**: Interface Swagger e ReDoc integradas
- **Testes abrangentes**: Cobertura completa de testes para todos os endpoints e serviços

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas:

- **API Layer**: Endpoints FastAPI para processar solicitações HTTP
- **Service Layer**: Lógica de negócios e operações do inventário
- **Data Layer**: Modelos SQLModel e acesso ao banco de dados
- **Auth Layer**: Autenticação e autorização com Keycloak

### Diagrama de Componentes

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  API Layer  │────▶│Service Layer│────▶│  Data Layer │
└─────────────┘     └─────────────┘     └─────────────┘
       │                                       │
       │                                       │
       ▼                                       ▼
┌─────────────┐                        ┌─────────────┐
│  Auth Layer │                        │   Database  │
└─────────────┘                        └─────────────┘
```

## 📊 Estrutura do Banco de Dados

- **groups**: Armazena informações sobre os grupos de hosts
- **hosts**: Armazena informações sobre os hosts individuais
- **group_vars**: Variáveis associadas a grupos específicos
- **host_vars**: Variáveis associadas a hosts específicos

## 📋 Requisitos

- Python 3.8+
- SQLModel 0.0.24+
- FastAPI 0.115.12+
- Uvicorn 0.34.1+
- Python-jose (para autenticação JWT)
- Requests (para comunicação com Keycloak)

## 🔧 Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/ansible-inventory-fastapi.git
   cd ansible-inventory-fastapi
   ```

2. Configure um ambiente virtual e instale as dependências:
   ```bash
   # Usando UV para criação do ambiente
   uv venv .venv
   source .venv/bin/activate  # Linux/Mac
   # ou
   .\.venv\Scripts\activate  # Windows

   # Instale as dependências
   uv pip install -r requirements.txt
   ```

3. Configure as variáveis de ambiente no arquivo `.env`:
   ```
   # Configurações do banco de dados
   DATABASE_URL=sqlite:///ansible_inventory.db

   # Configurações da API
   API_VERSION=v1
   PROJECT_NAME="Ansible Inventory API"

   # Configurações de autenticação do Keycloak
   KEYCLOAK_SERVER_URL=https://seu-keycloak-server/auth
   KEYCLOAK_REALM=seu-realm
   KEYCLOAK_CLIENT_ID=seu-client-id
   KEYCLOAK_CLIENT_SECRET=seu-client-secret
   KEYCLOAK_SSL_VERIFY=true
   ```

## 🚦 Executando o Projeto

Para iniciar o servidor de desenvolvimento:

```bash
# Usando o script de execução
./run.sh

# Ou diretamente
python -m app

# Ou com uvicorn
uvicorn app.main:app --reload
```

O servidor estará disponível em: http://localhost:8000

### 📖 Documentação da API

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## 🔑 Autenticação

A API usa autenticação OAuth 2.0 via Keycloak. Para acessar os endpoints protegidos, siga os passos:

1. Obtenha um token de acesso usando o endpoint de login:
   ```bash
   curl -X POST \
     "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"username":"seu-usuario", "password":"sua-senha"}'
   ```

2. Use o token recebido nos cabeçalhos de suas requisições:
   ```bash
   curl -X GET \
     "http://localhost:8000/api/v1/groups/" \
     -H "Authorization: Bearer seu-token-aqui"
   ```

3. Quando o token expirar, use o endpoint de refresh para obter um novo:
   ```bash
   curl -X POST \
     "http://localhost:8000/api/v1/auth/refresh" \
     -d "refresh_token=seu-refresh-token-aqui"
   ```

## 🧪 Testes

Execute os testes com:

```bash
# Todos os testes
python -m pytest app/tests

# Com cobertura
python -m pytest app/tests --cov=app

# Testes específicos
python -m pytest app/tests/test_group_service.py
```

## 📝 Endpoints da API

### Autenticação

- `POST /api/v1/auth/login` - Autenticar usuário e obter token
- `POST /api/v1/auth/refresh` - Renovar token usando refresh_token
- `GET /api/v1/auth/me` - Obter informações do usuário autenticado
- `GET /api/v1/me` - Obter informações do usuário autenticado (rota alternativa)

### Grupos

- `GET /api/v1/groups/` - Listar todos os grupos
- `POST /api/v1/groups/` - Criar um novo grupo
- `GET /api/v1/groups/{group_id}` - Obter detalhes de um grupo específico
- `PUT /api/v1/groups/{group_id}` - Atualizar um grupo existente
- `DELETE /api/v1/groups/{group_id}` - Remover um grupo

### Hosts

- `GET /api/v1/hosts/` - Listar todos os hosts
- `POST /api/v1/hosts/` - Criar um novo host
- `GET /api/v1/hosts/{host_id}` - Obter detalhes de um host específico
- `PUT /api/v1/hosts/{host_id}` - Atualizar um host existente
- `DELETE /api/v1/hosts/{host_id}` - Remover um host

### Variáveis de grupo

- `GET /api/v1/group-vars/group/{group_id}` - Listar variáveis de um grupo específico
- `POST /api/v1/group-vars/` - Adicionar uma variável a um grupo
- `GET /api/v1/group-vars/{var_id}` - Obter uma variável específica
- `PUT /api/v1/group-vars/{var_id}` - Atualizar uma variável existente
- `DELETE /api/v1/group-vars/{var_id}` - Remover uma variável

### Variáveis de host

- `GET /api/v1/host-vars/host/{host_id}` - Listar variáveis de um host específico
- `POST /api/v1/host-vars/` - Adicionar uma variável a um host
- `GET /api/v1/host-vars/{var_id}` - Obter uma variável específica
- `PUT /api/v1/host-vars/{var_id}` - Atualizar uma variável existente
- `DELETE /api/v1/host-vars/{var_id}` - Remover uma variável

### Inventário

- `GET /api/v1/inventory/ansible-format` - Exportar todo o inventário no formato Ansible
- `GET /api/v1/inventory/ansible-format-admin` - Exportar inventário (requer função de admin)

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia nossas [diretrizes de contribuição](CONTRIBUTING.md) antes de enviar um PR.

## 📄 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).