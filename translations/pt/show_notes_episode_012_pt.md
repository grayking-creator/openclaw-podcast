# OpenClaw Daily - Notas do programa do episódio 12
**"Modelos de fronteira gratuitos, memória multimodal e automações comunitárias que vão te impressionar"**
📅 12 de março de 2026
🔗 Liberação: https://github.com/openclaw/openclaw/releases/tag/v2026.3.11

---

## Resumo do episódio
A v2026.3.11 foi lançada com dois modelos furtivos de fronteira livre, o primeiro modelo de incorporação multimodal nativo do Google chega ao OpenClaw, um assistente de integração Ollama completo, currículo de sessão ACP para longas sessões de codificação e aprimoramento de aplicativos iOS/macOS. Além disso: um mergulho profundo nas automações reais da comunidade, economizando muito tempo das pessoas.

---

## Destaque da comunidade – Principais automações da BetterClaw

Usuários reais do OpenClaw, economizados em tempo real. Do top 10 do BetterClaw:

1. ** Briefings matinais ** — Calendário + síntese de e-mail, rascunhos de respostas com base no contexto, antes de você acordar
2. **Triagem de e-mail** — Categorize automaticamente, rascunhe respostas, agende compromissos — totalmente local e privado
3. **Assistente de Calendário Familiar** — Detecção de conflitos, agendamento, mensagens diretas para a família
4. **Self-Healing Home Server** — Monitora serviços, tenta correções automaticamente, alerta apenas sobre o inesperado
5. **Base de conhecimento pessoal (RAG)** — Pesquisa semântica em todas as notas, documentos e códigos

Criação de comunidade em destaque: mais de 5.000 notas, 15 cron jobs, 24 scripts personalizados — administrador de sistemas totalmente automatizado com verificações de integridade por hora, briefings diários e auditorias de segurança semanais. Raciocínio de IA baseado no contexto, não apenas scripts idiotas.

---

## Novos modelos gratuitos — Hunter Alpha e Healer Alpha
Ambos disponíveis agora no OpenRouter por tokens de US$ 0,00/M. (O nível gratuito pode ser temporário.)

**Caçador Alfa**
- 1 trilhão de parâmetros
- janela de contexto de 1 milhão de tokens
- Otimizado para casos de uso de agentes
- https://openrouter.ai/openrouter/hunter-alpha

**Curandeiro Alfa**
- Fronteira omnimodal: visão, audição, raciocínio, ação
- Janela de contexto de 262K
- https://openrouter.ai/openrouter/healer-alpha

---

## Memória Multimodal - Incorporação Gemini 2
O Google anunciou o Gemini Embedding 2 em 11 de março. O OpenClaw o integrou no mesmo dia.
https://deepmind.google/technologies/gemini/

- Primeiro modelo de incorporação multimodal nativo — texto, imagens, vídeo, áudio, PDFs em um espaço vetorial compartilhado
- Suporte de áudio nativo (sem etapa de transcrição)
- Limite de entrada de 8.192 tokens (4× anterior)
- Supera Amazon Nova 2 e Voyage Multimodal 3.5 em benchmarks
- Dimensões de saída configuráveis com reindexação automática na alteração
- Controle de fallback estrito — sem degradação silenciosa

Caso de uso: pergunte ao seu agente “encontre aquele artigo sobre pipelines de implantação” – ele exibe uma captura de tela, uma nota de voz E um arquivo de texto, tudo de uma vez. Significado sobre palavras-chave.

---

## Ollama — Assistente de integração completo de primeira classe
Ollama atingiu 10 bilhões de pulls: https://ollama.com
Os guias da comunidade (dev.to, FreeCodeCamp) tiveram milhares de leitores fazendo configuração manual. Agora está integrado ao assistente.

Dois modos:
- **Local** — 100% off-line, todas as inferências no dispositivo, zero nuvem, privacidade máxima
- **Cloud+Local** — Híbrido: local para tarefas rápidas, nuvem para raciocínio pesado. Pulo de pull do modelo inteligente no modo nuvem.

---

## ACP e ferramentas para desenvolvedores

**Currículo da sessão ACP** (`resumeSessionId`)
- Retomar uma conversa de subagente após reinicializações — sem reexplicação do contexto
- Repetição da transcrição em `loadSession`
- Encaminhamento de anexo de imagem — contexto visual preservado no currículo
- O streaming da ferramenta ACP agora inclui dicas de localização de arquivos
- `OPENCLAW_CLI` env var definido em processos filhos

https://docs.openclaw.ai/acp

---

## Atualizações de aplicativos

**iOS:**
- Nova tela de boas-vindas com visão geral do agente ao vivo
- Controles flutuantes substituídos por barra de ferramentas encaixada
- O bate-papo é aberto na sessão principal resolvida — o contexto persiste em todos os dispositivos

**macOS:**
- Troque de modelo diretamente da visualização de conversa - não é necessária nova sessão- As preferências de nível de pensamento persistem durante as reinicializações
- Proteção de reinicialização do LaunchAgent

**Provedor OpenCode Go** — Zen + Go agora compartilha uma chave na configuração do assistente

---

## OpenClaw Backup (lançado em 8 de março)
```
criação de backup openclaw
verificação de backup do openclaw
criação de backup openclaw --only-config
```
Faz backup de configuração, estado e espaço de trabalho. Use-o.
https://docs.openclaw.ai/cli/backup

---

## Links principais
- Versão v2026.3.11: https://github.com/openclaw/openclaw/releases/tag/v2026.3.11
- Caçador Alfa: https://openrouter.ai/openrouter/hunter-alpha
- Curador Alfa: https://openrouter.ai/openrouter/healer-alpha
-Olhama: https://ollama.com
- Incorporação Gêmeos 2: https://deepmind.google/technologies/gemini/
- Documentos OpenClaw: https://docs.openclaw.ai
- Discórdia da comunidade: https://discord.com/invite/clawd