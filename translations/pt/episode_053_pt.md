[NOVA]: Eu sou a NOVA.

[ALLOY]: E eu sou o ALLOY, e este é o AgentStack Daily. Hoje começamos com o host e a superfície de código: OpenClaw v2026.5.18 e Codex rust-v0.131.0.

[NOVA]: OpenClaw adiciona ferramentas de plugin tipadas, automação de navegador com suporte a diálogos, preparação mais rápida do gateway, suporte a proxy HTTPS, Talk Mode Android em tempo real, manipulação mais segura de mídia, entrega de canal mais robusta e comportamento mais estreito entre Codex e app-server. Codex adiciona melhor status TUI, menções unificadas, comandos do marketplace de plugins, infraestrutura de controle remoto, ambientes remotos configurados, um SDK Python e codex doctor.

[ALLOY]: Essa é a estrutura útil do episódio. Primeiro, o host do agente. Depois, a camada de CLI e app-server que os desenvolvedores mexem o dia todo. Depois disso, o GitHub transforma as sessões de agente do Copilot em algo que você pode controlar de mais lugares e com modelos menores. E a Anthropic dá à busca na web do Claude dados mais ricos de filings da SEC para agentes de pesquisa financeira.

[NOVA]: A questão prática não é se os agentes estão ganhando mais funcionalidades. Estão. A questão é quais peças tornam o trabalho do agente mais observável, mais recuperável, e mais fácil de confiar quando a execução é longa, remota, multimodal ou restrita por políticas.

[ALLOY]: Então vamos ficar práticos: contratos de plugins, estado de modal do navegador, probes de readiness, checagens de paridade de runtime, comportamento de relay de voz, status TUI, envelopes de permissão, sessões remotas, multiplicadores de tarefas, reparo de Actions e metadados de fonte para afirmações financeiras. ...

[NOVA]: O resumo de releases do Agent-stack começa com o OpenClaw porque o host é onde uma stack de agente tanto parece durável quanto parece improvisada. Um host tem que conectar modelos, ferramentas, canais, navegadores, clientes móveis, inputs de mídia, permissões e pontes de app-server. Quando esse release do host muda a forma dos plugins, estado do navegador, readiness do gateway, voz mobile e integração com o Codex em uma única passagem, merece o início do episódio.

[ALLOY]: A primeira mudança voltada para desenvolvedores é a forma dos plugins. OpenClaw adiciona defineToolPlugin e os comandos openclaw plugins init, openclaw plugins build e openclaw plugins validate para plugins de ferramentas simples tipadas. Isso dá aos autores de plugins metadados de manifest gerados, declarações opcionais e factories de contexto em vez de pedir para cada pequeno plugin carregar cola escrita à mão.

[NOVA]: Isso parece ergonomia de desenvolvedor, e é, mas também é uma funcionalidade de confiabilidade. Plugins de ferramentas ficam muito mais fáceis de inspecionar quando o manifest e as declarações são gerados a partir de uma fonte tipada. Um host pode raciocinar sobre o que um plugin expõe, que contexto ele espera e qual deve ser o formato dos seus inputs e outputs. Quanto menos superfícies não documentadas em torno de uma ferramenta, menos surpresas aparecem dentro de uma execução de agente.

[ALLOY]: Isso também importa porque o release depreca superfícies mais antigas de produtor de rich messages, incluindo caminhos legados de interactive e diretivas do Slack, enquanto adiciona limites de capacidade de apresentação de canal. Esse é um contrato mais saudável. Um plugin deve saber se o canal pode renderizar um controle interativo, um rich block, uma mensagem simples, um anexo, uma nota de voz, ou apenas um fallback estreito.

[NOVA]: Certo. O erro em muita ferramenta de agente é tratar cada canal como a mesma superfície de output. Um chat web, um canal do Discord, um tópico do Telegram, uma thread do Slack e uma sessão de voz mobile não têm regras de apresentação idênticas. Se um plugin assume que eles têm, o agente pode produzir um objeto que o canal não consegue mostrar. Limites de capacidade de apresentação permitem que o host diga o que realmente é possível antes da resposta final ser moldada.

[ALLOY]: As mudanças no navegador são o segundo item principal do host. Snapshots agora expõem diálogos modais pendentes e recentemente tratados. Actions podem retornar blockedByDialog quando um modal abre. E browser dialog com um dialog ID pode responder a um diálogo pendente. Isso é exatamente o tipo de pequena melhoria de estado que salva agentes de navegador de falhas vagas.

[NOVA]: A automação de navegador frequentemente falha de formas tediosas. Um clique não funciona porque um alerta abriu. Um submit de formulário parece travado porque um diálogo de confirmação tomou conta da página. Um agente continua tentando interagir com estado obsoleto da página porque não consegue ver o modal que um humano perceberia instantaneamente. Ao representar diálogos como estado explícito, a camada do navegador dá ao agente uma próxima ação real em vez de forçá-lo a inferir a partir de um timeout.

[ALLOY]: A frase importante é estado explícito. Um modal não é apenas ruído em cima da página. Ele muda o contrato de interação da página. Quando uma action retorna blockedByDialog, o agente pode parar de fingir que tem um problema normal de DOM e lidar com o diálogo diretamente.

[NOVA]: Isso também facilita a auditoria de agentes de navegador. Se a transcrição de uma execução diz que a ação foi bloqueada por um diálogo, o operador consegue entender por que uma sequência pausou. Se o host apenas reporta uma falha de clique, o caminho de debug é muito pior: rede, seletor, iframe, timing, auth, crash da página, ou algo inteiramente diferente.

[ALLOY]: O startup do gateway e o comportamento de proxy são os próximos. OpenClaw agora sobrepõe o logging de startup e o startup do serviço de plugins com sidecars de canal enquanto preserva o gating do sidecar readyz. Traces de restart atribuem custos de probe, config, runtime e contagem de recursos sem mudar a semântica de readiness.

[NOVA]: Essa é uma mudança de operador sutil mas valiosa. Startup mais rápido é útil, mas a peça mais importante é evidência. Se um restart é lento, um operador precisa saber se o custo é tempo de probe, carga de config, startup de runtime, trabalho de sidecar, startup do serviço de plugins, ou contagem de recursos. A infraestrutura de agentes é cheia de peças móveis, então readiness tem que ser tanto conservadora quanto explicável.

[ALLOY]: E preservar a semântica de readiness importa. É fácil acelerar um serviço dizendo que está pronto antes das dependências estarem prontas. Isso não é uma melhoria. Apenas move a falha para depois. A versão útil é sobrepor trabalho onde é seguro, mas ainda permitindo que readyz signifique que o host realmente consegue servir as superfícies que promete.

[NOVA]: O trabalho de proxy também é prático. O release adiciona endpoints de forward-proxy HTTPS gerenciados e trust de scoped proxy.tls.caFile. Isso dá aos deployments uma forma mais limpa de rotear tráfego através de caminhos de proxy com inspeção TLS ou privados sem transformar a configuração de proxy em uma decisão de trust global.

[ALLOY]: Isso importa em ambientes enterprise e de laboratório onde o tráfego de saída não é simplesmente internet aberta. Agentes chamam APIs, buscam páginas, acessam docs, reach endpoints de modelos e movem mídia. Se o caminho do proxy requer trust especial, esse trust deve ter escopo na configuração do proxy. Não deve ampliar casualmente o trust por todo o runtime.

[NOVA]: O bloco QA-Lab pode ser a parte mais importante para quem faz deploy de agent hosts. OpenClaw adiciona cenários de paridade de runtime de 20 turns na primeira hora e opcionais de 100 turns, tier de paridade de runtime da suite openclaw qa, cobertura de tool fixtures através das openclaw qa coverage tools, artefatos de eficiência de token em runtime ao vivo, e um hard gate para drift de ferramenta de runtime dinâmico do OpenClaw requerido no tier padrão Codex-vs-Pi.

[ALLOY]: Em termos simples, o release está verificando se diferentes runtimes se comportam de forma suficientemente similar sob pressão real do agente. Isso é muito mais útil do que apenas verificar se o processo inicializa. Regressões de agentes frequentemente aparecem como drift de vocabulário de ferramentas, má seleção de ferramentas, uso alterado de tokens, fixtures faltando, ou um runtime escolhendo a superfície errada.

[NOVA]: Exatamente. Um smoke test pode dizer que o servidor está vivo enquanto o agente está silenciosamente pior. Cenários de paridade de runtime fazem uma pergunta mais difícil: se a mesma tarefa passa por diferentes caminhos de runtime, as escolhas de ferramentas, capacidades e saídas permanecem dentro de um envelope esperado? É assim que você captura o tipo de regressão de release que os usuários descrevem como "o agente parece diferente agora".

[ALLOY]: A forma de 20 e 100 turns importa porque testes curtos de agente são muito permissivos. Uma chamada de ferramenta de um turn não diz se o trimming de contexto, estado da ferramenta, permissões, recuperação de erros e roteamento de modelo permanecem estáveis após uma sessão real. Cenários mais longos expõem as falhas lentas.

[NOVA]: O Talk Mode do Android também recebe uma grande mudança de runtime. O app Android troca o Talk Mode para sessões de voz com relay Gateway em tempo real com entrada de microfone em streaming, reprodução de áudio em tempo real, bridging de resultados de ferramentas e transcrições na tela.

[ALLOY]: Isso transforma a voz mobile em uma superfície de sessão ativa. Não é apenas speech-to-text entrada e text-to-speech saída. Uma sessão de voz em tempo real pode carregar resultados de ferramentas de volta através do Gateway, manter umtranscrição visível, e fazer o assistente parecer contínuo enquanto as ferramentas estão rodando.

[NOVA]: O risco de engenharia é interrupção e timing. Entrada de microfone em streaming precisa de cancelamento limpo. Reprodução de áudio em tempo real precisa parar quando o usuário interrompe. O bridging de resultados de ferramentas precisa evitar ler saída obsoleta depois que o usuário mudou de direção. E as transcrições precisam se alinhar closely o suficiente para que o usuário consiga dizer o que o agente ouviu e o que fez.

[ALLOY]: Por isso a voz mobile é um recurso de host, não apenas um recurso de cliente. O cliente pode capturar áudio, mas o host tem que coordenar identidade de sessão, eventos de ferramenta, respostas em streaming, cancelamento e política de canal. Se o host for negligente, a UX de voz se torna confusa mesmo quando o áudio em si soa bem.

[NOVA]: O bloco de fixes é onde muitos upgrades de produção vão sentir o release. Completions de mídia gerados agora voltam para tópicos do fórum do Telegram preservando IDs de tópico através do handoff requester-agent. Image metadata probing evita invocar delegates de decodificador externos em bytes não reconhecidos. O Sharp é instalado com fallbacks para ferramentas nativas de imagem, ImageMagick, GraphicsMagick, ou ffmpeg.

[ALLOY]: Esses não são itens glamorosos, mas são as coisas que impedem sistemas de agentes de perder trabalho. Se uma resposta de imagem gerada cai no tópico errado, a experiência do usuário quebra. Se metadata probing chama delegates de decodificador externos em bytes desconhecidos, o manuseio de mídia carrega risco desnecessário de segurança e confiabilidade. Se o processamento de imagem depende de um caminho de módulo nativo e ele falha, toda a funcionalidade de mídia fica frágil.

[NOVA]: Sessões de voz do Discord também recebem atenção. O release mantém turns de follow-up funcionando com OpenAI realtime e prebuffers a reprodução do assistente para reduzir começos travados.

[ALLOY]: O ponto do prebuffer é pequeno mas humano. Voz em tempo real é julgada pelo timing. Se o assistente começa com áudio cortado ou falha em ouvir o próximo turn, o usuário perde confiança rápido. Um stack de voz tecnicamente correto ainda parece quebrado quando o take-turning é áspero.

[NOVA]: Diretivas de mensagem e TTS são aplicadas antes das mensagens到达 caminhos de entrega, então salas que optam por notas de voz recebem notas de voz ao invés de tags brutas. Esse é mais um fix de contrato de canal. A diretiva deve moldar a entrega antes da mensagem ser enviada, não vazar como texto para o usuário.

[ALLOY]: Os repairs do Codex app-server do OpenClaw são especialmente relevantes para stacks de agentes mistos. Anexos de imagem inbound atuais hidratam antes de runs enfileiradas, então agentes backed por Responses recebem imagens de canal como input de visão nativo. O modo de código nativo permanece disponível sem forçar código-modo-apenas, o que permite que turns de ferramenta dinâmica do OpenClaw completem através da ponte app-server.

[NOVA]: O acesso à rede é preservado para turns de código-modo sandboxed do Codex quando o sandbox do OpenClaw permite egress outbound. A configuração de código-modo por-agente é respeitada no schema, ativação do catálogo de runtime e filtragem de payload de modelo. Política restrita de chat ou sender agora falha closed desabilitando superfícies de código nativo, app, ambiente e MCP de usuário para turns restritos.

[ALLOY]: Essa última parte é o limite de segurança. Em um agent host, turns restritos não devem simplesmente confiar no bom comportamento do modelo. O runtime deve remover superfícies que o sender não tem permissão de usar. Falhar closed significa que um usuário restrito não recebe código nativo, acesso a app local, acesso a ambiente ou superfícies MCP de usuário por acidente.

[NOVA]: O fix de hidratação de imagem também é importante. Um usuário enviando uma captura de tela através de um canal espera que o agente veja a captura de tela, não um placeholder ou um caminho de arquivo que o modelo não consegue inspecionar. Hidratar imagens antes de runs enfileiradas mantém o contexto multimodal anexado ao turn real.

[ALLOY]: E preservar acesso à rede sandboxed quando a política permite importa porque tarefas de código-modo frequentemente precisam de metadados de pacotes, docs, APIs ou testes que chamam recursos externos. O host não deve accidentalmente remover acesso à rede se o envelope de sandbox configurado permitir.

[NOVA]: As notas de migração são concretas. A linha mínima suportada do Node.js 22 sobe para 22.19. Pacotes Pi mudam para 0.75.1. Builds Docker e Podman devem preferir OPENCLAW_IMAGE_APT_PACKAGES, enquanto OPENCLAW_DOCKER_APT_PACKAGES permanece como fallback legado. A skill do Obsidian agora aponta para o obsidian CLI oficial ao invés do obsidian-cli de terceiros. A skill de revisão de closeout do Codex e o helper repo-local são renomeados para autoreview.

[ALLOY]: O caminho prático de upgrade é testar as superfícies reais que mudaram. Build e valide um pequeno plugin. Dispare um modal de browser e certifique-se de que o caminho do diálogo está visível. Reinicie o gateway e inspecione os traces de readiness. Exercite o caminho do proxy HTTPS se seu deployment usa trust privado. Tente o Talk Mode do Android com interrupção. Envie mídia através dos canais que você realmente usa. Rode turns do Codex app-server com imagens, rede sandboxed, código-modo e política restrita de sender.

[NOVA]: Um bom fluxo de trabalho para builders após este release é escolher uma tarefa real por superfície. Para plugins, construa uma pequena ferramenta que leia input, retorne output estruturado, e declare apenas o contexto que precisa. Para automação de browser, construa uma página de teste que abra um alert, um confirm, e um prompt, depois verifique se o agente consegue ver o estado de diálogo bloqueado e respondê-lo. Para mídia, envie uma imagem pequena, uma imagem malformada, e uma requisição de imagem gerada pelo caminho real do canal que você suporta.

[ALLOY]: Para readiness do gateway, o fluxo de trabalho deve incluir um restart sob carga normal, depois um restart com um sidecar ou serviço de plugin lento. O objetivo não é apenas um boot rápido. O objetivo é entender qual passo de probe, config, runtime ou recurso leva tempo. Se uma equipe faz ship do OpenClaw como infraestrutura interna, esse trace de restart se torna parte do fluxo de suporte quando alguém diz que o host do agente está lento após o deploy.

[NOVA]: Para o Talk Mode no Android, o fluxo de trabalho útil é um teste real de interrupção. Inicie uma sessão de voz, peça uma resposta com suporte de ferramenta, interrompa enquanto o áudio está tocando, depois faça uma pergunta de acompanhamento que depende do resultado da ferramenta anterior. Um bom resultado não é apenas que o speech funcione. Um bom resultado é que o cancelamento funcione, as transcrições permaneçam coerentes, e os resultados de ferramentas não cheguem como speech obsoleto depois que o usuário seguiu em frente.

[ALLOY]: Para política de remetente restrito, o fluxo de trabalho de build deve ser deliberadamente adversário. Tente um turno de um remetente restrito que peça código local, acesso a apps, acesso ao ambiente, e acesso MCP do usuário. O comportamento correto não é uma recusa educada do modelo. O comportamento correto é que essas superfícies de runtime estejam ausentes antes que o modelo possa alcançá-las.

[NOVA]: Essa é a leitura do OpenClaw: trabalho no host que torna plugins mais tipados, falhas de browser mais explícitas, startup mais observável, trust do proxy mais definido em escopo, QA mais consciente de runtime, voz mobile mais realtime, mídia mais segura, canais mais confiáveis, e integração do Codex mais consciente de política. ...

[ALLOY]: A segunda metade da leitura do release do agent-stack é Codex rust-v0.131.0. Se OpenClaw é a superfície do host, Codex é a superfície de coding: o TUI, o app server, o caminho de remote-control, o SDK, o sandbox, auth, state, e a bridge de ferramentas onde os desenvolvedores vivem.

[NOVA]: A primeira mudança visível é o status do TUI. O Codex agora expõe comandos de service-tier orientados por dados, uso de tokens misturado, permissões e modo de aprovação, workspace roots efetivos, e tabelas Markdown responsivas. Isso parece trabalho de display, mas muda como operadores gerenciam sessões longas.

[ALLOY]: Durante uma sessão de coding longa, você quer saber o envelope de permissão. O agente está em postura read-only, postura de escrita no workspace, ou algo mais permissivo? Qual modo de aprovação está realmente ativo? Quais workspace roots são efetivos? Qual service tier está em uso? Quanto do budget de tokens foi gasto? Se o TUI mostra esses fatos, o operador não precisa reconstruí-los a partir de config espalhada e memória.

[NOVA]: Isso importa porque os casos de falha são caros. Se um usuário pensa que o agente pode escrever em um diretório, mas o root efetivo é diferente, edits podem pousar no lugar errado ou falhar inesperadamente. Se o modo de aprovação for mal entendido, uma tarefa pode bloquear em prompts que o operador não esperava. Se o uso de tokens for invisível, uma sessão longa pode derivar para comportamento caro ou degradado sem aviso.

[ALLOY]: Menções ficam mais amplas também. A busca com @ agora cobre arquivos, diretórios, plugins e skills em um picker só, suportado por metadata de plugin do app-server. Isso corresponde a como builders pensam. A coisa que você precisa pode ser um arquivo fonte, uma pasta, uma skill local, ou uma capacidade de plugin. A interface não deveria forçar essas em quatro caminhos de descoberta separados.

[NOVA]: A cautela é disciplina de contexto. Um picker unificado é útil porque reduz fricção, mas a fricção às vezes estava protegendo a sessão de inchaço. O melhor uso é anexar o menor artefato que carrega o contexto necessário: um arquivo, um diretório, uma skill, ou uma referência de plugin, não uma pilha de tudo que parece adjacente.

[ALLOY]: Fluxos de trabalho de plugins avançam. O Codex adiciona comandos de CLI do marketplace, compartilhamento com versionamento, checkout de share, buckets de workspace compartilhado mais claros, e plugin hooks habilitados por padrão. Isso é uma mudança de plugins como pastas soltas locais para plugins como artefatos de desenvolvimento gerenciados.

[NOVA]: Compartilhamento com versionamento é uma grande mudança. Se dois usuários ou duas máquinas estão falando sobre o mesmo plugin, eles precisam saber se estão realmente usando a mesma versão. Checkout de share e buckets de workspace mais claros ajudam a tornar isso explícito. Hooks habilitados por padrão tornam a experiência mais suave, mas também elevam a barra de confiança.

[ALLOY]: Hooks são poderosos porque rodam em torno do processo de desenvolvimento. Isso significa que provenance, escopo, version gates e limites de workspace importam. Um marketplace de plugins não é apenas uma feature de conveniência. Ele se torna parte da supply chain para comportamento de agente.

[NOVA]: Trabalho remoto é uma das peças principais neste release do Codex. O release adiciona codex remote-control gerenciado por daemon, APIs de enable e disable de runtime, reads de status, ambientes remote configurados com suporte de registry, e contratos de API do app-server para ambientes remote e namespaces de config owned pelo desktop.

[ALLOY]: Remote control não é apenas rodar isso em algum outro lugar. Um ambiente remote real precisa de identidade, lifecycle, status, cleanup, limites de configuração, e comportamento de permissão. Se esses não forem explícitos, trabalho de agente remote se torna um processo shell com um rótulo mais bonito.

[NOVA]: A forma gerenciada por daemon importa porque trabalho de agente de longa duração precisa de um coordinator. O daemon pode expor status, gerenciar enablement de runtime, e manter estado de remote-control separado de uma sessão de terminal única. Essa é a diferença entre uma feature que funciona em demo e uma feature que sobrevive ao uso do dia a dia.

[ALLOY]: Ambientes remote configurados também importam para times e power users. Um ambiente remote não deveria ser um target improvisado toda vez. Ele deveria ser nomeado, discoverable, policy-aware, e recuperável. O contrato do app-server dá às integrações algo estruturado para chamar em vez de raspar output de terminal.

[NOVA]: O Python SDK agora é openai-codex e importa como openai_codex. Ele inclui tipos gerados em runtime com pin, roteamento de turns concorrentes, modos de aprovação, e cobertura de integração. Isso dá às aplicações Python um caminho real para dirigir turns do Codex sem tratar a CLI como um subprocesso só de texto.

[ALLOY]: Turn routing é o mecanismo chave. Se uma app dirige mais de um turn de agente, ela precisa de IDs e eventos estruturados. Caso contrário, aprovações, atividade de ferramentas, notificações e outputs podem se cruzar. Trabalho concorrente sem roteamento estruturado é onde bugs sutis se tornam terríveis: aprovação destinada a um turn fica associada a outro, ou um evento de ferramenta aparece sob a tarefa errada.

[NOVA]: Modos de aprovação também precisam ser explícitos em um SDK. Um app Python que embedding Codex precisa saber se um turn pode pedir permissão, se pode executar ferramentas, se pode escrever, e como essas aprovações são apresentadas ao aplicativo controlador. Isso não é um encanamento opcional. É o modelo de segurança.

[ALLOY]: O Codex também adiciona codex doctor para diagnósticos em runtime, auth, terminal, rede, config e estado local. É o tipo de comando que parece pequeno até o primeiro upgrade bagunçado.

[NOVA]: Um agente de codificação com falha pode falhar por auth desatualizado, peculiaridades do terminal, política de rede, conflitos de config, problema no banco de dados de estado local, incompatibilidade de runtime, comportamento de sandbox, ou inicialização do app-server. Sem diagnósticos, suporte vira um jogo de adivinhação. Um comando doctor pode coletar evidências prontas para suporte e encurtar o caminho de "quebrou" para "aqui está a camada quebrada".

[ALLOY]: O release também torna a inicialização do app-server e do estado local mais segura ao preservar dados SQLite, falhando fechado quando o estado não pode abrir, adicionando caminhos de recuperação, e suavizando falhas opcionais de sync de metadados. Essa combinação é boa engenharia. Preserve estado durável. Não prossiga sem segurança se o estado requerido não pode abrir. Recupere quando possível. Não deixe sync de metadados opcionais derrubar o caminho principal.

[NOVA]: O bloco de hardening é amplo. O comportamento de sandbox no Windows melhora em regras de deny-read, write roots com escopo, políticas de firewall ineficazes, e casos especiais de PowerShell. Restrições de leitura gerenciadas sobrevivem à escalada de permissões. A resolução de perfil de permissão do workspace-root é limpa.

[ALLOY]: A confiabilidade do Git e do auth melhora com root worktree hooks, ignorando repo hook e config de fsmonitor em comandos helper, vinculando callbacks OAuth MCP locais, e revogando tokens de login substituídos. Remote e Windows cleanup ganham timeouts de transporte mais longos no exec-server, taskkill mais silencioso, e leituras de plugin não enfileiradas.

[NOVA]: O padrão é recoverability. Um agente de codificação só é útil se pode funcionar dentro de repositórios reais, fluxos de auth reais, shells Windows reais, políticas de sandbox reais, e estado de app-server real. Esses ambientes são bagunçados. O release é menos sobre uma capacidade chamativa e mais sobre tornar sessões longas observáveis, recuperáveis e mais seguras.

[ALLOY]: O conselho de migração para o Codex é simples: após atualizar, exercite a status line do TUI, comandos de service-tier, menções unificadas, marketplace de plugins e comandos de share, fluxos de remote-control, ambientes remote configurados, roteamento de turn do Python SDK, codex doctor, casos de sandbox do Windows se relevantes, e recuperação de estado do app-server.

[NOVA]: Também teste visibilidade de permissões. Inicie uma sessão com o modo de aprovação e workspace roots que você espera, depois verifique se o TUI mostra a mesma realidade. Use menções com arroba com um arquivo, um diretório, uma skill e um plugin para garantir que o picker seja útil sem sobrecarregar o turn. Para ambientes remote, verifique leituras de status e cleanup, não só start.

[ALLOY]: Para builders de SDK, teste turns concorrentes deliberadamente. Rode dois jobs pequenos,触发 approval ou atividade de ferramenta em ambos, e certifique-se de que notificações pousem sob os IDs corretos. É aí que um SDK estruturado ganha confiança.

[NOVA]: Também existe um workflow limpo de build para o picker de menções unificadas. Comece com uma menção de arquivo estreita quando a tarefa é local. Mova para uma menção de diretório só quando o agente precisa de testes vizinhos ou módulos relacionados. Use uma menção de skill quando o contexto importante é um procedimento, não código fonte. Use uma menção de plugin quando a tarefa depende de uma capability. Esse workflow mantém a sessão focada enquanto ainda torna o novo picker valioso.

[ALLOY]: Para compartilhamento de plugins, o workflow deve incluir checagens de versão. Compartilhe um plugin, check-out em um segundo workspace, verifique a versão que carregou, depois exercite qualquer hook habilitado por padrão em um repositório pequeno antes de confiar neles em um maior. Compartilhamento suave de plugins é útil, mas não deve tornar o comportamento de hooks invisível.

[NOVA]: Para trabalho de remote-control, construa um teste de lifecycle. Inicie uma sessão, habilite remote control, leia status, envie uma correção pequena de uma segunda superfície, responda a um pedido de permissão, desabilite remote control, e confirme cleanup. Esse é o tipo de workflow que captura estado incompatível. Se start funciona mas status está errado, a feature será difícil de operar. Se disable funciona mas cleanup deixa estado stale, a próxima sessão pode herdar confusão.

[NOVA]: Então o readout do Codex é: estado operacional mais claro no TUI, anexação de contexto mais ampla através de menções unificadas, compartilhamento de plugins gerenciado, remote control com daemon, ambientes remote configurados, um Python SDK com roteamento de turn estruturado, diagnósticos, e uma longa lista de reparos em sandbox, auth, Git, Windows, app-server e estado.

[ALLOY]: Emparelhado com o OpenClaw, aponta na mesma direção. Ferramentas de agente estão se tornando menos mágicas e mais inspectable. O host pode explicar o que pode renderizar e qual dialog o bloqueou. O CLI pode explicar qual modo de permissão e workspace roots estão ativos. O SDK pode rotear turns concorrentes por ID. É assim que o trabalho de agente fica mais fácil de operar. ...

[NOVA]: O GitHub transforma agentes Copilot em uma fila de trabalho multi-superfície e de menor custo com três atualizações em 18 de maio: remote control para sessões Copilot CLI está geralmente disponível em mobile, web, VS Code e JetBrains; tarefas de agente cloud do Copilot podem usar modelos mais baratos para trabalho mais simples; e GitHub Actions falhando podem passar trabalho de reparo para o Copilot da página de logs de workflow.

[ALLOY]: A mecânica de remote-control é explícita. Um usuário pode começar com copilot remote, habilitar remote control dentro de uma sessão com remote on, ou configurar remoteSessions no arquivo de configurações do Copilot. Uma vez anexado, a superfície remote pode streamar atividade da sessão, aceitar input enfileirado, responder pedidos de permissão, parar uma sessão, e deixar o usuário conduzir o trabalho para fora do terminal original.

[NOVA]: Isso muda o formato do trabalho CLI-agente. O terminal local permanece a âncora de execução, mas a supervisão pode se mover. Um builder pode iniciar uma tarefa na mesa, depois verificar progresso do mobile ou de um browser, responder a um pedido de permissão, enfileirar uma correção, ou parar a sessão sem estar no mesmo editor.

[ALLOY]: As restrições importam. A máquina executando a sessão ainda precisa ficar online, e os docs do GitHub chamam atenção para keep-alive em trabalho mais longo. As sessões são específicas por usuário. Uso Business e Enterprise pode depender de políticas de admin para remote control e features de CLI. Então isso não é compute em nuvem desconectado. É uma sessão ao vivo com um plano de controle remoto.

[NOVA]: Essa distinção é importante. Remote steering é útil porque preserva o contexto local e permite que a supervisão se mova. Mas também significa que o ambiente local, estado de branch, credenciais, rede e sessão do terminal ainda importam. Se o laptop dormir, a sessão não está mágicamente rodando em algum outro lugar.

[ALLOY]: A segunda atualização do GitHub é a seleção de modelos mais baratos para tarefas de agente de nuvem do Copilot. Claude Haiku 4.5 e GPT-5.4-mini estão disponíveis com um multiplicador de 0,33x para trabalhos mais simples. Essa é a direção certa do produto, pois nem todas as tarefas de agente são igualmente difíceis.

[NOVA]: Uma pequena atualização de dependência, correção de lint, correção de digitação, refatoração mecânica, atualização de expectativa de teste ou um teste falho simples nem sempre precisa do modelo mais forte. Um modelo mais barato pode lidar com a tarefa, preservando o orçamento para os trabalhos que exigem raciocínio mais profundo: bugs ambíguos, mudanças de arquitetura, patches sensíveis à segurança ou mudanças de comportamento em vários arquivos.

[ALLOY]: Os pontos de entrada também importam aqui. O GitHub diz que a seleção de modelos está disponível em fluxos suportados, como atribuir um problema, mencionar o Copilot em um comentário de pull request, iniciar a partir de interfaces de agente, GitHub Mobile ou Raycast. Onde não há seletor, o "Auto" é usado.

[NOVA]: Isso significa que os desenvolvedores devem tratar a escolha do modelo como parte da triagem de tarefas. Se o ponto de entrada expõe um seletor, escolha deliberadamente. Se a tarefa for mecânica, use o modelo menor. Se for pesado em design ou arriscado, pague pelo caminho mais forte. Se não houver seletor e o "Auto" for usado, revise o resultado com essa incerteza em mente.

[ALLOY]: A terceira mudança é o reparo com um clique para falhas do GitHub Actions. A partir de uma página de logs de execução de fluxo de trabalho, os assinantes do Copilot Business e Enterprise podem clicar em "Fix with Copilot" (Corrigir com o Copilot). O agente de nuvem investiga a falha, envia uma correção para o branch e marca o usuário para revisão.

[NOVA]: Esse é um forte ponto de entrada de agente porque o pacote de contexto é robusto: logs de trabalho com falha, estado do branch, instruções do repositório e um ambiente de desenvolvimento em nuvem. Em vez de copiar logs para o chat, o usuário delega do local onde a falha já está visível.

[ALLOY]: Mas a disciplina de revisão não desaparece. Uma correção de branch enviada por um agente ainda é uma mudança de código. O revisor deve verificar se o agente corrigiu a causa real, preservou o design, evitou hacks amplos e não otimizou simplesmente para um CI verde.

[NOVA]: Isso é especialmente verdade com falhas do Actions. A correção mais fácil pode ser afrouxar um teste, pular um caso, fixar uma dependência antiga ou alterar a configuração do CI de uma forma que oculte um bug. A correção certa pode ser mais profunda. O agente pode rascunhar, mas a revisão humana ainda detém o julgamento de engenharia.

[ALLOY]: A direção maior do produto é clara. O GitHub está transformando os agentes Copilot em uma fila de trabalho que abrange várias interfaces. As sessões CLI locais podem ser controladas remotamente. As tarefas em nuvem podem usar modelos menores quando o trabalho é simples. As falhas de CI podem se tornar trabalhos de reparo delegados a partir da página de logs.

[NOVA]: Para as equipes, a camada de política importa. Controle remoto, agentes de nuvem, seleção de modelo e reparo do Actions, tudo isso precisa de configurações de administrador, instruções de repositório e normas de revisão. Sem isso, é fácil criar uma fila de agentes que é conveniente, mas inconsistente.

[ALLOY]: O padrão de construção útil é classificar as tarefas antes de atribuí-las. A manutenção simples de branches pode ir para um modelo de nuvem mais barato. O reparo de falhas de CI pode começar a partir dos logs do fluxo de trabalho. O trabalho que depende do estado local de um desenvolvedor pode permanecer na CLI, mas ser supervisionado remotamente. O trabalho de design arriscado ainda precisa de modelos mais fortes e uma revisão mais atenta.

[NOVA]: E a interface de supervisão deve corresponder ao trabalho. Se o agente está pedindo permissões, a aprovação móvel pode ser suficiente para uma operação simples e conhecida. Se a mudança for ampla, uma revisão no desktop é melhor. O objetivo não é tornar toda tarefa de agente remota. É permitir que o plano de controle se mova quando isso realmente ajuda.

[ALLOY]: Um fluxo de trabalho de equipe útil é rotear por custo e risco. Use os modelos de agente de nuvem menores para correções estreitas com testes claros. Use modelos mais fortes quando o problema tiver comportamento ambíguo, implicações de segurança ou amplo impacto no design. Use o controle remoto da CLI quando a tarefa precisar de estado local, mas o humano não puder ficar no terminal. Use o reparo do Actions quando o contexto da falha já estiver concentrado nos logs do CI.

[NOVA]: O fluxo de trabalho de revisão deve ser igualmente explícito. Para uma mudança de modelo barato, verifique se o agente permaneceu dentro da tarefa estreita. Para uma mudança remota da CLI, verifique o diff local e o histórico de comandos. Para um reparo do Actions, verifique se o agente alterou o código do produto, testes, dependências ou configuração do CI. O fato de o agente ter vindo de um ponto de entrada conveniente não altera o padrão de revisão.

[ALLOY]: É por isso que essas atualizações do GitHub se encaixam no bloco de lançamento. Elas não são apenas anúncios de recursos. Elas fazem parte da mesma mudança operacional: os agentes precisam de controle de ciclo de vida, portões de política, níveis de custo e melhores pontos de entrada dos locais onde o trabalho já acontece. ...

[NOVA]: A Anthropic fornece à pesquisa web do Claude dados mais ricos de registros da SEC para agentes financeiros citados. A nota de 18 de maio da Plataforma Claude é específica, mas importa para qualquer agente que resume ganhos, compara empresas públicas, elabora notas de due diligence ou monitora divulgações de risco.

[ALLOY]: A diferença entre um resultado de web genérico e uma pesquisa ciente de registros é a qualidade da fonte. Agentes de pesquisa financeira precisam saber se estão olhando para um 10-K, 10-Q, 8-K, declaração de procuração, declaração de registro ou outro registro primário. Eles também precisam de metadados suficientes para manter essa citação anexada depois que o modelo resume a afirmação.

[NOVA]: O modo de falha é familiar. Um modelo pesquisa na web, encontra uma afirmação financeira, a resume e perde a fronteira entre registros primários, comunicados de imprensa, comentários de analistas e artigos de notícias. A resposta final pode parecer confiante, mas a cadeia de evidências é fraca.

[ALLOY]: Dados mais ricos de registros da SEC ajudam a camada de ferramenta a levar melhores evidências para o contexto do modelo. Isso dá ao aplicativo uma chance melhor de preservar a identidade do registro, tipo de registro, data, empresa, URL da fonte, texto citado e metadados de recuperação. Mas o aplicativo tem que manter essa informação. Se ele colapsar tudo em prosa, o benefício desaparece.

[NOVA]: A recomendação prática é tratar os resultados da pesquisa como objetos de evidência. Mantenha o URL, título, tipo de registro, data, texto da citação, identidade da empresa e timestamp de recuperação. Se o agente escrever um memorando, cada afirmação material deve apontar de volta para o registro e, quando disponível, para a seção ou trecho. Se o agente escrever notas estruturadas, a fonte do registro deve ser um campo, não uma frase enterrada no meio.

[ALLOY]: Isso também muda a avaliação. Um agente de pesquisa financeira não deve ser avaliado apenas se o resumo parece plausível. Deve ser avaliado se as afirmações são rastreáveis para fontes primárias, se comentários secundários são separados dos arquivos, se datas são preservadas, e se evidências conflitantes são sinalizadas ao invés de serem suavizadas.

[NOVA]: Arquivos da SEC são artefatos legais e financeiros estruturados. Um fator de risco de 10-K não é o mesmo que uma atualização operacional trimestral. Um 8-K pode anunciar um evento específico. Um formulário de procuração pode explicar governança e remuneração. Se um agente simplifica isso para "a empresa disse", ele perde o contexto que torna a afirmação útil.

[ALLOY]: Para fluxos de trabalho de construção, o padrão de design é direto. A camada de recuperação retorna evidências. A camada de raciocínio pode resumir e comparar. A camada de relatório deve preservar citações. A camada de armazenamento deve manter metadados suficientes para que uma auditoria posterior possa reconstruir de onde veio uma afirmação.

[NOVA]: Isso é especialmente importante para planilhas downstream, notas de investimento, revisões de conformidade e pesquisas voltadas para clientes. Um resumo bonito com citações fracas é um passivo. Um resumo mais estruturado com campos de origem claros é mais fácil de confiar, mais fácil de revisar e mais fácil de corrigir.

[ALLOY]: O fluxo de trabalho de construção concreto é manter objetos de evidências vivos. Quando a busca na web do Claude retorna um resultado de arquivo, armazene o tipo de arquivo, empresa, data, URL, texto citado e horário de recuperação ao lado da afirmação. Quando o agente redigir uma comparação, carregue esses campos para a tabela de comparação ou memorando. Quando o agente exportar um relatório, inclua detalhes de citação suficientes para que um revisor possa abrir a fonte e verificar a afirmação sem reexecutar toda a busca.

[NOVA]: Para agentes financeiros, isso também sugere um fluxo de trabalho de falha melhor. Se uma afirmação não tiver fonte de arquivo primária, rotule-a como comentário secundário. Se dois arquivos parecerem conflitar, mantenha ambas as citações e peça revisão ao invés de suavizar a diferença. Se o tipo de arquivo for unclear, não deixe o modelo adivinhar. O agente deve preservar a incerteza como estado, porque a incerteza é frequentemente a coisa mais importante que o usuário precisa ver.

[ALLOY]: O mesmo padrão se aplica fora das finanças, mas finanças tornam as stakes óbvias. O ancoramento em fontes primárias não é um nice-to-have quando uma afirmação pode afetar uma decisão. Dados mais ricos de arquivos da SEC dão aos desenvolvedores um melhor resultado de ferramenta; o aplicativo ainda precisa preservar o limite de ancoramento até o usuário.

[NOVA]: Então a atualização da Anthropic é pequena em área de superfície e grande em implicação. Melhores metadados de busca tornam agentes financeiros mais auditáveis, mas apenas se os construtores mantiverem citações vivas através de todo o pipeline. ...

[ALLOY]: A prioridade de atualização para OpenClaw é testar as superfícies de host alteradas, não apenas instalar o release. Validar plugin init, build e validação. Disparar manipulação de modal do navegador. Inspecionar prontidão de reinicialização do gateway. Exercitar confiança de proxy HTTPS se necessário. Experimentar Talk Mode do Android com interrupção. Enviar mídia através de tópicos do Telegram e voz do Discord. Testar manipulação de imagem e turns do app-server do Codex com imagens, rede sandbox, modo de código e política de remetente restrita.

[NOVA]: Para Codex, atualize e inspecione o estado operacional. Verifique a linha de status do TUI, comandos de service-tier, permissões, modo de aprovação, raízes de workspace, menções unificadas, comandos de marketplace e compartilhamento, fluxos de controle remoto, ambientes remotos configurados, roteamento de turn do Python SDK, codex doctor, casos de sandbox do Windows se relevante, e recuperação de estado do app-server.

[ALLOY]: Para Copilot, use modelos de cloud-agent mais baratos para trabalho de reparo simples, mantenha sessões remotas com gating de política e revise correções de Actions de um clique como mudanças de código ao invés de respostas finais. Para agentes financeiros do Claude, preserve metadados de arquivos da SEC e citações como evidência estruturada, não apenas texto.

[NOVA]: O fio condutor dessas atualizações é maturidade operacional. Hosts estão tornando contratos de ferramentas e canais mais claros. CLIs estão expondo estado e permissões. Agentes remotos estão obtendo melhores planos de controle. Ferramentas de busca estão retornando evidências mais ricas. Esse é o trabalho que facilita o envio, debug e confiança em agentes.

[ALLOY]: Links de fontes e notas do episódio estão disponíveis em Toby On Fitness Tech ponto com.

[NOVA]: Isso é o AgentStack Daily. Eu sou a NOVA.

[ALLOY]: E eu sou o ALLOY. Estaremos de volta em breve.