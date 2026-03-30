# Episódio 015 — Remember Me: Como construímos um sistema de memória real para um assistente de IA

## Visão geral
Neste episódio, ARIA explica por que a maioria dos assistentes de IA se sente esquecido e por que isso quebra a continuidade, a confiança e a utilidade ao longo do tempo. A equipe explica como projetaram e implementaram uma pilha de memória prática, em vez de depender de hacks frágeis ou armazenamentos de vetores genéricos. No final, os ouvintes obtêm um plano realista para construir uma camada de memória local de longa duração que pode impulsionar um comportamento de IA mais confiável e personalizado.

## O que você aprenderá
- Por que a memória IA baseada em conversação padrão falha para assistentes e usuários reais.
- As restrições práticas que moldaram um sistema de memória real: latência, privacidade e controle local.
- Como avaliar múltiplas abordagens de memória antes de decidir por uma arquitetura.
- Os detalhes concretos de implementação da pilha de memória de produção (ingestão, incorporação, armazenamento, recuperação).
- Trocas importantes que a equipe fez em relação à qualidade do contexto, comportamento de recall e sobrecarga de manutenção.
- Por que rejeitaram o LanceDB e o que o substituiu.
- Como enviar um sistema de memória que possa evoluir sem se prender a decisões frágeis sobre fornecedores ou esquemas.

## Tópicos abordados
- 00h00 — Abertura a Frio
- 02:00 — O problema com a memória AI padrão
- 08:00 — O cenário da solução (todas as 7 opções)
- 20:00 — A construção: o que realmente implementamos
- 32:00 - Principais decisões e por quê
- 40:00 - Como é uma boa memória de IA
- 48:00 - O que vem a seguir
- 55:00 – Encerramento

## Principais tecnologias mencionadas
- Mem0 OSS v1.0.7
- Qdrant (modo de arquivo local)
- transformadores de sentença multi-qa-MiniLM-L6-cos-v1 (384 dims)
- Inferência distribuída EXO (mlx-community/gpt-oss-120b-MXFP4-Q8 no M3 Ultra)
- Servidor de incorporação local (porta 11435, compatível com OpenAI /v1/embeddings)
- macOS LaunchAgent
- LanceDB (e por que foi descartado)
- MEMORY.md + registros diários de remarcação

##Links
-OpenClaw: https://openclaw.ai
- OSS Mem0: https://github.com/mem0ai/mem0
- Qdrant: https://qdrant.tech
-LanceDB: https://lancedb.github.io/lancedb/
- transformadores de frases: https://www.sbert.net
-EXO: https://github.com/exo-explore/exo

## Transcrição
Transcrição completa disponível em: https://tobyonfitnesstech.com/pt/podcasts/episode-15/