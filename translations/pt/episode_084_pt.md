[NOVA]: Eu sou a NOVA.

[ALLOY]: Eu sou a ALLOY, e este é o AgentStack Daily...

[NOVA]: O agente de codificação baseado em terminal da OpenAI, o Codex rust .144, foi lançado em dois releases estáveis. Ele adicionou autenticação MCP interativa, manipulação compartilhada de credenciais OAuth, redirecionamentos de login hospedados, um limite de aprovação somente para escritas, WebSockets de Responses com suporte a proxy, e suporte a certificados personalizados. O follow-up ponto-um corrigiu falhas de instalação, expôs o host do Code Mode em pacotes macOS, e introduziu um fallback de runtime incorporado.

[ALLOY]: Hoje: Codex lidera com autenticação mais forte, transporte, aprovações e empacotamento; GPT-5.6 chega como Sol, Terra e Luna; Grok 4.5 entra na Responses API; GPT-Live ouve enquanto fala; e Mistral traz navegação apenas com câmera para um modelo de oito bilhões de parâmetros. Você também vai ouvir como o ChatGPT Work lida com projetos estendidos, como o Flint dá aos agentes uma linguagem de gráfico editável, e como novas pesquisas abordam memória de controle, viés de citação, benchmarks de codificação, fluxos de trabalho proativos, pesquisa recursiva, recuperação com consciência de procedimento, e segurança do mercado de energia.

[NOVA]: GPT-5.6 abrange três camadas de preço-desempenho e dá ao Sol uma janela de contexto acima de um milhão de tokens. Grok combina pontuações de codificação publicadas com serviço de oitenta tokens por segundo e preço de dois dólares para entrada. GPT-Live separa conversação imediata de raciocínio delegado, enquanto Robostral Navigate pergunta quanto de navegação física pode ser construída em torno de um stream RGB.

[ALLOY]: Em toda a pilha, cada release muda algo concreto que um agente pode fazer: autenticar em ferramentas, rotear trabalho por custo, manter uma troca de voz fluída, construir saídas utilizáveis, recuperar um padrão de implementação, ou agir sob restrições físicas sem otimizar para um comportamento inválido.

[NOVA]: ...

[NOVA]: A OpenAI lançou o Codex rust .144 e o follow-up ponto-um com mudanças em autenticação, aprovações, transporte, comportamento de runtime e instalação. Ferramentas MCP podem solicitar autenticação interativamente sem um opt-in experimental. Hosts de servidor de aplicativo podem fornecer autenticação do Codex em runtime, e então redirecionar um login concluído para uma página hospedada. Credenciais OAuth MCP compartilhadas também podem ser serializadas, dando às integrações gerenciadas uma forma definida de reter o estado de autorização entre sessões ao invés de reconstruí-lo para cada conexão.

[ALLOY]: Um novo modo de aprovação de escritas de aplicativo afia o limite de permissão. Ações declaradas como somente leitura podem prosseguir, enquanto escritas disparam um prompt. Isso funciona melhor do que tratar cada ação de aplicativo como igualmente sensível, especialmente quando um agente passa a maior parte de uma sessão pesquisando ou calculando antes de fazer uma mudança consequente. Sessões de aplicativo Codex hospedadas agora renovam autenticação expirada, enquanto avisos revisados de código de dispositivo explicam como reconhecer e parar tentativas de phishing durante o login.

[NOVA]: Correções de rede e runtime cobrem várias restrições de produção. WebSockets de Responses mantêm seu transporte de baixa latência enquanto respeitam proxies de sistema e autoridades de certificado personalizadas. Sessões sandbox do Windows podem deletar conteúdo dentro de raízes graváveis e alcançar o runtime primário gerenciado. A OpenAI corrigiu crashes do Code Mode em Intel Mac e sequências de controle de terminal que podiam corromper a interface ou o histórico de conversa retomado. Quando uma thread mais antiga do ChatGPT aponta para estado de compactação de um modelo descontinuado, o Codex tenta novamente com o modelo atualmente selecionado.

[ALLOY]: O follow-up ponto-um repara caminhos de distribuição. Instalação standalone não depende mais de uma ordem exata de metadados de release. Pacotes macOS expõem o host do Code Mode ao lado do Codex, e o Code Mode retorna ao seu runtime incorporado se aquele binário companheiro estiver indisponível. Na prática, .144 torna sessões MCP autenticadas, login hospedado, aprovações de escrita, roteamento de proxy corporativo e empacotamento do Code Mode mais confiáveis. Um limite importante permanece visível: o status somente leitura declarado de uma integração controla diretamente se um humano vê um prompt de aprovação.

[NOVA]: ...

[NOVA]: A OpenAI lançou o GPT-5.6 como três camadas de API ao invés de um modelo uniforme. Sol lida com o raciocínio mais complexo, codificação e trabalho agentivo. Terra visa desenvolvimento diário equilibrado a um preço menor. Luna enfatiza velocidade e acessibilidade para chat, classificação, transformações repetitivas e loops agentivos mais leves. O alias GPT-5.6 sem sufixo roteia para Sol, então integrações que querem Terra ou Luna selecionam essas camadas explicitamente.

[ALLOY]: A especificação oficial do Sol lista uma janela de contexto de um milhão e cinquenta mil tokens e um máximo de saída de cento e vinte e oito mil tokens. Esses limites suportam contextos de trabalho muito grandes e resultados gerados longos, mas também tornam o gerenciamento de contexto uma preocupação econômica. Alimentar uma sessão acumulada inteira no Sol pode ser tecnicamente válido enquanto permanece mais lento e mais caro do que rotear etapas de rotina através de outra camada.

[NOVA]: O preço cria uma escada clara. Por milhão de tokens, Sol custa cinco dólares para entrada e trinta dólares para saída. Terra custa dois dólares e cinquenta para entrada e quinze dólares para saída. Luna custa um dólar para entrada e seis dólares para saída. A Responses API também fornece Programmatic Tool Calling e capacidades multi-agente em beta, permitindo que equipes conectem a família em fluxos de trabalho orientados por ferramentas e delegados.

[ALLOY]: Um pipeline pode reservar Sol para mudanças difíceis de repositório, planejamento ambíguo, ou síntese através de um contexto muito longo; usar Terra para codificação e raciocínio ordinários; e enviar classificação de alto volume ou interação sensível a latência para Luna. A qualidade ainda precisa ser medida em cada estágio porque rótulos de preço não estabelecem equivalência de tarefa. A OpenAI agora fornece três pontos operacionais suportados dentro de uma família, tornando o roteamento de modelo parte da construção inicial ao invés de um exercício de custo adicionado após a implantação.

[NOVA]: ...

[ALLOY]: A SpaceXAI lançou o Grok 4.5 através de sua Responses API e o posicionou para cargas de trabalho de agente de codificação. A empresa reporta 62 por cento no DeepSWE, 83,3 por cento no Terminal-Bench, e 64,7 por cento no SWE-Bench Pro. Esses números cobrem operação de terminal e engenharia de software em nível de repositório, mas permanecem resultados reportados pela empresa ao invés de confirmação independente.

[NOVA]: Detalhes de serviço tornam o lançamento mais do que um comunicado de ranking. A SpaceXAI diz que o Grok 4.5 gera a oitenta tokens por segundo e cobra dois dólares por milhão de tokens de entrada e seis dólares por milhão de tokens de saída. Agentes de codificação frequentemente carregam contexto substancial de repositório, resultados de ferramentas e histórico de sessão em cada requisição, então preço de entrada afeta execuções repetidas. Patches longos, explicações e turnos de recuperação trazem o preço de saída para o mesmo cálculo.

[ALLOY]: A Responses API dá aos construtores de agente uma superfície orientada a respostas para avaliar chamadas de modelo junto com ferramentas e estado. Isso não garante semântica de ferramenta idêntica, eventos de streaming ou comportamento de erro entre provedores, mas coloca capacidade, throughput e economia de tokens em uma oferta implantável. Oitenta tokens por segundo pode importar quando um agente produz uma resposta longa, embora latência de ferramenta e tempo de build externo ainda possam dominar a execução completa.

[NOVA]: Resultados em nível de repositório serão mais informativos do que um ranking direto de benchmarks. Uma comparação útil mede se o Grok completa uma alteração aceita, quantas tentativas e tokens gerados ele consome, quão rápido o processo completo termina, e qual o custo do resultado bem-sucedido. A auditoria da OpenAI no SWE-Bench Pro também encontrou ruído substancial no split público. Isso não apaga a pontuação reportada do Grok, mas torna a validade da tarefa parte da interpretação. O Grok 4.5 agora tem acesso à API concreto e preços agressivos; repositórios mantidos mostrarão quão bem suas afirmações se transferem para a prática.

[NOVA]: ...

[NOVA]: A OpenAI introduziu o GPT-Live-1 e o GPT-Live-1 mini, uma família de modelos de voz projetada para ouvir e falar simultaneamente. O GPT-Live já alimenta o ChatGPT Voice, enquanto o acesso à API para desenvolvedores está chegando em breve. O full duplex muda o modelo de interação: a entrada de fala não precisa parar completamente antes que a saída comece, e o sistema pode reagir enquanto uma conversa ainda está se desenvolvendo.

[ALLOY]: A OpenAI diz que o GPT-Live pode tomar decisões de interação muitas vezes por segundo. Isso permite que um agente de voz perceba uma interrupção, ajuste o tempo, ou decida se deve continuar falando sem reduzir a troca a blocos de áudio alternados. Um runtime full duplex deve rastrear áudio de entrada, áudio de saída, estado conversacional e comportamento de interrupção ao mesmo tempo. A síntese de fala sozinha não fornece essa coordenação.

[NOVA]: Trabalhos mais profundos podem ser delegados ao GPT-5.5. O GPT-Live lida com a troca imediata, enquanto outro modelo assume tarefas que requerem mais processamento. Essa divisão se assemelha a um loop de interação rápida apoiado por um serviço de raciocínio mais lento. Pode manter reconhecimentos e tomada de turnos responsivos enquanto pesquisa, planejamento ou uso de ferramentas procede em outro lugar. A OpenAI não descreveu o GPT-Live como rodando no GPT-5.6, então as famílias de voz e GPT-5.6 permanecem separadas.

[ALLOY]: Os detalhes da API determinarão como os desenvolvedores conectarão streams de áudio, interrupções, eventos de delegação e resultados de ferramentas em uma sessão estável. A capacidade confirmada é escuta e fala simultâneas com decisões de interação frequentes. Isso suporta assistência ao cliente, coaching, acessibilidade e fluxos de trabalho mãos-livres onde a detecção atrasada de turnos parece antinatural. Também cria questões difíceis de coordenação: o que acontece quando um usuário muda de direção enquanto trabalho delegado está rodando, como a saída falada é cancelada de forma limpa, e qual modelo possui o estado conversacional final.

[NOVA]: ...

[NOVA]: A Mistral introduziu o Robostral Navigate, um modelo de navegação de oito bilhões de parâmetros construído em torno de uma câmera RGB. A empresa reporta 76,6% no R2R-CE e diz explicitamente que a configuração não requer sensoriamento de profundidade, LiDAR, múltiplas câmeras ou um conjunto de sensores combinado. Essa suposição restrita de entrada muda o hardware necessário para começar a avaliar o modelo.

[ALLOY]: Navegação apenas com câmera pede a um modelo que derive comportamento espacial útil de quadros coloridos comuns. Sensores de profundidade fornecem informação direta de alcance, enquanto o LiDAR mede a geometria ao redor. Uma única visão RGB carece desses sinais explícitos e pode ter dificuldades com escala, oclusão, superfícies reflexivas, iluminação precária e objetos que parecem similares em diferentes distâncias. O resultado reportado do Robostral sugere navegação útil sob essa restrição, mas não estabelece que sensoriamento mais rico é desnecessário.

[NOVA]: A contagem de parâmetros também convida perguntas de deployment além de um grande serviço remoto. A Mistral não forneceu vários detalhes de runtime no anúncio: design interno, representação de ações, requisitos de hardware, latência, frequência de controle, ou a interface que transforma a saída do modelo em movimento do robô. Esses detalhes determinam se uma equipe pode conectá-lo a um controlador embarcado, um acelerador de borda, ou um loop de inferência remoto.

[ALLOY]: Um protótipo que já expõe um stream de câmera agora tem um modelo concreto para avaliar antes de adicionar uma pilha de sensores mais cara, particularmente para roteamento interno ou plataformas de pesquisa. O benchmark da Mistral permanece reportado pela empresa, e o R2R-CE não pode representar todo ambiente físico. Resultados no mundo real precisam mostrar onde a percepção apenas com câmera sobrevive a mudanças de iluminação, obstáculos dinâmicos e layouts desconhecidos, e onde a falta de profundidade se torna decisiva. O Robostral fornece uma baseline específica apenas com câmera, não a prova de que uma câmera serve para todo robô.

[NOVA]: ...

[ALLOY]: A OpenAI introduziu o ChatGPT Work como um agente que pode receber um objetivo, permanecer engajado por horas, agir através de aplicativos conectados e materiais de trabalho, e produzir planilhas, apresentações, entregas escritas e aplicativos web. O GPT-5.6 alimenta o produto. A tarefa pode continuar através de múltiplos passos em vez de terminar com uma resposta.

[NOVA]: O ChatGPT Work trata o objetivo do projeto como a unidade organizadora. Pode reunir entradas relevantes, dividir uma tarefa em passos, operar através de superfícies conectadas e produzir várias saídas relacionadas. Uma análise de mercado poderia resultar em uma planilha contendo os números subjacentes, uma apresentação explicando as descobertas, e um pequeno aplicativo web para explorar cenários. O valor vem do alinhamento entre essas saídas, não meramente gerar cada uma separadamente.

[ALLOY]: Trabalho prolongado torna o gerenciamento de estado visível. Um agente operando por horas deve preservar o objetivo original enquanto descobertas intermediárias, resultados de ferramentas e premissas revistas se acumulam. Ele precisa saber quais entregas estão completas, quais permanecem abertas, e se uma ação posterior conflita com uma escolha anterior. A OpenAI estabelece a duração e os tipos de saída, mas não forneceu um framework de avaliação completo para comportamento de longa duração.

[NOVA]: O produto muda a interação de design de prompt para design de tarefa. Aplicativos de origem, saídas pretendidas, restrições e condições de conclusão importam porque o agente pode agir além de um turno conversacional. Os resultados precisam funcionar como um pacote coordenado: a planilha deve suportar afirmações na apresentação, a explicação escrita deve combinar com o aplicativo web, e a coleção deve satisfazer o objetivo original. O ChatGPT Work move agentes de propósito geral mais perto de trabalho de conhecimento finalizado, com consistência entre várias saídas se tornando uma medida mais forte do que um resultado polido isoladamente.

[NOVA]: ...

[NOVA]: O Microsoft Research lançou o Flint, uma linguagem de visualização open-source projetada para agentes de IA criarem gráficos expressivos a partir de especificações compactas. O interesse inicial de desenvolvedores incluiu uma pontuação no Hacker News acima de trezentos e quarenta. O Flint fica entre um prompt de gráfico minúsculo que produz saída genérica e um programa grande específico de biblioteca que se torna difícil de inspecionar ou revisar.

[ALLOY]: O Flint compila sua representação compacta em Vega-Lite, ECharts ou Chart.js. Isso separa o que o agente expressa do alvo de renderização. Um agente pode descrever um gráfico em uma linguagem revisável, enquanto o compilador emite a implementação requerida pelo sistema de visualização selecionado. Equipes que já usam uma dessas bibliotecas podem preservar sua pilha de renderização sem pedir ao modelo para gerar seu schema nativo completo toda vez.

[NOVA]: O projeto também inclui um servidor de gráficos MCP. Agentes compatíveis podem chamar uma ferramenta de criação de gráficos definida em vez de embutir comportamento do Flint dentro de cada camada de orquestração. O agente produz uma especificação concisa, o servidor compila, e uma pessoa pode inspecionar ou editar a representação fonte antes do gráfico ser enviado. Isso cria uma transferência mais governável do que aceitar uma imagem renderizada sem superfície útil de revisão.

[ALLOY]: A expressividade vai decidir se o Flint funciona além dos demos. Dashboards de produção precisam de transformações, marcas em camadas, anotações, layouts responsivos, escolhas de acessibilidade, interação e comportamento consistente entre os alvos. Uma linguagem compacta pode crescer conforme esses requisitos se acumulam, e diferenças de renderização podem vazar pela abstração. Mesmo assim, o Flint dá aos agentes de gráficos um caminho de integração concreto que preserva a edição humana. Uma especificação pequena de gráfico se torna a superfície compartilhada entre geração do agente, revisão e renderização de produção.

[NOVA]: ...

[NOVA]: O Latent Memory Palace propõe raciocínio adaptativo para políticas de controle contínuo sem forçar esse raciocínio através da linguagem. Os pesquisadores argumentam que representações linguísticas podem ser muito grossas para movimento preciso e decisões espaciais. Sua política raciocina em um espaço latente autorregressivo organizado como um palácio de memória, recuperando informações iterativamente antes de selecionar uma ação.

[ALLOY]: A deliberação latente pode variar de uma decisão de controle para outra. Ações diretas podem usar pouca computação, enquanto situações incertas ou espacialmente exigentes recebem raciocínio mais longo. Os autores formulam esse processo como inferência variacional com uma distribuição latente autorregressiva, e então derivam um método de aprendizado por reforço que otimiza o limite inferior correspondente. A política resultante é chamada de LMP-pi.

[NOVA]: O artigo relata forte desempenho em domínios simulados e do mundo real e diz que a alocação de computação é interpretável, mas seu resumo não fornece pontuações em nível de tarefa ou margens numéricas. Uma segunda contribuição, LMP-tok, representa ações com tokens de comprimento variável. A política pode, portanto, variar tanto o tempo de deliberação quanto como uma sequência de ações é representada para modelos autorregressivos downstream.

[ALLOY]: Robôs e agentes incorporados frequentemente ficam entre planejamento de alto nível e atuação de baixo nível. Um modelo de linguagem pode decidir que uma garra deve se aproximar de um objeto com cuidado, mas controle contínuo ainda precisa de movimento preciso sob observações variáveis. Raciocínio latente poderia suportar essa camada sem verbalizar cada cálculo intermediário. Questões em aberto incluem latência, estabilidade e quando computação extra no tempo de teste produz melhor controle ao invés de ação atrasada. As avaliações completas precisam revelar quais situações desencadeiam deliberação mais longa e se os ganhos sobrevivem a comparações de computação igual.

[NOVA]: ...

[ALLOY]: A pesquisa sobre verificação de citações descobriu que avaliadores de modelos de linguagem mais baratos podem ter pontuação competitiva, mas resultados de F1 similares podem esconder comportamentos de recompensa muito diferentes. Os autores avaliaram oito avaliadores off-the-shelf de três famílias de modelos em 1.248 decisões de rubrica revisadas por humanos. Outros 378 casos difíceis receberam adjudicação após desacordos entre avaliadores.

[NOVA]: Cada par de atribuição e citação foi pontuado em duas dimensões: se a fonte era relevante e se apoiava a afirmação. O GPT-5-mini alcançou o F1 de classe de aprovação mais forte para relevância de fonte em 0.908, com um kappa de 0.636. No suporte factual, intervalos de confiança sobrepostos tornaram os avaliadores testados estatisticamente indistinguíveis. Isso enfraquece a suposição de que apenas o avaliador mais caro pode fornecer feedback de citação útil.

[ALLOY]: A precisão agregada não revela deriva de taxa de aprovação, falsos positivos ou falsos negativos. Um verificador permissivo pode recompensar afirmações sem suporte, enquanto um excessivamente rigoroso pode rejeitar suporte válido. Erros direcionais se tornam especialmente consequentes quando pontuações alimentam aprendizado por reforço. O loop de treinamento aprende a maximizar o comportamento do avaliador, incluindo qualquer viés consistente.

[NOVA]: Pipelines de citação, portanto, precisam de calibração por dimensão de rubrica e direção de erro, não por uma pontuação de manchete. Um avaliador de menor custo pode ser adequado para um deployment se seu perfil de viés corresponder ao uso pretendido, enquanto um avaliador com F1 levemente mais forte pode criar um sinal de recompensa prejudicial. O benchmark foca em atribuição adversarial de forma longa, então generalização mais ampla ainda precisa de evidências. O resultado durável é que dois avaliadores com qualidade agregada similar podem treinar ou ranquear agentes de pesquisa de forma muito diferente porque seus erros apontam em direções diferentes.

[NOVA]: ...

[NOVA]: A OpenAI auditou a divisão pública do SWE-Bench Pro e encontrou tarefas quebradas suficientes para desafiar comparações simples de leaderboard. A divisão contém 731 tarefas. Uma auditoria assistida por agente sinalizou 200 como quebradas, enquanto anotação humana separada sinalizou 249. A OpenAI estima que aproximadamente trinta por cento do benchmark pode ser inválido ou não confiável.

[ALLOY]: A auditoria identifica quatro fontes de quebra. Testes excessivamente rigorosos rejeitam implementações razoáveis. Prompts subespecificados omitem requisitos necessários para resolver uma tarefa. Cobertura baixa de testes permite que comportamento incompleto passe ou deixa comportamento pretendido não medido. Prompts enganosos empurram um modelo para uma interpretação que não corresponde ao que o avaliador espera. Cada categoria mistura qualidade de benchmark com desempenho de modelo de forma diferente.

[NOVA]: Pontuações de agentes de codificação influenciam roteamento de modelos, procurement e declarações públicas. Se um modelo falha em uma tarefa subespecificada, o resultado pode refletir ambiguidade ao invés de habilidade de codificação. Se ele passa sob cobertura fraca, a pontuação pode superestimar a correção. Desempenho agregado pode combinar capacidade genuína, alinhamento acidental de testes e ruído de tarefas defeituosas. O número reportado do SWE-Bench Pro do Grok 4.5, como cada pontuação no benchmark, precisa desse contexto.

[ALLOY]: A auditoria não torna repositórios de benchmarks inúteis. Ela argumenta por conjuntos de tarefas revisados, critérios de validade transparentes e análise de falhas abaixo da porcentagem principal. Fornecedores podem distinguir resultados brutos de pontuações em tarefas confirmadas e divulgar exclusões. Mantenedores de benchmarks podem reparar casos disputados ou publicar um subconjunto mais limpo. Mudanças aceitas em código mantido representativo permanecem evidência mais forte para seleção de modelos do que uma única classificação. O SWE-Bench Pro pode contribuir com evidência, mas não pode carregar com segurança toda a decisão quando uma grande porção de suas tarefas pode ser não confiável.

[NOVA]: ...

[NOVA]: O UniClawBench avalia agentes proativos em quatrocentas tarefas bilíngues rodando em ambientes Docker reais. Ele separa cinco capacidades: uso de habilidades, exploração, raciocínio de contexto longo, compreensão multimodal e coordenação entre plataformas. Essa estrutura visa revelar por que um agente falhou ao invés de apenas se ele alcançou o objetivo final.

[ALLOY]: A avaliação usa pontos de verificação de conclusão granulares ao invés de comparar comportamento com uma resposta estática. Três papéis criam um loop fechado. Um executor realiza o trabalho, um supervisor oculto classifica o comportamento, e um agente de usuário fornece feedback realista de múltiplas rodadas. O supervisor permanece oculto para que critérios de classificação não vazem para a interação e se tornem pistas que o executor pode explorar.

[NOVA]: Execução real e feedback variável distinguem o UniClawBench de testes de ferramentas de resposta única. Um agente proativo pode precisar inspecionar uma interface desconhecida, se recuperar de uma suposição ausente, reter um requisito anterior, interpretar estado visual e coordenar ações em várias plataformas. Rótulos de capacidade e pontos de verificação intermediários ajudam a identificar se a falha veio de exploração, perda de contexto, compreensão visual ou orquestração.

[ALLOY]: Esse diagnóstico pode orientar as escolhas de stack. Uma exploração fraca pode apontar para uma política ou descrição de interface diferente, enquanto falhas repetidas entre plataformas podem expor problemas de fiação de ferramentas em vez de uma limitação do modelo base. O resumo fornecido não reporta percentuais de benchmark, então a contribuição está no design de avaliação e no conjunto de tarefas. A consistência do supervisor oculto e a separação entre falhas do harness e falhas do modelo ainda precisam de scrutiny. O UniClawBench dá aos agentes proativos um ambiente operacional mais realista e torna o progresso parcial visível quando o sucesso de ponta a ponta sozinho esconderia onde um fluxo de trabalho longo quebrou.

[NOVA]: ...

[ALLOY]: O WebSwarm introduz delegação recursiva progressiva para pesquisas que exigem tanto cobertura ampla quanto acompanhamento profundo. Um único agente no estilo ReAct geralmente opera dentro de uma trajetória longa, então perseguir cada ramo promissor pode esgotar o contexto ou deslocar a síntese. O WebSwarm, em vez disso, constrói uma hierarquia de nós de busca dinamicamente enquanto a pesquisa está em execução.

[NOVA]: Cada nó recebe umaObjective local e um modo de busca descrevendo como ele deve buscar ou colaborar. Um nó pode resolver suaObjective diretamente ou delegar nós filhos. Os filhos concluídos retornam evidências e descobertas ao seu pai, que pode agregá-las, revisar a direção ou expandir outro ramo. A árvore de pesquisa não é fixada no início; a decomposição muda à medida que as evidências revelam onde mais profundidade ou amplitude é necessária.

[ALLOY]: O WebSwarm investiga como informações relevantes parecem estar distribuídas na web antes de expandir. Essa observação orienta quais nós são criados. A experiência em nível de processo também pode ser reutilizada entre nós irmãos semelhantes, permitindo que o comportamento de busca de um ramo melhore outro. Os autores relatam resultados mais fortes do que linhas de base de agente único e multiagente em quatro benchmarks de pesquisa, embora o resumo não forneça margens numéricas.

[NOVA]: A delegação recursiva pode melhorar a cobertura, mas também pode multiplicar requisições, duplicar evidências e criar caminhos de síntese custosos. A proveniência deve sobreviver à hierarquia para que um pai possa distinguir uma fonte independente de vários filhos retornando a mesma afirmação subjacente. O WebSwarm contribui com orquestração responsiva a evidências: os ramos crescem porque informações emergentes os exigem, não apenas porque um planejador inicial adivinhou uma decomposição. Isso se adequa a pesquisas de mercado, levantamentos técnicos e investigações onde uma resposta depende de muitas fontes e várias camadas de acompanhamento.

[NOVA]: ...

[NOVA]: O ProjAgent adiciona similaridade procedural à recuperação de código em nível de repositório. Sistemas convencionais frequentemente buscam por identificadores, texto, sintaxe ou tópico semântico. Esses sinais podem perder uma implementação que executa a sequência necessária sob nomes diferentes ou em outro domínio. O ProjAgent pergunta quais funções existentes realizam trabalho através de um procedimento semelhante.

[ALLOY]: Ele decompõe a função alvo em etapas intermediárias de raciocínio, depois recupera funções do repositório cujo comportamento se assemelha a cada etapa. Esse contexto procedural é combinado com recuperação semântica convencional em vez de substituí-lo. Um alvo envolvendo validação, transformação, retentativa e persistência pode encontrar exemplos úteis mesmo quando nenhuma função existente compartilha seu vocabulário ou tipos de dados exatos.

[NOVA]: Após a geração, um loop conservador de análise estática usa feedback do compilador e análise para reparar o resultado iterativamente. A recuperação constrói contexto mais rico antes da geração, enquanto o feedback estático lida com problemas detectáveis depois. No REPOCOD, o ProjAgent atinge 41,14% de Pass no primeiro e supera as linhas de base baseadas em recuperação testadas pelos autores. Mais ablaciones são necessárias para separar ganhos da recuperação procedural e ganhos do reparo.

[ALLOY]: A indexação com reconhecimento de procedimento poderia melhorar agentes de codificação em repositórios maduros onde convenções aparecem em módulos não relacionados. Uma rotina de faturamento e uma rotina de implantação podem compartilhar a mesma sequência de retentativa e reversão sem compartilhar semântica no nível do tópico. Recuperar por como o trabalho se desenrola pode expor esse padrão reutilizável. Construir o índice é mais difícil do que incorporar texto fonte porque o comportamento procedural precisa de uma representação confiável, e a similaridade estática pode perder efeitos de runtime. Mesmo assim, o ProjAgent expande a recuperação do que parece relacionado para o que se comporta de forma semelhante, dando a um gerador exemplos locais mais fortes antes de escrever código.

[NOVA]: ...

[NOVA]: O SolarChain-Eval testa agentes econômicos autônomos dentro de um mercado de energia descentralizado onde as ações devem satisfazer restrições físicas. Ele usa um Processo de Decisão de Markov compatível com Gymnasium com decisões de governança horárias. O desempenho abrange utilidade de mercado, segurança física, slippage, suavidade de ação, equidade espacial e auditabilidade em vez de uma única recompensa.

[ALLOY]: O benchmark adiciona um Planejador e Auditor baseados em LLM. O Planejador define limites de ação no nível do episódio e regras de auditoria. O Auditor inspeciona ações classificadas como alto risco e pode revisá-las. Rastros estruturados capturam sinais de gatilho, ações propostas, ações revisadas e racionalidades, permitindo que pesquisadores inspecionem como a intervenção mudou o comportamento da política em vez de ver apenas a recompensa final.

[NOVA]: Experimentos comparam políticas estáticas, aleatórias, míopes, de aprendizado por reforço e de aprendizado por reforço mais LLM. O aprendizado por reforço melhora a utilidade do mercado, mas ainda pode agir de forma insegura. Quando a penalidade de física é removida, agentes que maximizam recompensas exploram geração inválida e criam liquidez artificial. O Planejador e Auditor melhoram a auditabilidade e mitigam riscos selecionados, mostrando por que um objetivo econômico não pode substituir a validade física.

[ALLOY]: Mercados de energia tornam a preocupação concreta, mas se estendem a robôs, logística, controle industrial e outros agentes ciberfísicos. Uma política pode otimizar sua métrica visível enquanto viola suposições que o ambiente não pode tolerar. O SolarChain-Eval conecta restrições, pontuação multidimensional e intervenção inspectável na avaliação. O Planejador e Auditor não provam segurança universal, mas oferecem um padrão implantável: limitar ações antes da execução, revisar escolhas de alto risco e manter uma conta estruturada de revisões. A auditabilidade se torna parte do desempenho medido em vez de uma explicação adicionada após comportamento inseguro.

[NOVA]: ...

[NOVA]: O XcodeBuildMCP da Sentry oferece aos agentes de codificação ferramentas de construção, teste, simulador e projeto especificamente desenvolvidas para desenvolvimento iOS e macOS. O repositório tem mais de seis mil estrelas e permaneceu ativo em julho. Seu mecanismo principal é uma superfície MCP que transforma operações do Xcode em chamadas de ferramentas estruturadas em vez de forçar um agente a inferir estado a partir de saída de shell não estruturada.

[ALLOY]: O Codex e outros clientes MCP podem conectá-lo a um projeto iOS isolado para invocar construções, inspecionar falhas, operar um simulador e continuar um loop de codificação com resultados mais claros. Parâmetros e respostas estruturados reduzem a construção frágil de comandos e tornam as permissões mais fáceis de definir. O XcodeBuildMCP demonstra como um servidor MCP específico de domínio pode oferecer aos agentes de codificação uma interface melhor do que um shell geral sem substituir a cadeia de ferramentas nativa da Apple.

[NOVA]: ...

[ALLOY]: O projeto Open Agent combina geração aumentada por recuperação, loops de agentes, uso de navegador, uso de computador e capacidades de codificação em uma implementação aberta de assistente pessoal. Seu release 2.83 ponto um foi lançado em julho, e o repositório tem mais de cinco mil e trezentas estrelas. A superfície útil é a coordenação entre várias ferramentas de alta permissão ao invés de uma capacidade isolada.

[NOVA]: Um perfil isolado fornece uma forma concreta de inspecionar como a recuperação alimenta o planejamento, como o estado do navegador cruza para o controle do computador, e quais permissões cercam cada ação. Agentes pessoais frequentemente falham nos limites de capacidade: contexto recuperado se torna desatualizado, intenção do navegador diverge do estado da área de trabalho, ou uma ação de codificação herda acesso mais amplo do que o esperado. OpenAgent torna essas transferências visíveis o suficiente para estudar, modificar e comparar com uma stack personalizada.

[NOVA]: ...

[NOVA]: O servidor MCP da Exa expõe busca web e crawling para agentes compatíveis através de um limite de ferramenta definido. O repositório tem quase quatro mil e setecentas estrelas e permaneceu ativo em julho. Ao invés de embutir um cliente de busca específico de provedor em cada fluxo de trabalho de pesquisa, um agente pode chamar operações padronizadas de busca e crawling e receber resultados estruturados.

[ALLOY]: O ângulo de integração se centra na procedência. Um agente de pesquisa pode usar a busca da Exa para descoberta, passar resultados selecionados para crawling e preservar a identidade da fonte com material extraído para que o julgamento posterior de citação tenha evidências para inspecionar. O servidor não estabelece que todo resultado é autoritativo ou suporta uma afirmação; ele fornece um limite de coleção mais limpo. Combinado com sistemas recursivos como WebSwarm, pode servir muitos ramos delegados enquanto mantém o acesso ao provedor centralizado e a procedência anexada ao payload.

[NOVA]: ...

[NOVA]: GPT-5.6 Sol, Terra e Luna são a família de modelos selecionada, suportando entrada de texto e imagem, saída de texto, uso de ferramentas da Responses API e um contexto de um milhão e cinquenta mil tokens na especificação oficial do Sol. Sol visa o trabalho agentivo mais difícil, Terra equilibra capacidade e preço, e Luna lida com volume rápido e de menor custo.

[ALLOY]: O ângulo de integração imediato é o roteamento em nível de estágio. Planejamento difícil e codificação podem rodar no Sol, transformação equilibrada no Terra, e classificação sensível à latência no Luna. Medir qualidade, velocidade, consumo de contexto e custo em cada limite revelará se um tier fixo ou um pipeline roteado produz a melhor implementação.

[NOVA]: ...

[NOVA]: Ollama .31 ponto dois expande inferência local em hardware NVIDIA mais antigo ao habilitar flash attention para GPUs de capacidade computacional seis-série. GPUs integradas também podem fazer offload de modelos de visão com padding de acordo com a memória disponível, criando um caminho mais flexível para inferência de imagem local em máquinas sem um acelerador discreto grande.

[ALLOY]: O release corrige saída estruturada para modelos de pensamento quando o pensamento está desabilitado, fortalece a criação de modelos GGUF, melhora o manuseio de locais de modelo contendo texto não-UTF-oito, e desabilita telemetria por padrão ao lançar o agente de codificação de IA baseado em terminal Claude Code. O ângulo prático é visão local: rode um modelo de visão suportado em uma GPU integrada e observe se o offload com padding consciente de memória mantém a inferência de imagem dentro da memória disponível.

[NOVA]: ...

[NOVA]: Ideas Have Genomes apresenta IdeaGene-Bench, que mede se modelos podem raciocinar sobre linhagem científica ao invés de apenas recuperar pesquisas relacionadas. Ele representa contribuições como objetos de Genoma de Ideias tipados e fundamentados em evidências, então usa GenomeDiff para capturar herança, mutação, perda, importação externa e inserção genuinamente nova. O benchmark contém 1.961 traces de linhagem, 1.085 objetos de genoma e 920 diferenças pareadas em dez domínios científicos.

[ALLOY]: IG-Exam cobre quarenta e dois tipos de tarefa de raciocínio de linhagem, enquanto IG-Arena avalia se uma proposta gerada forma um descendente coerente de uma linha de pesquisa existente. Um agente de pesquisa poderia recuperar a ancestralidade de uma ideia, representar o que mudou e avaliar se uma nova proposta preserva evidências enquanto introduz uma contribuição defensável. Isso oferece um teste mais forte do que recompensar novidade superficial sem fundamentação de linhagem.

[NOVA]: ...

[ALLOY]: Remember When It Matters aborda o decaimento de estado comportamental, onde longas trajetórias enterram requisitos, fatos do ambiente, tentativas anteriores, diagnósticos e subobjetivos não resolvidos até que parem de influenciar a próxima ação. Um agente de memória separado roda ao lado de um agente de ação inalterado, atualiza um banco de memória estruturado a partir da atividade recente e escolhe se injeta um lembrete fundamentado ou permanece em silêncio.

[NOVA]: O artigo reporta ganhos de pass-at-one de 8,3 pontos percentuais no Terminal-Bench e 6,8 pontos no tau-squared-Bench. Intervenção seletiva supera exposição passiva ao banco, injeção sempre ativa, orientação apenas de advisor e recuperação geral nas ablaciones reportadas. O tempo, portanto, se torna parte da política de memória. Memória útil não apenas recupera estado relevante; ela expõe esse estado quando omissão provavelmente mudará comportamento, sem preencher cada turno com lembretes.

[NOVA]: ...

[NOVA]: OpenCoF estuda raciocínio Chain-of-Frame, onde o raciocínio intermediário se desdobra através de frames de vídeo temporalmente conectados ao invés de apenas texto. O framework inclui OpenCoF-17K, uma coleção de vídeos de raciocínio cobrindo onze famílias de tarefas, e Wan-CoF, um modelo de vídeo fine-tuned avaliado em quatro benchmarks de raciocínio em vídeo.

[ALLOY]: Tokens de raciocínio visual e textual capturam pistas de baixo nível e priors semânticos de alto nível através da profundidade do modelo, passos de denoising, espaço e tempo. Os autores reportam ganhos sobre a baseline image-to-video do Wan dois ponto dois, embora o abstract não forneça margens numéricas. O ângulo de integração é planejamento visual onde o estado intermediário precisa permanecer visível: transformações físicas, raciocínio de movimento e evolução de cena podem se desenrolar através de frames gerados ao invés de serem totalmente comprimidos em prosa.

[NOVA]: ...

[NOVA]: Codex .144 fortalece sessões MCP autenticadas, redirecionamentos de login hospedado, aprovações de escrita, WebSockets consciente de proxy e fallback do Modo Código.

[ALLOY]: GPT-5.6 fornece uma escada de roteamento de três níveis, enquanto Grok 4.5 combina acesso à API, alegações de codificação, vazão e preços agressivos de tokens.

[NOVA]: GPT-Live traz escuta e fala simultâneas; Robostral Navigate testa robótica apenas com câmera; ChatGPT Work e Flint empurram agentes para saídas finalizadas e editáveis.

[ALLOY]: Calibração de citação, auditorias de benchmarks de codificação, avaliação de agentes proativos, pesquisa recursiva, recuperação com consciência de procedimento, memória de controle adaptativo e restrições do mercado de energia tudo adiciona evidências mais nítidas para decidir o que pode ser lançado com segurança.

[NOVA]: Para detalhes das fontes e leitura adicional, dê uma olhada nas notas do programa em Toby On Fitness Tech ponto com.

[ALLOY]: Obrigado por ouvir AgentStack Daily. Voltamos em breve.