# OpenClaw Daily - Episódio 016

**Título:** OpenClaw muda de pele  
**Subtítulo:** Aprofundamento do lançamento duplo v2026.3.22 e v2026.3.23

## 1) Resumo do episódio
Neste episódio, descompactamos as versões consecutivas 2026.3.22 e 2026.3.23 do OpenClaw, concentrando-nos nas mudanças mais significativas para mantenedores, desenvolvedores de plugins e usuários auto-hospedados. Detalhamos os pontos de pressão da migração (especialmente SDK de plug-ins, ferramentas de navegador e ecossistemas de matrizes/habilidades), o que quebra e o que fazer antes e depois da atualização. O objetivo é um estado de plataforma mais limpo e seguro, com menos surpresas em tempo de execução, melhor comportamento de autenticação/proxy e padrões mais limpos para UI, modelos e integrações de extensões.

## 2) O que cobrimos
- Destaques de alto impacto de **v2026.3.22** e **v2026.3.23**
- Por que `openclaw doctor --fix` se tornou o comando âncora de atualização
- Detalhes da migração do navegador/Chrome MCP e o que mudou nos fluxos de sessões existentes
- Mudanças no ecossistema de plug-ins: migração de SDK, comportamento em tempo de execução e remoção de antigas camadas de compatibilidade
- Instalação do primeiro plugin do ClawHub e correções de compatibilidade de marketplace/plugin
- Orientação de migração do plugin Matrix e correções de confiabilidade
- Acessibilidade + atualizações de aprimoramento da interface do usuário (incluindo ajuste de contraste alinhado às WCAG)
- Mudanças no provedor Qwen/DashScope e limpeza de configuração do modelo
- Sequenciamento prático de atualização e lista de verificação de verificação

## 3) Links de notas de lançamento
- [OpenClaw v2026.3.22](https://github.com/openclaw/openclaw/releases/tag/v2026.3.22)
- [OpenClaw v2026.3.23](https://github.com/openclaw/openclaw/releases/tag/v2026.3.23)

## 4) Tópicos principais com links
- [`openclaw doctor --fix`](https://docs.openclaw.ai/gateway/doctor) — ponto de entrada de migração e reparo para ambiente, plug-ins e desvios de configuração conhecidos
- [Navegador / Chrome MCP](https://docs.openclaw.ai/tools/browser) — atualizações sobre anexos de sessões existentes do navegador e remoção de caminhos de extensões legados do Chrome
- [Migração do SDK do plug-in](https://docs.openclaw.ai/plugins/sdk-migration) — substituindo suposições legadas de importação/interoperabilidade pela nova superfície do SDK
- [Visão geral do SDK do plug-in](https://docs.openclaw.ai/plugins/sdk-overview) — como os limites do tempo de execução do plug-in e as APIs devem funcionar agora
- [Migração Matrix](https://docs.openclaw.ai/install/migrating-matrix) — atualizações necessárias para a nova pilha de plugins Matrix
- [ClawHub](https://docs.openclaw.ai/tools/clawhub) — novo fluxo padrão para instalação/atualização/pesquisa e compatibilidade de pacotes
- [Guia de migração OpenClaw](https://docs.openclaw.ai/install/migrating) — princípios mais amplos de migração de configuração/estado
- [Qwen/DashScope (Model Studio)](https://www.alibabacloud.com/en/product/modelstudio) — alterações de provedor e atualizações de caminho de endpoint
- [WCAG 2.1 AA](https://www.w3.org/TR/WCAG21/) — linha de base de acessibilidade para contraste da IU e atualizações de controle na versão

## 5) Lista de verificação de atualização (9 etapas)
- [ ] **Faça backup de sua configuração/estado atual do OpenClaw** antes das atualizações (incluindo `.openclaw` + qualquer estado de plugin personalizado).
- [ ] **Atualização em sequência**: instale/atualize para `2026.3.22` primeiro, depois para `2026.3.23` para que as correções transitórias sejam colocadas em ordem.
- [ ] **Execute `openclaw doctor --fix` imediatamente após cada estágio de atualização** para reparar desvios de migração e referências de configuração obsoletas.
- [ ] **Alternar importações de plug-ins/agentes herdados** de superfícies de compatibilidade removidas para os novos padrões `openclaw/plugin-sdk/*` e modelo de execução de tempo de execução.
- [ ] **Migrar instalações de plug-ins e caminhos de metadados** para o ClawHub (fluxos `clawhub:<package>` quando disponíveis) e atualizar o estado de compatibilidade de habilidade/plugin.
- [ ] **Atualize a configuração do plugin Matrix** usando o guia de migração se vier da pilha Matrix antiga.
- [ ] **Migrar higiene de configuração**: substitua nomes de ambiente legados e locais de estado legados (`CLAWDBOT_*`/`MOLTBOT_*`, `~/.moltbot`) por equivalentes atuais do OpenClaw.- [ ] **Revise a configuração das ferramentas do navegador** para alterações no Chrome/Browser MCP (sessões existentes, anexo userDataDir, remoção do caminho de retransmissão de extensão).
- [ ] **Verifique os provedores e a UI/acessibilidade após a reinicialização** (endpoints Qwen/DashScope, padrões de modelo e principais fluxos de UI) e execute um breve teste de fumaça das ferramentas assistentes.

## 6) Links mencionados
- https://github.com/openclaw/openclaw/releases/tag/v2026.3.22
- https://github.com/openclaw/openclaw/releases/tag/v2026.3.23
- https://docs.openclaw.ai/gateway/doctor
- https://docs.openclaw.ai/tools/browser
- https://docs.openclaw.ai/plugins/sdk-migration
- https://docs.openclaw.ai/plugins/sdk-overview
- https://docs.openclaw.ai/install/migrating-matrix
- https://docs.openclaw.ai/tools/clawhub
- https://docs.openclaw.ai/install/migrating
- https://www.alibabacloud.com/en/product/modelstudio
- https://www.w3.org/TR/WCAG21/

## 7) Onde nos encontrar
Visite-nos em: **[tobyonfitnesstech.com](https://tobyonfitnesstech.com)**