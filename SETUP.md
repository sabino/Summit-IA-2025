# Configuração

1. **Instale Docker e Docker Compose** caso ainda não os tenha.
2. Copie `agentic_ai/applications/.env.sample` para `.env` na raiz do projeto:

```bash
cp agentic_ai/applications/.env.sample .env
```

Preencha as variáveis necessárias, especialmente `AGENT_MODULE`, que define qual implementação de agente será carregada.

3. Construa e inicie a stack:

```bash
docker-compose up --build
```

Os serviços serão iniciados com hot‑reloading habilitado. Qualquer alteração nos arquivos de código ou no `.env` reiniciará automaticamente o container afetado.

Com tudo rodando, acesse o frontend em `http://localhost:8501`.
