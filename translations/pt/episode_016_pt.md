## [00:00-02:30] OpenClaw Troca de Pele

NOVA: Eu sou NOVA, este é o OpenClaw Daily, e hoje temos um daqueles releases em que os números de versão parecem arrumados, mas a história real por baixo é bagunçada, consequente e, honestamente, meio fascinante. [PAUSE] Nesta semana, dois bugs atingiram um setup real de power-user com força suficiente para te contar quase tudo o que você precisa saber sobre onde o OpenClaw está agora.

ALLOY: É. Esses não eram edge cases bonitinhos e pequenos. Eram o tipo de bug que faz você duvidar do seu próprio setup, porque o que você vê não é o que o sistema está realmente fazendo.

NOVA: Bug um: um usuário tinha [EMPHASIS]MiniMax[/EMPHASIS] configurado como seu modelo de raciocínio. A API upstream estava retornando [EMPHASIS]api_error[/EMPHASIS]. O OpenClaw olhou para isso, decidiu que devia ser transitório, tentou de novo em silêncio, nunca expôs a falha, nunca acionou o fallback corretamente, e o usuário recebeu de volta um resultado degradado sem ter ideia de que a chamada original tinha falhado.

ALLOY: O que é brutal, porque os piores bugs são os que não explodem. Eles só pioram em silêncio. Você não recebe uma luz vermelha. Você recebe uma luz verde mais fraca.

NOVA: Exatamente. E o bug dois era uma classe diferente de dor, mas igualmente real. O usuário cola um token novo de [EMPHASIS]OpenAI Codex[/EMPHASIS], vê a confirmação, tudo parece bem-sucedido, reinicia o gateway, e o token volta para a credencial expirada.

ALLOY: Esse faz você se sentir maluco. Porque, da perspectiva do usuário, ele fez a coisa certa. Colou o token novo. O app disse: sim, salvo. Aí, depois do restart, não. Token antigo e ruim de novo. [PAUSE] Por baixo dos panos, o estado de auth em memória do gateway estava sobrescrevendo o valor recém-salvo em disco no restart.

NOVA: Ambos foram corrigidos em [EMPHASIS]v2026.3.23[/EMPHASIS]. Mas, para entender por que aconteceram, você precisa entender o que [EMPHASIS]v2026.3.22[/EMPHASIS] mudou. Porque a .22 é a grande. A .22 é o OpenClaw fazendo algo que provavelmente deveria ter feito há um ano.

ALLOY: O expurgo do legado.

NOVA: O expurgo do legado. Os nomes antigos, as camadas de compatibilidade, os caminhos de transição esquisitos, as muletas de browser relay, a geleia do plugin SDK — muita coisa foi arrancada. [PAUSE] E acho que a forma certa de enquadrar essas duas releases juntas é esta: a .22 remove a pele morta, e a .23 garante que a pele nova não rache.

ALLOY: Esse é o episódio inteiro. Se você mantém uma instalação real, essas não são atualizações decorativas. Elas são estruturais.

## [02:30-11:00] O Expurgo do Legado — Breaking Changes da v2026.3.22

NOVA: Vamos começar pela mudança mais carregada emocionalmente, porque as pessoas se apegam de um jeito estranhíssimo a nomes, mesmo quando esses nomes já deveriam ter sido aposentados para sempre. Os nomes de ambiente [EMPHASIS]CLAWDBOT_*[/EMPHASIS] e [EMPHASIS]MOLTBOT_*[/EMPHASIS] sumiram. Não deprecated. Não tolerados com warning. Sumiram.

ALLOY: E eu quero desacelerar isso, porque se você roda OpenClaw em um laptop e em nenhum outro lugar, talvez ouça isso e pense: ok, é só renomear algumas variáveis, beleza. Esse não é o modo real de falha. O modo real de falha é você ter um arquivo [EMPHASIS].env[/EMPHASIS] antigo no Docker Compose, ou uma unit [EMPHASIS]systemd[/EMPHASIS] toda empoeirada num VPS, ou alguma coisa num shell profile que você não olha há oito meses. Você faz upgrade, o OpenClaw sobe, e esses valores são ignorados em silêncio.

NOVA: Sem erro. Sem banner de migração.

ALLOY: Nada de “ei, eu vi [EMPHASIS]CLAWDBOT_TOKEN[/EMPHASIS] e isso está obsoleto”. Só config faltando. De repente o auth não bate, o caminho do state não está onde você achava, talvez um plugin não carregue, talvez um token pareça ausente. [PAUSE] Esse é o tipo de quebra que te pega às duas da manhã depois de um upgrade numa máquina em que você não mexia há um tempo.

NOVA: Dê grep nos seus arquivos de env. Em todo ambiente em que você roda OpenClaw. Todo host. Todo arquivo de Compose. Toda unit de startup. Todo bootstrap de shell. Se você tiver [EMPHASIS]CLAWDBOT_*[/EMPHASIS] ou [EMPHASIS]MOLTBOT_*[/EMPHASIS], trate isso como quebrado até corrigir.

ALLOY: Mesma história com o diretório de state antigo [EMPHASIS]~/.moltbot[/EMPHASIS]. Esse caminho já não faz parte do futuro. Se o seu state ainda mora lá, o OpenClaw não vai inferir isso magicamente para você depois do upgrade. Mova para [EMPHASIS]~/.openclaw[/EMPHASIS] ou defina [EMPHASIS]OPENCLAW_STATE_DIR[/EMPHASIS] explicitamente e encerre o assunto.

NOVA: E esta é uma daquelas escolhas em que eu realmente concordo com a dureza. Aliases de transição parecem gentis no curto prazo, mas fazem a arquitetura mentir sobre si mesma. Existe um custo real em fingir que nomes antigos ainda são de primeira classe.

ALLOY: Eu concordo com o estado final. Discordo de quão serenas as pessoas ficam em relação à dor da migração. Se você é a pessoa que gerencia cinco instalações e duas delas são esquisitas, isso não é uma limpeza filosófica. Isso é uma caça ao tesouro.

NOVA: Justo. [PAUSE] A segunda grande breaking change na .22 é que [EMPHASIS]ClawHub[/EMPHASIS] agora é first-class, e o significado prático disso é maior do que a formulação de marketing faz parecer. [EMPHASIS]openclaw plugins install name[/EMPHASIS] agora verifica o ClawHub primeiro, e só cai para npm se o ClawHub não tiver o pacote.

ALLOY: O que significa que o comportamento de instalação mudou, mesmo que você não tenha mudado o comando. É isso que as pessoas precisam ouvir. Se você tem scripts que assumem um caminho de resolução de pacote via npm, e esse mesmo nome agora existe no ClawHub, você pode receber a versão do ClawHub primeiro.

NOVA: Também existem comandos nativos agora: [EMPHASIS]openclaw skills search[/EMPHASIS], [EMPHASIS]openclaw skills install[/EMPHASIS], [EMPHASIS]openclaw skills update[/EMPHASIS]. [PAUSE] E, para mim, isto é o OpenClaw finalmente alinhando o produto ao ecossistema que ele pretendia ter. O ClawHub sempre deveria ser a casa das skills. Esta release torna isso real em vez de aspiracional.

ALLOY: Está mais limpo, mas teste sua automação. Se você tem scripts de bootstrap, dotfiles, docs de onboarding, garanta que eles ainda instalam o que você acha que instalam. A mudança é boa. Surpresas não são.

NOVA: Terceiro: o overhaul do [EMPHASIS]Plugin SDK[/EMPHASIS]. Isso não é um ajustezinho nas bordas. [EMPHASIS]openclaw/extension-api[/EMPHASIS] sumiu. Não existe shim de compatibilidade. A nova superfície é [EMPHASIS]openclaw/plugin-sdk/*[/EMPHASIS], com subpaths mais estreitos e limites muito mais claros.

ALLOY: Se você tem plugins customizados, isso é uma migração real. Não é opcional. Não existe fallback. Você não pode dizer “eu atualizo depois”. Depois é quebrado.

NOVA: Plugins bundled também agora precisam usar o runtime injetado para operações do lado do host, o que é uma daquelas mudanças que soa burocrática até você perceber que ela remove muito vazamento ambíguo de privilégio. O comportamento do host é explícito. Os limites do runtime são explícitos.

ALLOY: E a descoberta de mensagens também mudou. [EMPHASIS]describeMessageTool()[/EMPHASIS] agora é obrigatório. O fluxo antigo de [EMPHASIS]listActions[/EMPHASIS], [EMPHASIS]getCapabilities[/EMPHASIS], [EMPHASIS]getToolSchema[/EMPHASIS] foi removido. [PAUSE] Isso não é renomear. Isso é mudança de contrato.

NOVA: O novo SDK é realmente mais limpo. De verdade. Os imports são mais estreitos. A intenção é mais clara. O modelo de runtime é mais coerente. Mas você realmente precisa migrar. E se você é desenvolvedor de plugin, vá ler [EMPHASIS]docs.openclaw.ai/plugins/sdk-migration[/EMPHASIS]. Não improvise de memória.

ALLOY: Eu quero sublinhar isso. Esta não é a semana para fazer a migração no improviso, na base do feeling.

NOVA: Quarto bloco: hardening de segurança. Algumas dessas coisas são invisíveis até o momento em que te salvam, o que significa que elas não vão receber tanto tempo de fala, mas importam. O exec sandbox agora bloqueia [EMPHASIS]MAVEN_OPTS[/EMPHASIS], [EMPHASIS]SBT_OPTS[/EMPHASIS], [EMPHASIS]GRADLE_OPTS[/EMPHASIS], [EMPHASIS]ANT_OPTS[/EMPHASIS], além de [EMPHASIS]GLIBC_TUNABLES[/EMPHASIS] e [EMPHASIS]DOTNET_ADDITIONAL_DEPS[/EMPHASIS]. [PAUSE] Isso é basicamente uma varredura contra superfícies de injeção de runtime que as pessoas esquecem que existem.

ALLOY: Exato. Essas env vars são o tipo de coisa que atacantes adoram e operadores esquecem. Se o sandbox das suas ferramentas diz “estamos controlando o que roda”, mas você ainda deixa variáveis de injeção de build tool ou runtime passarem, você não está controlando muita coisa, de verdade.

NOVA: Também existe uma mudança sutil, mas inteligente, na allowlist: [EMPHASIS]time[/EMPHASIS] agora é transparente na avaliação da allowlist. Então [EMPHASIS]time ./approved-script[/EMPHASIS] se vincula ao script interno, não ao wrapper [EMPHASIS]time[/EMPHASIS].

ALLOY: Essa é muito prática. As pessoas envolvem comandos em [EMPHASIS]time[/EMPHASIS] o tempo todo durante debugging. Antes, wrappers podiam criar edge cases estranhos de policy. Agora ele avalia a coisa que você realmente queria rodar.

NOVA: E o hardening de voice webhook também ficou mais rígido: rejeitar assinaturas ausentes do provider antes de ler o body, com limite pré-auth de [EMPHASIS]64KB[/EMPHASIS] e [EMPHASIS]5s[/EMPHASIS]. Isso é simplesmente boa higiene de perímetro. Não gaste recursos fazendo parse de lixo não autenticado.

ALLOY: Por fim, nas correções silenciosas que importam: comandos slash do Discord. Carbon reconcile agora é o padrão, então restarts do gateway não ficam mais churnando comandos slash pelo caminho de deploy local.

NOVA: Eu adoro esse tipo de correção porque os usuários a vivenciam como menos fantasmas.

ALLOY: É. Silenciosa, mas real. Restarts estavam gerando comandos fantasmas. Agora não geram. Isso não é glamouroso, mas é exatamente o tipo de paper cut que faz uma plataforma parecer amadora se você deixa sem corrigir.

NOVA: Então a .22 em uma frase é: OpenClaw parou de fingir que o legado era inofensivo.

ALLOY: E se você não encostava no seu setup há um tempo, a .22 é a release que vai descobrir isso por você.

NOVA: Eu também acho que esta release traça uma linha entre compatibilidade e bagunça. Por muito tempo, o OpenClaw vinha carregando nomes antigos, suposições antigas de instalação, formatos antigos de descoberta de plugins e caminhos antigos de browser porque remover isso parecia arriscado. [PAUSE] Mas deixar tudo isso no lugar também era arriscado. Tornava a plataforma mais difícil de raciocinar.

ALLOY: Esse é o trade-off que as pessoas não enxergam. Compatibilidade retroativa não preserva só a função. Ela também preserva confusão. Cada alias, cada caminho antigo, cada ramo de “ainda aceitamos isso” vira mais uma coisa que o suporte precisa lembrar e mais uma coisa em que operadores tropeçam.

NOVA: E, assim que você centraliza em torno do ClawHub, do plugin SDK moderno e da nomenclatura atual, a documentação finalmente pode parar de falar em duas linhas do tempo.

ALLOY: O que importa mais do que as pessoas acham. Metade da dor operacional não é o bug em si. É a sensação de que cada guia que você lê pode ser de uma geração diferente do produto.

NOVA: Então, se a .22 parece dura, é porque ela está escolhendo uma realidade só.

ALLOY: É. Uma realidade, menos aliases, menos relíquias. Dor de curto prazo, sanidade de longo prazo.

## [11:00-17:00] Chrome MCP: A Extensão Morreu

NOVA: Precisamos dedicar tempo de verdade ao tooling de navegador, porque, para muita gente, esta é a maior mudança operacional individual de toda a dupla de releases. O relay legado da extensão do Chrome acabou. [EMPHASIS]driver: "extension"[/EMPHASIS], assets bundled da extensão, [EMPHASIS]browser.relayBindHost[/EMPHASIS] — tudo removido.

ALLOY: E, se você não estava por perto naquela era, aqui vai o que a extensão realmente era. O OpenClaw costumava distribuir uma extensão do Chrome que agia como relay para o [EMPHASIS]CDP[/EMPHASIS], o Chrome DevTools Protocol. Você instalava a extensão manualmente, concedia permissões ao navegador, e ela servia como ponte entre o OpenClaw e o browser.

NOVA: O que sempre pareceu um pouco improvisado.

ALLOY: Era improvisado. Útil, mas improvisado. Funcionava porque controlar navegador é bagunçado e a extensão te dava um caminho mais fácil do que explicar attach direto para todo mundo. Mas vinha com toda a bagagem de uma extensão: fricção de instalação, esquisitices de permissão, deriva de compatibilidade, peculiaridades de profile do navegador e mais uma peça móvel para diagnosticar quando as coisas saíam dos trilhos.

NOVA: O modelo substituto é simplesmente melhor. O OpenClaw agora se conecta diretamente a uma instância do Chrome em execução ou a um profile de usuário usando mecanismos padrão de CDP. Sem precisar de extensão. Sem relay customizado no meio. [PAUSE] Arquitetonicamente, isto é mais limpo. Menos camadas sob medida. Menos segredos escondidos no tooling.

ALLOY: Mas — e este é o alerta prático importante — se você fizer upgrade sem rodar [EMPHASIS]openclaw doctor --fix[/EMPHASIS] antes, ou pelo menos logo depois, sua automação de navegador pode quebrar completamente. E nem sempre vai quebrar de um jeito óbvio. Você não necessariamente vai receber uma mensagem amigável dizendo “extension relay removido”. O mais provável é que simplesmente falhe ao conectar, ou entre em loop esquisito de consentimento, ou seu caminho de attach pareça meio vivo e depois morra.

NOVA: [EMPHASIS]openclaw doctor --fix[/EMPHASIS] lê sua config atual e migra setups locais de browser no host para o modo moderno correto: [EMPHASIS]existing-session[/EMPHASIS] ou [EMPHASIS]user[/EMPHASIS]. Isso não é uma recomendação cosmética. Faz parte da migração.

ALLOY: E vale esclarecer os três modos agora. [EMPHASIS]existing-session[/EMPHASIS] significa anexar a um Chrome já em execução. [EMPHASIS]user[/EMPHASIS] significa iniciar com um profile de usuário. [EMPHASIS]CDP[/EMPHASIS] puro para setups em Docker, headless, sandbox, remotos — isso permanece basicamente inalterado.

NOVA: O que é a separação correta. O antigo caminho pela extensão era uma muleta. Esta é a direção certa.

ALLOY: Eu concordo em grande parte, mas quero defender por que os usuários gostavam da muleta. Uma muleta é um problema se impede a recuperação. É útil se permite que você ande. Para muita gente, a extensão era o único fluxo de navegador que conseguiam fazer funcionar de forma consistente.

NOVA: Justo, mas era consistência comprada com fragilidade. O sistema tinha uma ponte customizada extra só para disfarçar o modelo de attach.

ALLOY: Verdade. E a .23, na verdade, prova o seu ponto, porque, assim que a .22 removeu o caminho antigo, a .23 teve imediatamente de tornar o caminho novo confiável no mundo real. [PAUSE] Duas correções importam aqui. Primeiro, timing de attach de abas. O OpenClaw estava tratando o handshake do Chrome MCP como se o navegador estivesse completamente pronto no instante em que a conexão subia. No macOS, isso nem sempre era verdade. As abas existiam, mas ainda não estavam utilizáveis. Então o primeiro attach podia churnar consentimento, girar timeouts e, no geral, parecer assombrado.

NOVA: Essa correção importa porque prontidão não é binária. Um socket estar aberto não é a mesma coisa que a superfície de UI estar estável.

ALLOY: Exatamente. Segunda correção: reaproveitamento de loopback. Em setups headless ou loopback, o OpenClaw podia deixar passar um navegador em execução numa sondagem curta e cair imediatamente para relaunch. Isso criava regressões de segunda execução em que a primeira funcionava e a próxima parecia exigir que a sessão fosse atropelada. A .23 adiciona uma pequena espera antes desse fallback.

NOVA: O que parece minúsculo até você conviver com isso. Aí vira a diferença entre uma ferramenta de navegador que parece instável e uma que parece intencional.

ALLOY: É por isso que o meu resumo dessa transição de navegador é: a .22 removeu o caminho antigo, a .23 tornou o caminho novo confiável, e você precisa das duas. Se você estiver pensando só no nível das manchetes de release, vai perder o quanto essas duas versões realmente estão acopladas.

NOVA: Além disso, se você roda automação local de browser no host, deveria tratar [EMPHASIS]doctor --fix[/EMPHASIS] como parte da migração do navegador, não como uma tarefa geral de manutenção. Ele está fazendo trabalho direcionado.

ALLOY: Sim. Não é housekeeping opcional. É passo de migração.

NOVA: E há uma lição maior nessa mudança de navegador também. Automação de browser é um daqueles domínios em que as pessoas toleram complexidade absurda porque o retorno é muito alto. Vão instalar uma extensão, fixar versão, abençoar profile, carregar flags de launch esquisitas, qualquer coisa, desde que o navegador obedeça. [PAUSE] Mas todo workaround escondido vira dívida técnica com interface de usuário.

ALLOY: Essa é uma ótima forma de colocar. A extensão não era só dívida de código. Era dívida ritual de usuário. Você precisava lembrar que ela existia, lembrar como tinha sido instalada, lembrar por que um profile de browser era especial, lembrar o que quebrava se o Chrome atualizasse. Não é esse o tipo de história de plataforma que você quer para sempre.

NOVA: O attach via existing-session é um modelo muito mais honesto. Ou existe um navegador ao qual você consegue se anexar, ou não existe. Ou o profile é utilizável, ou não é. Existe menos mágica.

ALLOY: Menos mágica, mas mais responsabilidade de acertar prontidão e timing, e é por isso que as correções da .23 importam tanto. Se você vai remover a ponte antiga, o caminho direto tem que parecer tediosamente estável. Tedioso é sucesso em automação de navegador.

NOVA: Tedioso, confiável, legível. Esse é o objetivo.

## [17:00-22:00] Image Gen é Padronizado

NOVA: Próximo assunto: geração de imagem. Este é menos dramático do que tooling de navegador, mas te conta muito sobre para onde o OpenClaw está indo. A skill bundled [EMPHASIS]nano-banana-pro[/EMPHASIS] foi removida. Sumiu. Sem shim.

ALLOY: O que significa que, se você tinha workflows, prompts ou docs internos que chamam [EMPHASIS]nano-banana-pro[/EMPHASIS], encontre isso e substitua. É uma quebra dura. Não presuma que existe um alias esperando por você.

NOVA: A plataforma está padronizando em torno da ferramenta core [EMPHASIS]image_generate[/EMPHASIS]. E, filosoficamente, eu acho isso exatamente certo. Uma ferramenta, backend configurável, superfície de invocação consistente. Melhor do que carregar um wrapper bundled de skill para sempre só porque as pessoas se acostumaram com o nome.

ALLOY: Desde que você defina a config key. Esta é a parte que as pessoas pulam. Você precisa de [EMPHASIS]agents.defaults.imageGenerationModel.primary: "google/gemini-3-pro-image-preview"[/EMPHASIS]. Se você não definir isso, o comportamento fica indefinido. E indefinido em terra de config nunca significa empolgante. Significa confuso.

NOVA: Existe um padrão mais amplo aqui. O OpenClaw está tentando fazer capacidades core parecerem capacidades core. Geração de imagem não deveria parecer um truque lateral.

ALLOY: Certo, mas operacionalmente eu colocaria de forma mais direta: padronização só é bonita se os defaults forem explícitos. Se você arranca a coisa bundled antiga e não define o backend novo, criou uma arquitetura mais limpa e uma terça-feira pior.

NOVA: Crítica justa. [PAUSE] Também há melhorias de marketplace embrulhadas dentro dessa mudança. Instalações via marketplace agora são first-class, incluindo sintaxe [EMPHASIS]plugin@marketplace[/EMPHASIS] e suporte ao registry de marketplace do Claude.

ALLOY: O que reduz a quantidade de folclore na instalação de plugins. Menos momentos de “na verdade, para este plugin você faz de outro jeito”.

NOVA: E comandos de chat [EMPHASIS]/plugins[/EMPHASIS] e [EMPHASIS]/plugin[/EMPHASIS] restritos ao owner continuam exatamente essa mesma linha: dar à plataforma uma história coerente única para descobrir, instalar e gerenciar extensões.

ALLOY: Eu gosto que sejam restritos ao owner também. Quanto mais poderosa fica a superfície de instalação, menos você quer contextos aleatórios de runtime tratando isso como brinquedo.

NOVA: Para mim, a história da geração de imagem é esta: o OpenClaw está saindo de personalidade bundled e indo para capacidade configurada. [PAUSE] Isso é maturidade.

ALLOY: Para mim, é isto: atualize seus workflows, defina a model key, e não deixe chamadas quebradas de imagem paradas na automação para só descobrir durante uma demo.

NOVA: E existe uma sutil mudança de governança escondida nessa padronização. Quando geração de imagem é uma ferramenta core em vez de uma skill bundled querida, você pode trocar providers, melhorar a interface uma vez, documentar um comportamento só e auditar uma superfície de permissões só.

ALLOY: Exato. Deixa de ser “aquela coisa especial que funciona porque existe um wrapper” e passa a fazer parte do contrato real da plataforma. Isso é mais saudável.

NOVA: Também muda como as equipes deveriam pensar sobre portabilidade. Se o seu workflow diz [EMPHASIS]image_generate[/EMPHASIS] e seu backend é configurado separadamente, você pode migrar providers sem reescrever a lógica do workflow em si.

ALLOY: O que é muito bom em teoria e ainda melhor quando um vendor muda preço ou rate limit numa sexta-feira à tarde.

NOVA: Exatamente. Padronização não é só elegância. É alavancagem.

ALLOY: Desde que você defina a config key.

NOVA: Desde que você defina a config key. Você pode repetir isso até o fim dos tempos.

## [22:00-31:00] Fazendo Isso Funcionar — O Reliability Pass da .23

NOVA: Este é o coração do episódio. Porque a .22 é o expurgo, mas a .23 é o reliability pass que torna o expurgo sobrevivível. Vamos voltar ao primeiro bug da introdução: failover do MiniMax.

ALLOY: Esse é o bug. Esse é o que estava pegando fogo em cima das pessoas.

NOVA: O problema original era classificação. Respostas genéricas de [EMPHASIS]api_error[/EMPHASIS] do MiniMax estavam sendo tratadas como transitórias por padrão. Então o OpenClaw tentava de novo em silêncio, suprimia a falha real e nunca acionava o fallback corretamente quando o problema subjacente era algo como billing, auth ou contexto malformado.

ALLOY: E essa é a distinção crucial. Um erro transitório é: talvez a rede espirrou, talvez o provider teve um tremor breve, talvez uma nova tentativa realmente funcione. Mas um problema de billing não é transitório. Um problema de auth não é transitório. Uma rejeição de formato ou contexto não é transitória. Repetir esses casos só desperdiça tempo e esconde a verdade.

NOVA: A correção é precisa. Não é “pare de tentar de novo no MiniMax”. É “só tente de novo quando o erro realmente parecer transitório”. [PAUSE] Esse é o tipo de correção em que eu confio, porque preserva o objetivo original do design — resiliência — enquanto remove a classificação relaxada que fazia a resiliência se comportar como ocultação.

ALLOY: E, para operadores, aqui vai o impacto prático: chave ruim, estado ruim de conta, request malformado, janela de contexto estourada — agora essas coisas deveriam falhar de um jeito que apareça e permita que o fallback entre corretamente. Era isso que as pessoas esperavam desde o começo.

NOVA: É um daqueles bugs em que a experiência degradada era quase pior do que uma falha dura, porque o usuário recebia output e presumia que ele era fiel.

ALLOY: Sim. Resposta errada sem alarme visível é mais assustadora do que falha visível. Pelo menos a falha visível convida a investigar.

NOVA: Próximo: o bug de reversão do token da OpenAI. Este é um exemplo perfeito de deriva de estado entre memória e disco causando traição ao usuário. O caminho de escrita do auth-profile do gateway estava permitindo que valores stale em memória sobrescrevessem credenciais recém-salvas no restart.

ALLOY: Então você colava o token, via verde, reiniciava, expirado. Toda vez. [PAUSE] É por isso que esse bug parecia tão pessoal. Ele atacava a confiança no ato básico de salvar credenciais.

NOVA: E a correção é que colar token agora grava corretamente no agent store resolvido, em vez de deixar o snapshot stale em memória vencer durante o restart.

ALLOY: O que significa que, depois do upgrade, você deveria testar isso. Não assuma só porque a release note diz que foi corrigido. Cole um token novo, reinicie o gateway, verifique se persistiu. Esse é exatamente o tipo de bug em que você ganha confiança reproduzindo a falha antiga e vendo que ela não acontece mais.

NOVA: Terceiro: cron e horário de verão. Isso parece chato até acertar algo de que você depende.

ALLOY: Isso me pegou. Meu relatório matinal estava disparando uma hora fora depois que os relógios mudaram.

NOVA: Exemplo concreto: você agenda um job para [EMPHASIS]8 AM[/EMPHASIS]. Chega o DST. Antes da .23, esse “8 AM” podia virar [EMPHASIS]7 AM[/EMPHASIS] ou [EMPHASIS]9 AM[/EMPHASIS], dependendo de como o scheduler interpretava a fronteira. [PAUSE] Isso não é só um desencontro cosmético. Para uma rotina diária, é uma promessa quebrada.

ALLOY: A correção é que [EMPHASIS]--at --tz[/EMPHASIS] agora honra o horário de relógio local ao atravessar fronteiras de DST. E o OpenClaw também rejeita [EMPHASIS]--tz[/EMPHASIS] com [EMPHASIS]--every[/EMPHASIS], o que é bom porque semântica de intervalo recorrente e semântica de horário local com timezone não são a mesma coisa.

NOVA: Esse é o tipo de restrição que salva usuários de intuições falsas.

ALLOY: Exatamente. Se você quer dizer “a cada seis horas”, isso não é a mesma coisa que “quando meu relógio local marca oito”. A ferramenta agora reflete essa diferença em vez de embaralhá-la.

NOVA: Quarto: a correção de [EMPHASIS]422[/EMPHASIS] do Mistral. Configs persistidas antigas do Mistral vinham carregando limites de output do tamanho do contexto que o Mistral rejeita de imediato. Resultado: erros [EMPHASIS]422[/EMPHASIS] que parecem misteriosos se você não conhece a linhagem da config.

ALLOY: E, mais uma vez, [EMPHASIS]openclaw doctor --fix[/EMPHASIS] está fazendo trabalho real aqui. Agora ele detecta e corrige essas configs stale do Mistral.

NOVA: Mais um motivo para rodar [EMPHASIS]doctor --fix[/EMPHASIS]. As pessoas às vezes ouvem esse comando como uma espécie de consulta genérica, tipo talvez ele arrume umas coisas óbvias. Não. Nesta sequência de releases, ele está codificando conhecimento de migração.

ALLOY: Quinto: ClawHub no macOS. Duas questões aqui. Credenciais salvas não estavam respeitando corretamente o caminho do macOS Application Support, e o comportamento de browse-all estava batendo em rate limits [EMPHASIS]429[/EMPHASIS] sem autenticação.

NOVA: O que significa que a UI podia te induzir a pensar que o ClawHub estava vazio ou quebrado de maneiras vagas.

ALLOY: A navegação de skills estava caindo silenciosamente para modo não autenticado no macOS. Você via listas vazias e assumia que não existiam skills, ou achava que sua instalação estava quebrada, quando, na verdade, o tratamento do caminho de auth estava errado. [PAUSE] As correções foram respeitar o caminho correto de auth e trocar o browse-all para o endpoint de busca, o que é uma forma muito mais sensata de evitar throttling não autenticado sem sentido.

NOVA: Sexto: runtimes bundled de plugin. Sidecars de runtime de WhatsApp e Matrix estavam ausentes do pacote npm, o que significava que instalações globais podiam falhar de um jeito que parecia voodoo de empacotamento.

ALLOY: Isso é uma regressão das mudanças de empacotamento da .22, e, crédito ao OpenClaw, foi corrigido rápido na .23. Mas, se você roda esses runtimes de forma global, isso não é rodapé. Sidecars ausentes significam que a stack do plugin simplesmente não está completa.

NOVA: Sétimo: tratamento stale de provider no [EMPHASIS]web_search[/EMPHASIS]. A ferramenta estava usando qualquer state de provider que tivesse sido embutido no startup em vez da config ativa de runtime.

ALLOY: Que é exatamente o tipo de bug que faz você questionar se reload de config é real ou só decorativo.

NOVA: Você configura Brave, ele deveria usar Brave. Sempre deveria ter funcionado assim.

ALLOY: E agora funciona. De novo, não é glamouroso, mas é um reparo direto da expectativa versus comportamento.

NOVA: Oitavo: threading do Telegram. [EMPHASIS]currentThreadTs[/EMPHASIS] agora é populado no fallback de tool-context de threading para tópicos de DM do Telegram, então ferramentas thread-aware de fato recebem o contexto correto do tópico.

ALLOY: Essa é uma daquelas correções em que, se você não usa tópicos de DM no Telegram, você dá de ombros, e, se usa, diz graças a Deus. Porque tool context cego a thread é como você acaba com agentes respondendo no lugar errado ou perdendo a faixa da conversa.

NOVA: O que é especialmente doloroso em um sistema construído em torno de fidelidade de contexto.

ALLOY: Exatamente. O ponto todo é que a ferramenta deveria saber onde está.

NOVA: Então, olhando tudo junto, a release .23 não é chamativa no sentido tradicional de produto. É um reliability pass no sentido mais profundo da expressão. Ela aperta classificação, persistência de state, semântica de scheduler, wiring de providers, completude de empacotamento e contexto de thread.

ALLOY: Ela torna o novo mundo da .22 realmente habitável.

NOVA: E eu acho que é por isso que operadores deveriam ler essas duas releases como uma história só com dois capítulos. O capítulo um diz: “removemos os compromissos antigos”. O capítulo dois diz: “corrigimos os lugares em que as novas suposições ainda tinham arestas”. [PAUSE] Esse é um ritmo de desenvolvimento muito mais honesto do que fingir que a grande limpeza chegou perfeita no primeiro dia.

ALLOY: É. Eu realmente respeito a .23 porque ela não tenta esconder o que a .22 desestabilizou. Ela só corrige. Rápido. Diretamente. Sem ego.

NOVA: E, como usuário, é isso que você quer depois de uma release estrutural. Não negação. Correção rápida.

ALLOY: Especialmente para as coisas silenciosas. Fallback do MiniMax, persistência de token, config stale de provider — todos esses são bugs que corroem a confiança porque fazem o sistema parecer menos legível do que deveria.

NOVA: Confiabilidade é em parte correção e em parte compreensibilidade. A plataforma precisa fazer a coisa certa, e você precisa conseguir entender por que ela fez o que fez.

ALLOY: É por isso que a .23 importa mais do que importaria uma release de feature.

NOVA: Concordo.

## [31:00-35:00] Qwen, CSP e as Pequenas Coisas

NOVA: Vamos às mudanças menores, porque elas só são menores em área de superfície, não necessariamente em importância. Primeiro: [EMPHASIS]Qwen[/EMPHASIS] e [EMPHASIS]DashScope[/EMPHASIS]. O OpenClaw agora suporta endpoints padrão do DashScope para chaves de API do Qwen na China e globais, e o provider foi relabelado como [EMPHASIS]Qwen (Alibaba Cloud Model Studio)[/EMPHASIS].

ALLOY: Chaves pay-as-you-go agora funcionam. Essa é a mudança prática. Se você está fora da órbita padrão OpenAI-Anthropic, isso importa bastante.

NOVA: Qwen é uma das melhores famílias open-weight agora. Suporte adequado ao DashScope significa acessibilidade real para usuários que querem modelos fortes sem serem forçados aos mesmos dois ecossistemas de provider que todo mundo assume.

ALLOY: E uma nomenclatura melhor também importa. Relabelar para a identidade completa de Model Studio deixa a superfície de config menos críptica.

NOVA: Próximo: hardening de [EMPHASIS]CSP[/EMPHASIS]. Hashes SHA-256 para blocos de script inline. Scripts inline bloqueados por padrão.

ALLOY: Se você roda OpenClaw atrás de um reverse proxy rígido, esta é a versão para a qual fazer upgrade.

NOVA: Isso importa para segurança de supply chain. Um script injetado não vai executar porque o hash não vai bater. [PAUSE] Esse é o tipo de controle que não deixa uma demo mais bonita, mas deixa seu raio de dano menor.

ALLOY: E, francamente, plataformas maduras fazem isso. Elas param de depender de “bom, ninguém deveria injetar ali” e passam a construir em torno de “se alguma coisa for injetada, o que ainda assim não vai rodar?”.

NOVA: O tema [EMPHASIS]Knot[/EMPHASIS] também recebeu atenção: conformidade de contraste [EMPHASIS]WCAG 2.1 AA[/EMPHASIS], ajuste da paleta preto e vermelho, ícones de config, degraus discretos de arredondamento.

ALLOY: A correção de contraste AA é a que importa. Estava falhando em checks de acessibilidade. Estilo é divertido; legibilidade é obrigatória.

NOVA: E eu sempre gosto quando melhorias de acessibilidade são tratadas como melhorias padrão de qualidade, em vez de uma missão lateral de nicho.

ALLOY: Última pequena: os totais de uso do gateway agora incluem sessões rotacionadas e arquivadas.

NOVA: O que soa quase como contabilidade.

ALLOY: É contabilidade. Mas o uso estava sendo subcontado. Agora não está mais. Se você está tentando entender a carga real do sistema ou comparar atividade ao longo do tempo, deixar sessões arquivadas de fora não é erro de arredondamento. Está simplesmente errado.

NOVA: Então até as pequenas coisas nessas releases apontam na mesma direção: menos ambiguidades, menos omissões, representação mais precisa do que o sistema está realmente fazendo.

## [35:00-38:00] O Checklist de Upgrade

ALLOY: Certo, vamos tornar isso concreto. Se você vai fazer upgrade, aqui está o checklist, e digo checklist literalmente. Não confie em si mesmo para lembrar disso no meio da migração.

NOVA: O passo um é inegociável.

ALLOY: [EMPHASIS]openclaw doctor --fix[/EMPHASIS]. Primeiro, antes de qualquer outra coisa. E, honestamente, logo depois de cada etapa de upgrade também, se você estiver fazendo a sequência de forma limpa.

NOVA: Este é o comando âncora dessas releases. Não é algo bom de ter. É âncora.

ALLOY: Passo dois: dê grep em [EMPHASIS]CLAWDBOT_*[/EMPHASIS] e [EMPHASIS]MOLTBOT_*[/EMPHASIS] em todos os arquivos [EMPHASIS].env[/EMPHASIS], arquivos Docker, units do systemd, shell profiles, toda superfície de startup que você tiver.

NOVA: Se os nomes antigos existirem, assuma que agora eles são config morta.

ALLOY: Passo três: verifique se existe [EMPHASIS]~/.moltbot[/EMPHASIS]. Se existir, mova o state para [EMPHASIS]~/.openclaw[/EMPHASIS] ou defina [EMPHASIS]OPENCLAW_STATE_DIR[/EMPHASIS] explicitamente.

NOVA: Passo quatro: defina [EMPHASIS]agents.defaults.imageGenerationModel.primary: "google/gemini-3-pro-image-preview"[/EMPHASIS]. Não deixe geração de imagem num limbo indefinido.

ALLOY: Passo cinco: depois do upgrade, teste novamente o MiniMax com uma chave ruim e confirme que o fallback dispara. Não mande só um prompt happy path. Induza o modo antigo de falha.

NOVA: Passo seis: cole um token da OpenAI, reinicie o gateway e confirme que ele persistiu. Confie, mas verifique.

ALLOY: Passo sete: se você tem plugins customizados, migre de [EMPHASIS]openclaw/extension-api[/EMPHASIS] para [EMPHASIS]openclaw/plugin-sdk/*[/EMPHASIS]. Leia os docs de migração. Não trate erros de compilação como mapa.

NOVA: Passo oito: faça um spot-check nas skills do ClawHub depois da mudança de comportamento de instalação. Garanta que seus scripts e expectativas ainda correspondem ao que está sendo resolvido.

ALLOY: Passo nove: verifique jobs de cron usando [EMPHASIS]--at --tz[/EMPHASIS], especialmente se o DST já te queimou antes.

NOVA: O resumo mais profundo é que essas duas releases juntas são o OpenClaw concluindo o que começou. Os nomes Moltbot e Clawdbot sumiram. O extension relay sumiu. O plugin SDK está unificado. As falhas silenciosas foram corrigidas.

ALLOY: Doctor [EMPHASIS]--fix[/EMPHASIS] primeiro. Todo o resto é condicional ao que você está rodando. Mas [EMPHASIS]doctor --fix[/EMPHASIS] é incondicional.

NOVA: Esta é a plataforma que você queria que ele fosse.

## [38:00-39:30] Encerramento

ALLOY: E acho que essa é a nota certa para terminar. Essas releases são exigentes, mas são exigentes a serviço de algo real: uma plataforma que diz o que é, faz o que diz e carrega menos fantasmas de eras anteriores.

NOVA: O que, para uma ferramenta como OpenClaw, importa mais do que novidade. [PAUSE] Confiabilidade é uma feature. Consistência de nomenclatura é uma feature. Pressão de migração honesta é uma feature. Uma stack de navegador com menos pontes improvisadas é uma feature.

ALLOY: E, se você está no meio do upgrade agora, respire, faça o checklist, rode [EMPHASIS]openclaw doctor --fix[/EMPHASIS], e não pule as etapas de verificação só porque o serviço voltou a subir.

NOVA: Você pode encontrar as show notes, todos os links que mencionamos e o arquivo de episódios em [EMPHASIS]tobyonfitnesstech.com[/EMPHASIS]. Isso é [EMPHASIS]tobyonfitnesstech.com[/EMPHASIS].

ALLOY: Se este episódio te salvou de um setup de navegador quebrado, uma env var desaparecida ou mais uma falha misteriosa de auth, então ele fez o trabalho dele.

NOVA: Eu sou NOVA.

ALLOY: Eu sou Alloy.

NOVA: E isto foi OpenClaw Daily. Voltaremos em breve.

ALLOY: Até breve.
