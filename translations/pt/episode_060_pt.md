[NOVA]: Eu sou NOVA. [ALLOY]: Eu sou ALLOY, e este é o AgentStack Daily...

[NOVA]: Hoje vamos ficar em uma única linha o tempo todo: superfícies de controle. Não é sobre vibes, não é sobre "a IA está ficando mais inteligente", mas sim as alavancas práticas que definem o que um agente pode fazer, onde pode fazer, e como você pode supervisionar quando algo dá errado.

[ALLOY]: As novidades de lançamento e produtos no início são bastante específicas, mas operacionalmente importantes. A versão mais recente do Claude Code adiciona suporte ao modo automático em provedores de nuvem gerenciados—Bedrock, Vertex e Foundry—quando você ativa explicitamente com uma variável de ambiente. A atualização do app Codex da OpenAI adiciona uso de computador Windows e supervisão remota do celular ou Mac enquanto o host Windows mantém seu repo e runtime locais, além de comportamento mais rápido no navegador integrado e uma nova superfície de Codex Profiles para uso e atividade de tokens.

[NOVA]: Depois migramos para uma mudança na API voltada a desenvolvedores da Anthropic que é silenciosamente poderosa: a Messages API agora aceita entradas de sistema dentro do array de mensagens, o que significa que seu harness pode atualizar instruções de runtime no meio da execução sem se passar pelo usuário, e sem transformar seu prompt em um blob constantemente crescente.

[ALLOY]: E o radar de projetos é um único tema com quatro ângulos: memória arquitetural que você pode consultar, memória de agente que decai para não virar autoridade obsoleta, agentes de código locais apenas que tornam a iteração privada barata, e loops de reparo baseados em grafos que forçam evidências para a correção. Vamos entrar nisso. ...

[NOVA]: O fio condutor no EP060 é que "capacidade de agente" está começando a parecer menos uma escolha de modelo único e mais uma pilha de contratos explícitos.

[ALLOY]: Contrato um é a localização de execução. Se o agente está agindo dentro de um ambiente de provedor de nuvem gerenciado, isso muda identidade, logging, residência de dados e o trilha de auditoria que você pode obter depois. Contrato dois são os limites do host. Se o agente está controlando um desktop Windows, você precisa saber se os arquivos e shell vivem no host remoto ou foram copiados para outro ambiente. Contrato três é a propriedade das instruções. Se seu harness não consegue atualizar o contrato de sistema no meio da execução, o modelo acaba adivinhando o que mudou.

[NOVA]: E o contrato quatro é memória. Muitos times falam sobre "memória de agente" como se a resposta fosse manter toda transcrição para sempre e re-injetar. Na prática, essa abordagem tende a criar um novo modo de falha: orientação obsoleta é tratada como política atual, e detalhes irrelevantes sufocam os poucos fatos que você realmente precisava.

[ALLOY]: Então o ponto do conjunto de hoje é mostrar a pilha ficando mais explícita. O modo automático está protegido atrás de uma variável de ambiente para que possa ser testado deliberadamente. O uso de computador Windows mantém contexto local no host enquanto a supervisão se torna móvel. Entradas de sistema dentro de arrays de mensagens separam "o que o usuário quer" de "o que o runtime permite agora". E as ferramentas de memória que estamos cobrindo são principalmente sobre estrutura e frescor em vez de acumulação bruta.

[NOVA]: Se você teve um agente falhando no último mês, provavelmente você não perdeu porque o modelo não conseguia escrever código. Você perdeu porque a execução não tinha os guardrails certos, as evidências certas, ou a capacidade certa de atualizar premissas quando algo mudou.

[ALLOY]: Com esse enquadramento, vamos começar com o bloco de lançamentos e produtos do início do episódio. ...

[NOVA]: Primeiro item: a versão mais recente do Claude Code adiciona suporte ao modo automático no Bedrock, Vertex e Foundry para Opus 4.7 e Opus 4.8, mas apenas quando você define CLAUDE_CODE_ENABLE_AUTO_MODE=1.

[ALLOY]: Dois detalhes importantes estão escondidos dentro dessa frase aparentemente pequena. Um é que não é "modo automático está agora em todo lugar." É "modo automático existe em mais faixas de provedores, e você precisa opt-in." O outro é que as faixas de provedores importam tanto quanto o recurso em si, porque o modo automático é fundamentalmente uma superfície de permissão e roteamento.

[NOVA]: Vamos descompactar o modo automático em termos práticos. Em um agente de código, existe um espectro de ações: ler arquivos, buscar, rodar testes, instalar dependências, iniciar um servidor dev, editar código, fazer commits, abrir PRs, e assim por diante. "Modo automático" é o rótulo para o sistema deciding que certos passos podem ser executados automaticamente sem parar para confirmação humana em cada passo.

[ALLOY]: Isso não é apenas um toggle de conveniência. Muda o perfil de risco da execução do agente. Se seu agente pode rodar comandos automaticamente, o "limite de segurança" não é mais apenas o modelo. É a combinação de comportamento do modelo, política do harness, permissões de ferramentas, sandbox, e o ambiente do provedor onde essas chamadas de ferramentas acontecem.

[NOVA]: E é aí que entram as faixas de nuvem gerenciada. Bedrock, Vertex e Foundry são caminhos comuns quando um time quer acesso ao modelo com identidade e conformidade nativas da nuvem. Nesses ambientes, geralmente há uma forte preferência de que requisições e logs fiquem dentro de um limite específico de nuvem, vinculados a credenciais organizacionais, com políticas de acesso que você pode aplicar centralmente.

[ALLOY]: Então o suporte ao modo automático ali significa que você pode avaliar comportamento de ação automática sob a mesma realidade de IAM e auditoria da produção. Se você testa o modo automático apenas em um fluxo de workstation local de desenvolvedor e depois faz deploy em um contexto de nuvem gerenciada, você está mudando muito do sistema circundante ao mesmo tempo—identidade, networking, logging, e às vezes até padrões de acesso ao sistema de arquivos.

[NOVA]: O portão explícito da variável de ambiente é o outro ponto-chave. Se você está operando um toolchain de time, geralmente você não quer uma surpresa onde uma atualização muda comportamento de "pergunte antes de fazer coisas" para "faça coisas." Opt-in gating força um ponto de ativação intencional.

[ALLOY]: Esse gating também te dá uma estratégia de teste limpa. Você pode rodar as mesmas tarefas com e sem modo automático e comparar resultados: número de chamadas de ferramentas, número de ações destrutivas tentadas, se o agente escala apropriadamente quando está incerto, e se obedece restrições de "sem writes" ou "sem network" quando elas estão em efeito.

[NOVA]: Aqui está um jeito concreto de testar isso sem fazer seu repo o experimento. Escolha um projeto pequeno e descartável ou um branch seguro conhecido. Defina três categorias de tarefas.

[ALLOY]: Categoria um: tarefas apenas de leitura. Peça ao agente para produzir um resumo arquitetural, identificar pontos de entrada, listar os testes de integração e apontar quaisquer riscos óbvios de dependência. No modo automático, você quer ver ele fazer leituras de arquivos e buscas de forma eficiente, sem inventar chamadas de ferramentas que não precisa.

[NOVA]: Categoria dois: tarefas de execução segura. Deixe ele rodar a suíte de testes, iniciar o servidor de desenvolvimento, ou rodar um linter—coisas que são majoritariamente reversíveis e não modificam muito. Sua verificação aqui é se o agente escolhe comandos que são apropriados para o projeto e ambiente. Por exemplo: ele tenta npm test em um repositório que é claramente Python? Ele percebe pnpm-lock e usa pnpm? Ele roda o subconjunto mínimo de testes para uma mudança específica?

[ALLOY]: Categoria três: tarefas de escrita com restrições rigorosas. Dê a ele uma pequena mudança, como atualizar uma assinatura de função e atualizar os locais de chamada, ou adicionar uma verificação de null ausente. Seu harness ainda deve impedir qualquer coisa que você considere alto risco—como dar push, publicar pacotes, alterar arquivos de secrets, ou modificar manifests de deployment—a menos que você aprove explicitamente.

[NOVA]: O ponto é medir se o modo automático reduz o atrito nas tarefas que você quer acelerar, sem aumentar silenciosamente o risco. A variável de ambiente facilita rodar testes A/B e manter o comportamento de produção fixo até você estar satisfeito.

[ALLOY]: Agora, a história maior do produto: a atualização do Codex da OpenAI em 29 de maio. Há quatro mudanças práticas destacadas nas notas que estamos usando: uso do computador Windows, controle remoto de um dispositivo móvel ou Mac enquanto o Windows permanece como host, melhorias na velocidade e estabilidade do navegador in-app, e Codex Profiles com identidade, atividade, estatísticas de uso e atividade de tokens.

[NOVA]: Começando pelo uso do computador Windows. "Uso do computador" é a categoria onde o agente pode ver a UI do desktop e interagir com ela: clicando em botões, digitando em campos, trocando de janelas e navegando em apps que não estão convenientemente envolvidos em uma API.

[ALLOY]: No Windows especificamente, isso importa para muitos fluxos de trabalho reais de desenvolvimento. Existem stacks de apps nativos do Windows, ferramentas internas de enterprise e uma enorme quantidade de trabalho do tipo "a única forma de fazer isso é clicar através da GUI". Pense em installers, consoles administrativos proprietários, gerenciadores de credenciais e certos fluxos de IDE ou depurador.

[NOVA]: Mas a questão operacional central com qualquer produto de uso de computador é: onde a execução acontece e onde os arquivos ficam? O limite da atualização é explícito. Você pode supervisionar do iOS, Android ou Mac, mas a máquina Windows permanece como host para arquivos do projeto, shell, servidor de apps e contexto local.

[ALLOY]: Esse limite tem algumas consequências que vale destacar. Primeiro, reduz a duplicação de dados. O repositório não precisa ser copiado para um ambiente remoto só para o agente poder rodar. Segundo, reduz a latência no loop de "rodar o servidor, verificar o navegador, ajustar o código, rodar os testes novamente" porque o runtime é local aos arquivos.

[NOVA]: Terceiro, muda o modelo de confiança. Seu dispositivo de supervisão é mais como uma superfície de controle remoto e monitoramento, não o lugar onde o trabalho realmente é executado. Isso é útil porque significa que você pode se afastar da mesa e ainda assim conduzir a sessão, mas você não está acidentalmente movendo toda a operação para um limite de segurança diferente.

[ALLOY]: O risco a entender é que o uso de computador é, por design, autoridade ampla. Se o agente pode clicar e digitar, ele potencialmente pode fazer qualquer coisa que você pode fazer naquele ambiente, incluindo ações que são difíceis de reverter. Então a abordagem recomendada é: teste em um aplicativo de baixo risco antes de depender dele para trabalho importante.

[NOVA]: Baixo risco aqui significa um projeto que pode ser resetado, não toca credenciais de produção, e não vai causar danos se rodar um comando inesperado. Um bom alvo inicial é um app web de exemplo, um serviço demo local-only, ou um repositório que você pode descartar.

[ALLOY]: O primeiro teste é simplesmente confiabilidade: ele consegue interagir consistentemente com estados comuns de UI de desenvolvedor? Coisas como: uma janela de terminal que precisa de foco, um prompt de UAC, um navegador com múltiplas abas, um editor que弹出 "arquivo alterado no disco", um test runner que requer rolagem para ver falhas.

[NOVA]: O segundo teste é intenção delimitada. Dê a ele uma tarefa que tem uma condição de fim clara, como "rode os testes e me diga o nome do primeiro teste que falhou e o erro". Você quer ver se o agente fica na tarefa ou se distrai por caminhos paralelos, como atualizar dependências ou reformatar código que não foi solicitado.

[ALLOY]: O terceiro teste é recuperação. Crie intencionalmente pequenas interrupções: mate o servidor de desenvolvimento, desconecte a rede brevemente, cause uma falha de build mudando um config, ou abra um modal. Então observe se o agente percebe que está preso, reporta o problema e pede orientação quando atinge um limite que não consegue ultrapassar.

[NOVA]: Agora, as melhorias do navegador in-app. Em fluxos de trabalho com agentes, o navegador não é "só um navegador". É frequentemente a superfície de verificação. É onde você confirma que a correção realmente funciona, onde você reproduz o bug, onde você inspeciona chamadas de rede e onde você valida fluxos de UI.

[ALLOY]: Se o navegador in-app for lento ou instável, o loop de verificação do agente degrada. Isso leva a um dos piores padrões de falha em codificação automatizada: o agente afirma que uma correção está correta porque não consegue rodar de forma confiável o último passo que a disprovaria.

[NOVA]: Então "comportamento do navegador in-app mais rápido e estável" pode soar como uma linha depolimento de produto, mas impacta diretamente o quanto você pode confiar nas afirmações de conclusão do agente. Um caminho de navegador estável significa que o agente pode rodar novamente os passos de reprodução e realmente observar o resultado.

[ALLOY]: O item final da atualização do Codex é Codex Profiles: identidade, atividade ao longo do tempo, detalhes do perfil, estatísticas de uso e atividade de tokens. Esta é uma superfície de controle no sentido mais simples: inspectabilidade.

[NOVA]: Em sessões de longa duração, você precisa responder perguntas como: qual perfil executou esta tarefa, qual foi a pegada de uso, e o consumo de tokens corresponde ao que você esperava? Se você está supervisionando trabalho remoto entre dispositivos, você também quer confirmar traces de identidade e atividade, especialmente se múltiplas pessoas compartilham um host Windows.

[ALLOY]: A atividade de tokens como uma superfície exposta é importante para debugging. Se uma execução de agente de repente fica mais cara, a causa geralmente não é "o modelo piorou." É algo como: está lendo repetidamente os mesmos arquivos grandes, está re-summarizando histórico demais, está preso em um loop de testes falhando, ou está chamando ferramentas com saídas enormes.

[NOVA]: Uma superfície de profile que torna isso visível é a diferença entre "isso parece caro" e "conseguimos ver qual etapa do workflow inflou os tokens." E uma vez que você consegue ver, consegue corrigir: adicionar um limite de tamanho de arquivo, adicionar truncamento de logs, adicionar uma etapa de recuperação de memória mais estruturada, ou apertar o plano de verificação.

[ALLOY]: Juntando essas duas histórias principais — o modo automático do Claude Code em lanes de cloud gerenciada e o computer use do Codex Windows com supervisão remota — você obtém um único tema: o trabalho de agentes está ficando menos preso a uma única máquina e mais preso a pontos de governança explícitos.

[NOVA]: O modo automático no Bedrock, Vertex e Foundry é sobre trazer automação baseada em políticas para ambientes de cloud empresarial. A supervisão remota do Codex é sobre deixar um humano pilotar de qualquer lugar enquanto mantém a execução local no host que tem o repo e o app rodando.

[ALLOY]: O movimento recomendado não é "ligar tudo." É tratar ambos como experimentos controlados. Explicitamente controlar o modo automático, testar com tarefas seguras e medir o comportamento. Experimentar o computer use do Windows em um ambiente descartável, e só então decidir qual escopo de trabalho real você confia a ele.

[NOVA]: A seguir, vamos falar sobre uma mudança que é menos visível para usuários finais mas é extremamente visível para construtores de harness: instruções de runtime que podem ser atualizadas como entradas de sistema no meio da execução. ...

[ALLOY]: O anúncio do Opus 4.8 da Anthropic incluiu uma mudança voltada para desenvolvedores que importa mesmo se você nunca trocar de modelo: a API de Messages agora aceita entradas de sistema dentro do array de mensagens.

[NOVA]: Isso parece sutil, então aqui está o porquê muda como você constrói agentes. Historicamente, muitos harnesses tratam "prompt de sistema" como um blob fixo definido no início da execução. Então tudo mais — mensagens de usuário, saídas de ferramentas, observações — é adicionado em uma sequência.

[ALLOY]: Mas execuções reais de agentes não são estáticas. Permissões mudam. Orçamentos mudam. O ambiente muda. O harness aprende novos fatos que o modelo deve obedecer. E se você não consegue atualizar o contrato de sistema de forma limpa, acaba com padrões complicados.

[NOVA]: Padrão um é forçar a atualização através de um turno de usuário. Isso polui o audit trail, porque faz parecer que o usuário pediu mudanças de política quando na verdade o runtime está se adaptando ao estado.

[ALLOY]: Padrão dois é enfiar novas notas de política em um prompt de sistema crescente e reenviando tudo. Isso aumenta custo, aumenta pressão de contexto, e na prática pode quebrar otimizações de cache porque o "prefixo" continua mudando.

[NOVA]: Padrão três é pedir ao modelo para inferir estado alterado a partir de logs. Isso funciona até não funcionar. Se o modelo perder uma linha de log, vai continuar operando como se nada tivesse mudado — como se ainda tivesse permissão para escrever arquivos, ou ainda tivesse acesso à rede, ou ainda tivesse orçamento suficiente para rodar uma suite de testes completa.

[ALLOY]: Entradas de sistema dentro do array de mensagens dão ao harness uma ferramenta mais precisa: você pode inserir ou adicionar uma mensagem de role de sistema que diz, efetivamente, "o contrato agora é diferente," sem fingir que o usuário disse isso.

[NOVA]: E isso permite separação de responsabilidades. A lane do usuário pode permanecer como um registro limpo de intenções, aprovações e esclarecimentos. A lane de sistema pode permanecer como a declaração autoritativa de runtime de restrições: ferramentas permitidas, detalhes do ambiente, orçamento e regras operacionais.

[ALLOY]: Vamos deixar isso concreto. Imagine uma execução de agente de coding onde você começa com permissões amplas. O agente tem permissão para ler arquivos, rodar testes e escrever mudanças em um branch. No meio da execução, o harness detecta que está em um estado de repo protegido — talvez tenha aberto acidentalmente um worktree de produção, ou a política do branch mudou, ou o agente agora está operando em um diretório marcado como sensível.

[NOVA]: Com entradas de sistema editáveis, o harness pode injetar uma nova mensagem de sistema: "Escritas agora estão desabilitadas. Você só pode propor diffs e pedir aprovação." Isso é muito mais limpo do que dizer ao modelo em uma mensagem de usuário ou esperar que ele descubra.

[ALLOY]: Outro cenário comum: orçamento de tokens. Alguns harnesses alocam um orçamento por job ou por fase. No início da execução, você pode permitir exploração. Depois, uma vez que o agente tem um plano, você pode apertar o orçamento para focar em execução.

[NOVA]: Com entradas de sistema, você pode atualizar a instrução: "Orçamento restante agora está baixo. Prioritize leituras mínimas de arquivos, rode testes direcionados apenas, e resuma antes de agir." O ponto-chave é que é uma atualização de instrução atrelada ao estado de runtime, não uma preferência de usuário que pode se misturar com a tarefa.

[ALLOY]: Contexto de ambiente é outro. Suponha que o harness detecta que o sandbox mudou de um container de dev completo para um ambiente restrito sem rede. Ou detecta que um cache de dependências está vazio, então instalações serão lentas. Ou descobre que o repo usa uma ferramenta de monorepo que requer uma sequência particular de comandos.

[NOVA]: Você pode injetar esses como fatos de sistema. Isso significa que o modelo não precisa rediscover eles cada vez, e não precisa adivinhar baseado em observações parciais.

[ALLOY]: Agora, uma das principais alegações das notas é a preservação do cache de prompts. Em sessões longas, o cache é importante porque a parte mais cara das chamadas repetidas é frequentemente o "prefixo" repetido—as instruções estáveis, a orientação do repositório e o contexto de alto nível.

[NOVA]: Se o seu harness puder anexar mensagens do sistema como entradas discretas em vez de reescrever todo o prompt do sistema, você pode manter um grande prefixo estável inalterado. Isso melhora a eficácia das estratégias de cache e reduz a pressão para comprimir tudo em uma mega-instrução no início.

[ALLOY]: Mesmo sem cache explícito, isso ajuda na clareza. Em vez de um prompt de sistema gigante que inclui uma dúzia de atualizações históricas, você pode ter uma linha do tempo de mensagens do sistema: contrato inicial, depois atualizações conforme as condições mudam.

[NOVA]: Mas é necessária uma disciplina aqui. Se você usar entradas do sistema sem cuidado, pode criar instruções do sistema conflitantes. Por exemplo: o sistema inicial diz "Você pode escrever no repositório," depois o sistema diz "Escritas estão desabilitadas," e mais tarde novamente diz "Escritas permitidas para arquivos em /docs." Se você não definir precedência, o modelo pode tentar satisfazer todos de uma vez.

[ALLOY]: Então o harness deve tratar as entradas do sistema como atualizações de estado com um claro "o mais recente vence" ou uma sobrescrita claramente delimitada. Muitas vezes é útil escrever entradas do sistema de forma estruturada, mesmo que ainda sejam texto simples.

[NOVA]: Por exemplo, você pode incluir um pequeno formato de cabeçalho de seção dentro da mensagem do sistema: "Permissões: leitura sim, escrita não, rede não." "Orçamento: tokens restantes baixos." "Execução: rodar testes permitido, instalações não permitidas." O objetivo é facilitar para o modelo reconciliar o estado atual.

[ALLOY]: Você também quer manter as atualizações do sistema geradas por máquina distintas da política do sistema autoria humana. Um bom padrão é: uma mensagem inicial do sistema para sua política permanente e regras de segurança, e depois mensagens subsequentes do sistema que são puramente "fatos de runtime."

[NOVA]: Fatos de runtime podem incluir: nome da branch atual, se a árvore de trabalho está limpa, quais testes rodaram por último e seus resultados, se o agente já tentou uma correção e ela falhou, quais ferramentas estão atualmente disponíveis, e se o ambiente é sandboxed.

[ALLOY]: Essa última peça—disponibilidade de ferramentas—é um dos maiores pontos de falha no dia a dia em pilhas de agentes. Um agente acha que pode fazer algo porque fez isso antes na execução, mas então uma ferramenta é revogada ou uma permissão muda, e ele continua tentando a mesma chamada.

[NOVA]: Uma atualização de entrada do sistema pode fechar essa lacuna imediatamente. Se o harness revogar o acesso à rede, ele pode injetar: "Chamadas de ferramentas de rede agora são proibidas." Então o modelo deve parar de tentar curl, instalações de pacotes que requerem downloads, ou chamadas de API remotas.

[ALLOY]: Há outra vantagem sutil: separação auditável. Quando você revisar uma execução posteriormente, poderá distinguir entre o que o usuário solicitou e o que o runtime impôs. Isso importa para conformidade, mas também importa para depuração. Se uma execução se comportou de forma estranha, você pode ver se uma restrição do runtime a forçou por um caminho estranho.

[NOVA]: Em operações de agentes, essa é a diferença entre "o modelo fez uma má escolha" e "o harness mudou as regras e o modelo obedeceu." Esses são problemas diferentes com correções diferentes.

[ALLOY]: Teste sugerido para construtores de harness: implemente uma inversão de permissão no meio da execução e verifique se o modelo responde corretamente. Inicie uma execução onde escritas são permitidas. Deixe o modelo propor ou até começar edições. Então injete uma entrada do sistema que desabilite escritas e peça para ele continuar.

[NOVA]: Você está procurando alguns comportamentos. Um: ele para de tentar ações de escrita e troca para planejamento ou propostas de diff? Dois: ele reconhece explicitamente a mudança nas restrições? Três: ele tenta comportamento de contorno, como codificar conteúdos de arquivos no chat como um "patch sugerido" em vez de usar ferramentas?

[ALLOY]: Se você ver comportamento de contorno, talvez precise fortalecer a linguagem da sua política. O objetivo não é impedir o modelo de ser útil; é manter o contrato real. "Sem escritas" deve significar sem escritas, mesmo que o modelo acredite ter a correção perfeita.

[NOVA]: Outro teste recomendado: aperto de orçamento. Deixe o agente começar uma fase de exploração, então injete uma entrada do sistema que defina um orçamento estrito e uma lista de prioridades. Depois veja se ele realmente estreita suas chamadas de ferramentas: menos arquivos, diffs menores, testes direcionados.

[ALLOY]: Se não fizer isso, é um sinal de que você precisa tornar a instrução de orçamento mais concreta. Modelos respondem melhor a restrições operacionais quando você especifica o que fazer. Por exemplo: "Leia apenas os arquivos que você já referenciou. Rode apenas o teste que está falhando. Resuma as mudanças em cinco bullets antes de fazer edições."

[NOVA]: Reconecte isso à história de release anterior. O modo automático do Claude Code e a supervisão remota do Codex são ambos sobre tornar a superfície de execução mais capaz. À medida que você amplia essa superfície, a capacidade de atualizar restrições de runtime no meio da execução se torna mandatória. Caso contrário, você está rodando um agente mais poderoso com um contrato frágil.

[ALLOY]: A seguir vamos para o radar de projetos, começando com duas ferramentas complementares de memória: OpenLore para orientação arquitetural, e Mnemo para memória persistente com decaimento. ...

[NOVA]: Primeiro item do radar de projetos é OpenLore. A maneira mais simples de descrevê-lo é: uma camada de memória arquitetural local para agentes de codificação que se torna consultável através de MCP.

[ALLOY]: A premissa central é que agentes desperdiçam contexto ao redescobrir a estrutura do projeto. Até mesmo agentes de codificação fortes frequentemente começam uma sessão lendo uma árvore de diretórios, escaneando arquivos README, procurando pontos de entrada, dando grep em nomes de funções e montando um mapa mental do zero.

[NOVA]: Isso não é apenas caro em tokens e tempo. Também é propenso a erros. Se o agente identifica erroneamente um ponto de entrada, ele pode construir um plano inteiro baseado em uma suposição errada—como editar um serviço legado em vez do atual, ou modificar uma biblioteca compartilhada quando a mudança pertence a uma camada de adaptador.

[ALLOY]: O OpenLore ataca isso indexando a base de código em artefatos estruturados: saídas de análise estática, grafos de chamadas, clusters arquiteturais, "specs vivas" e detecção de drift. Depois, ele expõe ferramentas MCP como orientation e graph expansion para que um agente possa pedir primeiro um resumo compacto e só expandir o que precisa.

[NOVA]: Vamos detalhar por que grafos de chamadas e clusters são importantes. Um grafo de chamadas é o mapa de quais funções ou módulos chamam quais outros. Quando um agente recebe a tarefa de "corrigir um bug nos totais de checkout", não é suficiente encontrar o arquivo chamado checkout.ts. Você precisa saber onde os totais são calculados, quem consome esse resultado e quais caminhos são exercidos por quais fluxos.

[ALLOY]: Se você tem um grafo de chamadas, pode fazer perguntas como: "Quais são os chamadores upstream dessa função?" e "Quais são os efeitos downstream se eu mudar esse tipo de retorno?" Esse é exatamente o tipo de pergunta que reduz quebras acidentais.

[NOVA]: Clusters arquiteturais são um conceito de nível mais alto: agrupar arquivos ou módulos em subsistemas. Muitos repos se parecem planos para uma busca ingênua. Você pode ter vinte diretórios que todos contêm código de "service", mas apenas alguns são relevantes para a tarefa. O clustering ajuda um agente a evitar explorar vizinhanças irrelevantes do repo.

[ALLOY]: "Specs vivas" são particularmente úteis para fluxos de trabalho com agentes porque o código muda, mas a intenção por trás do código nem sempre vive nos comentários do código. Uma spec viva é um resumo mantido de como um subsistema ésuposto para se comportar, frequentemente derivado de análise estática mais documentação curationada.

[NOVA]: A detecção de drift é o trilho de segurança. Se a spec diz uma coisa e o código desviou, o OpenLore pode sinalizar isso. Para um agente, a detecção de drift é um sinal para desacelerar. Significa que o repo pode ter comportamento inconsistente ou migrações incompletas.

[ALLOY]: A camada MCP é o que torna isso imediatamente relevante para um stack de agentes. MCP é a interface que agentes usam para chamar ferramentas. Se o OpenLore fornece ferramentas MCP como "orientation" e "expand graph", então qualquer agente que consiga falar MCP—Claude Code, Codex em harnesses compatíveis com MCP, Hermes, sessões conectadas ao OpenClaw—pode puxar memória arquitetural sem ler metade do repo de novo.

[NOVA]: O ângulo da disciplina de tokens é onde isso se torna uma vantagem prática. Em vez de injetar um resumo gigante do repositório toda vez, você pode recuperar um blob de orientação pequeno: "Aqui estão os serviços de nível superior, os pontos de entrada principais, os caminhos de chamada-chave para a tarefa atual e os alvos de teste prováveis." Depois você deixa o agente pedir para expandir nós específicos.

[ALLOY]: Esse fluxo de trabalho de "expandir só o que importa" é a diferença entre uma camada de memória útil e uma bomba de contexto. Se a recuperação de memória sempre retorna um muro gigante de texto, o agente vai tanto ignorar quanto se afogar nele. A expansão de grafo é um botão de controle.

[NOVA]: Aqui está um fluxo de trabalho de avaliação recomendado para o OpenLore que não requer integração profunda no início. Escolha um repo onde agentes repetidamente cometem os mesmos erros de orientação. Exemplos comuns: monorepos com múltiplos apps, repos com implementações antigas e novas, ou sistemas com múltiplos pontos de entrada dependendo do ambiente.

[ALLOY]: Passo um: execute a indexação do OpenLore e use a ferramenta de orientation para produzir um resumo arquitetural. Passo dois: execute uma sessão de agente de codificação sem o OpenLore e peça para ele planejar uma mudança. Passo três: execute a mesma sessão de planejamento, mas forneça a saída de orientation do OpenLore primeiro.

[NOVA]: Compare os planos. Especificamente: o plano assistido pelo OpenLore escolhe arquivos diferentes? Ele identifica os pontos de entrada corretos mais rápido? Ele propõe testes que realmente estão conectados aos caminhos de código envolvidos?

[ALLOY]: Também compare a taxa de "primeiro erro". Em muitas execuções de agentes, o primeiro erro é selecionar o ponto de partida errado. Se o OpenLore reduz isso, ele já está se pagando.

[NOVA]: Agora item dois do radar de projetos: Mnemo. Ele trata a memória do agente como um grafo de conhecimento local com decaimento.

[ALLOY]: O posicionamento do Mnemo é "cognição de engenharia persistente," que é uma frase útil porque implica mais do que armazenar fatos. Cognição de engenharia inclui decisões, convenções, modos de falha conhecidos e o tipo de conhecimento institucional de "já tentamos isso e quebrou" que raramente vive no código.

[NOVA]: A característica operacional chave aqui é o decaimento de memória. Em sistemas de agentes, memória obsoleta é perigosa porque tem o tom de autoridade. Se você injeta uma decisão antiga em uma nova execução, o modelo pode tratá-la como política atual mesmo que o projeto tenha avançado.

[ALLOY]: Um mecanismo de decaimento é uma forma de desprover contexto antigo a menos que seja reforçado. Em equipes humanas, a memória decai naturalmente porque as pessoas param de falar sobre coisas desatualizadas. Em um store de memória de agente, tudo é igualmente recuperável a menos que você construa recência e reforço.

[NOVA]: O Mnemo também enfatiza recuperação híbrida: BM25 mais vetor mais busca em grafo. Essa combinação importa porque "o que você precisa" depende do tipo de consulta.

[ALLOY]: BM25 é ótimo para correspondência exata de termos—nomes de arquivos, mensagens de erro, nomes de bibliotecas específicas, termos internos de projeto. A recuperação vetorial é melhor para similaridade semântica—encontrar decisões relacionadas mesmo quando a redação muda. A recuperação em grafo adiciona estrutura—seguindo arestas como "decisão relacionada a subsistema," "convenção aplicável a módulo," ou "modo de falha acionado por dependência."

[NOVA]: A vantagem prática é que a memória não precisa ser uma lista plana de notas. Se sua memória é um grafo, você pode responder perguntas como: "Quais convenções se aplicam a esta pasta?" ou "Quais incidentes anteriores se relacionam com este erro?" ou "Quais decisões foram tomadas sobre fluxos de autenticação neste serviço?"

[ALLOY]: ganchos de ciclo de vida são outro conceito importante. Em um harness de agente, você pode decidir quando as memórias são escritas ou reforçadas. Por exemplo: quando um PR faz merge, você pode reforçar a memória que descreve a decisão. Quando um teste falha repetidamente, você pode criar uma entrada de memória descrevendo o modo de falha e sua correção. Quando acontece um release, você pode decair certas memórias antigas mais rapidamente porque elas se relacionam a uma versão anterior.

[NOVA]: Armazenamento local-first é a base operacional aqui. Se o repositório de memória for local, você pode manter a cognição sensível do projeto na máquina ou dentro do seu ambiente controlado, em vez de enviá-la para um serviço de memória remoto hospedado.

[ALLOY]: Aqui está a forma recomendada de começar com o Mnemo sem dar muita autoridade a ele cedo demais. Comece capturando quatro tipos de itens de memória.

[NOVA]: Um: uma decisão de projeto. Algo como "não usamos triggers de banco de dados; todas as regras de integridade ficam na camada de serviço." Dois: uma convenção. Exemplo: "Todos os novos endpoints devem incluir request IDs e campos de logging estruturado." Três: um contexto de tarefa ativa. Exemplo: "Estamos migrando da biblioteca X para a biblioteca Y; prefira Y para código novo." Quatro: um modo de falha conhecido. Exemplo: "Este teste de integração falha se o timezone não estiver definido como UTC."

[ALLOY]: Então inicie uma segunda sessão e consulte o que o Mnemo lembra. Inspecione como você inspecionaria a saída de um compilador ou linter. Você está verificando precisão, relevância e se o decaimento ou ranqueamento parecem razoáveis.

[NOVA]: O sinal de perigo é quando a recuperação de memória retorna itens obsoletos com o mesmo peso dos frescos. Se seu repositório de memória não consegue expressar frescor, você eventualmente vai tratá-lo como não confiável e parar de usá-lo.

[ALLOY]: Outro sinal de perigo é quando a memória se torna um canal de "injeção de política". Seu harness deve manter a memória como contexto consultivo, a menos que o item de memória esteja explicitamente marcado como política. Caso contrário, o modelo pode tratar qualquer nota recuperada como uma regra, mesmo quando era apenas uma gambiarra temporária.

[NOVA]: Junte o OpenLore e o Mnemo e você obtém uma história mais robusta do que "memória de agente." O OpenLore lembra a forma do codebase—estrutura, caminhos de chamadas, clusters, specs. O Mnemo lembra o conhecimento evolutivo do projeto—decisões, convenções, falhas—com sensibilidade temporal.

[ALLOY]: E ambos são mais controláveis do que stuffed transcripts. Transcripts são bagunçados, cheios de especulação, e frequentemente contêm pressupostos desatualizados. Ferramentas de memória estruturada visam recuperar contexto menor e mais relevante, e dar a você alavancas—expansão de grafo, decaimento, ranqueamento híbrido—que você pode ajustar.

[NOVA]: A seguir, vamos passar para o lado local-only e graph-repair do radar: OpenMonoAgent e Prometheus. ...

[ALLOY]: Terceiro item do radar de projetos: OpenMonoAgent. É um agente de codificação local baseado em .NET construído em torno de inferência local via llama.cpp, sandboxing com Docker, inteligência de código LSP e Roslyn, integração MCP e playbooks.

[NOVA]: A frase para focar é "padrão de agente de codificação local zero-metro." Não porque signifique que você nunca usa modelos em nuvem, mas porque te dá uma baseline onde ler código e tentar edições mecânicas é barato, privado e repetível.

[ALLOY]: Vamos começar com inferência local através do llama.cpp. Isso significa que o modelo roda na sua máquina, usando CPU e opcionalmente GPU, sem enviar prompts ou código para uma API hospedada por padrão. Os benefícios óbvios são privacidade e controle de custos.

[NOVA]: Mas o benefício operacional é a velocidade de iteração em uma dimensão diferente: você pode se dar ao luxo de rodar muitos pequenos experimentos. Se quiser pedir a um agente para propor cinco variantes de um plano de refatoração, ou analisar a estrutura de um repositório repetidamente, a inferência local pode tornar isso "tedioso e barato" em vez de "caro e medido."

[ALLOY]: Sandbox Docker é a próxima peça. Uma vez que um agente pode rodar comandos, você precisa decidir em qual ambiente ele roda. Um sandbox Docker pode limitar acesso ao sistema de arquivos, acesso à rede, e o raio de explosão de erros. Mesmo quando você confia no agente, você não necessariamente confia em todo script de instalação de dependência ou passo de build que ele possa invocar.

[NOVA]: A inteligência de código LSP e Roslyn é onde isso se torna mais do que "um chatbot com terminal." O LSP oferece operações com consciência de linguagem: ir para definição, encontrar referências, busca de símbolos, diagnósticos. O Roslyn é a plataforma de compilador .NET que pode fornecer compreensão semântica profunda para C# e linguagens relacionadas.

[ALLOY]: Quando você combina LSP/Roslyn com um loop de agente, você obtém edições mais direcionadas. Em vez de fazer grep cegamente, o agente pode perguntar: "Onde este símbolo é referenciado?" e então atualizar os sites de chamada sistematicamente. Esse é exatamente o tipo de mudança que agentes locais podem fazer bem, mesmo se seu raciocínio for mais fraco que modelos de fronteira.

[NOVA]: A integração com MCP é importante porque significa que o OpenMonoAgent pode participar de um ecossistema de ferramentas mais amplo. Você pode conectá-lo às mesmas ferramentas de orientação, ferramentas de memória, ou serviços internos que você expõe via MCP, sem integrar tudo no agente de forma hardcoded.

[ALLOY]: E os playbooks são o mecanismo de "captura de fluxo de trabalho". Um playbook pode codificar os passos para tarefas comuns: rodar testes, localizar arquivos com falha, aplicar um padrão padrão de refatoração, regenerar código, atualizar docs, e assim por diante. No contexto de um agente local, os playbooks ajudam a reduzir a quantidade de raciocínio necessário para operações rotineiras.

[NOVA]: Agora, trade-offs. Modelos locais frequentemente têm desempenho inferior em raciocínio profundo, planejamento de longo prazo e síntese complexa entre arquivos comparado a modelos de fronteira hospedados. Isso não significa que eles são inúteis. Significa que você deve mirá-los em tarefas onde restrições locais dominam e a carga de raciocínio é moderada.

[ALLOY]: Bons alvos para agentes locais incluem: orientação em repositórios, refatorações mecânicas, correções de formatação e lint, atualização de namespaces ou imports, geração de boilerplate, escrita de testes a partir de uma spec clara, e produção de resumos estruturados do que mudou entre commits.

[NOVA]: Alvos arriscados para modelos locais incluem: reviews de segurança sutis, redesigns arquiteturais em grande escala, bugs complicados de concorrência, ou qualquer coisa onde o agente precise inferir a intenção do produto a partir de sinais ambíguos. Esses são os trabalhos onde você frequentemente quer um modelo hospedado mais forte—ou um workflow que use ferramentas locais para evidências e modelos hospedados para raciocínio.

[ALLOY]: Isso sugere um workflow híbrido prático. Use um agente local para coletar evidências: mapear arquivos, extrair caminhos de chamadas, rodar testes, identificar casos de falha e propor localizações candidatas para edições. Então, se necessário, passe essas evidências para um modelo mais forte decidir a estratégia real de patch.

[NOVA]: Ou inverta: use um modelo forte para propor um plano, mas tenha o agente local executando os passos mecânicos—aplicar o diff, atualizar referências, rodar testes—dentro de um sandbox onde os dados não saem da máquina.

[ALLOY]: Um teste recomendado especificamente para OpenMonoAgent: rode contra um repo descartável sem nenhum provedor de cloud configurado. Peça para ele realizar uma tarefa rotineira mas não trivial, como "renomear um método público e atualizar todos os call sites", depois "rodar os testes unitários" e "resumir o que mudou".

[NOVA]: Meça algumas coisas. Ele usou corretamente a inteligência de código para encontrar referências? Ele evitou editar arquivos gerados? Ele manteve o diff mínimo? Ele rodou os comandos de teste certos? Ele parou e reportou quando algo falhou?

[ALLOY]: Essas medições te dizem onde ele se encaixa no seu stack. Se ele é forte em edições mecânicas e loops de verificação, ele pode se tornar seu padrão para trabalho de baixo risco, economizando chamadas de cloud para as partes realmente difíceis.

[NOVA]: Agora, quarto item do radar de projetos: Prometheus da EuniAI. Ele é apresentado como um agente de software orientado a grafos de conhecimento para mapear, entender e reparar codebases complexas.

[ALLOY]: A frase-chave é "reparo orientado a grafos ao invés de edições via chat". Muitos agentes de código hoje operam assim: leem alguns arquivos, formam uma hipótese, escrevem um patch, rodam testes, repetem. O ponto fraco é que a hipótese pode estar sub-constraintada. O agente pode pular para um patch porque parece plausível, não porque tem evidências de como o código realmente se conecta.

[NOVA]: Contexto de grafo pode constraint isso. Se o agente constrói um grafo de entidades—módulos, classes, funções, dependências, arestas de chamada—ele pode usar esse grafo para decidir onde um fix deve morar e o que ele pode quebrar.

[ALLOY]: Pense em um relatório de bug: "Login às vezes falha com um erro de referência nula." Um agente orientado a chat pode procurar por "null" e "login" e fazer patch na primeira coisa que ver. Um agente orientado a grafos pode mapear o fluxo de login: handler de UI → serviço de auth → parser de token → loader de usuário → adapter de banco de dados. Então ele pode procurar a aresta específica onde null pode ser introduzido e seguir esse caminho.

[NOVA]: A parte do loop de verificação é crítica. "Reparo" não é só geração de patch; é também selecionar a evidência certa para validar o patch. Um grafo pode ajudar a escolher testes. Se o grafo mostra que uma função é exercida por apenas dois testes de integração, esses testes devem estar no plano de verificação.

[ALLOY]: Ele também pode ajudar com recuperação de falhas. Se um patch falha nos testes, o agente pode usar o grafo para identificar o provável raio de explosão. Ele mudou uma interface compartilhada usada por muitos nós? Ele alterou um formato de serialização? Ele tocou um utilitário de baixo nível quefan out para muitos call sites?

[NOVA]: Na prática, você avalia um projeto de reparo orientado a grafos perguntando: o grafo materialmente muda as decisões do agente? Ou é apenas um índice fancy que o agente ignora?

[ALLOY]: Uma abordagem de avaliação útil é rodar Prometheus em uma tarefa estilo benchmark ou um repo descartável onde você pode inspecionar o comportamento. Então compare dois artefatos: a evidência do grafo e o patch final. Você está procurando por链接 direto.

[NOVA]: Por exemplo, se o patch muda uma função, o grafo mostra por que essa função é o ponto de estrangulamento certo? Se ele atualiza call sites, o grafo os enumera de forma abrangente? Se ele escolhe testes, o grafo justifica a seleção baseada na cobertura dos nós afetados?

[ALLOY]: Outro teste é introduzir um sinal intencionalmente enganoso. Coloque um nome de arquivo que pareça relevante mas não é, ou deixe um comentário desatualizado. Agentes orientados a chat frequentemente são seduzidos por esses. Sistemas orientados a grafos devem ser mais resilientes porque dependem de relações reais de código ao invés de texto superficial.

[NOVA]: Prometheus, OpenLore e Mnemo também se conectam conceitualmente. OpenLore fornece grafos arquiteturais para orientação. Mnemo fornece um grafo de conhecimento para cognição de projeto com decaimento. Prometheus usa grafos para impulsionar reparo e verificação. A ideia no nível de stack é que grafos podem servir como uma camada de aterramento para agentes—estrutura que é mais difícil de alucinar do que narrativa livre.

[ALLOY]: E isso é importante porque o próximo passo para agentes de codificação não é apenas modelos maiores. É fazer o loop provar o que entendeu: mostrar as bordas relevantes, mostrar as evidências, rodar os testes certos e revelar por que a mudança é segura.

[NOVA]: Em seguida, vamos encerrar com uma fila prática de "o que experimentar a seguir" que combina com o tema de hoje de superfície de controle. ...

[ALLOY]: Aqui está a fila prática do EP060, na ordem que reduz o risco.

[NOVA]: Primeiro: Claude Code latest auto mode em nuvens gerenciadas. Trate como um feature flag porque é exatamente isso. Habilite apenas com CLAUDE_CODE_ENABLE_AUTO_MODE=1, e comece na faixa do provedor que você realmente planeja usar—Bedrock, Vertex ou Foundry—para que seus testes reflitam seu ambiente real de identidade e logging.

[ALLOY]: Execute três tipos de tarefas: orientação apenas de leitura, execução segura como testes e lint, e uma pequena tarefa de escrita com guardrails estritos. Meça o comportamento de chamadas de ferramentas, o número de vezes que ele continua sem perguntar, e se escala apropriadamente quando incerto.

[NOVA]: Segundo: Codex Windows computer use. Comece com um app de baixo risco e teste explicitamente confiabilidade, intent limitado e recuperação. Confiabilidade é "consegue operar a UI sem travar." Intent limitado é "mantém o foco na tarefa que você deu." Recuperação é "reconhece bloqueios e pede orientação em vez de se debater."

[ALLOY]: Se você planeja supervisionar do celular ou Mac, teste explicitamente o limite de controle remoto. Inicie uma execução no host Windows, saia, conecte de um dispositivo diferente e confirme que você consegue controlar de forma significativa: responder perguntas, aprovar etapas e verificar o progresso. O objetivo é validar que a execução fica local enquanto a supervisão permanece prática.

[NOVA]: Também trate os Codex Profiles como evidência operacional. Confirme que a identidade é o que você espera, e observe o uso e atividade de tokens em uma execução onde você sabe aproximadamente o que deveria acontecer. Se o uso de tokens disparar, use isso como prompt de debug: leituras repetidas de arquivos, verbosidade de logs, loops de ferramentas ou direcionamento ruim de testes.

[ALLOY]: Terceiro: se você constrói ou mantém um agent harness, estude a mudança na Messages API: entradas do sistema dentro do array de mensagens. Use para separar intent do usuário de política de runtime e fatos de runtime. Implemente pelo menos uma atualização de sistema no meio da execução—mudança de permissão ou de orçamento—e verifique se o modelo responde mudando seu comportamento, não apenas reconhecendo o texto.

[NOVA]: Mantenha as atualizações de sistema estruturadas e evite linhas do tempo de instruções contraditórias. Prefira mensagens de "resumo do estado mais recente" para fatos de runtime em vez de uma longa cadeia de atualizações parciais que o modelo tem que reconciliar.

[ALLOY]: Quarto: escolha exatamente um experimento de memória para poder avaliar de forma honesta.

[NOVA]: Use OpenLore se sua dor é redescoberta arquitetural—agentes continuam pegando os pontos de entrada errados, perdendo caminhos de chamada importantes, ou queimando contexto lendo os mesmos diretórios. Compare um plano de edição com e sem a saída de orientação do OpenLore antes de permitir escritas.

[ALLOY]: Use Mnemo se sua dor é conhecimento perdido do projeto—decisões, convenções e modos de falha conhecidos que deveriam persistir entre sessões. Comece com um conjunto pequeno de memórias e audite a qualidade de recall em uma segunda sessão. Preste atenção especial ao comportamento de decaimento e ranqueamento, porque frescor é o que impede a memória de se tornar autoridade obsoleta.

[NOVA]: Use OpenMonoAgent se sua dor é privacidade, custo ou repetibilidade local. Faça dele sua baseline para leitura de repositório e edições mecânicas dentro de um sandbox, depois compare seus resultados com um agente hospedado nas mesmas tarefas. Você não está pedindo que ele seja o melhor em tudo; está pedindo para tornar a parte privada e barata do workflow tediosa.

[ALLOY]: Use Prometheus se sua pergunta de pesquisa é qualidade de reparo e verificação. Avalie se a evidência do grafo realmente restringe o patch e melhora a seleção de testes e recuperação de falhas. Se o grafo não muda decisões, ele não está justificando sua complexidade.

[NOVA]: Para cada experimento, defina o workflow do builder antes da ferramenta tocar trabalho importante: o caso de uso, o alvo do build, o limite do operador, a decisão de deploy ou ship, e o padrão de verificação que prova o resultado. O workflow de build útil coloca evidência no início, uma decisão de operador limitada no meio, e uma regra clara de ship, deploy ou stop no final; esse padrão de builder é o que impede experimentos de se transformarem em demos vagas.

[NOVA]: A lição duradoura de hoje é que stacks de agentes melhoram quando ficam mais explícitos: gating explícito para automação, limites de host explícitos para supervisão remota, atualizações de instrução de runtime explícitas para execuções longas, e recuperação de memória explícita que é estruturada, consultável e consciente de frescor.

[ALLOY]: Esse foi o AgentStack Daily do EP060. Toby On Fitness Tech dot com. Voltamos em breve.