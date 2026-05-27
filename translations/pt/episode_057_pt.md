[NOVA]: Eu sou o NOVA.

[ALLOY]: Eu sou o ALLOY, e este é o AgentStack Daily. Hoje começamos com o OpenClaw v2026.5.22 e o Claude Code 2.1.149, porque ambos os lançamentos mudaram a estrutura da qual as agent stacks dependem: inicialização do gateway, metadados de plugins, notas de reunião, callbacks do Discord, conectores MCP em nuvem, accounting de uso, diffs e segurança de shell.

[NOVA]: Depois as notícias se expandem. O Google está transformando agentes Gemini em ambientes Linux remotos gerenciados. A OpenAI está colocando o trabalho do Codex sob supervisão mobile e em configurações empresariais híbridas. A Anthropic comprou a Stainless e atualizou o Project Glasswing, que coloca geração de SDK, servidores MCP e varredura de segurança de IA na mesma conversa.

[ALLOY]: E a faixa de projetos do GitHub está realmente acontecendo hoje: mapas semânticos de código, ferramentas de documentação atualizadas, roteadores de modelo, construtores de MCP, agentes locais, pacotes de papéis e scanners de segurança. Não é trivial de repositório. Ferramentas que podem mudar o que o Claude Code, Codex, Hermes, OpenClaw e clientes MCP realmente podem ver e fazer. ...

[NOVA]: O OpenClaw v2026.5.22 é um lançamento denso, mas o título é limpo: o gateway fica menos frágil, a superfície de plugins fica mais reutilizável, notas de reunião se tornam uma melhor fonte de contexto para agentes, e vários caminhos de provedores e mídia ficam mais nítidos.

[ALLOY]: Comece pela inicialização do gateway. O OpenClaw agora usa leituras de catálogo de canais estáveis por processo e reutilização de snapshot de metadados de plugins. Isso significa que o sistema pode contar com estado estável de catálogo e metadados em vez de reconstruir repetidamente a mesma visão do mundo. Para um host de agente local, isso importa porque inicialização e verificações de status são o primeiro ponto de atrito. Se o host estiver ruidoso antes da tarefa começar, tudo acima dele parece não confiável.

[NOVA]: Trabalho preguiçoso de plugins em idle-inicialização entra no mesmo balde. Trabalho que não precisa bloquear o primeiro momento utilizável pode esperar. Probes de caminho Linuxbrew irrelevantes são pulados. Handlers de método principais do gateway e mapas de alias de superfície pública são limpos. Essas não são funcionalidades chamativas, mas mudam a sensação do plano de controle: menos verificações sem propósito, nomes de método mais previsíveis, e menos trabalho acontecendo só porque o processo acordou.

[ALLOY]: Notas de reunião recebem uma das atualizações de capacidade mais importantes. Plugins externos de notas de reunião e provedores de origem agora têm um contrato mais limpo. A captura pode iniciar automaticamente a partir da configuração. Importações manuais são suportadas. Existe acesso CLI somente leitura. Discord voice é tratado como uma primeira fonte ao vivo em vez de uma entrada lateral.

[NOVA]: Isso é uma característica real de agent-stack porque muita instrução valiosa não chega como texto digitado organizado. Ela chega como uma ligação, uma nota de voz, uma correção rápida, ou uma discussão em canal. Transformar essas fontes em contexto estruturado e legível sem dar a cada ferramenta acesso de escrita ao registro de origem é a parte útil.

[ALLOY]: O SDK de plugins também ganha mais operações ordinárias integradas: envio de pesquisa de mensagens de canal genérico, ajudantes de fluxo de trabalho de sessão, e contratos de capacidade de provedor de embedding mais claros. Isso parece encanamento, mas é o tipo de encanamento que impede cada autor de plugin de inventar uma versão ligeiramente diferente da mesma chamada de ferramenta.

[NOVA]: Subagentes também ficam menos desperdiçadores. O bootstrap padrão é aparado em direção aos arquivos que mais importam, e transferências de conclusão de subagente nativo recebem correções. Na prática, um agente delegado precisa de contexto suficiente para fazer a tarefa e um caminho confiável para devolver a resposta. Contexto herdado demais torna o subagente lento; uma transferência quebrada faz bom trabalho desaparecer no lugar errado.

[ALLOY]: O seletor de sessão de chat ganha busca e paginação de Carregar Mais. Essa é uma pequena funcionalidade de UI até o sistema ter semanas de sessões reais. Então encontrar uma execução antiga se torna parte do trabalho. Um gateway com histórico precisa de navegação, não apenas de uma pilha de chats recentes.

[NOVA]: Callbacks de componentes do Discord agora têm vida útil limitada. Essa é uma mudança saudável para botões de revisão, aprovações e pequenos controles interativos. Um botão em uma mensagem antiga não deveria permanecer ativo para sempre só porque a mensagem ainda existe. A superfície de interação agora tem um modelo de expiração mais claro.

[ALLOY]: O tratamento de provedores também fica mais concreto. OAuth do xAI pode ser reutilizado para busca web do Grok. Aliases de modelo e timeouts de operação recebem limpeza. CLI do Antigravity se torna fallback de imagem e vídeo de menor prioridade após APIs de provedores configurados. Geração de imagem com chave de API do Codex usa a API nativa de Imagens da OpenAI. Correções em bypasses de proxy local do Chrome e local do Ollama.

[NOVA]: Essa é a história real dos provedores: não apenas qual modelo responde, mas como a autenticação é reutilizada, quanto tempo as chamadas podem executar, qual fallback vence, e se serviços locais estão sendo roteados acidentalmente pelo proxy errado. Agent stacks falham nessas bordas tão frequentemente quanto falham no raciocínio.

[ALLOY]: O OpenClaw também atualiza dependências, move o protobufjs para 8.4.0, aperta o trabalho de dependências bloqueadas, poda catálogos, limpa locks de escrita de sessão, adiciona comportamento mais estrito para turns tool-free do vLLM, e corrige tratamento de tópicos do Telegram. Esta é uma versão de manutenção com uma longa cauda, mas a forma é coerente: inicialização, captura de fonte, reutilização de plugins, correção de provedores, navegação de sessão e higiene de dependências.

[NOVA]: A atualização do Claude Code é menor, mas cai no uso diário. O comando /usage pode decompor o uso de limites por categoria: skills, subagentes, plugins e custo por servidor MCP. Essa é uma mudança significativa porque sessões de agente de codificação não são mais uma única chamada de modelo. São chamadas de ferramenta, chamadas MCP, agentes auxiliares, skills, plugins e às vezes trabalho em segundo plano. Uso precisa de um mapa.

[ALLOY]: A visualização de detalhe do /diff ganha rolagem por teclado. A saída Markdown renderiza checkboxes de lista de tarefas no estilo GitHub. Essas são correções ergonômicas, mas agentes de terminal vivem e morrem nas superfícies de revisão. Uma visualização de diff melhor e listas de tarefas mais claras significam menos atrito quando um humano está decidindo se o agente realmente fez a coisa.

[NOVA]: Administradores empresariais ganham allowAllClaudeAiMcps, uma configuração gerenciada para carregar conectores MCP em nuvem do claude.ai junto com configuração MCP gerenciada. Esse é o lado de política da história do MCP. Conectores em nuvem são úteis, mas organizações precisam de um switch claro para quais superfícies de conector são permitidas em vez de deixar cada usuário improvisar.

[ALLOY]: As correções são a parte mais séria. O Claude Code repara bypasses de permissão do PowerShell através de funções integradas de mudança de diretório. Corrige allowlists de escrita de sandbox que podiam cobrir demais da worktree do git. Corrige bugs de regra de prefixo e curinga do PowerShell. Corrige rastreamento de variáveis obsoletas ao redor de PWD, OLDPWD e DIRSTACK. Corrige um problema de find no macOS que podia esgotar tabelas de arquivos em diretórios grandes.

[NOVA]: Isso é uma nota de release sobre segurança de shell, não apenas uma lista de bugs. Agentes de codificação executam comandos em ambientes bagunçados. Builtins que mudam diretórios, regras de wildcards, worktrees, variáveis de ambiente e limites de file-descriptors são exatamente onde uma política que parece segura pode vazar. Um agente CLI que leva permissões a sério tem que lidar com essas bordas chatas.

[ALLOY]: O próximo patch está no npm latest, mas sua entrada no changelog é apenas infraestrutura interna. Então o delta visível para o usuário é o patch anterior que acabamos de cobrir. Essa distinção importa: números de instalação podem mudar, enquanto a história das funcionalidades pertence ao release que realmente mudou o comportamento.

[NOVA]: O Codex e o Hermes não têm tags stable mais recentes para esta leitura de release, mas continuam no episódio porque as notícias sobre supervisão remota do Codex, ferramentas MCP, agentes locais e repos de inteligência de código afetam o mesmo stack. O segmento de releases é a fundação; o resto do episódio é onde o ambiente ao redor dessa fundação está se movendo. ...

[ALLOY]: O caso de uso mais forte para este release do OpenClaw é um gateway que precisa hospedar várias surfaces reais ao mesmo tempo: chat, voz, plugins, geração de mídia, busca e subagentes. Um setup de Brinquedo pode sobreviver a comportamentos estranhos de inicialização. Um build diário não pode. Quando catálogos de canais, metadados de plugins, captura de fonte e fallbacks de provedores ficam mais limpos no mesmo release, o host de agentes deixa de ser um amontoado de caminhos sortudos.

[NOVA]: O caso de uso mais forte para a atualização do Claude Code é uma equipe que já passou de um terminal e uma chamada de modelo. Uso por categoria mostra se skills, plugins, subagentes ou servidores MCP estão impulsionando os limites. Navegação de diff melhorada torna revisão de código menos dolorosa. Política MCP de nuvem dá aos administradores uma superfície de build mais clara. As correções de PowerShell e sandbox são os guardrails que tornam essas funcionalidades menos assustadoras em shells reais.

[ALLOY]: Juntando tudo, as notícias de release não são apenas "atualize suas ferramentas." É que o gateway local e o CLI de codificação estão ambos absorvendo as lições difíceis do trabalho com agentes: contexto vem de fontes bagunçadas, ferramentas precisam de política, comportamento de provedores precisa de nomes, e limites de shell precisam ser precisos. Essa é a direção de build para observar.

[ALLOY]: A história do Gemini do Google tem duas camadas. A primeira é o modelo: o Gemini 3.5 Flash está posicionado para trabalho agentic e codificação, com afirmações sobre Terminal-Bench, GDPval-AA, MCP Atlas, velocidade multimodal e tarefas de longo horizonte.

[NOVA]: Esses nomes de benchmarks importam porque apontam para trabalho pesado em ferramentas. Um modelo pode ser charmoso no chat e ainda assim desmoronar quando precisa usar um terminal, chamar ferramentas, inspecionar arquivos, se recuperar de observações ruins e manter estado através de uma tarefa longa. O Google está explicitamente tentando vender o Flash como rápido o suficiente para loops e capaz o suficiente para trabalho agentic.

[ALLOY]: A segunda camada é mais importante: Gemini API Managed Agents. Desenvolvedores podem iniciar um agente alimentado pelo Antigravity dentro de um ambiente Linux isolado e efêmero. O agente pode raciocinar, chamar ferramentas, executar código, gerenciar arquivos e navegar na web. Chamadas de acompanhamento podem reutilizar o ambiente, então uma tarefa pode continuar com estado de sessão real em vez de fingir que cada requisição começa do nada.

[NOVA]: Esse modelo de ambiente é o produto. Não é apenas "envie um prompt para um modelo." É um workspace Linux remoto com ferramentas, arquivos, navegação, continuação e instruções de agente. O Google também diz que agentes customizados podem ser definidos com arquivos estilo AGENTS.md e SKILL.md, mais dados extras. Esse é um sinal claro de que o harness ao redor do modelo está se tornando uma superfície de API de primeira classe.

[ALLOY]: Para usuários do OpenClaw, Hermes, Codex e Claude Code, a comparação interessante não é local versus cloud como slogan. É o que o ambiente tem permissão de saber e fazer. Um sandbox gerenciado é útil quando a tarefa é pública, descartável ou fácil de resetar: inspecionar um repo open-source, rodar uma reprodução limpa, navegar em docs, transformar um dataset não sensível, ou fazer um protótipo em um workspace controlado.

[NOVA]: Agentes locais ainda têm a vantagem quando o trabalho depende de arquivos privados, credenciais locais, ferramentas assinadas, um perfil de navegador real, acesso a dispositivo ou configuração específica de máquina. As notícias de managed agents não apagam o stack local. Dão aos construtores mais uma forma de execução: estado remoto descartável em vez de estado de workstation pessoal.

[ALLOY]: O delta de funcionalidade para lembrar é execução gerenciada stateful. Um agente remoto que pode manter arquivos, continuar uma sessão e navegar dentro de um ambiente Linux isolado é diferente de um endpoint de modelo stateless. Pode acumular evidências. Pode instalar dependências. Pode deixar artefatos para a próxima chamada. Pode também criar lock-in ao redor do sandbox e modelo de ferramentas da plataforma.

[NOVA]: É por isso que o suporte a arquivos de instrução customizados importa. Arquivos estilo AGENTS.md e SKILL.md permitem que o ambiente carregue regras de projeto e comportamento especializado. A mesma tendência aparece em agentes de codificação: o modelo é apenas uma parte. As regras, ferramentas, filesystem, navegador, política e modelo de continuação decidem se o agente pode trabalhar como software ou apenas falar sobre software.

[ALLOY]: A recomendação prática é curta: use agentes Gemini gerenciados primeiro onde o ponto é o isolamento. Triagem de repos públicos, reprodução limpa de bugs, scripts gerados e pesquisa respaldada por docs são encaixes naturais. Mantenha segredos, repos privados e workflows específicos de máquina em ambientes locais ou rigorosamente controlados até que o limite gerenciado seja claramente entendido.

[NOVA]: O sinal maior da indústria é que infraestrutura de agentes está agora sendo vendida diretamente. Não escondida como orquestração interna, não dependurada como um demo. O sandbox, executor de ferramentas, camada de navegação, store de sessão e arquivos de agente customizados são parte do produto para desenvolvedores. ...

[ALLOY]: Um caso de uso se destaca imediatamente: investigação reproduzível. Um agente gerenciado pode começar de um ambiente Linux limpo, buscar uma issue pública, construir a reprodução e deixar um rastro stateful para uma chamada de acompanhamento. Isso é diferente de perguntar a um chatbot o que pode estar errado. O ambiente pode conter o checkout real, logs, artefatos gerados e comandos que os produziram.

[NOVA]: Outro caso de uso é automação descartável em torno de dados públicos. Um agente gerenciado pode navegar, executar código e manter estado de sessão sem tocar em um laptop pessoal. Isso é útil para tarefas de pesquisa, exemplos gerados, verificações de benchmarks públicos e transforms de dados pequenos. Não é o lugar certo para todo build privado, mas é exatamente o formato certo para trabalho onde isolamento limpo é uma vantagem.

[ALLOY]: A implicação de build é que arquivos estilo AGENTS.md e SKILL.md estão se tornando packaging de agente portátil. Um projeto pode carregar suas próprias regras, preferências de ferramentas e convenções para um ambiente de agente remoto. Isso torna a camada de instrução mais durável que um prompt único e mais inspecionável que um preset de produto invisível.

[ALLOY]: As notícias do Codex da OpenAI são sobre onde o trabalho de agentes de codificação vive e como humanos supervisionam. O Codex no app móvel do ChatGPT pode conectar a trabalho ativo rodando em um Mac ou ambiente remoto. A visualização mobile pode mostrar estado do projeto em tempo real, saída do terminal, screenshots, resultados de testes e diffs. O usuário pode aprovar comandos e redirecionar a tarefa.

[NOVA]: Isso muda a forma do trabalho de codificação de longa duração. O agente pode continuar executando próximo ao workspace, enquanto a superfície de aprovação passa para o humano. Uma sessão não precisa ficar travada só porque a pessoa saiu da mesa. O importante não é a novidade móvel. É separar o local de execução do local de supervisão.

[ALLOY]: Estado de relay seguro é a arquitetura para ficar de olho. O código, credenciais, dependências e ferramentas ficam onde o agente realmente está executando. O humano recebe estado ao vivo suficiente para tomar decisões em outro lugar. Esse é um padrão melhor do que arrastar todo segredo local para uma superfície de chat remoto.

[NOVA]: O SSH remoto ficando disponíveis geralmente segue a mesma direção. O Codex pode trabalhar contra um host remoto onde o repo e as dependências já estão. Isso pode ser uma máquina de desenvolvimento, uma VM na nuvem, uma workstation ou um ambiente empresarial gerenciado. O limite de execução se torna uma escolha de deploy, não um efeito colateral de onde a janela de chat está aberta.

[ALLOY]: Tokens de acesso programáticos são outra peça importante. Agentes de codificação que executam em automação precisam de identidade com escopo. Uma sessão de navegador ou um segredo pessoal de longa duração é uma base precária para trabalho não interativo. Tokens dão aos fluxos de trabalho de agentes uma forma mais restrita e revogável de agir dentro de um workspace.

[NOVA]: Hooks adicionam política em torno dessa ação. Eles podem escanear prompts em busca de segredos, executar validadores, bloquear operações arriscadas ou impor regras locais antes que o trabalho siga em frente. É aqui que o Codex começa a parecer menos um ajudante de terminal esperto e mais um sistema de trabalho de agentes com pontos de verificação.

[ALLOY]: A parceria com a Dell aponta para a versão enterprise: Codex em ambientes híbridos e on-prem. Algumas organizações não podem mover casualmente código-fonte, logs ou dados para um loop de codificação em nuvem público. O Codex híbrido é sobre deixar o agente operar mais perto de limites aprovados de computação, armazenamento e política.

[NOVA]: A mudança de capacidade concreta do Codex é esta: supervisão móvel, hosts remotos, tokens com escopo, hooks e ambientes híbridos apontam todos para agentes de codificação que podem executar perto dos dados enquanto são supervisionados de outro lugar. Essa é a enquadramento útil. Não é "agente no meu laptop" versus "agente na nuvem", mas "onde essa tarefa deveria executar, e onde o humano deveria aprovar?"

[ALLOY]: Há também uma mudança de fatores humanos. Diffs, capturas de tela, saída do terminal e resultados de testes estão se tornando objetos de revisão que trafegam. Se esses objetos forem claros, a supervisão remota parece controle. Se forem vagos, a supervisão móvel se torna uma janelinha para olhar dentro de uma caixa preta.

[NOVA]: Então a recomendação não é jogar refatorações grandes no celular. Use supervisão móvel do Codex para pontos de decisão estreitos: approve um comando seguro, inspecione um resumo de diff, redirecione uma escolha de branch, pare uma tarefa que seguiu pelo caminho errado. As evidências pesadas ainda precisam ser boas o suficiente para confiar.

[ALLOY]: A recomendação empresarial é similar. Use tokens e hooks para as automações que precisam de identidade não interativa. Mantenha o ambiente de execução próximo ao repo, segredos e política de que precisa. O Codex está indo em direção a um mundo onde o trabalho de agentes pode ser remoto, supervisionado e governado sem fingir que localização não importa mais. ...

[NOVA]: O caso de uso imediato é revisão remota de uma sessão de codificação de longa duração. O agente já criou uma branch, rodou testes e preparou um diff. O humano está fora da mesa, mas ainda pode ver evidências suficientes para aprovar um comando, rejeitar uma direção arriscada ou parar a sessão. Isso transforma tempo de espera parado em um ponto de verificação supervisionado.

[ALLOY]: O caso de uso empresarial é execução controlada. Um ambiente Codex pode viver próximo ao codebase, dependências internas e computação aprovada. Supervisão móvel ou remota pode acontecer fora dessa fronteira, mas os arquivos e credenciais não precisam se mover junto com o revisor. Essa é a diferença arquitetural entre controle remoto conveniente e acesso remoto imprudente.

[NOVA]: Hooks fazem isso ser mais do que espiar a tela remotamente. Um hook pode bloquear um segredo de entrar no prompt, exigir um validador antes de um patch ser considerado pronto, ou impor uma fronteira de repo antes do agente agir. Tokens programáticos dão a esses trabalhos uma identidade com escopo. Juntos, eles fazem o Codex parecer mais um sistema de build governável para trabalho de agentes.

[NOVA]: A aquisição da Stainless pela Anthropic é uma história de conectividade de agentes. A Stainless transforma specs de API em SDKs, CLIs e servidores MCP em várias linguagens. A Anthropic diz que a Stainless gerou SDKs oficiais da Anthropic desde o início da API do Claude.

[ALLOY]: Isso importa porque agentes precisam de handles. Um agente que só pode ler texto é limitado. Um agente que pode chamar um SDK digitado, invocar uma CLI ou usar um servidor MCP pode agir em sistemas reais. A qualidade dessas superfícies geradas decide se a ação é segura, previsível e compreensível.

[NOVA]: Specs de API estão se tornando infraestrutura de agentes. Uma spec limpa pode virar documentação, bibliotecas de cliente, ferramentas de linha de comando e superfícies de ferramentas MCP. Uma spec vaga vira uma ferramenta de agente vaga. Se os nomes dos métodos forem unclear, auth for underspecified, paginação for inconsistente, ou erros forem ruidosos, o agente herda essa ambiguidade.

[ALLOY]: A Stainless dentro da Anthropic torna esse caminho de geração de ferramentas mais central para o ecossistema Claude. Não é difícil imaginar um futuro onde criar uma boa spec de API também cria uma boa superfície de ferramenta para o Claude: SDK para código de aplicação, CLI para humanos e automação, servidor MCP para agentes.

[NOVA]: A implicação curta para builders é simples: se uma API interna deve ser usada por agentes, a qualidade da spec agora importa mais. Tipos, escopos de auth, métodos somente leitura, métodos de mutação, paginação, limites de taxa e erros não são mais apenas detalhes de experiência do desenvolvedor. São a diferença entre um agente que pode chamar o sistema de forma limpa e um agente que improvisa.

[ALLOY]: O Project Glasswing é a outra metade. A Anthropic diz que o Claude Mythos Preview foi usado com parceiros em mais de mil projetos open-source e encontrou grandes quantidades de vulnerabilidades de severidade alta e crítica. O headline não é apenas "IA encontra bugs." É que modelos de fronteira podem aumentar a taxa de descoberta de vulnerabilidades o suficiente para que verificação e divulgação se tornem o gargalo.

[NOVA]: Essa é uma pressão muito diferente do code review ordinário. Um modelo pode superfície um caminho de exploit real, uma issue parcial, um falso positivo, ou uma descoberta que precisa de divulgação cuidadosa. Encontrar mais issues possíveis é útil só se mantenedores puderem verificar, priorizar, corrigir e comunicar de forma responsável.

[ALLOY]: Isso se conecta diretamente ao MCP e à geração de SDKs. Ferramentas melhor geradas dão aos agentes mais alcance nos sistemas. Modelos de segurança melhores dão aos agentes mais capacidade de inspecionar esses sistemas. A mesma aceleração torna tanto a produtividade quanto o risco maiores.

[NOVA]: A recomendação prática é tratar a varredura de segurança assistida por agentes como uma atividade delimitada, não um hobby casual de fundo. Use onde o repositório, os requisitos de evidência, o caminho de divulgação e o responsável pelo reparo estão claros. O resultado deve ser uma descoberta com evidências e uma direção de correção, não uma pilha dramática de afirmações.

[ALLOY]: A semana da Anthropic, vista em conjunto, diz que os agentes precisam de interfaces melhores e freios melhores. Stainless é a história da interface: transformar specs em SDKs, CLIs e servidores MCP. Glasswing é a história dos freios: descoberta mais rápida precisa de verificação, divulgação e capacidade de reparo.

[NOVA]: A versão mais forte dessa stack não é um agente com alcance ilimitado. É um agente com ferramentas bem descritas, permissões restritas, logs visíveis e ajuda de segurança suficiente para encontrar falhas reais sem inundar os mantenhedores com ruído. ...

[ALLOY]: O caso de uso do Stainless é direto: transformar uma descrição de serviço em ferramentas que tanto pessoas quanto agentes podem realmente usar. Uma spec de API limpa pode produzir um SDK tipado para código de aplicação, uma CLI para scripts e humanos, e um servidor MCP para chamadas de agente. Isso cria uma fonte única de verdade de interface em vez de três wrappers derivando.

[NOVA]: O caso de uso do Glasswing não é caça de bugs casual. É descoberta de segurança direcionada respaldada por evidências. Um modelo que pode inspecionar grandes codebases e encontrar problemas de alta gravidade muda a economia da pesquisa de vulnerabilidades. Mas o resultado útil ainda é uma descoberta verificada, um caminho mínimo de reparo e uma decisão de divulgação. Sem isso, descoberta mais rápida apenas cria uma fila maior de incerteza.

[ALLOY]: O ponto estratégico é que conectividade e segurança agora aceleram juntas. Quanto mais fácil fica construir surface de ferramentas, mais fácil fica para os agentes agirem. Quanto mais fortes ficam os modelos em descoberta de vulnerabilidades, mais essas surface de ferramentas precisam de permissões restritas e auditabilidade. Stainless e Glasswing são duas faces da mesma construção de agente-infraestrutura.

[ALLOY]: O primeiro grupo de projetos do GitHub dá aos agentes de codificação olhos melhores. Os nomes são Serena, Claude Context, Sourcebot, Understand-Anything, Chunkhound e Code Review Graph.

[NOVA]: Serena é o upgrade mais direto com sabor MCP aqui. Ele dá aos agentes de codificação ferramentas de recuperação semântica, edição, refatoração e depuração que se comportam mais como capacidades de IDE. O recurso importante é trabalho em nível de símbolo: definições, referências, relacionamentos e caminhos de refatoração em vez de apenas correspondências de texto.

[ALLOY]: Isso importa porque grep não é entendimento de código. É uma lanterna rápida. Um agente de codificação precisa saber onde um símbolo é definido, onde é usado, do que depende e quais testes cobrem o caminho. Serena tenta colocar esses movimentos de IDE atrás de uma surface de ferramenta que um agente pode usar.

[NOVA]: Claude Context é um MCP de busca de código semântica para Claude Code e outros agentes. Seu trabalho é tornar grandes repos pesquisáveis por significado sem enfiar diretórios enormes no prompt. Isso é útil quando o nome do código não corresponde à descrição humana, ou quando a lógica relevante está espalhada entre arquivos.

[ALLOY]: Sourcebot é a surface de busca e entendimento de código auto-hospedada. Oferece busca no repo, navegação, exploração de arquivos e Q&A do Ask Sourcebot com citações. A parte auto-hospedada importa porque inteligência de código frequentemente toca repositórios privados. Uma surface de busca compartilhada e citada pode ajudar humanos e agentes a argumentar a partir da mesma evidência em vez de impressões.

[NOVA]: Understand-Anything transforma codebases em grafos de conhecimento interativos com busca e Q&A, e se posiciona explicitamente para Claude Code, Codex, Cursor, Copilot, Gemini CLI e ferramentas relacionadas. Um grafo não é mágica, mas pode mostrar a forma da arquitetura antes de um agente começar a editar um sistema que mal entende.

[ALLOY]: Chunkhound e Code Review Graph empurram o ângulo local-first e mapa persistente. Essa é a categoria certa para equipes que querem contexto semântico ou de grafo sem enviar o repo inteiro para outro lugar. Um mapa de código persistente pode reduzir desperdício de contexto alimentando o agente com os poucos relacionamentos que importam em vez de um despejo gigante de transcrição.

[NOVA]: A recomendação para esse grupo é escolher baseado no que está faltando para o agente. Se faltam símbolos e referências, olhe para Serena. Se precisa de busca semântica dentro do Claude Code, olhe para Claude Context. Se humanos e agentes precisam de um navegador de código auto-hospedado compartilhado, olhe para Sourcebot. Se forma da arquitetura é o problema, Understand-Anything é interessante. Se indexação local e mapas de código persistentes importam mais, Chunkhound e Code Review Graph pertencem à lista curta.

[ALLOY]: A razão pela qual isso é uma faixa de notícias, não apenas uma lista de ferramentas, é que contexto de código está se tornando sua própria camada na stack. Janelas de contexto maiores ajudam, mas não substituem a qualidade da recuperação. Um modelo que vê um mapa melhor pode fazer uma edição menor e mais precisa. Isso geralmente é mais valioso do que entregar mais mil arquivos irrelevantes.

[NOVA]: É aqui que Hermes, OpenClaw, Codex e Claude Code todos se beneficiam de surfaces de ferramentas comuns. Se inteligência de código está disponível através de MCP, índices locais ou busca auto-hospedada, pode ficar abaixo de vários agentes. O agente muda; o mapa do repo permanece útil.

[ALLOY]: A recomendação curta é: adicione uma camada de inteligência de código apenas onde o tamanho do repo justifica. Um script de um arquivo não precisa de um grafo semântico. Um codebase maduro com comportamento espalhado provavelmente precisa. ...

[NOVA]: O melhor caso de uso do Serena é edição consciente de símbolos. Uma refatoração que cruza definições, referências e testes se beneficia de uma ferramenta MCP que entende relacionamentos de código. O melhor caso de uso do Claude Context é recuperação semântica quando o prompt descreve comportamento mas o código usa nomes diferentes. O melhor caso de uso do Sourcebot é uma surface de busca auto-hospedada onde humanos e agentes podem compartilhar citações.

[ALLOY]: Understand-Anything é mais forte quando a forma da arquitetura importa: serviços não familiares, dependências escondidas ou um repo onde o grafo de chamadas explica mais do que os nomes de arquivos. Chunkhound e Code Review Graph se encaixam no caso de uso local-first, onde mapas persistentes são valiosos mas o código não pode sair casual da máquina ou rede confiável.

[NOVA]: A tendência de desenvolvimento está clara: o contexto de código está se tornando um substrato reutilizável. O framework de agentes pode ser o Claude Code hoje, o Codex amanhã, o Hermes na próxima semana, e o OpenClaw ao redor de tudo isso. Um bom mapa de repo pode servir todas essas superfícies se for exposto através de MCP, um índice local, ou uma camada de busca auto-hospedada.

[ALLOY]: É por isso que essa faixa de projeto importa. Não se trata apenas de tornar um modelo mais inteligente. Se trata de dar a cada agente de programação um melhor ponto de partida: menos arquivos irrelevantes, referências mais precisas, arquitetura mais clara, e um caminho mais curto da pergunta à evidência.

[NOVA]: O segundo grupo de projetos muda como a stack roda. Context7, Claude Code Router, mcp-use, goose, gstack, deepsec, context-mode, e ai-setup ficam todos entre o modelo, o repo, as ferramentas e o humano.

[ALLOY]: Context7 cuida de documentação atual. Agentes de programação frequentemente falham porque a memória de biblioteca deles está desatualizada. Context7 dá aos LLMs e agentes de programação docs de biblioteca atualizados via CLI, skills, ou MCP. É especialmente útil para tarefas rápidas de JavaScript, Python, SDKs de IA e frameworks onde exemplos antigos parecem plausíveis mas quebram.

[NOVA]: Claude Code Router é sobre roteamento de provedores e modelos. Ele pode rotear requisições do Claude Code através do OpenRouter, DeepSeek, Ollama, Gemini e outros backends, com transformers e escolhas de modelo específicas por rota. O valor está em casar o backend com o trabalho: resumos baratos, experimentos locais, leituras de contexto longo, ou revisões de raciocínio pesado.

[ALLOY]: O risco é a responsabilização. Um roteador só ajuda se a rota for visível o suficiente para que o usuário saiba qual provedor e modelo lidou com a tarefa. Roteamento escondido pode economizar dinheiro e criar confusão ao mesmo tempo.

[NOVA]: mcp-use é um framework para construir apps e servidores MCP em TypeScript e Python, com caminhos de inspeção e deploy. Isso é importante porque MCP está passando de novidade para camada de integração. Times precisam de um jeito mais rápido de construir ferramentas pequenas, inspecionar chamadas, e empacotá-las para agentes sem criar cada servidor na mão.

[ALLOY]: goose é um agente de IA local com desktop, CLI, API, suporte multi-provedor, caminhos ACP, e extensões MCP. Agora está sob a Agentic AI Foundation, e vale a pena acompanhar como fallback ou ponto de comparação de agente local. A parte interessante não é se ele substitui tudo. É se o modelo de provedores e extensões dele facilita algumas tarefas locais para rodar fora de uma stack mais pesada.

[NOVA]: gstack empacota papéis e fluxos de trabalho do Claude Code para revisão, QA, release, segurança, planejamento e trabalho de produto. Packs de papel podem virar teatro se só renomearem prompts comuns, mas são úteis quando codificam comportamento repetível de revisão, evidência esperada e formatos de saída consistentes.

[ALLOY]: deepsec é o scanner de segurança nessa faixa. Ele usa agentes de programação para scanning de vulnerabilidades em grandes codebases, com scans retomáveis, matchers, processamento, revalidação e exportação. Isso coloca ele no mesmo universo do Glasswing, mas como uma ferramenta hospedada no GitHub que construtores podem inspecionar e rodar em configurações restritas.

[NOVA]: context-mode e ai-setup miram em dois problemas do dia a dia: ruído de output e drift de configuração. Quando uma stack inclui Claude Code, Codex, OpenCode, Gemini CLI, Hermes, OpenClaw, modelos locais, servidores MCP e roteadores, a configuração pode se tornar o modo de falha escondido. Ferramentas que mantêm o contexto firme e a configuração consistente podem ser mais úteis do que outro seletor de modelo.

[ALLOY]: A recomendação para esse grupo também é baseada em trabalho. Use Context7 quando documentação atual é a peça que falta. Use Claude Code Router quando a escolha de provedor realmente importa. Use mcp-use quando uma capacidade privada deve virar uma ferramenta MCP. Use goose quando um agente local com extensões é a comparação certa. Use gstack quando papéis de revisão repetíveis importam. Use deepsec só quando achados de segurança podem ser verificados e tratados.

[NOVA]: A tendência maior é que a stack de agentes está preenchendo o meio. Já temos modelos e superfícies de chat. A nova atividade está em roteadores, retrieval de docs, construtores de MCP, shells de agentes locais, packs de papel, mapas de código e scanners. É aí que o trabalho de agentes se torna mais controlável.

[ALLOY]: Também torna disciplina mais importante. Cada ferramenta extra adiciona autoridade, configuração, ou outro lugar para a evidência desaparecer. Um bom projeto conquista seu espaço tornando a tarefa mais clara: docs melhores, contexto de código melhor, roteamento de provedor mais claro, acesso a ferramentas mais estreito, ou achados de segurança mais verificáveis. ...

[NOVA]: O caso de uso central do Context7 é bibliotecas que mudam rápido. Quando um framework, SDK de IA ou cliente de banco de dados muda rapidamente, memória de modelo desatualizada produz código que parece certo e falha em runtime. Docs atuais no loop do agente são um jeito simples de melhorar o build sem mudar modelos.

[ALLOY]: O caso de uso do Claude Code Router é separação de carga de trabalho. Um modelo barato pode resumir logs. Um modelo local pode lidar com leitura de fundo privada. Um modelo mais forte pode revisar um patch arriscado. O roteador é útil quando essas escolhas são explícitas; é perigoso quando o roteamento se torna invisível.

[NOVA]: mcp-use é a ferramenta de build nesse grupo. Ele reduz o custo de transformar uma pequena capacidade em um servidor ou app MCP, especialmente em TypeScript e Python. O primeiro bom caso de uso geralmente é só leitura: consulta de status, busca de documentação, consulta de inventário, ou um relatório interno estreito. Uma vez que o formato é compreensível, ações de escrita podem ser tratadas como um privilégio separado.

[ALLOY]: goose é o caso de uso de agente local. Ele dá aos construtores outra superfície de desktop, CLI e API com suporte a provedores e extensões MCP. gstack é o caso de uso de papel repetível: prompts de revisão, QA, release, planejamento e segurança que se comportam de forma consistente o suficiente para serem julgados. deepsec é o caso de uso de segurança, com scans retomáveis e achados exportados. context-mode e ai-setup são o caso de uso de consistência, mantendo output e configuração de se espalharem conforme a stack cresce.

[NOVA]: O padrão útil em todos eles não é procedimento pelo próprio procedimento. É escolher a ferramenta que muda o resultado: menos APIs desatualizadas, escolha de provedor mais clara, superfície MCP mais estreita, um agente local que pode rodar sem a stack pesada, um papel de revisão que encontra bugs concretos, ou um scanner que produz evidência ao invés de ruído.

[ALLOY]: Tem mais um ponto de nível de stack nessa faixa de projeto. Essas ferramentas não estão competindo só em qualidade de modelo. Estão competindo em qualidade de contexto, clareza de roteamento, formato de interface e evidência. Context7 melhora a entrada de documentação. Serena e Sourcebot melhoram a entrada de código. Claude Code Router muda o caminho do modelo. mcp-use muda a interface de ferramentas. goose muda o shell de execução local. deepsec muda a lente de segurança. Essas são camadas diferentes, e misturá-las faz a stack ficar mais difícil de raciocinar.

[NOVA]: O melhor caso de uso para toda essa linha é um builder que já tem um modelo capaz, mas ainda assim obtém resultados medíocres porque o sistema ao redor é fraco. O agente lê docs desatualizados. Ele perde o arquivo certo. Ele usa o modelo caro para um resumo barato. Ele não consegue chamar o sistema interno de forma limpa. Ele produz uma afirmação de segurança sem evidência. Os projetos nessa linha atacam diretamente esses modos de falha.

[ALLOY]: É por isso que isso é mais interessante do que uma lista de estrelas. Um repositório ganha atenção quando muda uma das superfícies difíceis do trabalho de agentes: o que o modelo sabe, qual modelo responde, quais ferramentas podem ser chamadas, onde a execução acontece, como o código é mapeado ou como os achados são verificados. Isso é um upgrade concreto da stack, não um novo badge para o README.

[NOVA]: As builds mais fortes vão combinar essas camadas com cuidado. Docs atualizados para bibliotecas rápidas. Mapas de código semânticos para repos grandes. Roteamento visível para escolha de provedor. Servidores MCP pequenos para funcionalidades privadas. Agentes locais para execução sensível. Scanners de segurança onde a evidência pode ser tratada. O valor não está em ter cada ferramenta instalada. O valor está em saber qual camada está fraca e adicionar apenas a peça que a fortalece.

[NOVA]: A atualização de stack do EP057 é direta. OpenClaw v2026.5.22 torna o gateway, a camada de plugins, as fontes de notas de reunião, o comportamento de fallback do provedor, a navegação de sessão e os controles do Discord mais sólidos. Claude Code melhora a visibilidade de uso, revisão de diffs, renderização de listas de tarefas, política de conector MCP gerenciado em nuvem e vários recursos de segurança de shell e sandbox. O patch a seguir é apenas interno.

[ALLOY]: As notícias do Google Gemini dizem que ambientes de agentes gerenciados agora são uma superfície de produto: execução Linux remota, ferramentas, navegação, arquivos, continuação de sessão e arquivos de instrução de agente personalizados. As notícias do Codex da OpenAI dizem que o trabalho de coding-agent está se tornando remoto, supervisionado por celular, com escopo de token, governado por hooks e implantável em empresas.

[NOVA]: A aquisição da Stainless pela Anthropic diz que SDKs, CLIs e servidores MCP estão se tornando infraestrutura central de agentes. O Projeto Glasswing diz que modelos de fronteira podem encontrar vulnerabilidades rapidamente o suficiente para que a verificação e a divulgação se tornem o gargalo.

[ALLOY]: O radar de projetos do GitHub diz que os upgrades úteis da stack não são todos modelos. Serena, Claude Context, Sourcebot, Understand-Anything, Chunkhound e Code Review Graph melhoram o que os agentes conseguem entender sobre código. Context7, Claude Code Router, mcp-use, goose, gstack, deepsec, context-mode e ai-setup melhoram docs, roteamento, ferramental MCP, execução local, papéis repetíveis, varredura de segurança e consistência de setup.

[NOVA]: A recomendação curta é atualizar as ferramentas core e então adicionar apenas os projetos que resolvem um problema visível. Mapas de código melhores para repos grandes. Docs atualizados para bibliotecas que mudam rápido. Roteamento de modelo onde a escolha de provedor importa. Construtores de MCP para ferramentas com escopo. Scanners de segurança onde há um caminho real de verificação.

[ALLOY]: Essa é a versão útil de notícias sobre agentes: não uma pilha de nomes, e nem processo pelo bem do processo. Lançamentos concretos, capacidades concretas e uma imagem mais clara de para onde a stack está indo.

[NOVA]: Notas completas e links de origem estão nas notas do episódio em Toby On Fitness Tech dot com.

[ALLOY]: Obrigado por ouvir o AgentStack Daily. Voltamos em breve.