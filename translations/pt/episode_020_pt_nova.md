[NOVA]: A ferramenta virou o centro das conversas. Não o modelo por trás. Não a empresa. A ferramenta em si — a stack open-source que diz aos agentes o que fazer a seguir. E esta semana, de repente, essa ferramenta cresceu.

[NOVA]: O OpenClaw lançou sua release mais significativa em meses. A China enlouqueceu com isso, e depois Pequim tentou frear. A Microsoft apostou seu próximo movimento enterprise nisso. A Perplexity construiu uma versão que nunca dorme. E o dinheiro por trás de tudo isso? Um trimestre tão absurdo que todos os recordes anteriores parecem erro de arredondamento.

[NOVA]: Eu sou a NOVA.

[ALLOY]: E eu sou o ALLOY, e este é o OpenClaw Daily. ... Hoje temos cinco histórias, e todas as cinco são sobre a mesma mudança fundamental: o OpenClaw deixou de ser uma ferramenta inteligente e passou a ser infraestrutura. Temos a release que tornou isso real, o caso da China e suas consequências, a aposta enterprise da Microsoft, o agente local sempre ativo da Perplexity, e um trimestre de 297 bilhões de dólares que mostra onde a indústria está colocando suas fichas. Segurem os cintos — é um pesado.

[NOVA]: O fio condutor é uma transição. Transições em software não se anunciam de forma limpa. Elas se acumulam em release notes, mudanças de política e decisões de compra até que, de repente, você olha para cima e a ferramenta que você usava é a mesma ferramenta — mas as stakes são completamente diferentes.

[ALLOY]: Esse é o momento de plataforma. Quando a pergunta deixa de ser "isso pode fazer coisas legais?" e passa a ser "o que acontece se isso cair, for mal usado, ou for cortado?" Momentos de plataforma são empolgantes. Também são assustadores. Exigem mais de todos que estão construindo em cima.

[NOVA]: E o OpenClaw acabou de ter seu momento de plataforma. Vamos entender exatamente o que aconteceu.

[NOVA]: Vamos começar pela release. O OpenClaw v2026.3.31 chegou esta semana e parece menos um lançamento de funcionalidades e mais uma declaração de intenções. Esta é a release que diz: não estamos mais brincando.

[ALLOY]: A funcionalidade principal para mim é o painel de controle de tarefas em segundo plano. Pela primeira vez, ACP runs, subagent jobs, cron schedules e execuções CLI em background estão todos unificados sob um único ledger apoiado por SQLite. Um lugar para ver tudo. Um lugar para cancelar. openclaw flows list, openclaw flows show, openclaw flows cancel. É isso. Esse é o comando.

[NOVA]: E isso parece operacional — quase chato — até você perceber o que substitui. Antes, o trabalho em segundo plano no OpenClaw estava disperso. O ACP tinha sua contabilidade. Os subagents tinham seu próprio tracking. O cron fazia sua própria coisa. Se algo travasse ou saísse do controle, você precisava caçar em várias superfícies para entender o que estava acontecendo.

[ALLOY]: Agora você tem um ledger. Que é exatamente a palavra certa. Um ledger não apenas rastreia — ele cria responsabilização. Quando você pode ver cada run em segundo plano, seu estado, seu parent, seu histórico, você consegue raciocinar sobre o que seu sistema está fazendo de formas que simplesmente não podia antes. Isso é pensamento de infraestrutura.

[NOVA]: O segundo destaque é o que pode realmente quebrar algumas coisas para algumas pessoas: segurança de plugins falhando para fechado por padrão. Antes, instalações de plugins que continham código sinalizado iriam te avisar. Agora eles param. Se o scan de segurança encontrar um problema crítico, a instalação falha, ponto final, a menos que você passe explicitamente --dangerously-force-unsafe-install.

[ALLOY]: Essa é uma mudança de política real. Não é apenas um badge na UI dizendo "ei, pode ser arriscado." É um portão duro. E sim, haverá falsos positivos. Haverá autores de plugins que precisarão atualizar seus builds. Haverá desenvolvedores frustrados. Mas a direção está certa.

[NOVA]: Porque a alternativa — um framework de agentes de IA onde plugins perigosos silenciosamente dão certo porque ninguém quis incomodar o fluxo de instalação — é como você acaba numa situação em que a própria adoção do OpenClaw cria uma superfície de ataque que maus atores exploram em escala. A China, que vamos abordar, é literalmente um exemplo vivo de por que isso importa.

[ALLOY]: O pareamento de nodes também foi apertado. Antes, parear seu dispositivo era basicamente suficiente para habilitar comandos de node. Agora, comandos de node permanecem desabilitados até que o pareamento de node seja explicitamente aprovado. Parear e aprovar são dois passos separados. Isso não é burocracia. Isso é defesa em profundidade.

[NOVA]: As mudanças de auth do gateway vão além. Trusted-proxy agora rejeita configurações mistas de shared-token. Local-direct fallback requer o token configurado — ele não auto-autentica mais chamadores same-host. Essas parecem mudanças de encanamento menores nas release notes. Na prática, elas fecham a soft underbelly de muitos deployments auto-hospedados.

[ALLOY]: As pessoas que se importam com isso estão rodando o OpenClaw em algum lugar que não é o próprio desktop. Um servidor. Um VPS. Um setup multi-node em casa. Qualquer um que externalizou o gateway agora tem uma postura de segurança muito mais forte por padrão — sem precisar configurar manualmente.

[NOVA]: No lado dos canais, o QQ Bot agora vem junto. Isso significa que o OpenClaw tem um caminho de primeira linha para o ecossistema de mensagens da Tencent, o que — dado tudo o que vamos falar sobre a China — tem algumas implicações interessantes.

[ALLOY]: O Matrix ganhou streaming de replies. Respostas parciais agora atualizam a mesma mensagem no lugar em vez de floodar o chat com pedaços incrementais. Se você estava usando o OpenClaw no Matrix e observando ele spammar dez mensagens para uma única resposta longa, esta é a correção que você estava esperando.

[NOVA]: E o suporte MCP remote HTTP/SSE chegou. Essa importa para os builders que querem servir superfícies de ferramentas sem manter tudo local. Agora você pode servir endpoints MCP sobre transports remotos, o que abre uma nova classe de deployments onde o agente e as ferramentas que ele usa estão geograficamente ou arquitetonicamente separados.

[ALLOY]: Encaminhamento de notificações Android com filtragem de pacotes e quiet hours — finalmente. Se você está rodando o OpenClaw no Android ou encaminhando de um dispositivo Android, agora você pode controlar quais apps notificam e quando, com rate limiting incluso. Essa é a diferença entre um assistente ambiental útil e um celular que dispara a cada trinta segundos.

[NOVA]: Suporte a mídia outbound no LINE também. Imagens, vídeo, áudio — agora entregues pelo caminho específico do LINE, o que importa se você está construindo qualquer coisa para públicos do Sudeste Asiático ou Japão. O LINE não é um canal de nicho nesses mercados. É dominante.

[ALLOY]: Depois as mudanças que quebram compatibility. qwen-portal-auth removido. E — essa pessoa deveria ler com atenção — configs com mais de dois meses não fazem mais auto-migração. Se você estava rodando arquivos de config antigos e contando com a ferramenta para carregá-los silenciosamente, essa era acabou.

[NOVA]: O que na verdade é saudável. Janelas de auto-migração precisam de data de expiração ou se tornam dívida técnica permanente. A ferramenta não pode ser responsável para sempre pelas suas configurações de doze meses atrás. Em algum momento você atualiza. O soft deadline foi dois meses. Isso é razoável.

[ALLOY]: Também tem uma primeira versão de recovery hints do doctor para linkage de flow e task órfãos. Então se você atualizar e encontrar tasks quebradas, o comando doctor agora te dá orientação real e acionável em vez de uma parede de output de erro. Esse é o tipo de trabalho de qualidade de vida que não gera manchetes mas faz as pessoas realmente quererem atualizar.

[NOVA]: Tem também uma mudança mais quieta nesta release que acho que vai envelhecer bem: o idle-stream timeout para requests do embedded runner. Quando um stream de modelo trava — não erra, só fica pendurado, consumindo tempo sem produzir output — agora ele aborta de forma limpa em vez de bloquear até o run timeout geral disparar. Isso parece uma nota de rodapé. Não é. Em workflows de produção onde você está rodando múltiplas tarefas em segundo plano, um stream travado que bloqueia um slot por minutos é um problema operacional real. Abortar de forma limpa significa que outros trabalhos podem prosseguir.

[ALLOY]: A bridge ACPX plugin-tools MCP também ganhou documentação explícita e empacotamento reforçado. Essa é a bridge que permite sessões MCP interagirem com plugin tools. Antes desta release, essa superfície era funcional mas subdocumentada, o que em termos de segurança significa "funciona até não funcionar, e você não vai saber por quê." Torná-la explícita e default-off é a decisão certa. Você opta pela trust boundary quando entende, não por acidente.

[NOVA]: O quadro geral desta release é que o OpenClaw está fazendo o que plataformas maduras fazem. Está apertando o modelo de confiança. Está criando visibilidade operacional de primeira classe. Está tornando padrões mais seguros mesmo quando isso significa atrito de curto prazo. E está construindo a instrumentação que deployments sérios precisam.

[ALLOY]: A versão hobbyista desta ferramenta dizia "sim" para quase tudo por padrão. A versão infraestrutura diz "sim, mas me confirme que você entende o que está pedindo." Essa é uma mudança profunda em como o projeto se vê e para quem está construindo.

[NOVA]: A docs resume melhor: esta é a release onde o OpenClaw para de ser uma ferramenta de hobby e começa a ser infraestrutura. Eu acredito nisso. Acho que você deveria também.

[ALLOY]: Nossa segunda história começa com filas. Filas literais de pessoas em eventos pop-up organizados pela Tencent para instalar o OpenClaw em seus celulares e laptops. Em Shenzhen. Em Xangai. Por toda a China. Isso não é uma conferência de tecnologia. São aposentados e donas de casa formando fila para ter um agente de IA estrangeiro instalado em seus dispositivos pessoais.

[NOVA]: O OpenClaw virou genuinamente viral na China. Jensen Huang aparentemente chamou de "o próximo ChatGPT" de um palco, e essa citação se espalhou. Stars no GitHub do projeto brevemente superaram o React — ou seja, superaram uma das bibliotecas frontend mais usadas já criadas. Isso não é uma curva de adoção de nicho. É um momento cultural.

[ALLOY]: E na China, o OpenClaw tem um apelido: lobster. As razões são um pouco nebulosas — algo sobre como a ferramenta "agarra" as tarefas. Mas o nome pegou, e as consequências também. Porque na mesma semana que a Tencent estava hospedando eventos de instalação, os "vítimas do lobster" começaram a aparecer.

[NOVA]: Relatos de agentes de IA entregando dados sensíveis para estranhos. Relatos de agentes acumulando contas enormes rodando em segundo plano durante a noite. E um incidente particularmente vívido: um consultor em Xangai pediu ao wrapper WeChat da Tencent baseado no OpenClaw — o QClaw — para organizar seus arquivos em duas pastas. O agente apagou permanentemente dezenas de documentos. Relatórios de clientes. Trabalho realizado. Gone.

[ALLOY]: Esse é exatamente o modo de falha que as novas funcionalidades de segurança na v2026.3.31 foram projetadas para prevenir. Um agente com acesso demais, restrição de menos, e nenhum modo de falha graceful causa dano real a pessoas reais. A citação do consultor foi direta: "Não vou usar nada que precise ser instalado localmente e não vou deixar IA tocar no meu computador de trabalho nunca mais."

[NOVA]: Essa reação é totalmente racional. E aponta para a tensão central que a China está navegando. Pequim tem uma meta ambiciosa — mais de 70% de penetração de deployment de agentes de IA em saúde e manufatura até 2027. Eles estão contando com IA agentic como motor de crescimento econômico de longo prazo. Eles precisam dessa tecnologia funcionar. E ainda assim está claramente prejudicando usuários comuns de formas que estão gerando backlash.

[ALLOY]: Então os reguladores agiram. Funcionários de empresas estatais agora supostamente têm uso do OpenClaw banido. A PCWorld publicou um aviso oficial de segurança contra a instalação. Há rumores de escrutínio mais amplo de governança de dados. O governo que queria liderar a onda de IA agentic agora está tendo que simultaneamente acelerá-la e limpar a bagunça.

[NOVA]: A peça do Wire China vale a leitura completa — vamos linkar nas notas do show. O enquadramento de pesquisadores é perspicaz: esse é um caso de teste para como a China equilibra proteção ao consumidor com competitividade de inovação. E até agora a resposta parece ser "aplique band-aid nos incêndios mais visíveis, não pare o fogo por completo."

[ALLOY]: O canal QQ Bot que acabou de ser shipped na v2026.3.31 está bem no centro disso. O OpenClaw agora tem um caminho bundled para o ecossistema da Tencent. O que significa que a mesma plataforma que acabou de apertar sua postura de segurança e tornar instalações de plugins fail closed também está expandindo seu alcance diretamente para o ambiente de mensagens onde usuários chineses são mais ativos.

[NOVA]: Isso não é uma contradição. É uma estratégia. Feche os buracos de segurança óbvios. Depois expanda a distribuição. Você não pode expandir distribuição de forma sustentável com buracos de segurança escancarados, e você não pode tornar segurança significativa sem de fato estar presente no ecossistema. Ambos os movimentos estão corretos.

[ALLOY]: Para builders observando isso de fora da China: a história das vítimas do lobster é um presente. Não porque é engraçada — aquelas pessoas perderam arquivos e dinheiro de verdade. Mas porque é uma demonstração extremamente legível de como sistemas de agentes parecem quando falham sem guardrails. É fácil falar abstratamente sobre "a importância do controle de acesso." É muito mais concreto quando você pode apontar para um consultor cujos relatórios de cliente foram deletados por uma IA que só estava tentando ajudar.

[NOVA]: O que é a cruel ironia. O agente quase certamente não estava com defeito no sentido tradicional. Ele recebeu uma instrução. Ele executou. Ele provavelmente teve sucesso da própria perspectiva. "Organize arquivos em duas pastas" — feito. O problema não era um bug no sentido usual. Era um desalinhamento entre o que o usuário quis dizer e o que a instrução permitiu.

[ALLOY]: E essa lacuna — entre instrução e intenção, entre permissão e propósito — é exatamente o que estruturas de governança existem para fechar. Tetos de orçamento, gates de aprovação, restrições de escopo, trilhas de auditoria. Todas as funcionalidades "chatas" de infraestrutura que tornam operações reais seguras. As vítimas do lobster não tinham nada disso. Tinham acesso bruto.

[NOVA]: O momento da China com o OpenClaw é acelerado, caótico e instrutivo. Eles estão executando um arco de adoção de dois anos em cerca de dois meses. Todos os erros que a maioria dos ecossistemas espalha ao longo do tempo estão chegando simultaneamente. E o resto do mundo fica assistindo.

[NOVA]: A história três é sobre um tipo diferente de sinal de legitimidade. A Microsoft está ativamente integrando o OpenClaw no Microsoft 365. Não experimentando. Não piloto em um canto. Ativamente trabalhando para trazer agentes de IA pessoais alimentados pelo OpenClaw para as massas enterprise.

[ALLOY]: Vamos dedicar um momento para registrar o que isso significa. O Microsoft 365 tem cerca de 400 milhões de usuários. É a camada de produtividade para a maior parte das empresas americanas e uma fração substancial das empresas europeias e asiáticas. Se o OpenClaw se tornar uma capacidade nativa dentro do Teams, Outlook, Word e Excel, você foi de "ferramenta open-source com uma comunidade apaixonada" para "o framework de agentes de IA embedded no software que metade dos trabalhadores do conhecimento mundial usa todo dia."

[NOVA]: Esse é um marco de distribuição que a maioria dos projetos de software nunca se aproxima. E chega num momento interessante — justamente quando o hardening de segurança na v2026.3.31 o torna mais crível como infraestrutura enterprise. O timing quase certamente não é coincidência.

[ALLOY]: Há uma versão desta história onde é simplesmente validadora. A Microsoft aposta no framework de agentes open-source mais capaz. Compradores enterprise se sentem confortáveis porque a Redmond está por trás. A adoção acelera. O ecossistema cresce. Vitória em todos os fronts.

[NOVA]: E há outra versão onde é mais complicado. Deployments enterprise não são deployments de hobby. O threat model é diferente. As superfícies de acesso são diferentes. Um agente pessoal que tem acesso de leitura ao seu calendário é uma coisa. Um agente corporativo que tem acesso aos contratos da sua empresa, dados de RH, previsões financeiras e comunicações com clientes é categoricamente outra coisa.

[ALLOY]: As perguntas de governança de dados se tornam imediatas e sérias. Para onde os prompts vão? Onde o contexto é armazenado? Quem pode ver os logs de auditoria? O que acontece quando um agente num tenant 365 comete um erro do tipo que importa para oficiais de compliance, equipes jurídicas e reguladores?

[NOVA]: E quem é responsável? Se um agente pessoal rodado por um hobbyista deleta arquivos de clientes, isso é uma tragédia pessoal. Se um agente 365 deployed enterprise faz o equivalente em escala, é um evento de responsabilidade com implicações regulatórias potenciais em múltiplas jurisdições.

[ALLOY]: Não estou dizendo que a Microsoft não pode lidar com isso. Eles têm times inteiros cujo trabalho é tornar software enterprise suportável em escala regulada. Mas o fato de estarem integrando o OpenClaw não significa que esses problemas estão resolvidos. Significa que eles se comprometeram a resolvê-los. O que é uma coisa diferente.

[NOVA]: Quanto mais penso sobre esse acordo, mais acho que o enquadramento certo não é "validação vs. risco" — é "aceleração." A Microsoft acelera o alcance do OpenClaw. O OpenClaw acelera a história de agentes de IA da Microsoft. Ambos se movem mais rápido do que sozinhos. Os riscos também se movem mais rápido.

[ALLOY]: E para builders independentes, isso cria um conjunto específico de considerações. Se seu workflow depende de comportamentos do OpenClaw que estão em tensão com políticas enterprise — acesso direto a ferramentas, permissões amplas, execução autônoma sem loops de aprovação — você deveria estar prestando atenção em como a integração com 365 molda os padrões.

[NOVA]: Projetos com grandes sponsors enterprise às vezes derivam em direção às restrições do contexto desse sponsor. Não por má intenção. Porque muita pressão real do mundo real empurra nessa direção. Feature requests, requisitos de compliance, preocupações com responsabilidade, obrigações de suporte. Essas não são triviais.

[ALLOY]: O outro lado é que adoção enterprise financia o desenvolvimento que eventualmente volta para builders independentes. O trabalho de segurança feito para satisfazer compliance da Microsoft também é trabalho de segurança que torna seu deployment pessoal mais seguro. Essa não é uma troca pura.

[NOVA]: ... O headline é simples: o OpenClaw agora está no roadmap da Microsoft. Essa é uma das maiores declarações de distribuição na história da ferramenta. As implicações são tanto empolgantes quanto vale a pena assistir cuidadosamente enquanto se desenrolam.

[ALLOY]: A história quatro é diferente em sabor. Enquanto a Microsoft vai largo, a Perplexity vai fundo. Eles lançaram algo chamado Personal Computer — e o conceito é o que parece. Um agente de IA dedicado que roda num Mac mini, mora na sua casa ou escritório em tempo integral, e tem acesso persistente e contínuo aos seus arquivos e aplicativos locais.

[NOVA]: Isso não é um assistente na nuvem que você chama. Não é uma sessão que você abre e fecha. É uma inteligência residente. Está sempre ativo, sempre ciente do contexto, sempre disponível. Ele observa seu sistema de arquivos. Ele conhece o estado dos seus aplicativos. Quando você precisa dele, ele estava prestando atenção desde antes de você perguntar.

[ALLOY]: Essa é uma proposição de valor fundamentalmente diferente de IA baseada em API. A latência desaparece — não só latência de rede mas latência de contexto. A frustração de re-explicar sua situação toda vez que você abre uma nova janela de chat desaparece. O agente já sabe. Ele estava lá.

[NOVA]: O argumento de privacidade disso também é interessante. Seus arquivos, seu contexto, seus aplicativos — eles ficam no seu dispositivo. Nenhum upload para um endpoint na nuvem para ser processado no servidor de outra pessoa, logged na infraestrutura de outra pessoa, potencialmente visível para o team de compliance de outra pessoa.

[ALLOY]: O que importa mais conforme agentes de IA ganham acesso a superfícies mais sensíveis. Quando o agente pode ler seus rascunhos, suas notas, suas mensagens privadas, seus documentos financeiros — você quer saber onde esse contexto vive. "No meu Mac mini no meu home office" é uma resposta muito diferente de "num endpoint na nuvem num data center que você não tem visibilidade."

[NOVA]: Há trade-offs. Um Mac mini no seu home office não consegue igualar o compute de um cluster de inferência de hyperscale. Context windows muito grandes, raciocínio multi-step complexo e tarefas de geração computacionalmente pesadas serão mais lentos ou menos capazes do que você obteria de uma API de nuvem frontier.

[ALLOY]: Mas para os workflows onde latência, privacidade e contexto persistente importam mais que poder bruto do modelo, o trade-off pende para local. Ler seus arquivos de projeto e lembrar decisões de ontem não requer um modelo de 100 bilhões de parâmetros rodando em um rack de H100s. Requer um modelo capable o suficiente rodando perto de onde os dados vivem.

[NOVA]: E a classe de "capable o suficiente" tem se expandido rapidamente. O tipo de modelo que você pode rodar localmente em início de 2026 teria sido considerado performance frontier competitiva em início de 2024. Essa lacuna está fechando. A pergunta não é se local vai algum dia igualar cloud — a pergunta é se local é bom o suficiente para seu caso de uso específico. Para um número crescente de casos de uso, a resposta honesta é sim.

[ALLOY]: Há também um argumento de confiabilidade que é negligenciado nas comparações de capability. Inferência na nuvem tem variância de latência. Tem outages. Tem rate limits. Um modelo local rodando num dispositivo dedicado não tem nenhum desses modos de falha. Pode ser mais lento numa única request, mas é previsivelmente disponível de formas que workflows dependentes de API simplesmente não são.

[NOVA]: Essa previsibilidade importa especialmente para casos de uso ambientes e sempre ativos. Se seu agente de computador pessoal é suposto estar lá quando você precisa, "a API está com taxas de erro elevadas" é uma resposta inaceitável. O modelo local não tem esse problema. Ele tem um diferente — você tem que mantê-lo — mas é um modo de falha que você controla.

[ALLOY]: O que acho compelling no enquadramento da Perplexity é que ela pega uma marca de IA consumidor — que a maioria das pessoas associa com busca rápida na web e assistência de pesquisa — e reposiciona como a camada de IA doméstica. Não uma ferramenta de busca. Não uma interface de chat. Um residente. Essa é uma mudança de categoria ambiciosa.

[NOVA]: E posiciona a Perplexity de forma interessante em relação ao OpenClaw. Se o OpenClaw é o framework de agentes e a Microsoft é a distribuição enterprise, o Personal Computer da Perplexity pode estar mirando o tier doméstico e prosumer. Persistente, ambiente, local, privado, sempre disponível. Essa é uma lacuna real e não atendida.

[ALLOY]: Para usuários do OpenClaw especificamente, o Personal Computer representa tanto um complemento quanto um frame competitivo. Você pode rodar o OpenClaw localmente e alcançar muitas das mesmas propriedades de agente persistente sem o wrapper da Perplexity. Mas se o wrapper é melhor UX, melhor experiência de primeiro uso, e melhor para usuários que não querem configurar um stack do zero — pode capturar usuários que de outra forma eventualmente se tornariam power users do OpenClaw.

[NOVA]: ... O ponto mais amplo é que a pergunta "onde a IA mora" está sendo respondida de múltiplas formas simultaneamente. Nuvem, híbrido, embedded enterprise, e agora residencial dedicado. A arquitetura de acesso a IA está se diversificando. Isso é saudável para builders que querem opções. É complicado para quem apostou numa única arquitetura vencendo.

[NOVA]: E agora o dinheiro. A história cinco são os números de funding de venture do Q1 2026 e eles são simplesmente extraordinários. Dados do Crunchbase mostram que investidores despejaram 297 bilhões de dólares em startups globalmente no trimestre. Esse é um recorde absoluto. Com folga.

[ALLOY]: Para contexto: o Q1 2026 sozinho totaliza perto de 70% de todo o investimento de venture capital em todo o ano de 2025. A soma trimestral supera cada total anual completo indo até antes de 2018. Em um trimestre.

[NOVA]: Oitenta e um por cento foi para empresas de IA. São 239 bilhões de dólares em IA em um único trimestre. O recorde anterior foi Q1 2025, quando IA levou 55% do VC global. Em doze meses isso saltou para 81%. A concentração está acelerando, não plateauando.

[ALLOY]: Quatro deals impulsionaram grande parte do número do headline. A OpenAI levantou 120 bilhões. A Anthropic levantou 30 bilhões. A xAI levantou 20 bilhões. A Waymo levantou 16 bilhões. Esses quatro rounds sozinhos respondem por 186 bilhões — que é 64% de todo o investimento de venture global no trimestre.

[NOVA]: Deixe isso assentar por um momento. Quatro empresas. Sessenta e quatro por cento de todo o venture capital global. Em três meses. Esse não é um ambiente de funding broad-based. Isso é concentração extrema de capital em torno de um punhado de apostas na frontier.

[ALLOY]: E a concentração se estende geograficamente. Empresas americanas levantaram 247 bilhões — 83% de todo o venture capital global no trimestre. O segundo maior mercado foi a China com 16,1 bilhões. O Reino Unido veio em terceiro com 7,4 bilhões. A lacuna EUA-versus-rest não está diminuindo. Está aumentando.

[NOVA]: A CoreWeave secureou uma facilidade de financiamento de 8,5 bilhões de dólares, o que te diz algo importante sobre para onde o dinheiro está indo mesmo abaixo da camada de modelo frontier. Nem tudo está indo para construir IA mais inteligente. Uma porção enorme está indo para o compute e infraestrutura que roda IA. Chips. Energia. Cooling. Redes. O substrato físico.

[ALLOY]: O que se conecta a algo que já discutimos antes. Investimento em IA é cada vez mais investimento em infraestrutura — não só infraestrutura de software mas infraestrutura física. Data centers. Clusters de GPU. Fibra. Redes elétricas. O capital está fluindo para coisas que levam anos para construir e criam lock-in geográfico e físico.

[NOVA]: Esse é um perfil de risco diferente de software. Software é geralmente reversível. Infraestrutura não é. Se você commita 8,5 bilhões em capacidade de compute e o ambiente de demanda muda, você tem 8,5 bilhões em capacidade de compute. A aposta é real de uma forma que apostas em software geralmente não são.

[ALLOY]: A pergunta que este trimestre levanta — e que ninguém pode responder honestamente — é se a alocação de capital reflete retornos econômicos genuínos ou se reflete algo mais próximo de uma dinâmica de corrida, onde ficar para trás parece mais arriscado do que gastar demais.

[NOVA]: E "corrida" não é só uma metáfora aqui. O enquadramento geopolítico em torno de IA tem sido explícito por anos. A concentração de investimento americano, os números de funding da China, os movimentos regulatórios que vimos mirando vendors específicos — tudo reflete uma visão de que acumulação de capability de IA é um interesse nacional estratégico, não apenas uma oportunidade de mercado.

[ALLOY]: O que significa que os 297 bilhões não são só um sinal de mercado. São um sinal de política. Quando governos veem números assim fluindo predominantemente para empresas domésticas, isso reforça a visão de que direcionar política e procurement para vendors preferidos é economicamente racional.

[NOVA]: O board de unicórnios adicionou 900 bilhões em valuation durante o Q1 sozinho. Não market cap — valuations, a maioria privada, impulsionada pelo mesmo entusiasmo de investidores que está financiando os rounds. Há uma pergunta que pessoas sérias estão fazendoquietamente: o que acontece com esse ecossistema se o ambiente de valuation reverte? O capital está financiando a infraestrutura da qual builders dependem. Se os tamanhos de round comprimem, o investimento em infraestrutura comprime também. Esse é um risco de segunda ordem que a maioria dos builders não gerencia diretamente mas absolutamente vive com.

[ALLOY]: Para builders independentes, as implicações são mistas. Uma indústria com esse nível de commitment de capital cria recursos enormes para tooling, modelos, infraestrutura e talento. Muito do que você está construindo hoje existe por causa de fluxos de capital assim. Isso é real.

[NOVA]: Mas concentração também cria fragilidade. Se quatro empresas estão capturando a maior parte do capital e a maior parte da atenção estratégica, o long tail do ecossistema depende heavily das decisões delas. Projetos open-source, pequenos tool builders e praticantes individuais são beneficiários do trabalho frontier — e também um pouco à mercê dele.

[NOVA]: A posição do OpenClaw neste ambiente é na verdade instrutiva. É um projeto open-source, não um laboratório frontier apoiado por VC. Não tem 30 bilhões em seu treasury. Mas tem algo que esses laboratórios frontier cada vez mais precisam: uma camada de agente composable e distributable que fica em cima de qualquer modelo que você estiver rodando. O valor do OpenClaw não é que ele compete com os laboratórios. É que ele trabalha com todos eles.

[ALLOY]: Essa é uma posição durável. Enquanto a camada de modelo permanecer plural — enquanto não houver um modelo que vença tudo — há um trabalho real para uma camada de orquestração que fala todos eles fluentemente. O trimestre de 297 bilhões é um testemunho de quanto está sendo despejado na camada de modelo. Isso torna a camada de coordenação mais importante, não menos.

[NOVA]: ... O número é vertiginoso. Mas a história real não é o tamanho — é a estrutura. Concentração massiva no topo. Consolidação geográfica nos EUA. Apostas de infraestrutura física de uma escala que não pode ser facilmente desfeita. E um ecossistema open-source que está simultaneamente se beneficiando de e um pouco à mercê de como essas apostas se desenrolam.

[ALLOY]: Então o picture desta noite se clear como uma única palavra: infraestrutura.

[NOVA]: O OpenClaw v2026.3.31 não shipping nova mágica. Ele shipping a scaffolding que torna mágica segura para rodar em escala. Painéis de controle de tarefas em segundo plano. Segurança de plugins que falha fechado. Gates de aprovação de node. Auth hardening. Atualizações de streaming replies. Abortos de idle-stream. Comandos de schema de config. Preflight checks na atualização. Essas não são funcionalidades empolgantes. São funcionalidades necessárias. E necessário é do que infraestrutura é feita.

[ALLOY]: O momento lobster da China é infraestrutura faltando em tempo real. Ferramentas capazes, sem guardrails, pessoas reais prejudicadas. O estado agora está forçado a gerenciar a limpeza de adoção viral que ultrapassou a camada de segurança. A lição se escreve sozinha.

[NOVA]: A Microsoft apostando no OpenClaw para 365 é ambição de infraestrutura. Eles não estão apenas adicionando uma funcionalidade. Eles estão declarando onde a camada de agente vive para computação enterprise pela próxima década.

[ALLOY]: O Personal Computer da Perplexity é infraestrutura que se move na direção oposta — não para a nuvem, mas para casa. Persistente. Local. Privado. O modelo de inteligência residente.

[NOVA]: E o trimestre de 297 bilhões é infraestrutura em escala planetária. Compute, energia, redes, prédios, chips. A camada física que tudo isso roda, sendo apostada numa velocidade que não tem precedente histórico.

[ALLOY]: Agentes estão no ponto de inflexão. Não por causa de um modelo mágico que finalmente cruzou um limiar. Mas porque a scaffolding finalmente está acompanhando a capability. As partes chatas estão sendo construídas. As perguntas difíceis de governança estão sendo feitas. Os compradores enterprise estão chegando com seus requisitos e suas checklists de compliance, e de alguma forma — impropriamente — a comunidade open-source está os encontrando.

[NOVA]: Isso é o que é fácil perder se você só acompanha os benchmarks de modelo. Os benchmarks estavam se movendo rápido por dois anos antes de qualquer dessa governança de infraestrutura existir. Capability sem governança é uma demo. Capability com governança é um produto. E 2026.3.31 é o momento em que o OpenClaw cruzou de uma categoria para a outra.

[NOVA]: Isso não é uma coisa pequena. Isso é exatamente o que momentos de plataforma parecem por dentro. Desorganizado. Multi-direcional. Mais rápido do que confortável. Cheio de perguntas não resolvidas. Requerendo confiança antes da confiança ter sido totalmente ganha. E inconfundivelmente, irreversivelmente real.

[ALLOY]: Notas completas do show, links e arquivo de episódios estão em tobyonfitnesstech.com.

[NOVA]: Voltamos em breve.

[ALLOY]: Eu sou o ALLOY.

[NOVA]: E eu sou a NOVA. Obrigado por ouvir.