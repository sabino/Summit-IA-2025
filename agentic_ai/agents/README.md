# Visão Geral dos Agentes

Todos os agentes implementam a interface `BaseAgent` e podem ser escolhidos pela variável `AGENT_MODULE` no arquivo `.env`. A seguir está um resumo das implementações disponíveis e o caminho de módulo que deve ser configurado.

## Agentes AutoGen

- **Single Agent Loop** (`agents.autogen.single_agent.loop_agent`)
  - Executa um único assistente em loop utilizando o `RoundRobinGroupChat` do AutoGen.
  - As ferramentas são obtidas do serviço MCP na inicialização.
  - Defina `AGENT_MODULE=agents.autogen.single_agent.loop_agent`.

- **Collaborative Round‑Robin** (`agents.autogen.multi_agent.collaborative_multi_agent_round_robin`)
  - Quatro assistentes especializados mais um orquestrador se revezam em ordem fixa.
  - Indicado para solicitações de múltiplos domínios em que cada agente contribui com informações.
  - Defina `AGENT_MODULE=agents.autogen.multi_agent.collaborative_multi_agent_round_robin`.

- **Collaborative Selector Group** (`agents.autogen.multi_agent.collaborative_multi_agent_selector_group`)
  - Semelhante ao round-robin, mas utiliza `SelectorGroupChat` do AutoGen para escolher dinamicamente o próximo falante.
  - Defina `AGENT_MODULE=agents.autogen.multi_agent.collaborative_multi_agent_selector_group`.

- **Handoff Multi‑Domain** (`agents.autogen.multi_agent.handoff_multi_domain_agent`)
  - Utiliza uma arquitetura tipo Swarm onde um coordenador delega tarefas para especialistas de cobrança ou produto.
  - Defina `AGENT_MODULE=agents.autogen.multi_agent.handoff_multi_domain_agent`.

- **Reflection Agent** (`agents.autogen.multi_agent.reflection_agent`)
  - Implementa um par primário/crítico que refina a resposta iterativamente.
  - Defina `AGENT_MODULE=agents.autogen.multi_agent.reflection_agent`.

## Agentes Semantic Kernel

- **Single Chat Agent** (`agents.semantic_kernel.single_agent.chat_agent`)
  - Agente minimalista construído com Semantic Kernel e o `MCPSsePlugin`.

- **Collaborative Multi‑Agent** (`agents.semantic_kernel.multi_agent.collaborative_multi_agent`)
  - Implementação SK do orquestrador e especialistas multi-domínio utilizando `AgentGroupChat`.

- **Handoff Multi‑Agent** (`agents.semantic_kernel.multi_agent.handoff_multi_agent`)
  - Agente de triagem que direciona as solicitações para especialistas dentro do Semantic Kernel.

- **Reflection Multi‑Agent** (`agents.semantic_kernel.multi_agent.reflection_agent`)
  - Agentes primário e crítico coordenados por meio de threads de chat do Semantic Kernel.

## Serviço de Agente Legacy

- **FastMCP Agent** (`agents.agent_service.single_agent.agent`)
  - Protótipo inicial chamando funções MCP diretamente por meio do `fastmcp`.
  - Demonstra invocação manual de ferramentas sem AutoGen ou Semantic Kernel.

Para executar qualquer agente, defina o caminho de módulo correspondente no `.env` e reinicie a stack Docker. Todos os agentes dependem do backend para expor `/chat` e manter o estado de sessão.
