# Workshop de Agentes Provizio

Este repositório contém o código de demonstração do workshop **Do Prompt ao Protocolo** apresentado no Summit de Inteligência Artificial. O objetivo é mostrar como criar agentes autônomos ou colaborativos utilizando ferramentas open source, o Model Context Protocol (MCP) e uma arquitetura de microsserviços flexível.

- **Slides:** <https://gamma.app/docs/hailgn3c8h1p1at>
- **Arquitetura:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Guia de configuração:** [SETUP.md](SETUP.md)
- **Visão geral dos agentes:** [agentic_ai/agents/README.md](agentic_ai/agents/README.md)

---

## Visão Geral

A stack roda totalmente em Docker e fornece um ambiente completo para experimentar agentes conversacionais:

- **Backend FastAPI** expondo as APIs `/chat`, `/reset_session` e `/history`.
- **Frontend Streamlit** para interagir com os agentes em uma interface de chat.
- **Serviço MCP** que oferece ferramentas e acesso à base de conhecimento via Server‑Sent Events.
- **Banco SQLite** preenchido com clientes e cenários fictícios.

Todos os containers utilizam hot‑reloading; alterações no código ou no `.env` reiniciam automaticamente o serviço correspondente.

---

## Uso

1. Siga os passos de [SETUP.md](SETUP.md) para criar seu `.env` e iniciar a stack Docker.
2. Escolha qual implementação de agente executar definindo `AGENT_MODULE` no `.env`. Consulte [agentic_ai/agents/README.md](agentic_ai/agents/README.md) para as opções disponíveis.
3. Abra `http://localhost:8501` para conversar com o agente. O histórico é mantido por sessão.

Para entender como cada serviço se relaciona e como os agentes utilizam as ferramentas do MCP, leia [ARCHITECTURE.md](ARCHITECTURE.md).

---

**Autor:** Felipe Guilherme Sabino
