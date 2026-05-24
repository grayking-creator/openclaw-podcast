[NOVA]: Eu sou a NOVA.

[ALLOY]: E eu sou o ALLOY, e este é o AgentStack Daily. OpenClaw v2026.5.20 é a primeira coisa que merece atenção hoje porque muda coisas das quais um agente realmente depende: verificações de política, carregamento de segredos mais seguro, roteamento de provedores, entrega cron, retornos de subagente, contexto de voz e timeouts de geração de imagem.

[NOVA]: Codex 0.133.0 e Claude Code 2.1.148 estão na mesma zona prática: objetivos, prontidão de controle remoto, perfis de permissão, inventário de plugins, ganchos de ciclo de vida, sessões fixadas em segundo plano, revisão de código, paginação MCP, política enterprise, reparos de shell Windows, e uma correção de Bash que importa se o seu terminal de repente esqueceu como códigos de saída funcionam.

[ALLOY]: Hermes v2026.5.16 também ganha um lugar real à mesa: instalação PyPI, proxy local, provedores com OAuth, trabalho de navegador mais rápido, diagnósticos LSP, verificação de alteração de arquivo, mensagens, transferência, vídeo e uso de computador. Depois seguimos rápido por Codex Appshots, Secure MCP tunnels, Google Agent Executor, GKE Agent Sandbox, Antigravity CLI, MagenticLite, Data Agent Kit, endurecimento de API key do Gemini, e ferramentas de planejamento do Copilot. O ponto não é admirar nomes de lançamentos. O ponto é saber o que testar a seguir. ...

[NOVA]: O caminho de upgrade OpenClaw Codex Claude Code facilita a inspeção do stack de agentes local.

[ALLOY]: Comece pelo OpenClaw. Isso não é só um novo número de versão. Muda a camada host ao redor do agente. O plugin Policy empacotado dá ao OpenClaw um lugar real para colocar verificações de conformidade de canal com backup de política, achados de lint do doctor, e reparo de workspace opcional. Isso importa porque agentes não são mais apenas respostas de chat. Eles tocam ferramentas locais, sessões de navegador, tarefas agendadas, superfícies de voz, provedores e canais externos. Um problema de política não deveria viver como memória tribal. Ele deveria aparecer quando você rodar um diagnóstico.

[NOVA]: A ação mais imediata é rodar openclaw doctor depois do upgrade e realmente ler os achados. Procure por avisos de segredo em texto puro, configuração de provedor desatualizada, achados de política, e qualquer coisa que diga que um canal ou workspace não combina com o formato esperado. Depois corrija um item em vez de deixar o diagnóstico virar papel de parede.

[ALLOY]: O manuseio de segredos também fica mais afiado. Loaders de credenciais que solicitam rejeição de symlink agora falham fechado quando um caminho de token é um symlink. Isso parece um detalhe de segurança pequeno, mas é o tipo de detalhe pequeno que impede um leitor de credenciais confiável de ser silenciosamente apontado para outro lugar. O teste prático é fácil: saiba onde seus arquivos de token estão, certifique-se de que não são symlinks, e certifique-se de que o runtime falha em vez de adivinhar quando o caminho está errado.

[NOVA]: O roteamento de provedores é outra superfície útil. OAuth de device-code do xAI ajuda setups headless ou remotos a autorizar sem callback de navegador localhost. A política de roteamento do provedor OpenRouter é respeitada a menos que parâmetros de modelo ou agente sobrescrevam. Se você roda mais de um provedor de modelo, isso vale testar diretamente. Faça uma pequena chamada de modelo onde a rota do provedor importa, depois confirme que a rota foi a que você pretendia. O problema a evitar é achar que você está testando um backend enquanto outro backend silenciosamente进行处理.

[ALLOY]: Cron e transferência de subagente também recebem atenção. Trabalho agendado da sessão principal agora tem uma faixa mais limpa para não bloquear chat humano tão facilmente. Execuções agendadas bem-sucedidas podem entregar a saída preferida final do assistente mesmo se avisos diagnósticos venham atrás. A transferência de conclusão de subagente é mais resiliente quando a sessão solicitante está desatualizada ou dormente. O teste útil é uma tarefa agendada e uma tarefa deleg ada. Elas retornam ao lugar certo? A resposta final aparece, ou só o ruído ao redor dela?

[NOVA]: As mudanças de voz também são práticas. Sessões de voz do Discord podem seguir usuários configurados para canais de voz, e instruções de voz em tempo real podem incluir contexto de identidade e persona limitado. Isso não significa jogar um perfil inteiro em cada sessão de voz. Significa que um agente de voz pode carregar contexto estável suficiente para se comportar de forma consistente quando a conversa muda de texto para voz e vice-versa. Teste isso com um caso de uso de voz limitado antes de confiar para uma sessão mais longa.

[ALLOY]: Geração de imagem ganha um timeout padrão melhor. Chamadas dinâmicas de geração de imagem agora recebem um watchdog de 120 segundos quando nenhum timeout mais apertado está configurado. Isso importa porque chamadas de imagem frequentemente demoram mais que chamadas de texto. Um timeout de 30 segundos pode fazer uma geração válida lenta parecer quebrada. O item de ação é testar um provedor de imagem com o novo timeout e confirmar que a UI ou tarefa chamadora relata progresso lento em vez de perder silenciosamente o resultado.

[NOVA]: Agora o Codex. A mudança importante no release atual do CLI é estado. Objetivos estão habilitados por padrão com armazenamento dedicado e rastreamento de progresso. Um objetivo é útil porque trabalho de codificação mais longo precisa de um alvo durável. Sem esse alvo, um transcript pode estar cheio de boas intenções e ainda assim derivar. Experimente uma tarefa com uma condição final mensurável: corrija um teste, atualize um componente, ou produza um script validado. O objetivo deveria dizer ao agente onde fica o "pronto".

[ALLOY]: codex remote-control também se torna uma ferramenta mais crível. Ele espera por prontidão, reporta status da máquina, e mantém comportamento explícito de início e parada. Isso é importante se o Codex faz parte de um setup de controle remoto ou de desktop. Um comando remoto não deveria te deixar em dúvida se o host está pronto. Teste antes de precisar em situação real: inicie o caminho de controle, espere pela prontidão, verifique status, pare, e certifique-se de que a parada foi real.

[NOVA]: Perfis de permissão e descoberta de plugins são as outras superfícies para builders. Perfis ganham APIs de lista, herança, arquivos de requisitos gerenciados, refresh em runtime, e integração de sandbox Windows mais forte. Descoberta de plugins mostra versões instaladas, raízes do marketplace, e suporte a coleção remota. Extensões podem observar início e parada de subagente, execução de ferramenta, metadados de turn, e aprovações assíncronas. Isso significa que o Codex está se tornando algo que outras ferramentas podem inspecionar e construir ao redor, não apenas algo com que uma pessoa conversa.

[ALLOY]: Claude Code é o bloco de estabilidade do agente de terminal. Sessões fixadas em segundo plano em claude agents permanecem vivas quando ociosas, reiniciam no lugar para aplicar updates, e são descartadas sob pressão de memória só depois de sessões não-fixadas. O antigo comando simplify vira code-review, e seu trabalho fica mais claro: encontrar bugs de correção em um nível de esforço escolhido, com comentários opcionais inline de pull request GitHub. Isso é muito melhor que um comando vago de limpeza fingindo ser revisão.

[NOVA]: A correção de paginação MCP é fácil de subestimar. Se um servidor tem mais de uma página de recursos, templates ou prompts, o cliente não deveria agir como se a página um fosse o universo inteiro. Uma ferramenta faltando frequentemente parece uma falha de modelo, mas o bug real é descoberta. Depois do upgrade, teste um servidor MCP com recursos suficientes para paginar e confirme que o cliente vê tudo que deveria.

[ALLOY]: Claude Code também aperta diagnósticos do atualizador, política de login enterprise, comportamento PowerShell, aprovações em segundo plano, e tratamento de saída Bash. O conjunto de testes é direto: uma sessão fixada, uma revisão de código em um diff real, uma consulta de inventário MCP, um caminho de reutilização de permissão, e uma tarefa pesada de shell. Se esses passarem, esse update passou de nota de release para útil. ...

[NOVA]: O movimento de build é parar de tratar esses como brinquedos separados. Escolha um fluxo de trabalho de agente pequeno que cruze todas as três superfícies: OpenClaw inicia a tarefa, Codex edita ou inspeciona algo com um objetivo, e Claude Code revisa ou verifica um diff de terminal. Mantenha pequeno. O valor está em ver onde estado, permissões, roteamento e descoberta de ferramentas aparecem no mesmo trabalho. Se o fluxo parecer confuso, anote qual superfície causou a confusão. Essa resposta te diz onde melhorar seu setup antes que uma tarefa maior dependa dele.

[NOVA]: O release Hermes Agent Foundation afia o banco de agentes com assinaturas, ferramentas locais e mensagens.

[ALLOY]: Hermes ganha a própria seção porque esse release não é apenas um pequenopolimento de CLI. É um grande lançamento de "tornar a coisa mais fácil de instalar, mais fácil de conectar, mais rápida de iniciar e menos irritante de operar". Esse é um tipo de notícia muito boa de ouvir, porque toda pilha de agentes eventualmente esbarra no mesmo muro: o modelo está pronto, as ferramentas estão espalhadas, os caminhos de autenticação são estranhos, e o humano ainda está fazendo pequenas tarefas de configuração que deveriam ter desaparecido há dois meses.

[NOVA]: Vamos começar pela instalação. Hermes agora é um pacote PyPI de verdade, então o caminho de entrada fica pip install hermes-agent e depois hermes. Parece quase simples demais para gastar tempo falando sobre isso, mas fricção de instalação é fricção de produto. Se uma ferramenta exige um clone, um script de shell, uma convenção local e três notas meio esquecidas antes de até abrir, menos pessoas testam de forma honesta. Um caminho de pacote limpo significa que mais pessoas podem colocar em uma máquina nova e ver se o loop de agentes realmente é útil.

[ALLOY]: A próxima grande peça é o proxy local compatível com OpenAI. Execute hermes proxy, e ferramentas que já sabem conversar com um endpoint estilo OpenAI podem apontar para um endpoint Hermes local apoiado por qualquer provedor OAuth em que o usuário tenha feito login. Os nomes práticos são óbvios: Codex CLI, Aider, Cline, Continue, scripts customizados. A ideia interessante é que um provedor baseado em assinatura pode se tornar um endpoint local sem que cada ferramenta downstream precise de uma integração de autenticação personalizada.

[NOVA]: É aí que a diversão começa para os builders. Imagine Codex esperando uma API compatível com OpenAI. Em vez de inventar outro caminho secreto, você aponta para o proxy Hermes e deixa o Hermes cuidar da autenticação do provedor. O teste é simples: inicie o proxy, aponte um cliente para ele, execute uma pequena requisição e inspecione qual provedor realmente atendeu. Depois pare o proxy e certifique-se de que o fracasso é claro. Se falhar como uma ferramenta normal, você pode contornar. Se falhar como névoa, mantenha no laboratório.

[ALLOY]: SuperGrok OAuth e o caminho xAI importam da mesma forma. O release permite que Hermes use Grok através de um fluxo de conta logada em vez de tratar cada provedor como uma gaveta de chave de API estática. Isso dá mais variedade de provedores para a mesa de agentes, mas também levanta uma questão de controle: quais ferramentas devem ser permitidas para gastar qual assinatura, e como você sabe o que aconteceu depois do fato?

[NOVA]: É por isso que o teste de proxy deve incluir logging. Não uma grande cerimônia de observabilidade. Apenas evidências suficientes para responder: qual cliente chamou, qual provedor respondeu, qual modelo foi usado, e se um limite de credencial foi cruzado. Pilhas de agentes ficam muito menos misteriosas quando "qual backend fez isso?" tem uma resposta.

[ALLOY]: Hermes também adiciona x_search, que é útil porque agentes frequentemente precisam de conversas sociais ou de desenvolvedores atuais, mas não deveriam exigir uma skill customizada só para buscar no X. Trate como uma ferramenta de evidências, não um canhão de fofocas. Um bom primeiro uso é restrito: encontre uma thread de release, um post de mantenedor, ou um relatório de incidente recente, e depois cite o resultado específico de volta na tarefa. Um mau uso é deixar o agente nadar pelo ruído social e chamar de pesquisa.

[NOVA]: Mensagens também é uma grande faixa do Hermes. Microsoft Teams está conectado ponta a ponta, LINE e SimpleX Chat chegam, botões nativos de esclarecimento chegam para Telegram e Discord, e history backfill do Discord está ativado por padrão. Esse último é surpreendentemente importante. Um agente de chat entrando em um canal sem contexto recente é como uma pessoa entrando em uma reunião e imediatamente respondendo uma pergunta de vinte minutos atrás. History backfill dá ao agente a chance de saber o que já está na tela.

[ALLOY]: O item de ação ali não é "conectar cada plataforma." Escolha um canal e teste um controle conversacional. Botões de esclarecimento são um bom. Peça ao agente para escolher entre duas opções seguras e confirme que os botões aparecem, a resposta escolhida chega à execução, e o transcript registra a decisão. Esse é um teste pequeno, mas prova que a superfície de chat é mais do que texto colado em um vazio.

[NOVA]: Performance ganha números reais. Hermes diz que cold start cai em cerca de dezenove segundos, e avaliações de console do browser ficam dramaticamente mais rápidas através de uma conexão persistente do Chrome DevTools. Isso importa porque agentes locais são usados em loops pequenos. Se cada inspeção de browser leva um par de segundos, o agente parece grudento. Se a mesma inspeção é quase instantânea, reparo de browser e evidência de página ficam muito mais toleráveis.

[ALLOY]: Experimente uma inspeção de browser antes e depois da atualização. Peça ao Hermes para inspecionar uma página, execute uma avaliação JavaScript inofensiva e relate o resultado. Faça duas vezes. Se a segunda execução for mais rápida porque a conexão permanece aquecida, você aprendeu algo útil. Se ainda parecer lento, o gargalo pode ser seu perfil de browser, início da ferramenta, rede, ou a própria página.

[NOVA]: As funcionalidades de segurança de escrita são a parte que eu testaria imediatamente. Verificação de mutação de arquivo por turno significa que o agente recebe um rodapé após edições com o que mudou no disco. Diagnósticos semânticos LSP em cada escrita significa que o agente pode ver erros do language-server antes de dizer casualmente que o patch está pronto. Essas são as funcionalidades que impedem um agente confiante de estar confidentemente errado sobre se ele realmente editou o arquivo que pensa ter editado.

[ALLOY]: O teste rápido é uma pequena edição de código. Diga ao Hermes para mudar uma função com uma expectativa de tipo óbvia. Observe se o resumo de mudança de arquivo aparece. Observe se os diagnósticos LSP capturam um erro. Depois peça ao agente para corrigir. Isso não é glamoroso, mas é exatamente o tipo de loop que salva um builder de aceitar um patch quebrado porque a prosa soou pronta.

[NOVA]: /handoff é outra peça útil. Ele move uma sessão ativa para um modelo, persona ou perfil diferente sem perder contexto. O teste certo não é uma transferência dramática gigante. Comece uma pequena sessão de debugging com um provedor rápido, depois passe para um modelo mais profundo para a revisão final. Verifique se o alvo tem as mensagens, o histórico de ferramentas e os arquivos de que precisa. Se handoff funcionar, você obtém um caminho prático de escalação em vez de começar do zero.

[ALLOY]: Hermes também expande o uso de computer além de suposições only da Anthropic com o backend cua-driver, adiciona geração de vídeo conectável, URLs de terminal clicáveis, integração com Zed ACP Registry, roteamento OpenRouter Pareto Code, skills opcionais, eventos de aprovação de API, e chamadas LLM do lado do plugin através de ctx.llm. Isso é muito, então não tente digerir como uma lista. Escolha duas funcionalidades que removam um incômodo atual.

[NOVA]: Meu teste de bench do Hermes sugerido tem cinco partes. Um, instale ou atualize e execute doctor. Dois, inicie o proxy local e aponte uma ferramenta compatível com OpenAI para ele. Três, execute uma inspeção de browser e confirme que é rápida o suficiente para tolerar. Quatro, faça uma edição de arquivo e observe LSP mais verificação de mutação. Cinco, use handoff ou botões de esclarecimento em uma superfície de chat real. Isso é suficiente para saber se Hermes pertence à sua pilha diária ou fica como um experimento de fim de semana.

[ALLOY]: E se falhar em um desses testes, isso ainda é útil. Um bom bench não prova apenas que as ferramentas são brilhantes. Ele diz qual parte não está pronta: instalação, autenticação, proxy, browser, segurança de escrita, mensagens ou handoff. É assim que você transforma um grande release em uma decisão útil em vez de uma avalanche de funcionalidades. ...

[NOVA]: OpenAI Codex Appshots e modo goal tornam o trabalho visual de produto menos arriscado.

[ALLOY]: Appshots são a atualização de produto Codex mais imediatamente útil. No app macOS, você pode anexar uma janela de app a uma thread do Codex com um hotkey. A thread recebe uma screenshot e texto disponível. Isso muda o reparo de UI porque o humano não precisa mais traduzir cada problema visual em um parágrafo longo. O modelo pode ver o estado ruim, inspecionar a camada de texto e conectar o problema a um componente, rota ou regra de estilo.

[NOVA]: A versão para testar agora é um bug de UI. Não comece com um redesign enorme. Abra um estado de app onde algo está visivelmente errado: uma tabela cortada, um botão desalinhado, um modal que parece apertado, um título quebrando mal, ou um estado de sidebar que não combina com a página. Capture um Appshot. Dê ao Codex uma meta: conserte esse problema visível sem mudar o layout ao redor. Depois execute a página e capture o resultado novamente.

[ALLOY]: O modo de meta é a outra metade. Agora está geralmente disponível no app Codex, extensão de IDE e CLI. Isso importa porque uma meta é uma definição portátil de concluído. Se a tarefa começa no app de desktop e continua em um editor ou linha de comando, o alvo pode permanecer attached ao trabalho. A meta deve ser concreta: passar neste teste, remover este defeito visual, gerar este artefato, ou atualizar este caminho de API sem alterar comportamento não relacionado.

[NOVA]: Anotações no navegador tornam o feedback mais específico. Requisições de estilo frequentemente falham porque a instrução é espacial: alinhe isso com aquilo, reduza este espaço, mantenha este rótulo legível, faça o peso deste ícone combinar com o botão. Suporte a anotações permite que o feedback aponte para a região em vez de depender de prosa vaga. Para trabalho de frontend, isso pode economizar vários patches ruins.

[ALLOY]: Contexto JavaScript somente leitura é uma melhoria sutil de segurança. Ele dá ao agente uma forma de inspecionar o estado da página sem transformar inspeção em mutação. A ordem certa ainda é observar, raciocinar, editar, verificar. Se um agente pulo direto de ver uma página para mutá-la, o debug fica confuso rapidamente. Inspeção somente leitura ajuda a manter essas fases separadas.

[NOVA]: Uso de computador bloqueado é útil, mas deve ser tratado como continuidade sob supervisão, não como autonomia mágica. Usuários elegíveis de Computer Use no Mac podem manter o Codex funcionando remotamente após o Mac bloquear. Isso é bom para tarefas locais longas, verificações visuais, ou trabalho no navegador que leva tempo. Antes de usar para trabalho sério, teste o comportamento de wake, aprovações e recuperação. Uma máquina bloqueada não deve expandir acidentalmente o poder do agente.

[ALLOY]: O padrão prático é este: use Appshots para verdade visual, modo de meta para o alvo, anotações para feedback exato, JavaScript somente leitura para inspeção, e uso de computador bloqueado apenas após o caminho de aprovação ser previsível de forma entediante. Esse é um loop de produto melhor do que "descreva o bug, espere que o agente imagine a mesma página, e então faça patch em três arquivos." ...

[NOVA]: Uma boa trial de builder é um problema antes-e-depois. Capture a UI quebrada, peça ao Codex o menor fix possível, rode o build, capture a UI reparada, e compare os dois estados. Se a tarefa mudar mais do que o defeito visível, rejeite e estreite a meta. Isso mantém o workflow prático: evidência visual entra, mudança no código sai, verificação antes de confiar. Isso também dá um padrão reutilizável para QA de design, correções de acessibilidade, overflow de texto, polimento de dashboard, e suporte a apps de desktop.

[NOVA]: Túneis MCP seguros transformam ferramentas privadas em ferramentas de agente alcançáveis sem abrir portas de entrada.

[ALLOY]: Esta é uma das histórias de infraestrutura mais importantes porque muda como ferramentas privadas podem participar de sistemas de agente. A OpenAI e a Anthropic estão ambas avançando padrões de túnel MCP. O formato básico é conectividade de saída: um servidor MCP local ou interno se conecta através de um túnel, e uma superfície de agente pode alcançá-lo sem expor uma porta de entrada à internet pública.

[NOVA]: O motivo para se importar é simples. Muitas ferramentas úteis são privadas. Elas vivem em um laptop, dentro de uma rede corporativa, atrás de um firewall, ou anexadas a um serviço local. Sem um túnel, um time ou não consegue usá-las de uma superfície de agente hospedada ou precisa abrir um buraco na rede. Um túnel de saída dá um caminho de conectividade mais limpo.

[ALLOY]: Mas conectividade não é permissão. Esta frase é todo o risco. Um túnel pode tornar uma ferramenta alcançável, mas não decide automaticamente quem deve usar a ferramenta, quais métodos são permitidos, quais dados podem sair, ou quais ações requerem aprovação. Se o servidor MCP expõe ações poderosas, o túnel apenas aproxima o problema.

[NOVA]: O exercício para fazer agora é projetar uma ferramenta MCP privada como se ela fosse entrar em produção. Nomeie a ferramenta. Nomeie a conta ou projeto que pode alcançá-la. Liste os métodos que o agente tem permissão de chamar. Decida quais chamadas são somente leitura e quais são mutantes. Decida se chamadas mutantes requerem aprovação humana. Registre cada chamada com detalhes suficientes para auditar depois. Então decida onde o segredo local fica e como ele é rotacionado.

[ALLOY]: Isso não é burocracia. É a diferença entre "meu agente pode consultar um serviço de status interno" e "meu agente hospedado pode fazer qualquer coisa que meu servidor MCP de laptop expõe." O túnel deve ser estreito. Se uma ferramenta só precisa ler metadados de issue, não dê a ela um método que pode reescrever o issue. Se só precisa de um banco de staging, não aponte para produção. Se só precisa de um resumo, não retorne registros brutos por padrão.

[NOVA]: Os melhores casos de uso são entediantes de um jeito bom: busca interna, docs locais, status de build, dashboards somente leitura, verificações pequenas de deployment, uma ferramenta de disponibilidade de calendário privado, ou um inventário fonte-de-verdade. Uma vez que esses funcionem, avance com cuidado para ações de escrita. Uma ação de escrita através de um túnel privado deve parecer um pequeno release, não uma conveniência casual.

[ALLOY]: O ponto principal é prático. Túneis MCP seguros tornam ferramentas privadas mais fáceis de conectar. Eles não removem a necessidade de identidade, allowlists, logs de auditoria, segredos com escopo e portões de aprovação. Trate o túnel como o tubo. Projete o modelo de permissão em torno da ferramenta. ...

[NOVA]: O primeiro build deve ser somente leitura. Um workflow inicial útil é uma consulta de status interno, uma busca de documentação privada, ou uma query de saúde de staging. Faça a ferramenta retornar uma resposta pequena e um trace do que ela verificou. Depois adicione uma ação de escrita com aprovação mais tarde. Essa sequência mantém o túnel útil sem tornar a primeira versão assustadora. Se uma ferramenta somente leitura não pode ser limitada e auditada de forma limpa, uma ferramenta com capacidade de escrita não está pronta.

[NOVA]: O Google Agent Executor torna agentes de longa execução recuperáveis em vez de um tiro único.

[ALLOY]: Agent Executor é interessante porque nomeia a camada de runtime que muitos demos de agente pulam. Uma execução de agente séria precisa de um log de eventos, snapshots, reconexão e backfill, atores isolados, estado de sessão de gravador único, e trajetórias ramificáveis. Esses não são recursos glamorosos. São as coisas que tornam uma execução longa recuperável.

[NOVA]: Um prompt de um tiro pode viver dentro de uma transcrição de chat. Uma tarefa de agente de várias horas não pode. Ela pode navegar, chamar ferramentas, criar estado intermediário, esperar por um usuário, se recuperar após uma desconexão, e bifurcar uma estratégia após uma falha. Se tudo isso viver apenas como contexto de modelo, a execução é frágil. Quando o contexto é compactado, interrompido, ou confundido, o sistema perde o fio.

[ALLOY]: O log de eventos é a primeira peça útil. Ele te dá um registro do que aconteceu em ordem: decisões do modelo, chamadas de ferramenta, observações, aprovações, erros, retentativas, e saídas. Isso importa quando uma execução succeeds porque você pode explicar como chegou lá. Importa ainda mais quando uma execução falha porque você pode identificar qual evento estava errado em vez de culpar o modelo inteiro.

[NOVA]: Snapshots resolvem um problema diferente. Sessões de longa execução precisam de uma forma de pausar e retomar sem reproduzir o mundo inteiro. Um snapshot pode capturar o estado em um ponto no tempo, para que o sistema possa continuar após reconectar ou se recuperar. Isso é importante para agentes de navegador, agentes de codificação, agentes de dados, e qualquer tarefa que tenha estado fora do prompt.

[ALLOY]: Ramificação é útil para depuração e exploração. Se um agente seguiu um caminho ruim, você nem sempre quer começar do zero. Você pode querer ramificar a partir do último ponto bom e tentar um plano diferente. Isso é mais próximo de como desenvolvedores depuram código: encontre o último estado conhecido como bom, depois teste uma mudança menor.

[NOVA]: A tarefa de ação é mapear uma tarefa de agente existente nessa forma de runtime. Escolha uma tarefa que atualmente pareça instável. Faça cinco perguntas. Qual é o stream de eventos? Onde o estado durável está armazenado? Como a execução retoma após uma desconexão? Você pode ramificar a partir de um passo falho? Que prova resta depois que a execução termina?

[ALLOY]: Se você não consegue responder essas perguntas, a tarefa ainda pode funcionar, mas ainda não é um sistema de agente em que você pode confiar. O Agent Executor é útil porque empurra os construtores em direção a uma execução recuperável em vez de um prompting heroico. ...

[NOVA]: Um exercício prático para construtores é pegar uma tarefa instável e escrever seu run card. O card precisa de um evento de início, uma lista de eventos de ferramenta, um evento de aprovação se um humano estiver envolvido, um evento de sucesso e um evento de falha que possa ser retomado. Você não precisa de uma plataforma completa para aprender com isso. Até uma implementação local simples fica melhor quando o workflow tem eventos nomeados em vez de um transcript gigante. No momento em que você pode retomar a partir do último evento bom, a tarefa deixa de ser um teatro frágil e começa a virar software.

[NOVA]: O GKE Agent Sandbox e o Agent Substrate têm como alvo o formato estranho de agentes ociosos mas com estado.

[ALLOY]: Cargas de trabalho normais de servidor geralmente não se parecem com cargas de trabalho de agente. Um serviço web lida com requisições. Um job em lote executa e termina. Uma sessão de agente pode ficar ociosa por muito tempo, acordar de repente, precisar de isolamento, usar ferramentas, manter estado, e então ficar ociosa novamente. Multiplique isso por milhares ou milhões de sessões e o agendamento comum começa a parecer desajeitado.

[NOVA]: O trabalho do GKE Agent Sandbox e Agent Substrate do Google é focado nesse formato. As peças são pools aquecidos, snapshots, isolamento com gVisor, agendamento de ator e multiplexação de workers. O ponto não é apenas "executar agentes no Kubernetes." O ponto é tornar sessões isoladas com estado mais baratas e rápidas para acordar.

[ALLOY]: Pools aquecidos ajudam porque uma sessão pode começar a partir de capacidade pronta em vez de infraestrutura fria. Snapshots ajudam porque o estado ocioso pode ser suspenso e retomado. gVisor ajuda com isolamento. Mapeamento de ator para worker ajuda a plataforma a carregar muitas sessões lógicas em menos workers ativos. O tema não é decorativo; é uma resposta à economia das sessões de agente.

[NOVA]: A versão para testar agora é um esboço de formato de carga. Antes de construir um serviço de agente, estime quantas sessões estão ativas, quantas estão ociosas, por quanto tempo ficam ociosas, qual estado deve sobreviver, quais ferramentas podem acessar e quão rápido devem acordar. Se a carga de trabalho é principalmente ociosa mas deve retomar rapidamente, pools aquecidos e snapshots podem importar mais do que velocidade bruta do modelo.

[ALLOY]: Isso também muda a depuração. Se uma sessão de agente se move entre atores e workers, você precisa de identidade de sessão, logs, snapshots e traces de chamadas de ferramenta que a sigam. Caso contrário, uma falha parece que a plataforma engoliu a execução. A infraestrutura para agentes precisa ser observável no nível da sessão, não apenas no nível do pod ou processo.

[NOVA]: Agentes de codificação e servidores MCP são bons exemplos. Um agente de codificação pode precisar de um sandbox com um repositório, dependências, estado do navegador e um patch parcial. Um servidor MCP pode precisar de credenciais e contexto local. Se essas peças forem caras para recriar, o sistema precisa de uma história melhor de ociosidade e retomada.

[ALLOY]: A ação não é "mover todo agente para GKE amanhã." É reconhecer o formato da carga de trabalho. Se suas sessões de agente são poucas e curtas, mantenha simples. Se são muitas, isoladas, ociosas e com estado, comece a testar comportamento de snapshot e pool aquecido antes que a plataforma fique cara. ...

[NOVA]: Para um construtor, a pergunta prática é custo por sessão útil, não custo por container. Se um workflow passa a maior parte da vida esperando um usuário, uma ferramenta ou um acordado agendado, tempo de cold-start e custo de ociosidade dominam a experiência. Teste um pool pequeno com comportamento real de sessão: acorde, inspecione, chame uma ferramenta, pause, retome e termine. Depois meça o atraso percebido pelo usuário e as evidências de depuração deixadas para trás. Isso diz se o substrate ajuda o produto ou apenas faz o diagrama parecer sério.

[NOVA]: A migração do Antigravity CLI do Google é um prazo de planejamento real para usuários do Gemini CLI.

[ALLOY]: O Google diz que o uso gratuito e para consumidores do Gemini CLI para de servir requisições em 18 de junho de 2026, e o Antigravity CLI se torna a nova superfície de terminal. Isso não é apenas uma mudança de marca. É um evento de migração para qualquer pessoa que construiu hábitos, scripts, prompts, skills ou hooks em torno do Gemini CLI.

[NOVA]: A migração do Antigravity CLI do Google é a frase exata para colocar no calendário porque isso não é um empurrãozão vago no futuro. É uma mudança datada de superfície de terminal com scripts existentes, fluxos de auth e hábitos anexados a ela.

[NOVA]: A parte importante é a direção do harness. O Antigravity está posicionado em torno de skills, hooks, subagentes, plugins, trabalho assíncrono e contexto compartilhado entre CLI e desktop. Isso significa que o agente de terminal está se tornando menos como um executor de prompt único e mais como um ambiente de trabalho configurado.

[ALLOY]: A migração prática começa com inventário. Liste as tarefas do Gemini CLI que você realmente usa. Não as que você imaginou usar. As que executam toda semana. Para cada uma, registre o caminho de auth, modelo, config, arquivos que lê, ferramentas que chama, hooks dos quais depende e qual saída prova sucesso. Depois execute a tarefa de maior valor pelo caminho do Antigravity antes do corte.

[NOVA]: Preste atenção ao comportamento do consumidor versus enterprise. Uma migração de CLI pessoal pode ser irritante. Uma migração enterprise pode afetar política, método de login, auditoria e provedores permitidos. Se uma equipe tem scripts wrapper em torno do Gemini CLI, o wrapper deve falhar claramente quando o caminho antigo parar de servir requisições. Fallback silencioso é o inimigo aqui.

[ALLOY]: Skills e hooks precisam de cuidado especial. Uma skill que funciona em um harness pode assumir um layout de arquivo, um modelo de permissão, um formato de prompt ou um nome de ferramenta que não traduz. Um hook pode disparar em um ponto diferente do ciclo de vida da tarefa. Um subagente pode herdar menos contexto do que o esperado. Teste essas suposições diretamente.

[NOVA]: A próxima jogada é pequena. Escolha uma tarefa. Mova-a. Registre as diferenças. Se o resultado mudar, decida se o novo resultado é melhor, pior, ou apenas diferente. Se as chamadas de ferramentas mudarem, decida se isso é aceitável. Se a autenticação mudar, documente a nova configuração enquanto está fresca.

[ALLOY]: O prazo está perto o suficiente para que esperar seja um plano ruim. Migrações ficam mais fáceis quando o primeiro teste acontece enquanto a ferramenta antiga ainda funciona. ...

[NOVA]: O melhor fluxo de trabalho de migração é uma execução paralela. Mantenha o caminho antigo do Gemini CLI como referência enquanto ele ainda responde. Execute o mesmo prompt de build através do Antigravity. Compare não apenas a resposta de texto, mas as ferramentas usadas, aprovações solicitadas, artefatos alterados, e o tempo até um resultado utilizável. Se o Antigravity mudar a forma da tarefa, isso pode ser fine. O que você quer evitar é descobrir a diferença depois que o caminho antigo ficou quieto.

[NOVA]: O Microsoft MagenticLite mostra como agentes de uso de computador de modelos pequenos podem ser úteis quando o harness é projetado ao redor deles.

[ALLOY]: O MagenticLite é interessante porque não começa com "dar toda tarefa ao maior modelo." A Microsoft Foundry Labs está emparelhando um harness, um orquestrador, modelos de uso de computador, aprovações, e sandboxing. O MagenticBrain é baseado no Qwen três oito bilhões e treinado dentro do harness. O Fara um ponto cinco lida com tarefas de uso de computador nas variantes de quatro, nove, e vinte sete bilhões de parâmetros.

[NOVA]: O mecanismo-chave é o co-design. O orquestrador vê o mesmo tipo de schemas de ferramentas durante o treinamento e a inferência. Isso reduz a lacuna entre o comportamento em benchmark e o comportamento em produto. Muitos fracassos de agentes acontecem quando um modelo aprende um formato de tarefa, e então o produto entrega a ele uma forma de ferramenta diferente, modelo de aprovação, ou estado de navegador diferente.

[ALLOY]: O MagenticLite também usa o sandbox QEMU do Quicksand para sessões de navegador e execução de código. Isso importa porque agentes de uso de computador tocam páginas desconhecidas, downloads, conteúdo local, e às vezes código. Executar esse trabalho dentro de uma fronteira resetável é um melhor padrão do que deixar o agente vagar pelo desktop principal.

[NOVA]: O design de aprovação é tão importante quanto o modelo. Um bom agente de uso de computador deve pausar para login, submissão, exclusão, pagamento, mudanças de conta, ou qualquer outra coisa que cruze de navegação reversível para consequência. Ele não deve pedir aprovação em cada clique inofensivo. O sistema tem que saber quais ações são sensíveis.

[ALLOY]: A pergunta de "tentar agora" não é "isso pode substituir um modelo de codificação frontier?" A pergunta é "quais tarefas repetitivas de uso de computador são estreitas o suficiente para um orquestrador menor mais um modelo especializado de navegador?" Candidatos incluem verificar um dashboard, preencher um formulário rascunho, coletar evidências de página, navegar uma ferramenta web conhecida, organizar artefatos locais em um sandbox, ou rodar uma demo visual.

[NOVA]: A economia importa. Se cada clique chama o modelo mais caro, muitas automações úteis nunca se tornam acessíveis. Um orquestrador menor pode tornar tarefas de alta frequência plausíveis se a confiabilidade permanecer alta o suficiente. Treinamento fiel ao harness é a aposta: molde o ambiente para que o modelo menor tenha menos surpresas.

[ALLOY]: A avaliação deve ser prática. Ele consegue se recuperar quando uma página muda? Um humano pode assumir? Ele consegue explicar por que delegou para um modelo de navegador? O sandbox reseta de forma limpa? Ele pausa nos momentos certos? Ele termina a tarefa chata sem transformar o humano em supervisor de cada passo?

[NOVA]: Essa é a lente útil para o MagenticLite. Modelos pequenos não são mágica. Mas modelos pequenos dentro de um harness cuidadoso podem ser exatamente o certo para uma fatia do trabalho de uso de computador. ...

[ALLOY]: Um caso de uso forte primeiro é algo repetitivo com sucesso óbvio: colete três fatos de uma ferramenta web conhecida, preencha um formulário rascunho sem submetê-lo, verifique um dashboard para uma mudança de status, ou prepare um relatório local dentro de um sandbox. Esses são fluxos de trabalho construíveis porque o objetivo é visível e o risco é limitado. Não comece com pagamentos, mudanças de conta, exclusões de produção, ou pesquisa ambígua. Comece onde o modelo menor pode vencer sendo barato, rápido, e previsível.

[NOVA]: O Google Data Agent Kit empacota acesso a dados como ferramentas de agente configuradas em vez de schema colado.

[ALLOY]: Esta história importa porque trabalho com dados é um dos lugares onde agentes podem se tornar úteis rapidamente e perigosos rapidamente. O Google Data Agent Kit traz habilidades de dados e ferramentas estilo MCP para superfícies de agente de desenvolvedor incluindo Codex, Claude Code, Gemini CLI, VS Code, e Antigravity. As fontes incluem BigQuery, AlloyDB, Spanner, e Cloud Storage.

[NOVA]: A mudança útil é de contexto colado para acesso configurado. Colar schema, linhas de exemplo, e credenciais em um prompt é frágil. Pode estar desatualizado, muito amplo, e difícil de auditar. Uma ferramenta de dados configurada pode ter escopo, credenciais, validação, e uma interface repetível.

[ALLOY]: O item de ação é delimitar o escopo do agente de dados antes de dar a ele poder. O que ele pode ler? O que ele pode escrever? Quais datasets são fora dos limites? Ele pode rodar consultas caras? Ele precisa de segurança em nível de linha? Ele deve retornar dados brutos, resumos, ou planos de consulta? Quem revisa uma query gerada antes dela tocar produção?

[NOVA]: Habilidades de otimização de query e validação são úteis porque um agente de dados pode de outra forma ser confiadamente caro. Uma query ruim não está apenas errada; ela pode ser lenta, custosa, e barulhenta. O agente deve ser capaz de explicar as tabelas que está usando, os filtros que aplicou, e a validação que realizou.

[ALLOY]: Verificações de drift e governança são outro encaixe bom. Se um dashboard muda, um schema deriva, ou um pipeline começa a produzir valores inesperados, um agente pode ajudar a investigar. Mas novamente, o escopo de acesso importa. Um agente de dados não deve obter acesso de escrita amplo só porque consegue explicar um gráfico.

[NOVA]: A primeira construção prática é somente leitura. Dê ao agente um dataset, um tipo de pergunta, e um requisito de validação. Faça ele produzir a query, a resposta, e a evidência. Então decida se ações de escrita pertencem ao sistema. ...

[ALLOY]: O fluxo de trabalho fica mais forte quando o agente precisa mostrar seu trabalho em partes verificáveis por máquina. Peça a consulta, o resultado, a verificação de validação e os limites de confiança separadamente. Se a consulta for cara, exija uma estimativa antes da execução. Se a resposta afetar uma decisão, exija a tabela de origem e a lógica de filtro. Isso torna o agente de dados útil para os desenvolvedores porque pode acelerar a análise sem esconder as partes que precisam de revisão.

[NOVA]: O aviso da API do Gemini do Google dá aos desenvolvedores de agentes uma tarefa de segurança que eles podem fazer hoje.

[ALLOY]: O Google é direto sobre a premissa: as chaves de API do Gemini são chaves de API padrão do Google, e chaves de API são segredos abertos. Trate-as como tokens de portador pagos. Se elas acabarem em um cliente navegador, um repositório gerado, uma demo pública ou uma extensão não confiável, o risco não é teórico. Pode virar uso inesperado e cobrança.

[NOVA]: A orientação sobre chave de API do Gemini é útil porque transforma a segurança de uma repreensão nebulosa em uma tarefa finita.

[NOVA]: A primeira correção é o isolamento. Crie chaves em projetos independentes em vez de misturar cada experimento em um projeto de produção. Depois adicione restrições de API para que a chave possa chamar apenas o serviço pretendido, como a API do Gemini. Se uma chave vazada puder chamar mais serviços do que o app precisa, o raio de destruição é maior do que o necessário.

[ALLOY]: As restrições de aplicativo vêm a seguir. Uma chave pode ser restringida por site, faixa de IP, identificador de bundle do iOS ou par de package e certificado do Android. Como uma chave usa um tipo de restrição de aplicativo, formatos de aplicativo separados devem receber chaves separadas. Um app de navegador, processo de servidor, app iOS e app Android não devem compartilhar uma única string de uso geral.

[NOVA]: As chaves do lado do servidor pertencem a um cofre de segredos como o Secret Manager ou um sistema equivalente. Elas não devem ser incluídas em código cliente visível. Um exemplo gerado que chama uma API de modelo pago diretamente de um cliente navegador público é um rascunho, não um padrão implementável.

[ALLOY]: O monitoramento fecha o ciclo. Use o Cloud Asset Inventory ou listagem de chaves para saber o que existe. Observe as métricas de contagem de requisições por ID de credencial. Se uma chave se espalhar, rotate-a e recrie a substituição com as mesmas restrições. Não faça a rotação de uma chave frouxa para outra chave frouxa.

[NOVA]: A tarefa de testar agora é direta. Escolha uma chave do Gemini. Confirme o projeto. Confirme as restrições de API. Confirme as restrições de aplicativo. Confirme onde está armazenada. Confirme como o uso é monitorado. Confirme como fazer a rotação. Se alguma resposta for "não tenho certeza", essa é a próxima correção. ...

[ALLOY]: Isso também é um problema de app gerado. Um desenvolvedor pode pedir a um agente para estruturar uma demo, e a demo pode casualmente colocar uma chave paga em código do lado do cliente. O fluxo seguro é colocar a chamada do modelo atrás de uma rota do servidor, ler o segredo do ambiente do servidor, retornar apenas o resultado necessário ao navegador e documentar como a chave é restringida. Isso não é engenharia de segurança sofisticada. Esse é o caminho mínimo do protótipo para algo que você pode compartilhar sem convidar uma bagunça de cobrança.

[NOVA]: O Copilot Auto e a busca semântica de issues tornam o planejamento e o roteamento de modelos parte da superfície do agente de codificação.

[ALLOY]: O Copilot Auto agora roteia baseado em sinais de tarefa enquanto respeita a política de admin e mostra qual modelo foi selecionado. Isso é útil para o trabalho diário porque nem toda tarefa precisa do modelo de raciocínio mais pesado. Uma explicação curta, uma pequena edição ou um diagnóstico de primeira passagem podem ser melhor atendidos por algo mais rápido ou mais barato.

[NOVA]: O Copilot Auto do GitHub é o lado do roteamento de modelos, e a busca semântica de issues é o lado do contexto. Junte-os e o trabalho de bugs começa com melhores evidências.

[NOVA]: O tradeoff é a reprodutibilidade. Se a escolha do modelo muda baseada em classificação de tarefa, disponibilidade, confiabilidade, assinatura ou política, duas execuções do mesmo prompt podem não ser comparáveis. Para trabalho de baixo risco, isso pode ser fine. Para migrações, correções de segurança, patches de produção ou reprodução de incidentes, registre o modelo ou fixe-o.

[ALLOY]: A busca semântica de issues é o recurso do Copilot mais acionável para equipes. Ele permite que o Copilot Chat encontre issues relacionadas por significado, não apenas por texto exato ou labels. Isso pode mudar a ordem do trabalho de codificação. Em vez de jogar um repositório em um agente e pedir para ele corrigir uma reclamação vaga, primeiro peça issues relacionadas agrupadas por sintoma, plataforma, modo de falha ou área de release.

[NOVA]: O padrão de testar agora é: pesquise primeiro, edite depois. Peça o cluster de issues relacionadas. Pergunte quais modos de falha se repetem. Escolha um cluster estreito. Depois passe essa tarefa refinada para um agente de codificação com os links de issues relevantes e uma condição de sucesso. Isso dá ao agente melhor contexto e reduz a chance de ele corrigir o sintoma mais barulhento enquanto perde o padrão real.

[ALLOY]: A política de admin importa aqui também. Se uma organização desabilita certos modelos ou define regras de roteamento, a superfície do agente deve respeitar isso. O roteamento de modelos agora faz parte da governança de ferramentas de desenvolvedor. Não é apenas uma preferência pessoal.

[NOVA]: O hábito prático é tratar a escolha do modelo e a recuperação de issues como evidências. Qual modelo respondeu? Quais issues foram consideradas? Qual cluster foi selecionado? Qual teste prova a correção? Isso é trace o suficiente para tornar o trabalho do agente de codificação menos misterioso. ...

[ALLOY]: Um bom fluxo de trabalho em equipe é fazer da busca semântica de issues o primeiro passo do trabalho de bug. Pesquise o sintoma, agrupe os relatórios relacionados, escolha um cluster e só então peça ao agente de codificação um patch. Para edições de baixo risco, o Copilot Auto pode escolher o modelo. Para edições de alto risco, fixe ou registre o modelo. Isso mantém velocidade para o trabalho diário e rastreabilidade para mudanças que talvez precisem ser reproduzidas depois.

[ALLOY]: Junte tudo isso e a próxima fila está clara. Atualize o OpenClaw, Codex e Claude Code, depois teste as superfícies alteradas em vez de apenas imprimir versões. Para o OpenClaw: descobertas de políticas, rejeição de symlink de segredo, roteamento de provedor, saída de cron, conclusão de subagente, transferência de voz e comportamento de timeout de imagem.

[NOVA]: Para o Codex: uma captura de tela de app, uma tarefa orientada a metas, uma verificação de prontidão de controle remoto, uma inspeção de perfil de permissão, uma verificação de inventário de plugins e um evento de ciclo de vida que você realmente registraria. Para o Claude Code: uma sessão pinned em background, uma revisão de código em um diff real, um servidor MCP paginado e uma tarefa pesada de shell.

[ALLOY]: Para as notícias mais amplas: projete um túnel MCP com permissões antes da conectividade, esboce um estado durável para um agente de longa execução, estime se um serviço de agente está principalmente ocioso e stateful, migre uma tarefa do Gemini CLI para o Antigravity, experimente uma tarefa de uso de computador com um modelo pequeno dentro de uma sandbox, defina o escopo de um agente de dados somente leitura, bloqueie uma chave do Gemini e use busca semântica de issues antes de editar.

[NOVA]: O critério não é "o modelo disse algo inteligente?". O critério é se o sistema é observável, tem escopo definido, é recuperável e útil o suficiente para rodar duas vezes. A boa notícia de hoje é que mais partes da stack de agentes estão expondo as peças necessárias para chegar lá.

[ALLOY]: A melhor forma de tornar isso acionável é escolher um fluxo de trabalho de build para amanhã, não dez de uma vez. Por exemplo: pegue um bug de UI, capture com o Appshots, defina uma meta do Codex, corrija e verifique o resultado. Ou pegue uma ferramenta de status privada, exponha através de um túnel MCP somente leitura e registre cada chamada. Ou pegue uma tarefa de agente de longa execução instável, escreva a sequência de eventos e decida onde o resume deveria acontecer. Um build pequeno funcionando ensina mais do que um plano gigante.

[NOVA]: E mantenha cada fluxo de trabalho honesto. Ele deve ter um trigger, um limite de permissão estreito, uma condição de sucesso, uma condição de falha e um passo de verificação. Isso se aplica seja o fluxo de trabalho uma query de agente de dados, uma tarefa de navegador com modelo pequeno, um triage de issues do Copilot ou um cron job do OpenClaw. Se o agente não consegue te dizer o que fez, o que usou e o que mudou, o build não está pronto para uso diário.

[ALLOY]: Mais um filtro prático: escolha o fluxo de trabalho que remove a maior chatice repetida. Se um humano fica rechecando o mesmo dashboard, faça disso a tarefa de navegador com modelo pequeno. Se um time fica fazendo a mesma pergunta de banco de dados, faça disso o agente de dados somente leitura. Se um agente de código continua perdendo contexto de issues, faça da busca semântica de issues o passo de intake. As notícias importam porque dão aos construtores melhores alças em problemas que eles já têm, e melhores formas de enviar sem chutar.

[NOVA]: Exttras de picks dos builders também merecem um scan final rápido: feature flags para comportamento de IA, trabalho de eficiência de imagem e benchmarks de modelos de edge. Adicione um kill switch em torno de uma mudança de prompt ou config, faça benchmark de um caminho de imagem para latência e custo, ou teste um modelo local no dispositivo real ao invés de assumir que números de desktop se transferem.

[ALLOY]: Links de fontes estão na página do episódio desta semana agora mesmo. Isso é o AgentStack Daily. Eu sou ALLOY.

[NOVA]: E eu sou NOVA. Voltamos em breve. Toby On Fitness Tech dot com.