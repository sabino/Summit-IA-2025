# Arquitetura

O projeto é composto por quatro serviços Docker definidos em `docker-compose.yml`.

| Serviço     | Descrição |
|-------------|---------------------------------------------------------------|
| **db-setup** | Inicializa o banco SQLite com dados de exemplo antes dos demais serviços. |
| **mcp**      | Executa o serviço MCP expondo ferramentas e base de conhecimento via Server‑Sent Events. |
| **backend**  | Aplicação FastAPI que carrega a implementação do agente e expõe `/chat` e outros endpoints. |
| **frontend** | Interface Streamlit usada para conversar com os agentes. |

Os serviços `backend` e `frontend` montam o diretório `agentic_ai`. Cada Dockerfile utiliza `watchmedo auto-restart`, portanto qualquer alteração em arquivos Python ou no `.env` reinicia automaticamente o container, permitindo um ciclo rápido de desenvolvimento.

Os agentes se comunicam com o serviço MCP por HTTP/SSE para obter ferramentas e contexto. O backend encapsula a classe de agente escolhida (definida por `AGENT_MODULE`) e fornece uma API simples consumida pelo frontend Streamlit.

