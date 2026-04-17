OPENCLAW DAILY — EPISODE 033 — 17 de Abril de 2026

[00:00] INTRO / HOOK
O OpenClaw lança uma atualização que move seu caminho padrão da Anthropic para o Claude Opus 4.7 e adiciona síntese de voz Gemini. A Anthropic coloca o Opus 4.7 em disponibilidade geral com melhorias em codificação e visão. A Salesforce diz que a futura pilha empresarial é headless e nativa para agentes. O Roblox transforma o desenvolvimento de jogos em um loop de planejamento. A Physical Intelligence diz que os robôs estão começando a improvisar. E os números da Adobe sugerem que o tráfego de compras por IA finalmente está se tornando um canal de negócios real, não apenas uma novidade.

[02:00] HISTÓRIA 1 — OpenClaw v2026.4.15: Melhores Padrões, Melhor Fala, Melhores Sinais
O OpenClaw 2026.4.15 é importante porque afina o produto exatamente nos lugares que um operador diário realmente sente.

A maior mudança visível é que os padrões inclusos da Anthropic, aliases e padrões do CLI do Claude agora apontam para o Claude Opus 4.7. Isso significa que a plataforma está se movendo rapidamente com o modelo principal mais recente da Anthropic em disponibilidade geral, em vez de tratar a seleção de modelo como uma configuração defasada. No lado da voz, o plugin do Google incluso agora suporta síntese de voz Gemini, incluindo registro de provedor, seleção de voz, saída de resposta WAV e saída de telefonia PCM.

A interface de controle também fica mais útil operacionalmente. Agora existe um cartão de status de autenticação de modelo que exibe a saúde do token OAuth e a pressão de limite de taxa do provedor em um relance, o que é exatamente o tipo de coisa que ajuda um operador a entender se uma falha é sobre credenciais, cota ou sobre o próprio modelo.

E a lista de correções não é enchente. A versão aperta o bypass local confiável do `MEDIA:` para que ferramentas definidas pelo cliente não possam personificar as built-ins, melhora a recuperação de replay, fortalece as bordas do webchat e Matrix, reduz os orçamentos de prompt para modelos locais mais fracos e corrige vários problemas de runtime de cauda longa em transcrições, loops de ferramentas, plugins inclusos e fala. Isso é o que um runtime de agente sério parece quando está amadurecendo: mais capacidade, mas também limites de confiança mais estreitos.
→ https://github.com/openclaw/openclaw/releases/tag/v2026.4.15

[07:00] HISTÓRIA 2 — Claude Opus 4.7: Codificação Forte, Visão Melhor e um Teste de Proteção Cibernética
A Anthropic diz que o Claude Opus 4.7 é uma melhoria notável em relação ao Opus 4.6 em engenharia de software avançada, especialmente em tarefas longas e difíceis. O enquadramento da própria empresa é revelador: esta é a versão que os desenvolvedores podem entregar trabalho mais difícil com menos supervisão porque planeja mais cuidadosamente, segue instruções mais rigorosamente e se auto-verifica antes de报告ar.

A Anthropic também diz que o Opus 4.7 tem visão substancialmente melhor, com suporte para compreensão de imagens de maior resolução e qualidade de saída mais forte em tarefas profissionais como interfaces, slides e documentos. Então o lançamento não é apenas sobre código. É sobre elevar o piso no trabalho multimodal que precisa parecer polido, não apenas correto.

Mas a parte mais estrategicamente interessante pode ser a postura de segurança. A Anthropic está lançando o Opus 4.7 com proteções automáticasaimadas a bloquear solicitações cibernéticas proibidas ou de alto risco, enquanto convida pesquisadores de segurança legítimos para um programa de verificação. Isso torna este lançamento um experimento ao vivo sobre se um laboratório de fronteira pode enviar um modelo mais capaz amplamente, enquanto ainda cerca os casos de uso mais perigosos.
→ https://www.anthropic.com/news/claude-opus-4-7

[12:30] HISTÓRIA 3 — Salesforce Headless 360: Reconstruindo a Pilha Empresarial para Agentes
A Salesforce está dizendo o que todo mundo pensa: se sua plataforma ainda assume que o progresso acontece através de um humano navegando em um navegador, ela não está pronta para a empresa agentiva.

Sua resposta é o Headless 360, uma versão decomposta da pilha da Salesforce que expõe a capacidade central da plataforma como APIs, ferramentas MCP e comandos CLI. A empresa diz que isso inclui mais de 60 ferramentas MCP e mais de 30 habilidades de codificação pré-configuradas, além de uma camada de experiência que pode render interações ricas em superfícies como Slack, voz, WhatsApp e front-ends React personalizados.

O ponto mais profundo não é apenas a contagem de ferramentas. A Salesforce está tentando possuir o loop completo: construir com agentes de codificação, avaliar e observar comportamento, então implementar a mesma lógica de negócios em qualquer interface que o humano ou o agente venha a usar. Em outras palavras, o navegador não é mais o centro de gravidade. A plataforma é.
→ https://www.salesforce.com/news/stories/salesforce-headless-360-announcement/

[18:00] HISTÓRIA 4 — O Assistente do Roblox Para de Ser uma Caixa de Prompts Brincalhona
O Roblox está atualizando seu Assistente para que ele possa ajudar criadores a planejar, construir e testar jogos como um colaborador de múltiplas etapas, em vez de apenas spitting out uma única resposta de um único prompt.

A adição chave é o Modo de Planejamento. Em vez de executar uma ideia cegamente, o Assistente pode inspecionar o código e modelo de dados do jogo, fazer perguntas esclarecedoras sobre escolhas de estilo e assets, e transformar a solicitação em um plano de ação editável antes que a implementação comece. Isso é importante porque a geração de uma única tentativa frequentemente falha precisamente no ponto onde a intenção do criador ainda está vaga.

O Roblox também está adicionando Geração de Mesh e introduzindo Modelos Procedurais, enquanto o loop de teste pode ler logs, tirar capturas de tela, simular entradas, identificar bugs e alimentar essas descobertas de volta ao Assistente para que ele possa corrigir problemas automaticamente. Este é um forte exemplo de para onde o design de produtos agentivos está indo: não apenas gerar o artefato, mas participar de todo o fluxo de trabalho ao redor dele.
→ https://techcrunch.com/2026/04/16/robloxs-ai-assistant-gets-new-agentic-tools-to-plan-build-and-test-games/

[23:00] HISTÓRIA 5 — O π0.7 da Physical Intelligence e o Caso do Cérebro Robótico Geral
A Physical Intelligence publicou pesquisa sobre um novo modelo chamado π0.7 que diz poder direcionar robôs a executar tarefas que nunca foram explicitamente treinados, combinando pedaços de conhecimento prévio de novas formas.

O exemplo da air fryer é o gancho. Segundo a empresa, os dados de treinamento continham apenas dois episódios fracamente relevantes envolvendo uma air fryer, ainda assim o modelo conseguiu uma tentativa plausível e então completou a tarefa com sucesso uma vez que um humano o guiou pelos passos em linguagem natural. Se isso se mantiver, sugere que a história de scaling para robótica pode começar a parecer muito com a que já vimos em linguagem e visão: uma vez que os sistemas cruzam o limiar de remix, cada novo pedaço de dados pode desbloquear mais de uma nova tarefa.

Os pesquisadores têm cuidado para não exagerar. O π0.7 ainda luta com autonomia multi-etapa complexa, e a qualidade do prompt ainda importa muito. Mas se a afirmação central for real, esta é uma das sinais mais claros de que a robótica pode estar passando de treinamento rotineiro para competência genuinamente transferível.
→ https://techcrunch.com/2026/04/16/physical-intelligence-a-hot-robotics-startup-says-its-new-robot-brain-can-figure-out-tasks-it-was-never-taught/

[28:00] HISTÓRIA 6 — Dados de Tráfego de IA da Adobe: O Canal de Comércio Para de Parecer Experimental
Os últimos dados de varejo da Adobe sugerem que o tráfego de compras por IA não é mais apenas uma curiosidade estranha do topo do funil. Está começando a parecer um canal de comércio real.

Segundo a Adobe, o tráfego de IA para sites de varejo dos EUA subiu 393% no primeiro trimestre em relação ao ano anterior. Mais importante, a qualidade desse tráfego mudou em relação ao padrão do ano passado. Em março de 2026, o tráfego de IA converteu 42% melhor que o tráfego não-IA, com usuários passando mais tempo nos sites, visualizando mais páginas e gerando 37% mais receita por visita.

O aviso dentro da oportunidade é que muitos varejistas ainda não estão prontos para esse tráfego. A Adobe diz que porções significativas de páginas iniciais, páginas de categoria e especialmente páginas de produtos permanecem mal acessíveis para LLMs. Então a próxima batalha de otimização no e-commerce pode não ser apenas SEO ou aquisição paga. Pode ser se o assistente de IA pode realmente ler e recomendar seu catálogo corretamente.
→ https://techcrunch.com/2026/04/16/ai-traffic-to-us-retailers-rose-393-in-q1-and-its-boosting-their-revenue-too/

[32:30] OUTRO / ENCERRAMENTO
Esse é o mapa de hoje: OpenClaw apertando o runtime em torno de um novo modelo padrão e pilha de fala, Anthropic testando como enviar capacidade mais forte com proteções cibernéticas, Salesforce reconstruindo software empresarial para agentes, Roblox transformando criação em um loop de planejamento, robótica avançando em direção a aprendizado por transferência que realmente transfere, e comércio descobrindo que o tráfego de IA pode já valer a pena projetar.

→ Responda aqui para aprovar a geração da transcrição.