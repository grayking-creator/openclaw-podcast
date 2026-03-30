# Mostrar notas - Episódio 10: A revolução do documento e da memória

## Detalhes do episódio
- **Episódio:** 10
- **Data:** 4 de março de 2026
- **Anfitriões:** Nova (britânica calorosa) e Alloy (americana)
- **Meta de duração:** 30-35 minutos
- **Tema:** OpenClaw evolui de plataforma de chat/agente para uma plataforma completa de documentos e memória

---

## Parte 1 - Do lançamento: OpenClaw 3 de março de 2026
**Notas de versão:** https://github.com/openclaw/openclaw/releases/tag/v2026.3.2

Tudo nesta seção foi enviado na versão de 3 de março:

### 1. Ferramenta de análise de PDF *(NOVO)*
- Ferramenta `pdf` de primeira classe — suporte nativo da Anthropic/Google (o modelo vê o PDF diretamente), substituto de extração para todos os outros
- Configurável: `agents.defaults.pdfModel`, `pdfMaxBytesMb`, `pdfMaxPages`
- O que isso desbloqueia: contratos, faturas, trabalhos de pesquisa, qualquer documento com o qual você realmente trabalhe

### 2. Ollama Memory Embeddings *(NOVO – aprofundamento no episódio)*
- `memorySearch.provider = "ollama"` — memória local completa/pilha RAG, nenhuma API de nuvem necessária
- Na primeira vez, você pode executar tudo — inferência E memória — sem tocar em um provedor de nuvem
- Honrs `models.providers.ollama` configurações para solicitações de incorporação
- Por que isso é importante: seu agente agora pode lembrar milhares de interações usando apenas computação local

### 3. Expansão SecretRef *(NOVO)*
- 64 alvos de credenciais agora cobertos pelo SecretRef
- Fail-fast em referências não resolvidas em superfícies ativas — sem falhas silenciosas
- Abrange: coletores de tempo de execução, planejamento/aplicação/auditoria de segredos, integração do SecretInput UX

### 4. Anexos de sessões *(NOVO)*
- `sessions_spawn` suporta anexos de arquivos embutidos (tempo de execução do subagente)
- Codificação Base64/utf8, limpeza do ciclo de vida, limites via `tools.sessions_spawn.attachments`
- Os agentes agora podem passar arquivos diretamente uns para os outros

### 5. Padrões de streaming de telegrama
- O padrão de streaming agora é `parcial` (estava `desligado`) — visualização ao vivo pronta para uso para novas configurações
- O streaming DM usa `sendMessageDraft` para visualização privada

### 6. MiniMax-M2.5-alta velocidade
- Suporte de primeira classe em catálogos e integração – variante mais rápida do MiniMax-M2.5

### 7. Validação de configuração CLI
- `openclaw config validar --json` — detecta erros antes da inicialização do gateway
- Caminhos detalhados de chaves inválidas em erros de inicialização

### 8. Plug-in pessoal Zalo reconstruído
- Integração nativa `zca-js`, totalmente em processo - sem transporte CLI externo

### 9. Saída multimídia
- Discord, Slack, WhatsApp, Zalo unificados com `sendPayload` compartilhado + iteração multimídia

### 10. Plug-in SDK/STT
- `api.runtime.stt.transcribeAudioFile()` — extensões agora podem fazer conversão de fala em texto

---

## Parte 2 — Esta semana no OpenClaw

### Artigo 1: OpenClaw ultrapassa 250.000 estrelas do GitHub
**Fonte:** ainvest.com – 3 de março de 2026
**URL:** https://www.ainvest.com/news/openclaw-github-star-count-surpasses-250-000-ai-agent-boom-2603/

OpenClaw atingiu 250.000 estrelas no GitHub – o projeto de IA mais rápido a atingir esse marco. O artigo também destaca que C3.ai (IA empresarial) perdeu as previsões de receita em 30% e anunciou uma redução de 26% na força de trabalho. O contraste é impressionante: a IA empresarial tropeça enquanto a IA auto-hospedada de código aberto explode. O design local e o suporte multiplataforma do OpenClaw são citados como principais diferenciais.

### Artigo 2: Por dentro do OpenClaw — A arquitetura que explica tudo
**Fonte:** dev.to – 4 de março de 2026
**URL:** https://dev.to/jiade/inside-openclaw-how-the-worlds-fastest-growing-ai-agent-actually-works-under-the-hood-4p5nUm mergulho técnico profundo sobre por que o OpenClaw cresceu enquanto centenas de outras estruturas de agentes de IA não. Abrange: a estratégia de incorporação do Pi SDK, o sistema de memória de duas camadas, o modelo de simultaneidade Lane Queue e o mecanismo de pulsação. A tese: não é marketing, é arquitetura. Bom episódio para explicar o que torna esta plataforma diferente de LangChain, AutoGPT e outras.

### Artigo 3: OpenClaw no mundo real (padrões de produção)
**Fonte:** Trilogia AI / Rahul Subramaniam – 3 de março de 2026
**URL:** https://trilogyai.substack.com/p/openclaw-in-the-real-world

O artigo de verificação da realidade. Abrange três modos de falha que as pessoas atingem após a configuração inicial alta: a memória falha, você perde trabalho quando a máquina é reiniciada e a confiabilidade começa a ser mais importante do que a experimentação. Fornece padrões de produção para passar de uma "demonstração interessante" para um sistema do qual você realmente depende. Conecta-se diretamente ao tema de memória do Episódio 10.

---

## Principais conclusões
Esta versão ultrapassa um limite: análise de documentos + memória local persistente + passagem de arquivos entre agentes = OpenClaw como um segundo cérebro, não apenas uma interface de chat. O marco de 250 mil estrelas e o artigo de produção no mundo real sinalizam a mesma coisa – as pessoas não estão mais experimentando, elas dependem disso.

## Padrões de construção discutidos
1. **Revisor de documentos jurídicos** — ferramenta PDF + memória + saída Slack
2. **Assistente de pesquisa local** — Embeddings Ollama + ferramenta PDF, API de nuvem zero
3. **Pipeline de credenciais seguro** — SecretRef + anexos de sessões para fluxos de trabalho multiagentes

---
📋 Roteiro completo: `openclaw-podcast/episode_010.md` (3.530 palavras)
✅ Auditoria de tópico: todos os tópicos verificados como limpos em relação aos episódios 0–9
⏳ **Aguardando sua aprovação para prosseguir com a geração de áudio**