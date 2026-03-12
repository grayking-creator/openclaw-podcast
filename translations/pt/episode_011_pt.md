# OpenClaw Daily Episode 11

## "OpenClaw Vai para Hardware: A Camada de Agentes Ficou Real"

---

## Segmento 1 — Lançamento: OpenClaw v2026.3.7

[NOVA]: Bem-vindos de volta ao OpenClaw Daily, pessoal. Eu sou a Nova.

[ALLOY]: E eu sou o Alloy. É um prazer estar com você novamente, Nova. Estava ansioso por este episódio.

[NOVA]: Eu também. Temos um lançamento genuinamente empolgante para conversar hoje, além de algumas notícias importantes sobre hardware, alguns casos de uso fascinantes da comunidade, e todas as atualizações habituais. Vamos direto ao assunto.

[ALLOY]: Com certeza. Qual é a grande novidade no fronts de lançamentos?

[NOVA]: O OpenClaw v2026.3.7 está fora, e honestamente, este pode ser o lançamento mais substancial que vimos nos últimos meses. Há muito o que analisar aqui, então vamos passar por isso sistematicamente.

[ALLOY]: Estou pronto. Me dá os destaques.

[NOVA]: Ok, vamos começar com o que estou chamando de funcionalidade adormecida de todo o lançamento. Você está pronto para isso? A Interface de Plugin do Motor de Contexto.

[ALLOY]: Ooh, isso parece técnico. Para quem não está tão por dentro, o que isso realmente significa na prática?

[NOVA]: Ótima pergunta. Então, anteriormente, o Motor de Contexto — a parte do OpenClaw que gerencia memória e contexto entre conversas — era meio que uma coisa fixa. Funcionava bem, mas você não podia realmente personalizar como ele lidava com memória, como ele compactava informações, o que era lembrado e o que era descartado.

[ALLOY]: Certo, era uma caixa preta.

[NOVA]: Exatamente. Agora, com a Interface de Plugin do Motor de Contexto, ela é totalmente conectável. Você pode conectar estratégias de memória personalizadas e estratégias de compactação. Estamos falando de hooks de ciclo de vida para bootstrap, ingest, assemble, compact, afterTurn, prepareSubagentSpawn, onSubagentEnded.

[ALLOY]: Isso é um conjunto completo de hooks. Você realmente pode entrar em cada estágio do ciclo de vida da conversa.

[NOVA]: Pode. E aqui está a parte realmente convincente: existe um plugin chamado lossless-claw que pode substituir completamente como o contexto é gerenciado. Contexto sem perda significa que nada — nem um único token — é descartado do histórico da conversa.

[ALLOY]: Isso é enorme para certos casos de uso. Processos legais, requisitos de conformidade, qualquer coisa onde você precisa de uma trilha de auditoria completa.

[NOVA]: Exatamente. E a coisa bonita é, se você não quer nada disso, se está feliz com o comportamento padrão, há zero de mudança. Tudo simplesmente funciona como antes. Sem mudanças que quebram configurações existentes.

[ALLOY]: Essa é a abordagem certa. Não force as pessoas a mudarem se elas estão felizes.

[NOVA]: Concordo. Agora, passando para algo que tem sido solicitado por um tempo. Enlaces de Canal ACP Duráveis para Discord e Telegram.

[ALLOY]: Ah, sei exatamente o que é isso. É sobre a sobrevivência dos tópicos durante reinicializações do gateway, certo?

[NOVA]: É isso mesmo. Anteriormente, se seu gateway caísse — talvez você tenha reiniciado para uma atualização, talvez tenha havido uma interrupção — quando ele voltasse, você perderia a continuidade do tópico. O contexto da conversa nos threads do Discord ou tópicos do Telegram seria perdido.

[ALLOY]: Isso era frustrante. Você teria que explicar tudo novamente para seu agente.

[NOVA]: Exatamente. Agora, os tópicos sobrevivem às reinicializações do gateway. O estado é preservado. É uma melhoria de qualidade de vida que foi solicitada desde os primeiros dias.

[ALLOY]: Lembro-me de ver essas reclamações. Que bom que isso foi corrigido.

[NOVA]: E construindo sobre essa base, temos roteamento de agente por tópico para grupos de fórum do Telegram. Isso é genuinamente legal.

[ALLOY]: Me conta mais. Não tenho certeza se entendi completamente.

[NOVA]: Ok, então no Telegram, você pode ter grupos de fórum com múltiplos tópicos — como threads dentro de um grupo. Anteriormente, todos esses tópicos iam para o mesmo agente. Agora, cada tópico pode ir para um agente diferente, com sessões completamente isoladas.

[ALLOY]: Oh! Então você poderia ter um fórum com uma dúzia de tópicos diferentes, cada um tratado por um agente especialista?

[NOVA]: Precisamente. Um agente para perguntas de suporte, um para dúvidas sobre faturamento, um para documentação técnica, um para chat geral. Todos eles são completamente isolados um do outro. Eles não compartilham contexto a menos que você configure explicitamente para isso.

[ALLOY]: Isso é incrivelmente poderoso para gerentes de comunidade ou empresas que executam fóruns do Telegram. Você pode ter agentes especialistas sem precisar de grupos de chat separados para cada um.

[NOVA]: É elegante. Agora, vamos falar sobre sub-agentes. Houve uma atualização na forma como você pode passar arquivos para eles.

[ALLOY]: Qual é a mudança?

[NOVA]: sessions_spawn agora aceita arquivos base64 ou UTF-8 diretamente como anexos inline. Você não precisa configurar armazenamento externo, não precisa fazer upload para S3 ou algo assim. Basta passar o conteúdo do arquivo diretamente.

[ALLOY]: Isso simplifica muito. Para fluxos de trabalho que precisam processar documentos ou arquivos de dados, isso vai economizar muita complexidade.

[NOVA]: Deveria. Agora, para usuários do Telegram especificamente, streaming agora é ativado por padrão. Nenhuma configuração necessária.

[ALLOY]: Isso é legal. Sempre achei um pouco estranho que não fosse ativado por padrão, na verdade.

[NOVA]: Yeah, era uma solicitação comum. Agora é simplesmente como funciona fora da caixa.

[ALLOY]: Bom. Agora, vamos falar sobre segurança, porque houve algum trabalho importante ali.

[NOVA]: O SecretRef passou por uma reformulação completa. Agora há 64 destinos de credenciais suportados, o que é um aumento significativo. E ele falha rápido — se algo estiver mal configurado, você saberá imediatamente em vez de ter algo que simplesmente não funciona silenciosamente.

[ALLOY]: Isso é importante. Segurança que falha alto é muito melhor do que segurança que falha silenciosamente. Se algo estiver mal configurado, você quer saber imediatamente, não descobrir seis meses depois que suas credenciais realmente não estavam funcionando.

[NOVA]: Com certeza. Agora, a busca também recebeu uma melhoria. A API de Busca do Perplexity agora retorna resultados estruturados com filtros. Isso significa que você pode obter respostas de busca muito mais direcionadas, e elas são estruturadas de uma forma que facilita para os agentes analisarem e usarem sem precisar fazer muito pós-processamento.

[ALLOY]: Isso vai ser útil para qualquer agente que precisa fazer pesquisa. A saída estruturada faz uma grande diferença quando você está tentando extrair informações específicas dos resultados de busca.

[NOVA]: Realmente faz. Antes, você recebia um blob de texto e tinha que descobrir o que era relevante. Agora, os resultados vêm pré-analisados, pré-estruturados, prontos para seu agente trabalhar.

[ALLOY]: Isso é uma melhoria de qualidade de vida para desenvolvedores que constroem aplicações de agentes. Agora, usuários de iOS, há uma boa notícia para vocês. O preparo para o App Store Connect com o Fastlane está pronto.

[NOVA]: Fastlane! Esse é o padrão para CI/CD do iOS. Então, se alguém quiser construir um aplicativo iOS que usa o OpenClaw, a estrutura está ali?

[ALLOY]: Exatamente. Agora você pode integrar o OpenClaw ao seu pipeline de implantação de aplicativos iOS usando o Fastlane. Isso é um grande negócio para qualquer pessoa que construa produtos iOS com capacidades de agente.

[NOVA]: Isso é enorme. Estava esperando por isso.

[ALLOY]: E temos suporte de primeira linha para o Gemini 3.1 Flash-Lite. É agora um modelo suportado fora da caixa, sem necessidade de configuração personalizada.

[NOVA]: O Google temempurrado esse modelo bastante. É uma escolha sólida para requisitos de modelo mais rápidos e leves.

[ALLOY]: É. Agora, para quem hospeda por conta própria, há um build Docker multi-stage slim. Você pode definir OPENCLAW_VARIANT=slim e obter uma imagem de container muito mais enxuta.

[NOVA]: Imagem menor significa implantações mais rápidas e menos armazenamento. Sempre bem-vindo.

[ALLOY]: Com certeza. Agora, aqui está o ponto criticamente importante que todos precisam ouvir. Há uma mudança que quebra neste lançamento.

[NOVA]: Oh, estava me perguntando quando chegaríamos a isso. Qual é a mudança?

[ALLOY]: Se você tiver tanto gateway.auth.token quanto gateway.auth.password definidos na sua configuração, você deve adicionar gateway.auth.mode e defini-lo como token ou password. Se você não adicionar esse campo de modo, o gateway não will start.

[NOVA]: Essa é uma mudança que quebra claramente. As pessoas precisam verificar suas configurações antes de atualizar.

[ALLOY]: Exatamente. Então, antes de qualquer um atualizar para v2026.3.7, eles precisam olhar sua configuração gateway.auth. Se eles tiverem tanto token quanto password definidos, eles precisam adicionar o campo de modo. Vamos falar sobre isso no final do episódio também, porque é tão importante assim.

[NOVA]: Entendi. Não vamos deixar ninguém esquecer.

[ALLOY]: Agora, Nova, você mencionou antes que deberíamos fazer um aprofundamento no Motor de Contexto. Acho que o público apreciaria isso.

[NOVA]: Eu acho. Acho que isso merece uma olhada adequada, porque é honestamente uma das adições mais poderosas ao OpenClaw que já vi em um tempo. Vamos detalhar.

[ALLOY]: Ok, então a Interface de Plugin do Motor de Contexto — o que alguém pode realmente fazer com isso?

[NOVA]: Então, anteriormente, o gerenciamento de contexto era fixo. Você recebia o que recebia. Agora você pode personalizar cada aspecto dele. Você pode conectar estratégias de memória personalizadas em cada estágio do ciclo de vida. Você pode definir exatamente como a informação é comprimida, o que é priorizado, como as sessões são montadas.

[ALLOY]: E o plugin lossless-claw?

[NOVA]: Esse é o plugin principal. Contexto sem perda significa que cada token de cada conversa é preservado. Nada é descartado, nada é comprimido, nada é esquecido.

[ALLOY]: Parece que isso usaria muita memória muito rapidamente.

[NOVA]: Usa, e esse é o trade-off. Contexto sem perda é caro em termos de memória e tokens, mas para casos de uso onde você absolutamente não pode perder informação, é essencial. Trabalho jurídico, conformidade, análise detalhada, raciocínio multi-turn complexo — todos são casos onde o contexto sem perda brilha.

[NOVA]: Exatamente. E a arquitetura de plugins significa que você pode escolher seu trade-off. Sem perda quando você precisa, a compactação padrão para uso normal, ou escreva sua própria estratégia personalizada que equilibra memória e fidelidade exatamente como você quer.

[ALLOY]: Esse é o poder de ter um sistema aberto. Você pode construir exatamente o que precisa.

[NOVA]: Com certeza. Agora, e sobre roteamento por tópico? Parece que isso poderia mudar como as pessoas configuram suas comunidades do Telegram.

[ALLOY]: Realmente poderia. Pense nisso: você tem um grupo de fórum com dezenas de tópicos. Antes, todos esses tópicos iam para o mesmo agente. Agora, cada tópico pode ter seu próprio agente dedicado com sua própria sessão isolada.

[NOVA]: Então você poderia ter um agente para suporte, um para faturamento, um para feedback de produto, um para chat geral.

[ALLOY]: Exatamente. E eles não interferem um com o outro. Cada um mantém seu próprio contexto, seu próprio histórico, seu próprio estado. É como ter múltiplos agentes em um grupo, mas sem a complexidade de gerenciar grupos de chat separados.

[NOVA]: Isso é realmente elegante. Eu adoro esse design.

[ALLOY]: Eu também. É um ótimo exemplo de como o OpenClaw continua ficando mais poderoso sem ficar mais complicado de usar.

[NOVA]: Ok, isso foi o lançamento. Vamos passar para algumas notícias emocionantes de hardware.

---

## Segmento 2 — SwitchBot AI Hub

[NOVA]: Então Alloy, você ouviu abuzz sobre o SwitchBot AI Hub?

[ALLOY]: Ouvi, e estou extremamente animado com isso. Este é um enorme desenvolvimento para o ecossistema OpenClaw. Este é o primeiro dispositivo de hardware que executa o OpenClaw nativamente.

[NOVA]: Sim. Sem PC necessário. Sem dependência de nuvem também. Está sempre ativo logo fora da caixa, 24/7, executando em hardware dedicado na sua casa.

[ALLOY]: Esse é o diferenciador. A maioria das plataformas de agentes requer que você tenha algum tipo de servidor ou computador funcionando. Você precisa manter seu laptop ligado, ou configurar um Raspberry Pi, ou alugar um servidor em nuvem. Este é o primeiro produto de consumidor que simplesmente funciona. Você conecta, e você tem um agente OpenClaw funcionando.

[NOVA]: E não é como se fosse alguma versão reduzidatambém. Este negócio está lotado de capacidades. Tem VLM — modelos de linguagem de visão — então pode entender imagens e vídeo.

[ALLOY]: Isso mesmo. E tem integração completa com casa inteligente. Estamos falando Home Assistant, Apple Home, Google Home. Ele pode controlar suas luzes, seu termostato, suas fechaduras, suas câmeras, suas campainhas, tudo.

[NOVA]: Então ele se torna este hub central para toda a sua casa inteligente, alimentado por um agente OpenClaw.

[ALLOY]: Exatamente. E tem capacidades de NVR local com Frigate. Então você pode ter vigilância de vídeo, tudo processado localmente no dispositivo. Sem câmeras de nuvem, sem serviços de assinatura.

[NOVA]: Isso é enorme para privacidade. Tudo fica na sua casa.

[ALLOY]: Tudo fica local. Seus feeds de vídeo, seus dados, a memória do seu agente. Zero dependência de nuvem.

[NOVA]: Adoro essa filosofia. É a abordagem anti-SaaS. Você ownsua seu hardware, você ownsseus dados.

[ALLOY]: Com certeza. E como você se comunica com ele?

[NOVA]: WhatsApp, iMessage e Discord. Então você pode usar qualquer plataforma de mensagens que já prefira. Nenhum novo aplicativo para aprender, nenhum cliente especial para instalar.

[NOVA]: É a decisão certa. Encontre as pessoas onde elas já estão.

[ALLOY]: Agora, algo para realmente ansiar: SwitchBot Skills para OpenClaw estãorolando no final de março.

[NOVA]: Então em apenas algumas semanas, vamos ver integrações dedicadas do OpenClaw da SwitchBot. Mais capacidades, mais integração estreita.

[ALLOY]: Esse é o plano. Essas habilidades vão permitir que você faça ainda mais com o hardware. Vai desbloquear muitos novos casos de uso.

[NOVA]: Este é um momento realmente significativo para o OpenClaw. É a plataforma indo para hardware-nativo. Não é mais apenas software executando em computadores de propósito geral. É um produto físico que as pessoas podem comprar, desembalar e executar em suas casas.

[NOVA]: E o ângulo aqui é realmente importante: zero dependência de nuvem. A maioria dos produtos de casa inteligente hoje em dia quer que você se inscreva no serviço de nuvem deles, compartilhe seus dados, dependa dos servidores deles. Esta é a abordagem completamente oposta.

[NOVA]: É propriedade. Você está executando o agente você mesmo, no seu próprio hardware, controlando sua própria casa inteligente. Sem intermediário, sem assinatura, sem dados saindo das suas dependências a menos que você explicitamente queira.

[NOVA]: Eu acho que isso vai ressoar com muitas pessoas. Especialmente à medida que as pessoas se tornam mais conscientes sobre privacidade e mais cansadas de assinaturas.

[ALLOY]: Com certeza. E não é como se você estivesse sacrificando capacidade para obter essa privacidade. VLM, controle de casa inteligente, NVR local, mensagens em múltiplas plataformas. Isso é uma configuração completa que rivaliza com qualquer solução baseada em nuvem.

[NOVA]: É hardware impressionante. Estou genuinamente animado para ver onde isso vai. Este é o OpenClaw entrando em espaços físicos de uma forma que não vimos antes.

[ALLOY]: Concordo. Vamos ficar de olho naquelas SwitchBot Skills saindo no final de março. Vai ser um grande momento.

[NOVA]: Com certeza. Agora, vamos falar sobre algo mais que tem gerado muito burburinho na comunidade.

---

## Segmento 3 — 50+ Casos de Uso Reais do OpenClaw

[NOVA]: Então tem um artigo da comunidade de sidsaladi no Substack que está circulando. Ele cataloga mais de cinquenta casos de uso do mundo real para o OpenClaw.

[ALLOY]: Esse é um recurso fantástico. É uma coisa falar sobre o que o OpenClaw pode fazer tecnicamente, mas é outra completamente diferente ver como as pessoas estão realmente usando em suas vidas e negócios diários.

[NOVA]: Exatamente. Deixa eu pegar alguns e podemos conversar sobre quais ressoam mais conosco.

[ALLOY]: Parece bom. Vamos ouvi-los.

[NOVA]: Ok, primeiro caso de uso: triagem automática da caixa de entrada, rascunho de respostas, e apenas mostrar as coisas que realmente precisam de uma decisão humana.

[ALLOY]: Oh, isso é tão bom. Pense em quanto desordem de e-mail a maioria das pessoas lida todos os dias. Newsletters, notificações, mensagens automatizadas, spam, e-mails importantes reais. É uma mangueira de incêndio.

[NOVA]: Realmente é.

[ALLOY]: Então, em vez de navegar por tudo você mesmo, seu agente OpenClaw lê sua caixa de entrada, rascunha respostas para as coisas rotineiras, e apenas sinaliza as decisões genuinamente importantes para você. As coisas que realmente precisam de um toque humano.

[NOVA]: Transforma o e-mail de uma mangueirade incêndio em um feed curado. Você está lidando apenas com as coisas que realmente importam.

[ALLOY]: Exatamente. E o agente pode aprender com seu feedback também. Com o tempo, ele fica melhor em saber o que é importante para você e o que não é.

[NOVA]: Esse é o poder de ter um agente que vive no seu fluxo de trabalho. Ele aprende suas preferências, suas prioridades, seu estilo de comunicação.

[ALLOY]: Com certeza. Esse é um que pode economizar horas toda semana para alguém que lida com muito e-mail.

[NOVA]: Ok, segundo caso de uso: freelancer roteando mensagens de Slack de clientes através do OpenClaw, que registra horas faturáveis automaticamente.

[ALLOY]: Isso é inteligente. Então o agente não está apenas transmitindo mensagens entre o freelancer e seu cliente, ele está fazendo controle de tempo ao mesmo tempo.

[NOVA]: Certo. Cada conversa com um cliente é automaticamente registrada como tempo faturável. Sem controle de tempo manual, sem esquecer de registrar horas, sem scramble no final do mês para reconstruir no que você trabalhou.

[ALLOY]: Isso vai economizar muito trabalho administrativo para freelancers. E todos nós sabemos quanto freelancers odeiam trabalho administrativo.

[NOVA]: É o pior. Isso permite que eles foquem em realmente fazer o trabalho em vez de rastrear o trabalho.

[ALLOY]: Adoro isso. Ok, o que vem depois?

[NOVA]: Terceiro caso de uso: usuário de casa inteligente recebendo uma verificação "tem alguém em casa?" via WhatsApp usando feeds de câmera.

[ALLOY]: Isso é prático. Você está longe de férias, ou está no trabalho, e quer saber se tem alguém em casa. Você apenas envia uma mensagem para seu agente OpenClaw pelo WhatsApp e pergunta.

[NOVA]: E ele verifica as cameras, processa o vídeo, e dá um status update. Tem alguém em casa? Sim ou não. Talvez até detalhes sobre quem viu ou qual atividade detectou.

[ALLOY]: Perfeito para paz de espírito quando você está fora. E porque isso é tudo local com o hub SwitchBot que conversamos agora, isso poderia acontecer sem serviços externos absolutamente.

[NOVA]: Certo. Sem nuvem, sem terceiros, apenas seu agente verificando suas câmeras e respondendo sua pergunta. Privacidade intacta.

[ALLOY]: Esse é o sonho. Ok, o que vem depois?

[NOVA]: Quarto: criador gerando automaticamente rascunhos de newsletter a partir do histórico do navegador e favoritos.

[ALLOY]: Isso é interessante. Então o agente junta tudo o que você está lendo, tudo o que você salvou, e usa isso para rascunhar uma newsletter para você.

[NOVA]: Em vez de ficar olhando para uma página em branco tentando lembrar sobre o que queria escrever, o agente curaciona toda a sua leitura recente e apresenta um ponto de partida.

[ALLOY]: Isso pode realmente ajudar com consistência. Muitos criadores lutam para aparecer regularmente. Se seu agente pode pelo menos dar um primeiro rascunho baseado no que você já está consumindo, isso é um começo enorme.

[NOVA]: Exatamente. É como ter um assistente de pesquisa que faz o trabalho de perna para você.

[ALLOY]: Gosto disso. Ok, último para hoje?

[NOVA]: Último: check-in no Telegram no final do dia para humor e acompanhamento de diário.

[NOVA]: Esse é um caso de uso pessoal-legal. Em vez de ter que abrir manualmente um aplicativo de diário e digitar seus pensamentos, você apenas envia uma mensagem para seu agente no Telegram.

[NOVA]: O agente solicita, pergunta como você está, o que aconteceu hoje, pelo que é grato. Ele registra seu humor e seus pensamentos. É como um companheiro digital que faz check-in com você.

[ALLOY]: Isso torna o diário tão baixo em atrito. Você não tem que tomar uma decisão para fazer diário, você apenas responde quando seu agente pergunta. É assim que você constrói o hábito.

[NOVA]: Exatamente. Não é sobre substituir o diário, é sobre torná-lo sem esforço.

[NOVA]: Todos são tão diferentes, certo? De produtividade de negócios para bem-estar pessoal para automação de casa. Isso realmente mostra a amplitude do que o OpenClaw pode fazer.

[NOVA]: E esses são apenas cinco de mais de cinquenta. A comunidade está encontrando aplicações que provavelmente nunca imaginamos quando estávamos construindo a plataforma.

[ALLOY]: Essa é a magia do open source. Você constrói as ferramentas, a comunidade encontra os casos de uso.

[NOVA]: Adoro ver o que as pessoas constroem. É genuinamente inspirador toda vez.

[ALLOY]: Com certeza. Devemos linkar aquele artigo nas notas do show para as pessoas explorarem todos os cinquenta e mais casos de uso.

[NOVA]: Ótima ideia.

---

## Segmento 4 — Novita OpenClaw CLI

[NOVA]: Agora, vamos falar sobre algo que torna a implantação do OpenClaw muito mais fácil para pessoas que não querem lidar com infraestrutura.

[ALLOY]: O que é isso?

[NOVA]: Há uma nova ferramenta chamada Novita OpenClaw CLI. E ela faz exatamente o que diz na lata. É implantação em nuvem persistente com um comando.

[ALLOY]: Um comando? Isso é incrivelmente simples.

[NOVA]: Um comando. Você roda, e sua instância do OpenClaw é implantada e executada na nuvem. Sem configuração manual de servidor, sem arquivos de configuração para lidar, sem scripts de implantação para escrever.

[ALLOY]: Isso é drasticamente simplificado. O que costumava levar horas de configuração e implantação agora pode ser feito com um único comando.

[NOVA]: Essa é a ideia. E é persistente — seu agente continua funcionando. Não é uma função serverless que para entre requisições. É uma implantação persistente que continua, pronta para responder sempre que você precisar.

[NOVA]: Isso é importante para casos de uso onde você precisa de agentes sempre ativos, como as coisas de casa inteligente que discutimos antes. Você quer seu agente disponível 24/7, não acordando de cold start toda vez que faz uma pergunta.

[ALLOY]: Com certeza. E há uma citação realmente ótima do Andrej Karpathy que captura por que isso importa. Deixa eu ler exatamente:

[ALLOY]: "Assim como agentes LLM emergiram como uma nova camada em cima de LLMs, Claws são a próxima camada em cima de agentes — levando orquestração, agendamento, contexto, chamadas de ferramenta e persistência mais longe do que agentes sozinhos."

[NOVA]: Isso é uma articulação realmente limpa do que é a camada de agente. Karpathy entende. Ele está pensando sobre essas coisas há muito tempo.

[ALLOY]: Ele realmente entende o espaço. E esta CLI está tornando essa camada acessível para mais pessoas. Você não precisa mais ser um especialista em DevOps para rodar o OpenClaw na nuvem.

[NOVA]: É a democratização da implantação de agentes. Qualquer pode fazer, independentemente do seu histórico técnico.

[ALLOY]: Exatamente. E acho que veremos mais ferramentas assim. A tendência na indústria é hacia tornar a implantação de agentes o mais fácil possível. A parte difícil deve ser construir a lógica do agente, não descobrir como hospedá-lo.

[NOVA]: É o futuro para o qual estamos nos direcionando. Infraestrutura como commodity, inteligência como diferencial.

[NOVA]: Bem dito. A Novita está cuidando do lado da infraestrutura, então você só precisa focar em usar o OpenClaw e construir seus agentes.

[NOVA]: Isso é grande. Abaixo significativamente a barreira de entrada.

[ALLOY]: Com certeza. E estou animado para ver o que as pessoas constroem com isso.

---

## Segmento 5 — Guia de Auto-Hospedagem

[NOVA]: Agora, se você quer ir ainda mais hands-on e ter controle completo sobre sua configuração, há um guia completo de auto-hospedagem no dev.to que orienta você na configuração de uma pilha OpenClaw completa em menos de uma hora.

[ALLOY]: Menos de uma hora? Isso é bem rápido para uma configuração completa auto-hospedada.

[NOVA]: É. E o guia faz um ponto que acho que vale destacar. A maioria das plataformas quer você na nuvem, nos seus termos, no seu preço.

[ALLOY]: Isso é verdade. Muitas plataformas de agentes são SaaS-first. Você se inscreve, você paga sua assinatura mensal, você usa a infraestrutura delas. É conveniente, mas você está preso ao ecossistema delas.

[NOVA]: OpenClaw é diferente. Você pode auto-hospedar tudo se quiser. Seu próprio servidor, seu próprio banco de dados, seus próprios agentes. E este guia mostra exatamente como fazer isso.

[ALLOY]: E podemos contrastar com o que conversamos antes com o SwitchBot. Isso é auto-hospedagem hardware-nativa. Este guia é auto-hospedagem software-nativa. De qualquer forma, é sobre possuir sua pilha.

[NOVA]: Certo. De qualquer forma, é sobre possuir seus dados e sua infraestrutura. Você decide onde seus dados vivem, como são processados, quem tem acesso. Sem intermediário, sem assinatura, sem lock-in de fornecedor.

[NOVA]: Essa é a filosofia. É controle versus conveniência, e o OpenClaw te dá a opção de escolher controle. Se você quer a conveniência da nuvem, ótimo. Se você quer o controle de auto-hospedagem, isso também é ótimo.

[NOVA]: O guia cobre a pilha completa. Tenho certeza de que passa por Docker, configuração do gateway, configuração do agente, como conectar canais, como configurar modelos, tudo.

[NOVA]: É um tutorial completo. Ehopefully inclui aquele aviso de mudança que quebra que conversamos antes, dado quando foi publicado.

[NOVA]: Hopefully. Esse é o tipo de coisa que atrapalha as pessoas. Uma configuração perdida e nada funciona, e você não tem ideia do porquê.

[NOVA]: De qualquer forma, para qualquer um que quis rodar o OpenClaw em seu próprio servidor, esse guia é um ótimo ponto de partida. Ele demistifica o processo.

[NOVA]: Com certeza. Vamos garantir que isso esteja nas notas do show para qualquer um que quer se aprofundar.

---

## Segmento 6 — Canto da Comunidade

[NOVA]: Hora do Canto da Comunidade, onde reunimos o que está acontecendo no ecossistema OpenClaw. Tem havido muita atividade, então vamos entrar nisso.

[ALLOY]: Vamos começar com algo importante do Reddit. Houve um PSA posted sobre o que aconteceu após a atualização 2026.3.2. Muitas pessoas foram pegas nisso.

[NOVA]: Oh, me lembro disso. Ferramentas foram desativadas por padrão naquele lançamento, certo?

[ALLOY]: Exatamente. Após atualizar para 2026.3.2, os usuários descobriram que seus agentes de repente pareciam burros. Eles não estavam usando ferramentas. Eles estavam apenas respondendo com texto e não fazendo nenhuma ação. Era muito confuso.

[NOVA]: Posso imaginar o pânico. Em um minuto seu agente está fazendo tudo, no próximo ele está apenas sentado lá respondendo com texto e não fazendo nada.

[ALLOY]: A razão era que ferramentas agora estavam desativadas por padrão — por razões de segurança, faz sentido começar com tudo desligado e deixar os usuários explicitamente habilitar o que precisam — mas pegou muitas pessoas desprevenidas.

[NOVA]: Essa é uma mudança significativa para não comunicar bem. Como a comunidade reagiu?

[ALLOY]: Houve muita discussão. O PSA do Reddit passa pela armadilha: você precisa explicitamente habilitar ferramentas na sua config agora. Não é mais automático.

[NOVA]: E acho que o aprendizado ali é que padrão-desligado é mais seguro de uma perspectiva de segurança, o que é ótimo, mas requer que as pessoas atualizem suas configurações.

[NOVA]: É um equilíbrio. A equipe do OpenClaw tem sido muito boa em comunicar mudanças nas notas de lançamento, mas sempre há um período de ajuste quando algo fundamental muda.

[NOVA]: Isso é justo. Leva tempo para a comunidade se adaptar a novos padrões.

[ALLOY]: Exatamente. Agora, vamos falar sobre algo mais positivo. Há uma peça no HackerNoon intitulada "A Saga do OpenClaw: Como as Últimas Duas Semanas Mudaram o Mundo da IA Agêntica Para Sempre."

[NOVA]: Esse é um título dramático. Ele realmente se apoia na narrativa.

[ALLOY]: É. É uma retrospectiva sobre os recentes desenvolvimentos no ecossistema OpenClaw. O grande lançamento, os anúncios de hardware, o crescimento da comunidade. Ele amplia e olha para o momento.

[NOVA]: É interessante ver a narrativa se formando ao redor do OpenClaw. Este artigo enquadramento como um ponto de viragem no espaço de IA agêntica.

[ALLOY]: E honestamente, não está errado. O ritmo de desenvolvimento tem sido incrível nos últimos meses. Estamos vendo novas capacidades, novos casos de uso, novo hardware, novas opções de implantação. É muita mudança em pouco tempo.

[NOVA]: Realmente parece que o OpenClaw está atingindo seu ritmo. A plataforma está amadurecendo rápido.

[ALLOY]: Concordo. Agora, mais uma do lado do GitHub. Há o PR número 38506, que adiciona um comando /learn para memória explícita.

[NOVA]: Me conta mais sobre isso. Como é diferente do que o OpenClaw já faz?

[ALLOY]: Então, atualmente, o OpenClaw tem memória automática. Ele aprende com conversas, com contexto, com interações. Ele absorve coisas passivamente ao longo do tempo.

[NOVA]: Certo, é como os humanos apenas lembram coisas sem tentar.

[ALLOY]: Exatamente. Mas este PR adiciona um comando /learn que permite ensinar explicitamente coisas ao agente. Em vez de esperar que ele absorva algo passivamente, você pode dizer diretamente, "Lembre-se disso. Isso é importante. É assim que gosto das coisas feitas."

[NOVA]: Então é memória intencional versus memória automática. Duas abordagens diferentes que se complementam.

[ALLOY]: Essa é uma ótima maneira de colocar. Às vezes você quer que o agente apenas aprenda naturalmente da conversa. Outras vezes você precisa ser explícito, como contar suas preferências pessoais ou fatos importantes que de outra forma poderia perder.

[NOVA]: Posso ver ambos sendo úteis em diferentes situações. Para fazer onboarding de um novo agente, você provavelmente seria muito explícito. Mas para uso diário, o aprendizado automático seria suficiente.

[NOVA]: O PR ainda está sendo discutido, mas é um bom exemplo de como a comunidade está moldando a direção do OpenClaw. Alguém viu uma necessidade e construiu uma solução.

[NOVA]: Esse é o poder do open source. A comunidade continua encontrando maneiras de melhorar o OpenClaw.

[ALLOY]: Com certeza. E é isso que adoramos ver.

---

## Segmento 7 — Encerramento

[NOVA]: Ok, vamos encerrar. O que todos devem levar deste episódio?

[ALLOY]: Há muito em que pensar, mas deixa eu destacar os pontos principais. Primeiro, se você está atualizando para v2026.3.7, verifique sua configuração de auth. Isso é crítico.

[NOVA]: Qual é o problema?

[ALLOY]: Se você tiver tanto gateway.auth.token quanto gateway.auth.password definidos na sua configuração, você deve adicionar gateway.auth.mode e defini-lo como token ou password antes de atualizar. Se você não adicionar esse campo de modo, o gateway não vai iniciar.

[NOVA]: Isso é crítico. Não seja pego por essa mudança que quebra. Verifique sua config antes de atualizar.

[ALLOY]: Com certeza. Segundo, fique de olho nas SwitchBot Skills. Elas estãorolando no final de março, e isso vai ser grande para OpenClaw hardware-nativo.

[NOVA]: O primeiro produto de consumidor executando OpenClaw nativamente com zero dependência de nuvem. Isso é enorme. É o começo de um novo capítulo para a plataforma.

[ALLOY]: Exatamente. E terceiro, se você tem um caso de uso interessante do OpenClaw, realmente queremos ouvir sobre isso. Compartilhe no Discord da comunidade OpenClaw. É assim que todos aprendemos uns com os outros.

[NOVA]: A comunidade tem sido fantástica em descobrir aplicações criativas. Apenas arranhamos a superfície com os cinco casos de uso que discutimos hoje. Há mais de cinquenta naquele artigo, e tenho certeza de que há centenas mais por aí que ninguém ainda escreveu.

[ALLOY]: Exatamente. Então compartilhe sua história. Você pode inspirar outra pessoa a tentar algo que nunca pensou.

[NOVA]: Esse é o espírito. Mais alguma coisa, Alloy?

[ALLOY]: Acho que esse é o principal. Este é um momento empolgante para o OpenClaw. A plataforma está crescendo em todas as direções — software, hardware, implantação em nuvem, auto-hospedagem, novos casos de uso todos os dias. É um ótimo momento para fazer parte da comunidade.

[NOVA]: Concordo. O momento é real, e está acelerando.

[NOVA]: E isso é um wrap. Obrigado por ouvir, pessoal. Até a próxima.

[ALLOY]: Bye pessoal. Construam algo legal.
