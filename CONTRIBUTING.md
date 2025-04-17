# Contribuindo para o Ansible Inventory API

Obrigado por considerar contribuir para o Ansible Inventory API! Este documento fornece diretrizes e passos para contribuir com o projeto.

## Como contribuir

Existem várias maneiras de contribuir com o projeto:

1. **Reportar bugs**: Abra uma issue descrevendo o bug, incluindo passos para reproduzi-lo
2. **Sugerir melhorias**: Abra uma issue descrevendo a melhoria ou nova funcionalidade
3. **Enviar pull requests**: Implemente correções de bugs ou novas funcionalidades

## Processo de Pull Request

1. Faça um fork do repositório
2. Clone seu fork localmente
3. Crie um branch para suas alterações
   ```bash
   git checkout -b feature/nome-da-funcionalidade
   ```
4. Implemente suas alterações
5. Adicione testes para novas funcionalidades
6. Execute os testes para garantir que estão passando
   ```bash
   python -m pytest app/tests
   ```
7. Faça commit das suas alterações
8. Envie para seu fork
9. Abra um Pull Request para o repositório principal

## Diretrizes de código

- Siga o estilo de código PEP 8
- Documente novas funções, métodos e classes
- Mantenha a cobertura de testes
- Evite dependências desnecessárias

## Executando testes

```bash
# Executar todos os testes
python -m pytest app/tests

# Executar testes com cobertura
python -m pytest app/tests --cov=app

# Executar testes específicos
python -m pytest app/tests/test_group_service.py
```

## Estrutura do projeto

- `app/`: Código fonte principal
  - `api/endpoints/`: Endpoints da API REST
  - `core/`: Configuração e funcionalidades centrais
  - `db/`: Configuração do banco de dados
  - `models/`: Modelos de dados SQLModel
  - `schemas/`: Esquemas Pydantic
  - `services/`: Lógica de negócios
  - `tests/`: Testes automatizados

## Fluxo de desenvolvimento

1. Verificar issues abertas ou abrir uma nova para discutir suas alterações
2. Implementar alterações em um branch separado
3. Adicionar ou atualizar testes conforme necessário
4. Garantir que todos os testes passem
5. Enviar um Pull Request

## Versionamento

Este projeto segue o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## Código de Conduta

Ao contribuir para este projeto, você concorda em respeitar todos os colaboradores e manter um ambiente amigável e produtivo.