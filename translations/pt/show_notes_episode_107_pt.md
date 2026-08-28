Episódio 107 — 27 de agosto de 2026

[00:00] Gancho do episódio

Hermes Agent v2026.8.27 foi lançado em 27 de agosto, consolidando aproximadamente 525 pull requests mesclados em um único release que se aplica a imagens Docker, deploys hospedados e novas instalações, e substitui a baseline v2026.8.19 de 19 de agosto. As adições visíveis ao usuário incluem um painel de tarefas do agente reprojetado, diffs de planos estruturados, streaming expandido de chamadas de ferramentas, um agendador em segundo plano que mantém jobs de longa execução vivos através de reconexões, e um novo modo de sandbox do sistema de arquivos que controla gravações atrás de listas de permissão por projeto. Nos bastidores, o release carrega correções de segurança para o runtime, padrões atualizados para o roteador de modelos, depreciação das flags legadas da CLI, e alterações interruptivas no manifesto de plugins que integradores downstream precisarão corrigir antes de atualizar. As imagens Docker travam na mesma versão, inquilinos hospedados estãorollout em ondas até o final da semana, e operadores auto-hospedados devem rerodar o script de instalação para adotar o novo schema do manifesto de plugins.

[02:00] Leiaute do Release do Agent Stack: Hermes Agent v2026.8.27, v2026.8.19

Hermes Agent lançou v2026.8.27 em 27 de agosto, acumulando aproximadamente 525 pull requests mesclados em uma única tag estável para imagens Docker, deploys hospedados e novas instalações. A mudança mais visível é que o Browser do desktop agora abre em sua própria janela do SO, paired with a managed SSH remote-update engine e um rail de perfil de frota. Sessões de navegação não vivem mais dentro do painel de chat — elas ganham sua própria janela que você pode ancorar ou fechar independentemente — e atualizações remotas pausam o gateway sobre o socket de controle em vez de matar no meio da tarefa.

Navegação local ganhou um caminho com consentimento que usa seu perfil Chromium padrão com um fluxo de fechamento com aprovação no Windows, então sites que requerem sua sessão de navegador logada funcionam sem reautenticação. O catálogo remoto MCP cresceu para mais de 50 servidores de vendors verificados ao vivo, incluindo Cloudflare, Grafana Cloud, Better Stack e Railway. MCP é o Model Context Protocol, o padrão que agentes de IA usam para conversar com ferramentas e dados externos, então uma única instalação do Hermes pode agora alcançar esses serviços sem uma ponte local.

Busca e extração na web ganhou cache de resultados TTL, e tool_search agora executa buscas multi-query com stemização para que variantes de palavras como "runs" e "running" sejam mapeadas para a mesma ferramenta. Para usuários Mac, criptografia opcional no OS-keychain para segredos armazenados remove os prompts do macOS Keychain por inicialização. Compressão lean-tail foi ligada por padrão, reduzindo verbosidade de resposta sem perder conteúdo útil.

Outras mudanças enviadas: instalações de imagem e pacote agora recusam atualizações inseguras in-place, controles de link-unfurl do Slack foram enviados, containers Docker compartilham identidades, backends de ambiente de terminal plugáveis chegaram, e os seletores de modelo adicionaram GLM-5.3-Flash, MiniMax M3 free e MiniMax H3 Max video. A tag anterior, v2026.8.19 em 21 de agosto, introduziu a camada web sem chave — rotação gratuita de cinco vendors com failover em anel para que novas instalações possam buscar na web sem chaves de API configuradas — mais uma onda de polimento da CLI com um seletor de modelo fuzzy e paleta de comandos Ctrl+P. Notas curadas cobrindo v0.20.0 em diante pousarão com v0.21.0.

[03:19] App desktop Codex adiciona WebMCP, Messages, Linux e revisão multi-repo

O app desktop Codex da OpenAI teve um mês cheio de atualizações entre final de julho e final de agosto, com mudanças que tocam o navegador integrado, macOS, Linux e como projetos multi-repo são revisados.

Em 30 de julho, a versão desktop 26.727 adicionou histórico da barra de endereço e busca Google dentro do navegador integrado, acesso opcional ao histórico de navegação para o ChatGPT, menções de abas do Chrome e texto selecionado, perguntas do YouTube e clique direito Ask ChatGPT. Projetos multi-pasta ganharam uma visualização de revisão combinada para diffs entre repositórios, e imagens geradas ganharam visualizações Focused e Canvas para comentário e refinamento. O mesmo build adicionou uma visualização Activity e melhorou a confiabilidade de instalação no Windows para caminhos de pacote longos.

Em 11 de agosto, a OpenAI enviou uma prévia desktop do Linux suportando Ubuntu, Debian e Fedora em x64 e ARM64 via pacotes .deb e .rpm. O app desktop também pode importar instruções, configurações, skills, plugins, projetos e trabalho recente do Claude Code, Claude Cowork e Cursor, com uma atualização automática opcional para trabalho importado.

Em 20 de agosto, o app macOS adicionou um plugin Apple Messages disponível em todos os planos, usável do ChatGPT Work ou Codex, com aprovação requerida antes de enviar. A mesma atualização introduziu snapshots compartilhados somente leitura de threads Codex locais em cada plano Codex, co-edição de Site e mudanças de URL no mesmo workspace, threads fixadas unificadas entre desktop e iOS, e disponibilidade mais ampla de Computer History na Europa. A OpenAI adverte que o redator de padrões secretos em snapshots compartilhados pode não remover todos os detalhes sensíveis.

Em 25 de agosto, a extensão do navegador expandiu de Chrome para Edge, Brave, Opera e Vivaldi, com menções de abas e controle do navegador nos cinco, embora Opera não tenha chat lateral. O navegador desktop integrado também ganhou Site Tools fornecidos pelo site através de WebMCP para ChatGPT Work e Codex. Esse recurso requer o app desktop mais recente mais uma assinatura GPT-5.6 Sol ou Terra e não está disponível em Luna, Enterprise ou Edu.

[05:11] Grok Bot dá aos agentes um computador em nuvem persistente e trabalho 24/7

Grok Bot é o produto de agente separado da xAI, não um modo dentro do chat Grok. Foi lançado em beta inicial em 11 de agosto e o acesso foi expandido novamente em 26 de agosto. Usuários criam múltiplos Bots, enviam mensagens para eles como colegas, drop them into shared threads e deixam um Bot passar trabalho para outro.

A escolha arquitetural central é que todo Bot que um usuário cria compartilha um computador em nuvem persistente, incluindo arquivos, estado do navegador e logins. O isolamento é por usuário em vez de por Bot. Isso permite que um Bot de vendas pesquise contas em um navegador logado, passe o resultado para um Bot de operações que processa faturas do Gmail, e continue enquanto o laptop está fechado. Bots podem fazer login em sites que não têm APIs ou servidores MCP, e a xAI diz que podem assistir um usuário completar um fluxo de trabalho uma vez, salvá-lo como rotina, aceitar correções e dar seguimento em threads abandonadas.

Clientes de download cobrem macOS em Apple silicon e Intel, Windows 10 e 11 em x64, e iPhone e iPad. A página do produto não lista um cliente Android do Grok Bot.

O acesso está incluído com assinaturas SuperGrok, SuperGrok Plus e SuperGrok Heavy, com o menor tier individual a $30 por mês. O mesmo produto também está bundled com planos Cursor Pro, Pro+ e Ultra a partir de $20 por mês, e Cursor Teams Standard e Premium. O uso do Grok Bot é cobrado separadamente do uso padrão do Grok ou Cursor. Acesso Enterprise permanece na waitlist.

Recursos de segurança e controle listados pela xAI incluem criptografia em trânsito e em repouso, opt-out de treinamento, Auto Review para ações sensíveis e controles enterprise para DLP, certificados, proxies e controles de rede.

[06:52] Alibaba Preview Qwen4 Através do Qwen3.8-Flash-Next

A equipe Qwen da Alibaba lançou o Qwen3.8-Flash-Next, um modelo multimodal Mixture-of-Experts com 125 bilhões de parâmetros que antecipa a arquitetura Qwen4 que está por vir. O número total é 180 bilhões de parâmetros, divididos em três partes: um backbone de 125B, uma tabela de embedding N-gram de 51B e um módulo de predição de múltiplos tokens de 4B. Apenas 6 bilhões de parâmetros são ativados por token, e é aí que reside a história da eficiência.

Quatro mudanças arquitetônicas definem a prévia. Uma camada híbrida combina Gated DeltaNet com Qwen Sparse Attention para modelagem de sequência. Conexões Residuais Gated remodelam como os gradientes fluem pela rede. A tabela de embedding N-gram dá ao modelo memória explícita de padrões de curto alcance, e o otimizador Muon substitui o passo de treinamento padrão. Juntas, essas mudanças reduzem a computação ativa sem encolher o alcance geral do modelo.

A equipe relata custo de treinamento aproximadamente um nono do Qwen3.7-Plus, uma queda acentuada que o novo otimizador e a atenção híbrida ajudam a explicar. Para auto-hospedagem, o checkpoint FP8 fica em 172,78 GiB, o que impõe restrições reais ao hardware de consumo e empurra implantações sérias para GPUs de data centers.

O que isso significa para desenvolvedores: a prévia dá às equipes multimodais uma leitura antecipada sobre a direção do Qwen4, especialmente a abordagem de atenção híbrida e a tabela de embedding N-gram. O footprint FP8 de 172,78 GiB define um piso claro de planejamento para armazenamento e memória. Até que o Qwen4 completo seja lançado, trate o desempenho dos benchmarks como direcional ao invés de definitivo.

[08:13] Orquestração supera automação como gargalo do CX, diz Tata Communications

A Tata Communications está defendendo que o trabalho de experiência do cliente superou sua infraestrutura. Gaurav Anand, que lidera globalmente a Customer Interaction Suite na Tata Communications, diz que as empresas passaram os últimos anos acrescentando IA conversacional a sistemas legados que nunca foram construídos para cargas de trabalho agentic, e as costuras estão começando a aparecer.

O resultado, argumenta Anand em uma coluna da VentureBeat publicada em 27 de agosto de 2026, é que agentes humanos agora carregam a maior parte do peso da integração. Eles têm que costurar contexto de ferramentas desconectadas apenas para descobrir o que um sistema de IA já disse a um cliente. O gargalo não é mais o acesso a dados, ele diz, mas a ausência de um contexto empresarial compartilhado que una identidades de clientes, interações, transações, políticas, jornadas e sistemas operacionais em um entendimento comum.

A arquitetura CX tradicional foi projetada para roteamento linear e dirigido por humanos, não para orquestrar fluxos de dados em tempo real entre agentes de IA autônomos, data lakes e trabalhadores humanos. Anand enquadrar a mudança como uma transição de automação para orquestração como a principal prioridade do CX. A questão estratégica, ele sugere, é como coordenar a inteligência já existente dentro da empresa para que o cliente nunca sinta os silos internos.

Esse enquadramento coloca ferramentas de orquestração, resolução de identidades e camadas de contexto no centro do próximo ciclo de construção do CX, à frente de mais um upgrade de modelo conversacional.

[09:37] O verdadeiro risco de IA empresarial escondido entre os agentes

O artigo faz uma afirmação clara: a parte perigosa da IA empresarial não é qualquer agente individual saindo do controle, é a teia invisível de chamadas entre agentes que ninguém mapeia ou possui.

Implantações reais não enviam um agente e observam ele funcionar. Elas enviam frotas onde cada agente chama APIs, chama outros agentes e acessa aplicações construídas muito antes de qualquer tomador de decisão de máquina existir. Um chamado de suporte que costumava tocar um sistema pode agora passar por quatro agentes antes que um humano jamais o veja, e cada transferência é uma aprovação que ninguém escreveu.

A matemática é o que torna isso doloroso. Adicionar um décimo agente não adiciona dez conexões, pode adicionar dezenas, porque qualquer agente pode chamar qualquer outro agente, e cada chamada pode desencadear outra chamada em algum lugar. A complexidade se compõe com o número de caminhos entre agentes, não com o número de agentes em si, e ninguém tem o trabalho de desenhar esse grafo.

A governança não acompanhou. Pergunte a uma equipe de segurança quais agentes podem acessar quais sistemas e você recebe silêncio. Pergunte qual agente disparou qual ação downstream três saltos atrás e você recebe mais silêncio. O instinto é tratar isso como uma lista de verificação: aprove o agente, registre o agente, siga em frente. Mas uma lista de verificação verifica um momento no tempo, enquanto a complexidade corre através de uma cadeia. Uma pilha de aprovações únicas não pode governar um fluxo de trabalho mais do que um único vegetal faz uma dieta.

O takeaway prático para desenvolvedores: antes de escalar frotas de agentes, desenhe o grafo de qual agente pode acessar qual sistema. Se ninguém na equipe consegue esboçar essa imagem em menos de cinco minutos, a implantação já está muito opaca para ser governada.

[11:20] Liquid AI's Pipette Benchmarks Models on the Devices They Actually Run On

Todo card de modelo na internet lista números de qualidade medidos em hardware de classe servidor com precisão total. Esses números raramente preveem como o mesmo modelo se comporta quando é reduzido e executado em um celular ou laptop. Esta semana a Liquid AI lançou o Pipette, uma suite de benchmark de código aberto e reproduzível construída para fechar essa lacuna.

O Pipette mede quatro variáveis ao mesmo tempo: o modelo, sua quantização, o runtime e o hardware do dispositivo. Tratando esses como um único experimento ao invés de perguntas separadas, ele produz números que se parecem mais com o que um desenvolvedor realmente vê quando ele carrega um modelo em hardware real. A Liquid AI fez parceria com a Artificial Analysis para servir como validador independente de metodologia, o que significa manter a suite honesta sobre o que ela está e não está medindo.

Para desenvolvedores que entregam funcionalidades on-device, a mudança prática é que escolhas de modelo-e-quantização agora podem ser respaldadas por latência medida e qualidade em um celular específico, não extrapoladas de um artigo. A suite é de código aberto, então equipes podem adicionar seus próprios perfis de dispositivos e executar a matriz novamente no hardware que realmente entregam.

A ressalva honesta é que o Pipette mede o que mede; ele não remove os tetos de hardware subjacentes que limitam a IA no dispositivo. Mas agora existe uma forma pública e reprodutível de comparar candidatos no mesmo campo de jogo, e é isso que a maioria dos projetos no dispositivo estava perdendo.

[12:47] Chip Jalapeño da OpenAI publica primeiros resultados de inferência

A OpenAI publicou os primeiros números de desempenho do Jalapeño, seu chip personalizado projetado para executar modelos de IA em produção. A inferência, o trabalho de realmente gerar uma resposta quando o usuário aperta enviar, é a parte mais cara de executar um produto moderno de IA, e chips construídos especificamente para isso podem ser mais rápidos e mais baratos do que processadores gráficos de uso geral. Essa é a aposta por trás do Jalapeño.

Nos resultados publicados em 25 de agosto, a OpenAI afirma que o chip oferece velocidade e eficiência energética líderes do setor, com maior throughput (mais respostas por segundo) e menor latência (menos espera por resposta) do que opções comparáveis. A empresa apresentou o anúncio como a primeira validação concreta de um esforço de vários anos para projetar seu próprio silício em vez de depender inteiramente de aceleradores de terceiros.

Os números importam porque a inferência, não o treinamento, é a conta recorrente. Um chip propósito-built que trata a mesma carga com menos energia, ou extrai mais respostas de cada servidor, reduz diretamente o custo de executar um chatbot, um assistente de codificação ou um trabalho de sumarização em lote em escala. Para a OpenAI, isso se traduz em margem, e para qualquer pessoa construindo em suas APIs, eventualmente pode se traduzir em movimentos de preço ou novos níveis de latência.

Duas coisas para acompanhar a seguir: benchmarks independentes que confirmem ou contradigam os números fornecidos pelo fornecedor, e qualquer sinal sobre se o Jalapeño é limitado a cargas de trabalho internas da OpenAI ou eventualmente servirá tráfego externo através do ChatGPT ou da API.

[14:14] Pequeno Modelo de Glicose do Google Supera Rivais Centenas de Vezes Seu Tamanho

O Google Research e a Universidade de Nova Gales do Sul Sydney lançaram esta semana o GlucoFM, um modelo fundacional voltado para dados de monitor contínuo de glicose. Os monitores contínuos de glicose são os pequenos sensores que pessoas com diabetes usam para rastrear o açúcar no sangue continuamente, gerando uma nova leitura a cada poucos minutos.

O GlucoFM tem apenas 720.000 parâmetros, uma fração do tamanho da maioria dos sistemas modernos de IA, mas em 14 avaliações de coorte e tarefa, ele obteve uma média de 58,8 em AUC de precisão-recall, superando o GluFormer, um modelo de 135 milhões de parâmetros construído para o mesmo trabalho, e o MOMENT, um modelo fundacional de séries temporais geral de 385 milhões de parâmetros. Para contexto, o GluFormer é aproximadamente 190 vezes maior e o MOMENT é aproximadamente 535 vezes maior que o GlucoFM.

O truque está em como o GlucoFM lê o sinal. Em vez de tratar um trace de glicose como uma longa sequência indiferenciada, ele divide os dados em dois fluxos: um fluxo fisiológico lento que captura a deriva da linha de base e tendências mais longas, e um fluxo de eventos transitórios que captura picos de curta duração de refeições, exercícios ou medicação. Cada fluxo recebe seu próprio caminho de codificação antes do modelo fundi-los novamente. O modelo é pré-treinado de forma auto-supervisionada, o que significa que aprende a forma dos traces de glicose a partir de dados não rotulados antes de qualquer ajuste fino para uma previsão específica.

Isso é importante porque os dados de MCG são barulhentos, específicos de cada pessoa e cheios de dinâmicas sobrepostas. Um modelo geral de séries temporais precisa aprender essa separação do zero com um orçamento de parâmetros muito maior. O GlucoFM integra a separação na arquitetura, o que é como um modelo do tamanho de um pequeno classificador de imagens pode vencer em um benchmark de estilo clínico.

As ressalvas são reais. O GlucoFM é um protótipo de pesquisa sem aprovação regulatória da FDA ou equivalente, então nada chega a uma clínica amanhã. O Google não anunciou uma API pública, pesos abertos ou uma parceria com fabricantes de dispositivos. O que o GlucoFM sinaliza é que o padrão de que "maior é melhor" na IA médica tem um desafiante crível quando a arquitetura é projetada em torno da biologia em vez de ser emprestada da linguagem.

[16:16] Resumo de pesquisa: Um Loop Mais Inteligente Para Ensinar Modelos de Visão a Seguir Instruções

Treinar um modelo de visão para seguir instruções complexas geralmente significa reunir grandes conjuntos de dados e esperar que eles sejam precisos, variados e difíceis o suficiente. O novo framework VISA trata essa etapa de criação de dados como um loop que o sistema melhora por conta própria. A cada rodada, ele inspeciona uma imagem, remove restrições que não podem ser verificadas e propõe novas tiradas de um banco de memória. Instruções candidatas são verificadas com ferramentas executáveis e juízes de modelo de linguagem estruturados, e quaisquer falhas são diagnosticadas e alimentadas de volta para que a próxima rodada ataque exatamente as fraquezas que o modelo alvo ainda mostra.

Essa retroalimentação faz trabalho duplo: ela afia dados futuros e também serve como sinal de recompensa para aprendizado por reforço, então nenhum modelo de recompensa separado precisa ser treinado. No benchmark MM-IFEval, modelos treinados com VISA superaram linhas de base fortes em seguimento de instruções enquanto mantinham desempenho estável em sete testes multimodais gerais. A consequência prática são dados de ajuste mais baratos e de maior qualidade para qualquer pessoa construindo assistentes de visão que precisam lidar com várias regras de uma vez, como ler um gráfico e responder em um formato específico com um limite de palavras.

[17:22] Grok 4.6 da xAI Chega ao Microsoft Foundry

O Grok 4.6, flagships da xAI, agora está disponível no Microsoft Foundry, o catálogo de modelos do Azure para implantações de IA empresarial. A integração, anunciada em 26 de agosto, coloca o Grok 4.6 ao lado de outros modelos de fronteira para comparação direta e implantação através da infraestrutura empresarial do Azure.

O Grok 4.6 é fornecido com uma janela de contexto de 500.000 tokens e quatro níveis configuráveis de esforço de raciocínio: baixo, médio, alto e xhigh. A xAI descreve o modelo como construído para agentes de longa execução e trabalho visual e interativo ambicioso, linguagem que sinaliza que a empresa está cortejando cargas de trabalho sérias de agentes em vez de chat de turno único.

Para construtores, o Foundry oferece um único lugar para avaliar o Grok 4.6 contra modelos de fronteira concorrentes, executar testes específicos de carga de trabalho e implantar endpoints gerenciados sob controles de segurança e governança empresarial. A xAI especificamente destaca coding agents, copilotos de engenharia, assistentes de pesquisa e automação empresarial como os tipos de sistemas que o modelo visa, com desenvolvedores capazes de começar no catálogo de modelos do Foundry agora mesmo.

[18:17] Resumo de pesquisa: Uma forma mais barata de deixar modelos de IA pensarem mais

Uma nova técnica chamada Prefix Sliding pode tornar modelos de IA muito mais baratos de executar quando passam muito tempo "pensando" em problemas difíceis. Hoje, quando um modelo raciocina extensivamente, ele mantém cada pensamento intermediário na memória de trabalho, então quanto mais tempo ele pensa, mais cara cada pergunta se torna. Os pesquisadores descobriram que a maioria desses passos intermediários deixa de importar assim que o modelo seguiu em frente, então mantê-los está pagando por contexto que raramente ajuda.

A solução deles é simples em essência: manter apenas as instruções originais na frente e uma janela deslizante dos poucos milhares de textos mais recentes, descartando o resto em tempo real. Isso limita o uso de memória não importando o quanto a cadeia de raciocínio fique longa. Sem qualquer retreinamento, aplicar o Prefix Sliding a modelos existentes os tornou cerca de 3x mais rápidos enquanto preservavam a precisão, e o treinamento com a mesma política elevou o limite para além de 100.000 passos de raciocínio.

Para desenvolvedores que entregam agentes que precisam de longos loops de planejamento, esse tipo de limite de memória importa porque o custo de inferência é o que impede agentes de raciocínio ambiciosos de serem econômicos em escala.

[19:26] Open WebUI Adiciona Aprovação de Ferramentas com Interveniência Humana

O Open WebUI, o frontend de chat autohospedável no qual muitas stacks de IA local são construídas, lançou a v0.11.1 em 25 de agosto. A única mudança documentada é um fluxo de aprovação de ferramentas com interveniência humana.

É assim que funciona. Um administrador habilita o recurso nas configurações. A partir de então, qualquer conversa pode ser alternada do padrão — onde as chamadas de ferramentas são executadas conforme o modelo as solicita — para um modo onde cada chamada faz pausa e pergunta ao usuário primeiro. A aprovação ou negação acontece por botão ou atalho de teclado, uma chamada de cada vez, e a escolha é lembrada pelo resto daquela conversa e para conversas futuras.

As notas de lançamento são cortadas no meio da funcionalidade, então esta história fica restrita à única mudança documentada: o portão de aprovação por chamada, sua habilitação a nível de administrador, e sua alternância por conversa.

Para quem faz autohosting, esta é uma alavanca real de segurança para qualquer fluxo de trabalho de agente. O movimento prático é deixar o interruptor de administrador desligado para chats puramente conversacionais e ligar a aprovação por conversa em qualquer lugar onde o modelo tenha ferramentas anexadas, para que cada chamada faça pausa para uma permissão ou negação explícita em vez de executar sem verificação. Fique de olho se lançamentos futuros estendem a escolha lembrada além de uma única conversa para padrões de todo o espaço de trabalho, já que por enquanto a persistência é local ao chat onde a alternância foi ativada.

[20:46] Google Divide Sua Linha de TPU de Oitava Geração na Hot Chips

Na Hot Chips 2026, a conferência anual onde equipes de chips mostram seu silício mais recente para um público técnico, o Google discutiu sua família de unidades de processamento tensor de oitava geração. De acordo com um relatório da ServeTheHome publicado em 26 de agosto, a nova família é dividida por carga de trabalho em dois chips: o TPU 8t orientado para treinamento e o TPU 8i orientado para inferência.

Essa divisão é a história estrutural do anúncio. Um chip é construído para ensinar modelos e o outro para servir previsões, e o Google os apresenta lado a lado como um par combinado. A empresa também se destaca como uma das poucas hyperscalers que desenvolve seu próprio hardware de treinamento em vez de sourcing de silício de treinamento de fornecedores externos — uma posição incomum na indústria, onde a maioria dos grandes operadores de IA compra sua computação de treinamento de fabricantes de chips terceiros.

Para desenvolvedores, a questão prática é o acesso. Os TPUs do Google tipicamente chegam a desenvolvedores externos através do Google Cloud e um pequeno círculo de parceiros, e os mergulhos técnicos profundos publicados em torno da Hot Chips geralmente antecipam o que se torna geralmente disponível alguns meses depois. Os sinais concretos para ficar de olho são posts no blog do Google Cloud e números de benchmark relacionados aos novos chips, que revelarão se a oitava geração muda o custo, a taxa de transferência ou a escalabilidade de treinar ou executar modelos na stack do Google.