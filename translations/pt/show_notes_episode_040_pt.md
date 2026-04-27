OPENCLAW DAILY — EPISODE 040 — April 26, 2026

[00:00] INTRO / HOOK
OpenClaw v2026.4.24 é a versão estável mais recente, e como a v2026.4.23 já foi coberta nos episódios recentes, a v2026.4.24 é o único bloco de release válido no início do EP040.

E ela conquista esse lugar ao tornar a colaboração em tempo real muito mais concreta. O Google Meet se torna uma superfície OpenClaw integrada, Talk e Voice Call podem consultar o agente completo durante sessões de voz ao vivo, a automação de navegador fica mais robusta, e a infraestrutura de modelo-mais-plugin continua ficando mais leve e mais explícita.

Após o deep dive sobre o release, passamos ao marketplace experimental Project Deal da Anthropic, aos conectores de apps pessoais do Claude, e ao sinal de mercado por trás da rodada de financiamento mais recente do ComfyUI.

[01:30] STORY 1 — OpenClaw v2026.4.24 Torna Reuniões ao Vivo e Sessões de Voz Muito Mais Práticas
O centro da v2026.4.24 é o Google Meet.

O OpenClaw agora inclui um plugin de participante do Google Meet integrado com autenticação Google pessoal, entradas explícitas em reuniões, transports Google Meet e Twilio em tempo real, suporte a Chrome pareado por nó, exportação de artefatos e presença, e ferramentas de recuperação para abas já abertas. Isso não é uma pequena adição de plugin. É o OpenClaw transformando uma superfície de colaboração ao vivo em algo que o runtime realmente pode controlar.

A diferença prática é enorme.
Uma ferramenta de reunião só é valiosa se conseguir lidar com as partesbagunçadas ao redor da reunião, não apenas o botão de entrada idealizado. Este release adiciona recuperação de estado do navegador, fluxos de diagnóstico OAuth, `recover_current_tab`, fluxos de trabalho de presença e registro de conferência, exportação de transcrição e gravação, e a capacidade de inspecionar abas do Meet já abertas em vez de abrir duplicatas cegamente. Esses são os tipos de detalhes que transformam um recurso de "demonstrável" para "operável".

E o OpenClaw não trata o Meet como uma ilha isolada.
Talk, Voice Call e Google Meet agora podem usar loops de voz em tempo real que consultam o agente OpenClaw completo para respostas mais profundas apoiadas por ferramentas. Isso importa porque muda o teto sobre o que uma sessão de áudio ao vivo pode fazer. Em vez de ficar presa dentro de uma interação de modelo em tempo real fina, a sessão pode delegar para o agente completo quando precisa de memória mais ampla, ferramentas ou trabalho mais deliberado. Isso faz a voz ao vivo parecer menos uma interface de novelty e mais um frontend sério para o resto do sistema.

Há também uma história de nó pareado aqui que importa para operadores reais.
O release suporta explicitamente setups no estilo Chrome-node para hosts que precisam de Chrome especializado, roteamento de áudio ou ambientes semelhantes a VM. Esse é exatamente o tipo de detalhe de deployment no mundo real que diz que o recurso foi projetado para ambientes bagunçados, não apenas para um caminho único de laptop limpo.

[10:30] STORY 1B — Controle de Navegador, Catálogos DeepSeek e Infraestrutura de Startups Ficam Mais Nítidos
A próxima grande linha na v2026.4.24 é que o OpenClaw continua reduzindo fricção na forma como agentes realmente agem no mundo.

A automação de navegador ganha cliques por coordenadas, orçamentos de ação padrão mais longos, sobrescritas headless por perfil, reutilização de abas mais estável e recuperação mais forte para sessões e bloqueios obsoletos. Isso parece incremental até você lembrar com que frequência a automação de navegador falha exatamente nessas bordas. Uma ferramenta de navegador se torna útil quando agentes podem sobreviver a esperas longas, recuperar anexos obsoletos, reutilizar a aba correta e continuar se movendo sem pedir ao operador para cuidar de cada estado quebrado.

Este release também empurra operações de navegador para controle mais claro do operador.
Há diagnósticos de doctor, limites de segurança mais fortes em requisições de navegador, melhor tratamento de timeout de screenshot, identificadores de aba mais estáveis e comportamento de sessão existente mais robusto. Então a superfície de navegador não está apenas ganhando recursos. Está ganhando um modelo operacional mais confiável.

O lado do catálogo de modelos também se move.
DeepSeek V4 Flash e V4 Pro entram no catálogo integrado, com V4 Flash se tornando o padrão de onboarding, enquanto o comportamento de replay e pensamento é corrigido para turns de chamada de ferramenta subsequentes. Isso importa porque a disponibilidade de modelo é apenas parte da história. Operadores precisam que o runtime preserve comportamento de raciocínio de forma limpa em sessões multi-turn, chamadas de ferramenta e provedores sensíveis a replay. Caso contrário, uma nova linha de modelo é principalmente decorativa.

Então há o encanamento de startup e catálogo.
O OpenClaw continua se movendo em direção a catálogos estáticos, linhas de modelo sustentadas por manifest, dependências de provedor mais lazy e installs empacotadas mais leves. Essa é uma boa arquitetura de runtime. Isso significa que listar modelos, ler metadados de setup e inspecionar capacidades pode acontecer sem sempre arrastar estado pesado de plugin runtime para a memória. Em um nível de produto, isso faz o sistema parecer mais rápido. Em um nível de arquitetura, isso faz capacidades mais inspectáveis e menos mágicas.

[18:30] STORY 1C — As Correções Mostram o OpenClaw Apertando o Runtime, Não Apenas Expandindo
Muito do valor real na v2026.4.24 mora na lista de correções.

O agendamento de heartbeat fica mais resistente contra timers superdimensionados e vazamento de prompt. Continuações de reinício se tornam mais duráveis. O manuseio de sessão e transcrição fica menos frágil. Caminhos do Telegram, Discord, Slack, WhatsApp e navegador todos recebem melhorias de confiabilidade específicas. Replay do DeepSeek é corrigido. Sessões de navegador existentes param de envenenar anexos futuros. Chamadas locais ou de provedor de longa duração herdam melhor comportamento de timeout. E execuções cron isoladas param de vazar estado obsoleto de sessões anteriores.

Há também uma limpeza importante voltada para operadores ao redor de modelos.
`/models add` é depreciado ao invés de silenciosamente mutar configuração de modelo do chat, enquanto linhas originadas de manifesto e melhorias em listas read-only tornam superfícies de modelos mais explícitas. Essa é uma correção saudável. O runtime está ficando mais poderoso, mas também está sendo empurrado em direção a limites de propriedade mais claros sobre o que deve acontecer no chat, o que deve acontecer no setup e o que deve ser auditável como configuração.

O release até inclui uma mudança de quebra real para desenvolvedores de plugins.
A antiga rota de compatibilidade de fábrica de extensão embarcada apenas para Pi é removida em favor da rota de middleware de resultado de ferramenta do agente com declarações de harness. Isso não é apenas limpeza pela limpeza. É parte do OpenClaw tentar manter runtimes estilo Pi e Codex em um contrato compartilhado mais honesto ao invés de deixar costuras de compatibilidade legadas derivarem para sempre.

Então a leitura prática da v2026.4.24 é direta.
Este é um release sobre tornar superfícies ao vivo mais utilizáveis, automação de navegador mais confiável, infraestrutura de modelo e plugin mais legível, e o runtime menos surpreendente sob carga real.
→ https://github.com/openclaw/openclaw/releases/tag/v2026.4.24

[26:30] STORY 2 — O Project Deal da Anthropic Testa O Que Acontece Quando Agentes Negociam por Pessoas
O Project Deal da Anthropic é fácil de descartar como um experimento interno quirky.
Isso seria um erro.

A empresa diz que executou um marketplace interno classificado onde agentes de IA representavam compradores e vendedores, fechavam negócios reais e negociavam sobre valor real para um grupo de funcionários auto-selecionados. A Anthropic diz que foram realizados 186 negócios, totalizando mais de $4.000 em valor, com os participantes recebendo um pequeno orçamento e as transações sendo realmente honradas após o experimento.

O motivo pelo qual isso importa não é a escala absoluta.
O motivo pelo qual isso importa é o formato do teste. Não se trata de "um agente pode responder perguntas" ou "um agente pode clicar em botões." É um teste de negociação, representação, assimetria, incentivos e ação econômica delegado.

A Anthropic diz que modelos mais avançados tendiam a obter resultados objetivamente melhores, enquanto os usuários do lado mais fraco não necessariamente percebiam que estavam perdendo. Isso deveria chamar atenção imediatamente. Se as diferenças de qualidade entre agentes se tornarem reais em contextos de negociação, então a próxima versão da vantagem de modelo pode não se manifestar apenas como uma prosa mais bonita ou pontuações de benchmark mais fortes. Pode se manifestar como quem consegue o melhor negócio em um mercado automatizado.

Isso tem implicações óbvias para construtores.
Uma vez que agentes começam a comprar, vender, rotear requisições, negociar disponibilidade ou decidir em quais contrapartes confiar, a qualidade do agente se torna uma questão econômica. Justiça, transparência e revisão de ações começam a importar muito mais porque um usuário pode não conseguir perceber quando seu agente está sistematicamente tendo desempenho inferior contra um melhor.

Então o Project Deal parece pequeno, mas aponta para uma categoria futura maior: marketplaces de agentes onde a verdadeira questão não é apenas se os agentes podem agir, mas se podem representar interesses humanos bem o suficiente sob competição.
→ https://techcrunch.com/2026/04/25/anthropic-created-a-test-marketplace-for-agent-on-agent-commerce/

[32:30] HISTÓRIA 3 — Os Conectores de Apps Pessoais do Claude Expandem a Superfície de Confiança
A outra movimentação relevante da Anthropic nesta semana é muito mais voltada para produto.

O Claude está expandindo seu modelo de conectores além de apps de trabalho para serviços pessoais como Spotify, Uber, Instacart, AllTrails, TripAdvisor, Audible e TurboTax. Isso importa porque aproxima a superfície do agente de tarefas da vida normal, não apenas de software empresarial ou fluxos de trabalho de desenvolvedores.

O significado do produto está na camada de orquestração.
Uma vez que o Claude consegue ver múltiplos apps conectados e sugerir eles no contexto, o assistente para de parecer um único destino de chat e começa a parecer mais uma camada de coordenação entre serviços. A Anthropic diz que os dados dos apps conectados não são usados para treinar seus modelos, que os apps não veem outras conversas do usuário com o Claude, e que o Claude solicita verificação antes de executar ações como compras ou reservas. Esses limites de confiança não são notas de rodapé. São requisitos de produto centrais se agentes forem avançar de recomendação para ação.

Para construtores, esta história importa porque reforça para onde a competição está indo.
A próxima corrida de agentes não é apenas sobre modelos mais inteligentes. É sobre quem pode dominar a superfície de ação entre apps enquanto preserva confiança suficiente para que os usuários realmente permitam que o sistema faça algo consequente.

Por isso design de confirmação, escopo de conectores e contexto entre apps são todas questões estratégicas de produto agora.
→ https://www.theverge.com/ai-artificial-intelligence/917871/anthropic-claude-personal-app-connectors

[37:30] HISTÓRIA 4 — A Avaliação do ComfyUI É Uma Aposta Contra Fluxos de Trabalho Criativos Apenas com Prompts
O ComfyUI captando investimento com avaliação de $500 milhões não é apenas teatro de startup.
É um sinal de onde ainda reside valor em fluxos de trabalho de mídia com IA.

O pitch da empresa é que sistemas apenas com prompts frequentemente levam você a maior parte do caminho até um resultado de imagem ou vídeo, mas não ao último trecho sem transformar cada mudança em uma roleta de reroll. O workflow baseado em nodes do ComfyUI oferece controle muito mais granular sobre etapas individuais no processo de geração, e o TechCrunch relata que a empresa diz que agora tem mais de 4 milhões de usuários.

A implicação mais profunda é que modelos melhores não eliminam automaticamente a necessidade de superfícies de controle.
Na verdade, modelos melhores podem aumentar a demanda por eles, porque uma vez que a qualidade base é alta o suficiente, o valor restante muda para repetibilidade, precisão e edições direcionadas. É exatamente aí que sistemas baseados em nodes vencem.

Para construtores e operadores, este é um lembrete útil.
Se você está projetando em torno de saídas de imagem, vídeo ou multimodais, ainda há demanda real por fluxos de trabalho que permitem aos usuários conduzir, inspecionar e refinar o pipeline em vez de colapsar cada ajuste de volta em mais um prompt.

Então a avaliação do ComfyUI é realmente uma tese sobre controle.
Prompts continuam sendo a rampa de entrada fácil. Mas trabalho criativo de qualidade de produção ainda quer superfícies que possam preservar a intenção através de múltiplas etapas sem forçar o usuário a apostar as partes boas do resultado toda vez.
→ https://techcrunch.com/2026/04/24/comfyui-hits-500m-valuation-as-creators-seek-more-control-over-ai-generated-media/

[43:00] ENCERRAMENTO
Isso é suficiente para hoje.
O OpenClaw v2026.4.24 avançou colaboração ao vivo, voz em tempo real, confiabilidade do navegador e infraestrutura de catálogo de formas práticas.
A Anthropic usou o Project Deal para dar uma amostra do que mercados de agentes realmente podem testar.
O Claude expandiu para ações em apps pessoais.
E o ComfyUI lembrou todos que modelos melhores não apagam o prêmio sobre controle.

→ Responda aqui para aprovar a geração da transcrição.