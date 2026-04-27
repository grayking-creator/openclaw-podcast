OPENCLAW DAILY — EPISODE 041 — 27 de Abril de 2026

[00:00] INTRO / GANCHO
Hoje estamos reescrevendo a pauta porque agora existe um OpenClaw v2026.4.25, e isso é um lead muito melhor do que forçar uma história aleatória de fusões e aquisições de IA corporativa para a posição principal.

Este release não é um único título limpo. É um release de sistemas. A voz fica mais séria. A inicialização de plugins fica mais fria e mais rápida. A observabilidade fica mais ampla. A automação de navegador fica mais segura. A configuração fica mais suave. Os caminhos de instalação e atualização ficam mais difíceis de quebrar. E a integração com Codex dá mais um passo em direção ao comportamento nativo de app-server.

Aí usamos isso como ponte para o próprio Codex. O app Codex não é mais apenas um auxiliar de IDE. O conjunto de recursos começa a parecer um espaço de trabalho de engenharia: worktrees, threads de app-server, ambientes persistentes, perfis de permissão, automações, mercados de plugins, Git integrado, terminais e um navegador integrado para feedback visual.

Depois ampliamos o foco: a Meta está reservando energia futura de uma startup de energia solar espacial, porque a computação de IA está se tornando um problema de logística energética. E encerramos com montadoras usando IA em loops reais de design e simulação, e não apenas para fazer renders bonitas de carros.

[02:00] HISTÓRIA 1 — OpenClaw v2026.4.25 Torna o Runtime Mais Pronto para Produção
O OpenClaw v2026.4.25 é um release grande, mas o tema é surpreendentemente claro: tornar o runtime de agentes mais fácil de operar no mundo real.

A primeira peça óbvia é a voz. Este release melhora o TTS em toda a stack. Há `/tts latest` para ler a última resposta em voz alta, controles com escopo de chat como `/tts chat on`, `/tts chat off` e `/tts chat default`, substituições por agente e por conta, e uma superfície de provedores maior: Azure Speech, Xiaomi, Local CLI TTS, Inworld, Volcengine ou BytePlus Seed Speech, e ElevenLabs v3.

Isso importa porque a voz não é mais apenas uma camada de novidade. Se os agentes estão dentro do WhatsApp, Telegram, Discord, chamadas, Talk Mode e superfícies de colaboração ao vivo, a voz precisa ser configurável por contexto. A voz que você quer para um assistente privado não é necessariamente a voz que você quer em um chat de grupo, uma chamada telefônica, um fluxo de trabalho no Feishu ou uma conta de bot. O v2026.4.25 move o TTS em direção a esse modelo mais realista: credenciais compartilhadas de provedor, mas controle local sobre voz, provedor, persona, conta e comportamento de canal.

A segunda peça principal é a inicialização de plugins. O OpenClaw está movendo a inicialização de plugins, descoberta de provedores, metadados de instalação e fluxos de reparo para um registro frio persistente. Em termos simples: a inicialização normal não deveria precisar vasculhar um universo amplo de plugins e importar um monte de código de runtime apenas para responder perguntas como o que está instalado, qual provedor possui este modelo ou quais escolhas de configuração estão disponíveis.

Isso não é glamoroso, mas é exatamente o tipo de engenharia que faz um runtime se sentir rápido e previsível. O release adiciona `openclaw plugins registry`, altera `plugins list` para ler o registro frio por padrão, atualiza o índice após mudanças de plugins de chat e CLI, e aponta operadores para reparo de registro em vez de velhos switches de emergência. O ponto do produto é simples: sistemas de plugins são poderosos apenas se não transformam cada inicialização, verificação de status ou prompt de configuração em uma varredura lenta de runtime completo.

A terceira peça é a observabilidade. A cobertura do OpenTelemetry se expande por chamadas de modelo, uso de tokens, loops de ferramentas, execuções de harness, processos exec, entrega de saída, montagem de contexto e pressão de memória. O detalhe importante é que o release mantém os atributos limitados e com baixa cardinalidade. Ele está tentando tornar Grafana, Prometheus, traces e métricas úteis sem vazar prompts, respostas, identificadores de sessão, texto de comandos, dados de destinatários ou IDs de requisição brutos do provedor.

Essa é a direção certa para infraestrutura de agentes. Se os agentes vão executar tarefas, chamar ferramentas, gerar subagentes, enviar mensagens, gerenciar abas do navegador e usar modelos de vários provedores, os operadores precisam responder perguntas básicas: para onde foi a latência, qual agente está queimando tokens, as chamadas de modelo estão falhando, um processo exec travou, uma entrega falhou, a montagem de contexto está crescendo, a pressão de memória está aumentando. Mas os diagnósticos não podem se tornar um segundo vazamento de dados.

A automação de navegador também recebe uma passagem significativa de confiabilidade: URLs de abas mais seguras em respostas de agentes, snapshots de função com consciência de iframe, fallback nativo de CDP para snapshot de função, detecção de clique no cursor, preparação de attach de alvo, sondagem mais profunda do `browser doctor --deep`, suporte a lançamento headless de uma só vez e mais ajuste para hosts lentos como Raspberry Pi. Essa é uma história para construtores porque a automação de navegador é um dos lugares onde os agentes parecem mágicos quando funcionam e frágeis quando não funcionam. Referências melhores, diagnósticos melhores e manuseio mais seguro de abas são as coisas tediosas que tornam os agentes de uso de computador utilizáveis.

A UI de Controle e o fluxo de configuração também recebem polimento prático: suporte a instalação de PWA, notificações Web Push para chat do Gateway, reparo de primeira execução do Crestodian, configuração TUI, seleção de modo de contexto, indicadores de progresso e uma saudação de inicialização mais curta. E a lista de endurecimento de instalação/atualização é enorme: comportamento de tarefa agendada do Windows, rotação de token do LaunchAgent do macOS, configuração de serviço Linux, empacotamento Docker, reinicializações de serviço Node, dependências de runtime de plugins empacotados, verificação de gateway de versões mistas, avisos de disco baixo e reparos de doctor após atualização.

O ponto principal é que o v2026.4.25 não está tentando vencer com uma única demo. Ele está tentando tornar o OpenClaw mais confiável como um sistema operacional diário de agentes. Voz, plugins, diagnósticos, controle de navegador, configuração, atualizações, Codex e canais todos avançaram.

→ https://github.com/openclaw/openclaw/releases/tag/v2026.4.25

[12:00] HISTÓRIA 2 — Codex Está se Tornando uma Plataforma de App Real
A história complementar mais interessante é a do Codex, porque o v2026.4.25 inclui algumas mudanças específicas do Codex, e o changelog próprio do Codex da OpenAI aponta na mesma direção.

O OpenClaw agora requer Codex app-server 0.125.0 ou mais recente para o harness do Codex. Ele cobre payloads nativos de MCP `PreToolUse`, `PostToolUse` e `PermissionRequest` através do relay de hooks do OpenClaw. Ele ensina prompts e `agents_list` a mostrar a disponibilidade nativa do Codex app-server, então agentes podem preferir o caminho nativo `/codex` em vez de voltar para caminhos antigos do Codex ACP a menos que ACP seja explícito. Ele também corrige controles modernos de raciocínio do Codex, prepara metadados nativos de subagentes do Codex, melhora o tratamento de erros do app-server e aperta os limites de mídia e aprovação do Codex.

Isso parece restrito até você conectar com o que o Codex em si está se tornando. O Codex CLI 0.125.0 da OpenAI adiciona trabalho de integração de app-server em torno de transporte Unix socket, resume e fork amigáveis à paginação, ambientes persistentes, configuração de thread remota e encanamento de armazenamento de thread, instalação e atualização de marketplace de plugins e perfis de permissão que fazem round-trip através de sessões TUI, turnos de usuário, estado de sandbox MCP, escalação de shell e APIs de app-server.

Os documentos de recursos do app tornam a forma do produto mais clara. O app Codex é descrito como uma experiência desktop para trabalhar em threads do Codex em paralelo, com projetos, worktrees, automações, recursos Git e um terminal integrado. Você pode executar tarefas locais diretamente em um projeto, isolar experimentos em worktrees Git ou executar trabalho na nuvem remoto. O painel de diff permite revisar alterações, comentar inline, stage ou reverter trechos, fazer commit, push e criar pull requests. O terminal é escopado para o projeto ou worktree, e o Codex pode ler a saída do terminal, então um teste falho ou um servidor dev em execução se torna parte do contexto da thread.

O navegador in-app é outra peça importante. Ele dá ao usuário e ao Codex uma visualização renderizada compartilhada de uma página web dentro da thread. Isso significa que uma tarefa de frontend pode incluir visualização visual e comentários visuais sem trocar constantemente entre o editor, terminal, navegador e chat. Ele não pretende substituir seu navegador pessoal logado para tudo, mas para servidores de desenvolvimento locais, visualizações baseadas em arquivos e páginas públicas, ele fecha o loop entre mudança de código, revisão visual e instrução de acompanhamento.

Esta é a história maior: agentes de codificação estão passando de autocompletar e chat para superfícies de trabalho. Os recursos que importam não são apenas a qualidade do modelo. Eles são isolamento, revisão, aprovações, observabilidade, gerenciamento de ambiente, threading, comportamento de resumir/bifurcar e a capacidade de executar múltiplas peças de trabalho sem pisar no checkout atual do usuário.

É por isso que o suporte app-server do Codex importa dentro do OpenClaw. Se o Codex está se tornando uma plataforma de aplicativo nativo para tarefas de engenharia, então o OpenClaw quer rotear trabalho para ele através do melhor harness disponível, preservar eventos de permissão, gerenciar hooks e expor disponibilidade nativa para os agentes. A pergunta interessante já não é "pode uma IA escrever uma função?" É "pode um workspace de IA manter um trabalho de software bagunçado desde a intenção até o diff, teste, revisão e deploy sem perder o controle?"

→ https://developers.openai.com/codex/changelog
→ https://developers.openai.com/codex/app/features
→ https://developers.openai.com/codex/app/browser

[21:00] HISTÓRIA 3 — A Meta Reserva Capacidade Solar Transmitida do Espaço para Centros de Dados de IA
Agora faça zoom out das operações de software para operações de energia.

A Meta assinou uma reserva de capacidade com a Overview Energy, uma startup trabalhando em satélites que coletariam energia solar em órbita e transmitiriam luz infravermelha próxima para grandes fazendas solares. Essas fazendas solares então converteriam a luz em eletricidade usando infraestrutura solar terrestre, potencialmente produzindo energia solar à noite para clientes de centros de dados.

A manchete é estranha, mas a pressão por baixo é muito normal: centros de dados de IA precisam de quantidades enormes de eletricidade confiável. O TechCrunch relata que os centros de dados da Meta usaram mais de 18.000 gigawatt-hora de eletricidade em 2024, e que a empresa se comprometeu a construir 30 gigawatts de fontes de energia renovável com foco em solar industrial em escala. O desafio é que a computação de IA não para ao pôr do sol.

A abordagem da Overview é diferente dos conceitos clássicos de solar espacial por micro-ondas. A empresa está falando sobre converter a energia solar coletada em órbita em um amplo feixe infravermelho próximo apontado para grandes instalações solares, em vez de disparar um feixe denso em um pequeno receptor. A reserva da Meta é de até um gigawatt de energia futura. A Overview planeja uma demonstração em órbita baixa da Terra em 2028 e espera começar a lançar satélites para o compromisso da Meta por volta de 2030.

O cronograma importa. Esta não é uma correção de curto prazo para os gargalos da rede elétrica de hoje. É um sinal. Os hyperscalers não estão mais apenas comprando GPUs, locais de centros de dados e networking. Eles estão comprando opcionalidade energética futura.

A lição para builders é que estratégia de produto de IA e estratégia energética estão se fundindo. Todo agente always-on, gerador de vídeo, assistente em tempo real, workflow de longo contexto e loop de automação em segundo plano tem um perfil de energia. O usuário vê um botão. O operador vê uma chamada de modelo. A equipe de infraestrutura vê um cluster. A equipe de energia vê carga, intermitência, restrições da rede, baterias, licenciamento e contratos de energia de longo prazo.

Então, independentemente de o solar espacial se tornar real no cronograma da Overview, o movimento da Meta é interessante porque mostra quão longe a busca por energia para IA está se expandindo. O futuro da computação pode depender tanto da aquisição de energia quanto de chips.

→ https://techcrunch.com/2026/04/27/meta-inks-deal-for-solar-power-at-night-beamed-from-space/

[29:00] HISTÓRIA 4 — Carros Projetados por IA Passam de Arte Conceitual para Loops de Feedback Industrial
A última história é uma versão melhor de uma história de IA na indústria porque não é apenas sobre fazer imagens. É sobre encurtar loops de feedback.

O Verge relata como a GM, Nissan e Neural Concept estão usando IA no design e desenvolvimento de veículos. O antigo ciclo de desenvolvimento de veículos pode levar cinco anos ou mais: esboços, revisões de design, modelos 3D, argila, simulação, engenharia, software, restrições de fabricação e mais revisão. Esse ciclo é doloroso quando regulamentações, tarifas, incentivos para EVs, demanda dos consumidores e requisitos de software mudam mais rápido que o programa do carro.

Os designers da GM estão usando ferramentas como Vizcom para transformar esboços humanos em modelos e animações 3D mais ricos mais rapidamente. O detalhe chave é que o esboço humano ainda inicia o processo. A IA está ajudando a equipe a ver possibilidades mais cedo, comparar mais direções e criar material visual interno sem esperar por uma cadeia lenta de transferência.

A parte mais operacional é simulação. A Neural Concept usa redes neurais para acelerar a dinâmica de fluidos computacional. O Verge relata que a Jaguar Land Rover descreveu trabalhos aerodinâmicos que costumavam levar quatro horas agora levando cerca de um minuto, e a GM está desenvolvendo um túnel de vento virtual alimentado por IA que pode dar aos designers feedback quase instantâneo sobre arrasto conforme as superfícies mudam.

Essa é a mudança importante. Se o feedback aerodinâmico chega enquanto os designers ainda estão explorando formas, direções ruins podem ser eliminadas mais cedo e direções promissoras podem ser refinadas antes do design ser congelado. A IA é valiosa não porque ela desenha um carro uma vez, mas porque permite que a equipe teste mais versões enquanto o custo da mudança ainda é baixo.

O ângulo da Nissan são veículos definidos por software. Ela está usando ferramentas de geração de código para tarefas de software de nível mais baixo, como testes unitários, visando melhorar a velocidade e qualidade do desenvolvimento. Isso importa porque carros modernos são cada vez mais sistemas de software, e integração de software é onde os programas podem escorregar.

A cautela é que esses workflows ainda precisam de supervisão humana. Iteração mais rápida pode criar produtos melhores, mas também pode amplificar más suposições ou aumentar a pressão sobre os trabalhadores. O enquadramento útil é que a IA está entrando em loops industriais onde a saída não é o artefato final. A saída é um sinal anterior que ajuda humanos a decidir o que fazer a seguir.

→ https://www.theverge.com/transportation/918411/gm-ai-car-design-nissan-neural-concept

[36:00] OUTRO / ENCERRAMENTO
Esse é o episódio.

OpenClaw v2026.4.25 é o destaque porque torna o runtime mais pronto para produção em termos de voz, plugins, observabilidade, automação de navegador, configuração, atualizações e Codex. O próprio Codex está se tornando uma plataforma real de aplicativos de engenharia, com worktrees, automações, revisão de Git, threads de servidor de aplicativos, perfis de permissão e fluxos de trabalho de navegador no aplicativo. A aposta espacial-solar da Meta mostra o quão estranha fica o planejamento de infraestrutura de IA quando a energia se torna o gargalo. E os carros projetados por IA mostram o padrão mais forte de IA industrial: não geração em uma única tentativa, mas ciclos de feedback supervisionados por humanos mais rápidos.

→ Responda aqui para aprovar a geração da transcrição.