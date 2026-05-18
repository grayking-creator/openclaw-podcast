# OpenClaw Daily EP052: Agentes Locais Ganham Sua Semana de Hardware

Este episódio acompanha seis movimentos concretos no stack de agentes. O centro de gravidade é a infraestrutura local-first: executores de modelos locais, aceleração Apple Silicon, DGX Spark como máquina de agente local, inferência distribuída EXO, CLIs de agentes de codificação e a camada de gateway que mantém o roteamento de modelos de não se tornar frágil.

[00:00] Ollama evolui de executor de modelo para plataforma de agentes de codificação

Os lançamentos recentes do Ollama mostram que ele está se tornando mais do que um servidor local de modelos. Os principais destaques são o suporte ao Codex App através do Ollama Launch, suporte a modelos de visão para opencode launch, correções locais de caminhos de imagem para resultados de ferramentas do Claude e cache de resposta de API show que melhora a latência mediana de carga de integração em cerca de 6,7x.

O item mais importante com olhar para o futuro é a versão 0.30.0 release candidate. O Ollama afirma que essa versão muda a arquitetura para suportar diretamente llama.cpp, permite compatibilidade com arquivos GGUF e usa MLX para acelerar inferência no Apple Silicon. O trabalho feito em maio também adicionou speculative decoding MTP do Gemma 4 no executor MLX, com mais de 2x de aumento de velocidade reivindicado para tarefas de codificação do Gemma 4 31B.

A leitura prática: o Ollama está se aproximando de ser uma camada de runtime local para agentes de codificação e ferramentas de IA desktop. Portabilidade de modelos, aceleração MLX, chamadas de metadados mais rápidas, integrações de launch e entradas de visão importam quando um agente local precisa fazer trabalho real de projeto em vez de apenas responder prompts.

Fontes:

- https://github.com/ollama/ollama/releases

[05:00] LM Studio melhora inferência de visão MLX e aponta para servidores locais compartilhados

O LM Studio 0.4.13 Shipsa mlx-engine v1.8.1. O changelog oficial diz que melhora significativamente a performance e adiciona predições paralelas para modelos com capacidade de visão incluindo Qwen 3.5/3.6 e Gemma 4. A mesma versão corrige o tratamento de newlines colados e inclui hardening de segurança.

Isso parece pequeno até você colocar ao lado de para onde o LM Studio está indo com máquinas maiores. Seu material do DGX Station descreve um daemon headless, llmster, pareado com LM Link para que uma máquina possa servir modelos locais para outros dispositivos. Também menciona os SDKs do LM Studio, a API do LM Studio e APIs compatíveis com OpenAI e Anthropic.

A relevância para builders é direta: IA local está se tornando um stack de duas partes. Um laptop ou Mac pode ser a interface, enquanto uma máquina local maior lida com a carga do modelo. Para agentes de visão, melhorias de predição paralela MLX importam porque capturas de tela, imagens, estado de UI e contexto de projeto multimodal estão se tornando inputs normais, não demos.

Fontes:

- https://lmstudio.ai/changelog/lmstudio-v0.4.13
- https://lmstudio.ai/blog/dgx-station

[10:00] DGX Spark se torna um alvo sério para agentes locais

A mensagem atual da NVIDIA sobre DGX Spark e RTX é explicitamente sobre agentes locais. A empresa está posicionando essas máquinas como computadores de agentes para executar agentes pessoais localmente, privadamente e sem custos de token. Seu material do GTC destaca Nemotron 3 Nano 4B, Nemotron 3 Super 120B, otimizações Qwen 3.5, Mistral Small 4 e stacks de agentes locais rodando através do Ollama, LM Studio e llama.cpp.

O DGX Spark importa por causa do formato de memória e deployment. A NVIDIA descreve o DGX Spark com 128GB de memória unificada, suficiente para modelos acima de 120 bilhões de parâmetros. Nemotron 3 Super é descrito como um modelo aberto de 120B com 12B parâmetros ativos, enquanto modelos menores como Nemotron 3 Nano 4B miram máquinas RTX mais restritas.

O ponto não é que todo builder deveria comprar um. O ponto é que software de agente local agora tem um tier de hardware acima de um desktop único e abaixo de infraestrutura GPU de nuvem alugada. Se agentes locais vão manter contexto privado, rodar o dia todo e chamar ferramentas sem pagar custos de cloud por token para cada passo, máquinas como DGX Spark se tornam infraestrutura relevante.

Fontes:

- https://blogs.nvidia.com/blog/rtx-ai-garage-gtc-2026-nemoclaw/
- https://build.nvidia.com/spark/hermes-agent

[15:00] EXO mais DGX Spark mostra que inferência local distribuída é real mas ainda rough

Uma issue do EXO sobre DGX Spark é mais útil que um press release limpo porque mostra o modo real de falha. O cluster tinha Macs e um DGX Spark na mesma rede local, conectividade básica funcionou, acesso ao dashboard EXO funcionou e as portas estavam acessíveis. Mas os nodes ainda não formaram um cluster de inferência distribuída funcionando.

A correção reportada teve duas partes. Primeiro, o módulo de rede exo_pyo3_bindings do Rust, que contém libp2p networking, descoberta mDNS e lógica de rede privada, precisou ser compilado manualmente no Linux/aarch64. Segundo, todos os nodes precisavam do mesmo EXO_LIBP2P_NAMESPACE para que a chave de rede privada libp2p combinasse em todo o cluster.

Depois disso, o DGX Spark apareceu no painel EXO e participou de inferência distribuída. Essa é a verdadeira história: o EXO está tackling o problema certo de cluster local, mas a inferência local distribuída vive ou morre com discovery, packaging, alinhamento de namespace e builds específicos para arquitetura. Computação bruta não é suficiente se os nós não conseguirem encontrar e confiar uns nos outros de forma confiável.

Fontes:
- https://github.com/exo-explore/exo/issues/1682

[20:00] Grok Build chega, mas redirecionamentos de modelos e preços precisam de atenção

Os docs do Grok Build da xAI descrevem uma superfície completa de CLI de coding-agent: um TUI interativo, scripting headless, saída plain/json/streaming-json, sessões retomáveis, ACP através do stdio do agente Grok, configuração customizada de modelos, skills, plugins, hooks e descoberta de servidor MCP.

Isso coloca o Grok Build na mesma categoria de outros coding-agent CLIs: um agente nativo de terminal com automation hooks, não apenas uma superfície de chat. Os docs oficiais também mostram configuração customizada de modelos, o que importa porque cada vez mais builders querem shells de coding-agent que possam rotear para diferentes backends de modelos.

A história de custos e migração é separada, mas importante. A página de descontinuação de 15 de maio da xAI diz que slugs de raciocínio depreciados redirecionam para Grok 4.3 com baixo esforço de raciocínio, slugs não-raciocinadores redirecionam para Grok 4.3 sem esforço de raciocínio, e grok-code-fast-1 redireciona para Grok 4.3. A página lista o preço da API do Grok 4.3 a $1,25 por milhão de tokens de entrada e $2,50 por milhão de tokens de saída. A recomendação prática é fazer pin de modelos de substituição explicitamente em vez de deixar slugs depreciados mudarem silenciosamente o comportamento e o faturamento.

Fontes:
- https://docs.x.ai/build/overview
- https://docs.x.ai/build/cli/headless-scripting
- https://docs.x.ai/developers/migration/may-15-retirement

[25:00] LiteLLM e Envoy fortalecem a camada de gateway de modelos

O LiteLLM v1.84.0 é uma release de fortalecimento do gateway. A release muda o versionamento para PEP 440, autentica endpoints pass-through por padrão, melhora a aplicação de budget multi-pod, evita congelamentos de reconnect do Prisma, reduz o footprint de memória através de feature routers lazy-loaded, adiciona suporte a OAuth MCP e descoberta Azure Entra, e adiciona tracking durável de workflow runs através de uma superfície de API workflow-runs.

O Envoy AI Gateway v0.6.0 está se movendo na mesma direção pelo lado do gateway Kubernetes. Ele graduate core CRDs para v1beta1, adiciona suporte a endpoint Anthropic em backends compatíveis com OpenAI, adiciona embeddings Gemini e context caching, suporta header forwarding por backend para MCP, adiciona redaction de body de request/response, e atualiza a baseline do Envoy/Gateway.

O motivo pelo qual isso pertence a um episódio de agente local é que local-first não significa gateway-free. Agentes ainda precisam de roteamento, auth, budgets, redaction, compatibilidade com provedores e autorização MCP. Quanto mais backends de modelos e runtimes locais você adiciona, mais importante o plano de controle se torna.

Fontes:
- https://docs.litellm.ai/release_notes/v1.84.0/v1-84-0
- https://aigateway.envoyproxy.io/release-notes/