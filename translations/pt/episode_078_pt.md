[NOVA]: Sou NOVA.

[ALLOY]: Sou ALLOY, e este é o AgentStack Daily...

[NOVA]: OpenClaw 6.11 corrigiu respostas mal direcionadas, envios travados, reconexões perdidas, falhas de configuração do modelo, comportamento de compactação de sessão e padrões administrativos mais seguros em canais, sessões, provedores, a UI de Controle e a UI do terminal.

[ALLOY]: O agente de codificação baseado em terminal OpenAI Codex .142.5 aperfeiçoou o registro de traces ao impedir que payloads completos de requisições WebSocket de Responses apareçam na saída de traces, o que é importante em qualquer lugar onde a telemetria do Codex flui para sistemas de observabilidade compartilhados.

[NOVA]: Claude Fable 5 está disponível novamente após Washington ter removido as restrições aos modelos Mythos e Fable da Anthropic em 30 de junho, e a listagem no OpenRouter está no ar com uma janela de contexto de um milhão de tokens, entrada de texto, imagem e assets enviados, e suporte a raciocínio.

[ALLOY]: Hoje: OpenClaw e Codex lideram o resumo de lançamentos, Claude Fable 5 retorna como o nível de classe Mythos no topo da cadeia acima do Opus, Claude Sonnet 5 traz um dial de raciocínio de quatro níveis no OpenRouter, e o Google adiciona o Nano Banana 2 Lite para geração rápida de imagens.

[NOVA]: Você vai ouvir onde o Fable 5 se posiciona contra o GPT-5.5 na fronteira atual, como o Fable encadeia trabalhos de múltiplas etapas a partir de um único prompt, por que o paper world-latent do Orca está chamando atenção, como o Agents-A1 alega desempenho de agente de classe trillion-parameter a partir de um student de mixture-of-experts de 35B, e por que OmniRoute, BlockPilot, composição generativa de skills e TRIAGE importam para agent stacks em produção.

[NOVA]: ...

[ALLOY]: Dois lançamentos estáveis de harness de agente chegaram. OpenClaw 6.11 é uma passagem de confiabilidade nas áreas onde sessões de agente costumam ser frágeis: entrega de canais, reconexões, configuração de modelo, padrões administrativos e recuperação após problemas com provedores. O lançamento foca em Telegram, WhatsApp, Matrix, Google Chat, iMessage, Feishu, Mattermost, WebChat, a UI de Controle e a UI do terminal. Na prática, mensagens diretas mais recentes do Google Chat deixam de ser interpretadas erroneamente como conversas em grupo, usuários de webhook do Telegram continuam recebendo mensagens diretas e de grupo através de reinicializações e recargas de configuração, e gateways criptografados do Matrix evitam crescimento de memória de longa duração que pode tirar canais do ar.

[NOVA]: O trabalho de runtime importa porque o agente não apenas responde uma vez; ele tem que manter uma sessão viva enquanto canais reconectam, provedores falham, contexto compacta e humanos continuam enviando instruções. OpenClaw agora usa um timeout de compactação padrão de 180 segundos enquanto ainda respeita configurações explícitas, preserva a propriedade de compactação do context engine do Codex, e mantém o estado do ciclo de vida de falha de provedor correto. Verificações de heartbeat com capacidade de raciocínio também param de vazar raciocínio interno para o Telegram e WhatsApp, exibindo a resposta pretendida do assistente em vez disso.

[ALLOY]: OpenAI Codex .142.5 é muito mais focado, mas o patch carrega peso operacional real. Codex para de escrever payloads completos de requisições WebSocket de Responses nos logs de traces. Isso não é um título de feature; é uma correção de higiene de dados para equipes que direcionam traces do Codex para monitoramento compartilhado, revisão de incidentes ou busca de logs hospedados. O agente de codificação baseado em terminal ainda pode ser observado, mas o corpo da requisição bruta não se torna mais telemetria acidental.

[NOVA]: Juntos, esses lançamentos tornam a camada de harness mais fácil de conectar, fazer deploy e operar. OpenClaw aperta entrega e recuperação em canais voltados para humanos; Codex aperta o que sai do runtime do agente durante debugging. O ganho prático é confiabilidade sem mudar como desenvolvedores configuram sessões, roteiam canais, conectam provedores ou enviam observabilidade ao redor do agente.

[NOVA]: ...

[ALLOY]: Claude Fable 5 está disponível novamente. Na fronteira pública, o nível mais alto é Claude Mythos 5, Claude Fable 5 e OpenAI GPT-5.5. Mythos 5 é o mais forte dos três, mas permanece restrito atrás de uma lista de organizações aprovadas. Fable 5 é o mesmo modelo base com salvaguardas adicionais para capacidades de uso duplo, e é a versão que o roteamento de API comum pode alcançar. GPT-5.5 fica logo atrás desse par. Fable 5 é geralmente considerado o melhor modelo que você pode rotear hoje.

[NOVA]: O que torna o Fable 5 diferente é o encadeamento de único prompt. Dê ao Fable uma mensagem de usuário com várias instruções independentes e o modelo decompõe o trabalho por conta própria: ele identifica cada subtarefa, planeja uma ordem, executa elas em sequência e retorna um resultado que já considera as dependências entre elas. Modelos de fronteira mais antigos precisavam que o orquestrador dividisse o prompt, chamasse o modelo uma vez por instrução e costurasse as respostas de volta. Fable 5 faz essa decomposição internamente.

[ALLOY]: O formato de deployment suporta isso. A listagem do OpenRouter expõe uma janela de contexto de um milhão de tokens, entrada de texto e imagem mais assets de projeto enviados, saída de texto e suporte a raciocínio. A Anthropic o posiciona para trabalho autônomo de conhecimento e codificação. OpenClaw já conectou suporte ao provedor Claude Fable 5 em meados de junho, então a integração do lado harness precede a reabertura da janela de disponibilidade.

[NOVA]: ...

[ALLOY]: Claude Sonnet 5 é a segunda nova listagem da Anthropic no OpenRouter neste ciclo, e a comparação prática é contra Fable 5 em vez de versões mais antigas do Sonnet. Sonnet 5 vem com a mesma janela de contexto de um milhão de tokens que Fable 5 e expõe pensamento adaptativo através de quatro níveis de esforço selecionáveis: baixo, médio, alto e máximo. O formato é o mesmo que Fable 5 em contexto e raciocínio, a diferença é a profundidade por requisição e o custo por token de solicitar isso.

[NOVA]: Pensamento adaptativo é o destaque. Onde Fable 5 escolhe a profundidade de raciocínio internamente como parte de seu comportamento de encadeamento, Sonnet 5 expõe esse dial para o chamador. Uma rodada de planejamento pode solicitar esforço máximo, uma rodada de formatação pode ficar em baixo, e um orquestrador pode rotear raciocínio custoso apenas onde o trabalho compensa. O endpoint é acessível como anthropic/claude-sonnet-5 no OpenRouter, servido pela Anthropic, com entrada de texto e imagem e saída de texto.

[ALLOY]: No ranking atual da fronteira, Sonnet 5 fica um nível abaixo de Fable 5 em capacidade bruta, mas à frente da classe mais antiga Sonnet 4 e da maioria dos endpoints de peso aberto em cargas de trabalho de agente de codificação. Desenvolvedores que estavam roteando suas sessões mais pesadas através de padrões de classe Opus agora podem alcançar um Sonnet de forma Mythos com um dial de esforço ajustável, que muda o cálculo de custo em sessões longas de agente sem abrir mão da superfície de contexto longo.

[NOVA]: Vale ficar de olho se os clientes de roteador exibem o controle de esforço em quatro etapas de forma clara. O valor depende de o comportamento por requisição ser consistente entre o SDK próprio do provedor e a passagem pelo OpenRouter, não apenas na listagem do catálogo.

[NOVA]: ...

[ALLOY]: O Google listou o Nano Banana 2 Lite no OpenRouter sob a marca Gemini 3.1 Flash Lite Image. Ele é posicionado como o modelo de imagem Gemini mais rápido e mais econômico, construído para pipelines de desenvolvedores de alta velocidade e exploração visual rápida, em vez de máxima fidelidade visual.

[NOVA]: A listagem expõe uma janela de contexto de 65.536 tokens e um endpoint de geração de texto para imagem. O tier Flash-Lite deixa claro a troca pretendida: inferência menor e mais rápida com melhor economia por unidade, não a qualidade de renderização mais pesada da classe Pro. Isso o torna adequado para ideação em massa, variações de mockups de produtos, miniaturas, estados de interface, conceitos de anúncios e qualquer fluxo de trabalho que precise de muitas imagens candidatas baratas antes que um humano ou um modelo mais pesado escolha os vencedores.

[ALLOY]: No ranking de modelos de imagem, o Nano Banana 2 Lite fica abaixo dos endpoints Gemini de classe Imagen e Pro em qualidade visual bruta, mas bem acima da maioria dos modelos de imagem open leves em aderência ao prompt e seguimento de instruções. O OpenRouter torna o ângulo de integração direto. Se uma stack de agente de imagem já roteia através da plataforma, o novo endpoint do Google pode ser selecionado com uma mudança na string do modelo. O resto do pipeline pode manter a mesma forma de requisição, wrapper de moderação, construtor de prompts e tratamento de resultados.

[NOVA]: A ressalva é a qualidade. O Flash-Lite foi construído para ser utilizado em volume, não para vencer todas as comparações estéticas. Construtores que usam geração de imagem como sub-rotina de alto volume agora têm uma opção nativa do Google; renders finais críticos para a marca ainda pertencem a um modelo mais pesado.

[NOVA]: ...

[ALLOY]: O Orca, em alta no HuggingFace Daily Papers com 161 upvotes, propõe um espaço latente mundial unificado construído através de previsão multimodal do próximo estado. O objetivo de treinamento é a contribuição real do artigo: alimentar o modelo com observações multimodais do mundo e pedir que ele preveja o próximo estado, o que força um espaço latente compartilhado a codificar a dinâmica mundial em vez de features por domínio.

[NOVA]: Os autores então testam essa representação em tarefas downstream e relatam superar linhas de base especializadas que foram treinadas por domínio. Um espaço latente geral que supera modelos mundiais específicos por domínio é incomum; esse é o sinal dos 161 upvotes. O identificador do arXiv é 2606.30534, a página do projeto está hospedada no site do modelo mundial Orca no GitHub.

[ALLOY]: O mecanismo por trás do resultado é a loss do próximo estado. Prever o próximo estado a partir de uma entrada multimodal requer que o espaço latente capture consequências de ações, persistência ao longo do tempo e alinhamento cross-modal de uma vez. Modelos mundiais especializados por domínio só precisam capturar seu próprio recorte. O argumento do Orca é que o objetivo conjunto produz uma representação que transfere, e os benchmarks são a prova.

[NOVA]: Para construtores que planejam pipelines agentic ou embodied, o sinal prático é que o pré-treinamento de modelos mundiais gerais está se tornando uma alternativa crível a stacks específicas por tarefa. A implicação mais ampla: um espaço latente mundial compartilhado pode mudar o cálculo de custos para longe de feature engineering por domínio nos próximos 12-18 meses, o que vale acompanhar para qualquer equipe construindo simuladores, agentes embodied ou planejadores de estado persistente.

[NOVA]: ...

[ALLOY]: O Agents-A1 da InternScience é um modelo agentic mixture-of-experts de 35 bilhões de parâmetros que afirma alcançar resultados de classe de trillion-parâmetros através de scaling de trajetória de longo horizonte e scaling de habilidade de agente heterogêneo. O artigo está em alta no feed diário do HuggingFace com 73 upvotes, e a atração é a receita, não apenas a contagem de parâmetros.

[NOVA]: Os treinos acontecem em três estágios. Primeiro, fine-tuning supervisionado em traces de agente longos ensina ao modelo comportamento estendido multi-turn em vez de movimentos isolados de prompt-resposta. Segundo, professores por domínio se especializam em capacidades como codificação, uso de ferramentas e recuperação. Terceiro, destilação multi-professor funde esses especialistas em um único estudante MoE de 35B.

[ALLOY]: Nos benchmarks agentic, o Agents-A1 reporta números que ficam próximos de modelos proprietários de trillion-parâmetros em suites de uso de ferramentas de longo horizonte enquanto roda no custo de servir de um MoE de 35B. Essa lacuna entre capacidade e custo de deploy é o ponto do artigo. Se a receita se replicar fora da configuração de avaliação dos autores, a história de orçamento para servir agentes de fronteira muda de "você precisa de um cluster de hyperscaler" para "você precisa de um único host MoE de 35B".

[NOVA]: A prova independente ainda precisa vir. Fique de olho em pesos abertos, replicação de benchmarks e evidências de que os ganhos de longo horizonte sobrevivem fora da configuração de avaliação dos autores. Mas a direção é importante: comportamento agentic de fronteira pode vir cada vez mais da qualidade da trajetória e composição do professor, não apenas de escala bruta.

[NOVA]: ...

[ALLOY]: O OmniRoute, um gateway de IA open-source, entrou em alta no GitHub ao consolidar 231 provedores de modelos em um único endpoint compatível com OpenAI, com aproximadamente 50 provedores oferecendo tiers gratuitos. Ele é meant to sit between coding agents and upstream model APIs, including Cursor, Cline, Copilot, Codex, and the terminal-based AI coding agent Claude Code.

[NOVA]: O mecanismo é um plano de roteamento mais compressão. O OmniRoute aplica um pipeline stacked de compressão de token, modo RTK mais Caveman, antes dos prompts chegarem aos provedores upstream. O autor alega reduções de uso de 15% a 95%, dependendo da carga de trabalho. Uma camada inteligente de auto-fallback reroteia requisições falhadas ou com rate limit para outro provedor em vez de deixar o agente travado em loop.

[ALLOY]: A compatibilidade com MCP e A2A mantém chamadas de ferramentas e mensagens agente-para-agente em jogo, enquanto as superfícies Desktop e PWA facilitam a operação como gateway local em vez de serviço apenas na nuvem. O ângulo de integração é direto: uma única URL base compatível com OpenAI pode substituir o接线 por provedor, permitindo que equipes configurem um gateway e deployem agentes em upstreams pagos e gratuitos.

[NOVA]: Os compromissos a observar são latência, qualidade de compressão e política de fallback. Se a compressão prejudica a fidelidade do prompt ou o fallback pula para provedores mais fracos no momento errado, os agentes podem derivar. Mas para loops de codificação longos que atingem limites rotineiramente, um gateway que abrange provedores pagos e gratuitos é um plano de controle prático.

[NOVA]: ...

[ALLOY]: BlockPilot, em alta no HuggingFace Daily Papers com 64 upvotes, propõe aprendizado de política adaptativo por instância para decodificação especulativa baseada em difusão. Em vez de usar um tamanho de bloco fixo para cada prompt, o método prevê quantos tokens o redator de difusão deve produzir por etapa.

[NOVA]: A rede de políticas lê os estados ocultos do estágio de pré-preenchimento e outputting um tamanho de bloco por solicitação. Então o redator de difusão gera essa quantidade de tokens antes que o modelo alvo os verifique. Horários estáticos gastam o mesmo orçamento de rascunho em prompts fáceis e difíceis; o BlockPilot condiciona a profundidade da especulação na aparência real do prompt.

[ALLOY]: Os autores relatam speedups significativos em relação a abordagens de tamanho de bloco estático com overhead mínimo, e o grupo AMAP-ML lançou a implementação e a política treinada junto com o preprint. Isso importa porque a técnica visa melhorar a eficiência de inferência sem retreinar o modelo alvo.

[NOVA]: Para equipes que já usam decodificação especulativa, o tamanho do bloco passa de um knob de implantação para uma decisão aprendida em tempo de execução. A questão em aberto é a generalização: se a política lançada transfere entre famílias de modelos ou funciona principalmente dentro da distribuição de treinamento usada no artigo.

[NOVA]: ...

[ALLOY]: Xinyu Zhao, Zhen Tan e Vaishnav Tadiparthi enquadram a composição de habilidades como um gargalo crescente para agentes LLM. À medida que as bibliotecas de habilidades procedimentais se expandem, duas abordagens comuns começam a falhar: despejar todas as habilidades no contexto queima tokens, enquanto a recuperação por embedding pode perder combinações úteis entre habilidades.

[NOVA]: O artigo propõe composição generativa de habilidades. Em vez de recuperar uma habilidade fixa ou expor a biblioteca completa, o modelo sintetiza uma combinação sob demanda para a tarefa. A seleção de habilidades se torna geração, não ranqueamento. O agente raciocina sobre como combinar procedimentos em vez de agarrar a correspondência mais próxima de um catálogo.

[ALLOY]: Essa mudança se alinha com como as pilhas de agentes amadurecem. Sistemas iniciais podem sobreviver com um punhado de ferramentas e recuperação simples. Sistemas maiores acumulam habilidades de refatoração, habilidades de sandbox, habilidades de navegador, habilidades de build, habilidades de dados e habilidades de deploy. A parte difícil se torna compô-los sem inchaço de contexto.

[NOVA]: O recado para builders é que a estrutura da biblioteca de habilidades importa tanto quanto o tamanho da biblioteca. Se a composição generativa supera os métodos de recuperação, os runtimes de agentes futuros precisarão de scaffolding que ajude modelos a sintetizar procedimentos seguros e relevantes a partir de peças menores.

[NOVA]: ...

[ALLOY]: TRIAGE adiciona atribuição de crédito com tipos de papel ao aprendizado por reforço agentic. GRPO padrão frequentemente aplica um resultado final do verificador como vantagem uniforme em cada token de ação em um rollout, então passos de busca, clique, edição, navegação e interação com objetos recebem todos o mesmo sinal de aprendizado.

[NOVA]: TRIAGE insere um juiz estruturado entre o rollout e a atualização de gradiente. O juiz rotula cada segmento de rollout por papel semântico antes que a vantagem seja calculada, tornando a atualização condicional ao papel em vez de plana. Isso muda a atribuição de crédito sem mudar a função de recompensa em si.

[ALLOY]: Os ganhos reportados se concentram em rollouts com uso intensivo de ferramentas, o que faz sentido. Em longas trajetórias de agentes, apenas algumas ações decidem o resultado. Um passo de busca útil dentro de um rollout falho não deve ser punido da mesma forma que uma ação sem saída, e cliques redundantes dentro de um rollout bem-sucedido não devem ser reforçados apenas porque a resposta final passou.

[NOVA]: Para equipes treinando políticas de agentes com RL, TRIAGE aponta a atenção para o peso das ações. A qualidade do verificador ainda importa, mas uso intensivo de ferramentas precisa de crédito mais nítido. O modelo juiz se torna o ponto de pressão, porque os rótulos de papel precisam ser consistentes o suficiente para melhorar o aprendizado em vez de adicionar variância.

[NOVA]: ...

[ALLOY]: PrefectHQ fastmcp é um framework Pythonic para construir servidores e clientes do Model Context Protocol. Ele dá aos desenvolvedores ergonomia estilo FastAPI para declarar ferramentas, recursos e prompts, para que agentes possam descobrir capacidades tipadas através de MCP em vez de chamadas de função ad-hoc.

[NOVA]: O ângulo de integração é limpo: adicione fastmcp a uma pilha como Hermes, Codex, OpenClaw ou adjacente a Claude Code quando serviços internos precisam se tornar ferramentas validadas por schema. Em vez de fazer manualmente o encanamento JSON-RPC, equipes podem expor operações tipadas com interfaces inspecionáveis e deixar clientes compatíveis com MCP descobrirem.

[ALLOY]: Isso importa porque a adoção do MCP está passando de demos para fiação em produção. Um framework que faz declarações de ferramentas parecerem código de serviço Python comum reduz o custo de transformar APIs internas em superfícies prontas para agentes.

[NOVA]: ...

[NOVA]: DeusData codebase-memory-mcp é um binário estático único que indexa um repositório em um grafo de conhecimento persistente e responde consultas estruturais em 158 idiomas. O projeto afirma consultas estruturais sub-milissegundos e aproximadamente 99% menos tokens do que reenviar código bruto para um modelo.

[ALLOY]: O encaixe é por baixo dos agentes de codificação. Monte-o como a camada de recuperação de código de longa duração para OpenClaw, Codex, ou qualquer cliente compatível com MCP, e perguntas de navegação podem ser resolvidas contra o grafo em vez de acionar novos embeddings ou preenchimento de contexto grande a cada turno.

[NOVA]: O ganho concreto é latência mais disciplina de tokens. Um agente de codificação que pode perguntar onde um símbolo é definido, quais sites de chamada o tocam, ou como módulos se conectam recebe uma resposta compacta antes de decidir o que editar, construir ou enviar.

[NOVA]: ...

[ALLOY]: O mcp-for-beginners da Microsoft é um currículo multilíngue para o Model Context Protocol, com exemplos práticos em C#, Java, TypeScript, JavaScript, Rust e Python. Ele foca em padrões práticos cliente-servidor para fluxos de trabalho de agentes modulares, escaláveis e seguros.

[NOVA]: O ângulo de integração é habilitação de equipe. Se uma stack tem um runtime em Python, outro em TypeScript, e uma equipe de serviço em Java ou C#, os exemplos dão a cada grupo um caminho nativo para MCP sem forçar uma escolha de linguagem.

[ALLOY]: As peças úteis não são apenas ferramentas hello-world. As lições cobrem padrões em torno de limites cliente-servidor, autenticação e exposição de ferramentas com escopo, que são exatamente as partes que determinam se um agente pode chamar com segurança capacidades de produção.

[NOVA]: ...

[NOVA]: Claude Fable 5 foi selecionado porque a disponibilidade retornou neste ciclo. No ranking atual de fronteira, ele está no topo do nível geralmente disponível ao lado do GPT-5.5, compartilhando paridade de modelo subjacente com o Mythos 5 mais salvaguardas adicionais de uso duplo, e enviando com o comportamento de encadeamento de prompt único que o distingue de endpoints de fronteira mais antigos. Ele é alcançável através do OpenRouter em anthropic/claude-fable-5, carrega uma janela de contexto de um milhão de tokens, suporta texto, imagem, entrada de ativos carregados e saída de texto, e traz suporte a raciocínio. O caminho de avaliação imediato é uma sessão de agente de codificação ou pesquisa autônoma contra padrões atuais da classe Opus, focando em se o comportamento de encadeamento reduz o trabalho de planejamento no nível do orquestrador.

[ALLOY]: Claude Sonnet 5 foi selecionado porque é uma nova listagem de modelo de provedor principal com janela de contexto de um milhão de tokens e esforço de raciocínio selecionável. O ângulo prático é rotear uma sessão de codificação ou agente através do Sonnet 5 e comparar esforço baixo, médio, alto e máximo em latência, custo e qualidade de conclusão, especialmente para sessões onde o Fable 5 é muito caro.

[NOVA]: Google Nano Banana 2 Lite foi selecionado porque adiciona um endpoint de imagem de provedor principal otimizado para velocidade e custo. Ele expõe uma janela de contexto de 65.536 tokens e geração de texto para imagem através do OpenRouter, tornando-o útil para exploração visual de alto volume e geração de ativos em massa.

[ALLOY]: Não houve entradas de modelos não selecionados na verificação de descoberta.

[NOVA]: ...

[NOVA]: Ollama .31.1 traz uma grande aceleração Apple Silicon para Gemma 4 ao se apoiar em previsão multi-token. Em vez de gerar um token por passagem direta, MTP gera rascunha de vários tokens e os verifica em paralelo.

[ALLOY]: O release mantém o fluxo de trabalho local de binário único e os contratos de API existentes, então a mudança interessante é performance em vez de churn de integração. Em um benchmark de agente de codificação, a geração é relatada em aproximadamente 90% mais rápida em hardware da série M.

[NOVA]: O ângulo prático é assistência de codificação local em um Mac da série M. Puxe o Gemma 4, execute um prompt de conclusão de código através do Ollama, e compare tokens por segundo contra um build .30 mais antigo para ver se o ganho MTP aparece na sua própria máquina.

[NOVA]: ...

[ALLOY]: O repo Anthropic-Cybersecurity-Skills empacota 817 habilidades estruturadas de cibersegurança para agentes de IA, mapeadas entre MITRE ATT&CK, NIST CSF, MITRE ATLAS, D3FEND, NIST AI RMF e o framework de combate a fraudes da MITRE.

[NOVA]: Cada habilidade é enviada como um manifesto no estilo agentskills.io, dando aos agentes uma taxonomia fixa em 29 domínios de segurança. Isso o torna relevante para stacks de agentes de segurança que precisam de procedimentos controlados em vez de improvisação livre de ferramentas. A pergunta útil é se a taxonomia melhora a qualidade de despacho quando um agente precisa escolher entre fluxos de trabalho de reconhecimento, defesa, fraude e risco de IA.

[NOVA]: ...

[ALLOY]: AxDafny estuda geração de código verificada agentiva em Dafny, onde um modelo precisa gerar tanto código executável quanto o material de prova necessário para verificação.

[NOVA]: O framework executa reparo guiado por verificador. O verificador baseado em SMT do Dafny captura invariantes falhados, assertions e argumentos de terminação, e então o LLM propõe o próximo reparo. Esse loop dá ao agente contraexemplos concretos em vez de feedback vago. Para desenvolvedores que trabalham com geração de código de alta garantia, o AxDafny mostra como um verificador pode se tornar o canal de feedback mais direto do agente.

[NOVA]: ...

[ALLOY]: Surrogate Fidelity pergunta quando LLMs abertas podem explicar modelos fechados. Interpretabilidade mecanicista geralmente precisa de acesso interno, mas modelos fechados amplamente implantados expõem apenas sinais limitados de API, frequentemente probabilidades de tokens.

[NOVA]: O artigo trata modelos de pesos abertos como probes de medição. Ele usa log-odds de tarefas binárias como escalares compatíveis com API e atribuição leave-one-out para testar quando afirmações mecanicistas transferem entre onze modelos. O ângulo de integração é cautela na avaliação: um surrogate aberto pode ajudar a explicar um modelo fechado apenas quando as condições de transferência são medidas, não assumidas.

[NOVA]: ...

[ALLOY]: OpenClaw 6.11 aperta a entrega de canais e recuperação de sessão, enquanto Codex .142.5 reduz a exposição de trace-log do tráfego Responses WebSocket.

[NOVA]: Claude Fable 5 está de volta ao topo da fronteira geralmente disponível junto com o GPT-5.5, com acesso do roteador, contexto de um milhão de tokens, entrada multimodal, raciocínio e encadeamento de prompt único para trabalho multi-instrução.

[ALLOY]: Claude Sonnet 5 adiciona um endpoint Sonnet de um milhão de tokens com esforço de raciocínio por requisição entre baixo, médio, alto e máximo.

[NOVA]: Nano Banana 2 Lite oferece aos pipelines de agentes de imagem um caminho do Google mais rápido e barato para geração de alto volume.

[ALLOY]: Orca, Agents-A1, BlockPilot, composição generativa de skills e TRIAGE todos empurram as pilhas de agentes em direção a melhores representações, comportamento de longo horizonte mais barato, inferência mais rápida, composição procedural mais forte e RL de crédito mais nítido.

[NOVA]: fastmcp, codebase-memory-mcp e mcp-for-beginners mostram o MCP amadurecendo em uma camada de integração prática para ferramentas tipadas, conhecimento de código e serviços de agentes multi-idioma.

[ALLOY]: Ollama .31.1 torna fluxos de trabalho de codificação local do Gemma 4 mais rápidos no Apple Silicon através de predição multi-token.

[NOVA]: Para os detalhes das fontes por trás de cada item, veja as notas do show em Toby On Fitness Tech ponto com.

[ALLOY]: Obrigado por ouvir o AgentStack Daily. Voltamos em breve.