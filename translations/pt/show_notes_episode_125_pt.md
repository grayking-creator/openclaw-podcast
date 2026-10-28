Episódio 125 — 25 de outubro de 2026

[00:00] Gancho do episódio

Nous Research lançou o Hermes Agent v0.22.5 em 22 de outubro de 2026, reunindo 81 pull requests mesclados em uma versão de correção que abrangeu a CLI e os instaladores, o aplicativo da Microsoft Store, o Docker e o Hermes Cloud. A Anthropic também abriu o código do sandbox-runtime, o sandbox em nível de sistema operacional por trás do Claude Code, que restringe o acesso a arquivos e redes para agentes de IA, servidores MCP e ferramentas de linha de comando. A OpenRouter adicionou o Kimi K3.1 Pro da Moonshot AI, com uma janela de contexto de 1.048.576 tokens, enquanto a OpenAI introduziu a Decisions API para添加 decisões a aplicativos, com ênfase em respostas rápidas e resultados objetivos. A Recursive lançou o Flint, um modelo de programação baseado em texto, com licença Apache 2.0 e arquitetura mixture-of-experts, com 39,8 bilhões de parâmetros totais e aproximadamente 2,5 bilhões ativos por token. A Mistral lançou o Timestral-209M, um modelo de base para séries temporais voltado à previsão zero-shot, capaz de lidar com uma ou várias séries relacionadas e incorporar informações externas.

[02:00] Leitura do Agent Stack Release: Hermes Agent v0.22.5, v0.22.4, v0.22.3

O Hermes Agent v0.22.5, lançado pela Nous Research em 22 de outubro de 2026, reúne 81 pull requests mesclados e 30 issues fechadas, distribuídos em 231 commits que não são de merge e 804 arquivos alterados. A atualização abrange a CLI e os instaladores, o aplicativo da Microsoft Store, o Docker e o Hermes Cloud.

A mudança mais significativa é a delegação plugável. O Hermes pode encaminhar tarefas para subagentes usando mapas de modelos ou perfis, e o roteamento selecionado pode mudar a cada sessão. Isso oferece aos desenvolvedores uma maneira de separar diferentes modelos ou perfis por tipo de tarefa, sem precisar tratar cada backend como parte do aplicativo principal.

O sistema de plugins também ficou mais capaz. Plugins podem expor comandos de barra com opções selecionáveis, disponibilizar o Hermes por meio do Model Context Protocol e importar agentes existentes. O fluxo de configuração pode oferecer um importador quando detecta outro agente, enquanto o Desktop ganha instalação de plugins com um clique, selos de nível e controles de arrastar para fixar na barra lateral.

O gerenciamento de contas e sessões também ficou mais claro. O login agora usa o login de dispositivo sem restrições, convidados do nível gratuito podem transferir seu trabalho para uma conta e o resultado mostra quem está conectado. Os conectores oferecem opções de login em vez de abrir silenciosamente uma sessão de convidado. Os planos com janela de uso ganham medidores, cartões de limite e recuperação para troca de modelos.

O Hermes Agent v0.23.0 é o próximo marco a ser acompanhado, pois a Nous Research afirma que ele conterá as notas completas e selecionadas sobre as alterações acumuladas nestas versões.

[02:35] OpenRouter lista Kimi K3.1 Pro com janela de contexto de 1M tokens

A OpenRouter listou o Kimi K3.1 Pro, descrito no registro como o modelo multimodal de raciocínio com pesos abertos da Moonshot AI e sucessor pós-treinado do Kimi K3. Ele foi criado para programação de longo prazo, o que lhe confere um potencial especial para trabalhos prolongados de desenvolvimento de software e grandes bases de código. Sua característica mais concreta é uma janela de contexto de 1.048.576 tokens. A arquitetura do registro informa que o modelo aceita texto, imagens e vídeo e produz texto, permitindo que desenvolvedores levem diferentes tipos de material ao mesmo prompt. Isso é relevante para fluxos de trabalho nos quais código, capturas de tela e vídeos precisam contribuir para um único resultado. O registro da OpenRouter lista preços por token de US$ 0,000002 para prompts, US$ 0,00001 para conclusões e US$ 0,0000002 para leituras de entradas em cache. A listagem disponibiliza o Kimi K3.1 Pro para avaliação por meio da OpenRouter, com tamanho do contexto, entrada multimodal e custo por token como os principais pontos a avaliar. A Moonshot AI descreve o Kimi K3.1 Pro como sucessor pós-treinado do Kimi K3. O Kimi K3.1 Pro aceita texto, imagens e vídeo, produz texto e tem uma janela de contexto de 1M tokens. A OpenRouter lista o Kimi K3.1 Pro em seu registro de modelos.

[03:42] Anthropic abre seu sandbox de agentes além dos containers

A Anthropic lançou o sandbox-runtime, ou srt, como um sandbox de código aberto em nível de sistema operacional para agentes de IA. O projeto é o sandbox por trás do Claude Code e dá suporte a agentes, servidores MCP e ferramentas de linha de comando sem exigir containers.

Sua função principal é simples: restringir o acesso a arquivos e redes disponível para essas ferramentas. No macOS, utiliza o Seatbelt, o mecanismo de sandboxing do próprio sistema operacional; no Linux, utiliza o bubblewrap. Portanto, a mesma abordagem está disponível em dois ambientes importantes de desktop e servidor, sem obrigar os desenvolvedores a colocar cada agente ou ferramenta em um container.

Para os desenvolvedores, isso muda a escolha de implementação na execução de código orientado por agentes. Em vez de recorrer a um container, um desenvolvedor pode colocar um agente, um servidor de ferramentas ou um utilitário de linha de comando dentro de um sandbox em nível de sistema operacional, com acesso controlado a arquivos e redes. A Anthropic também está disponibilizando para inspeção e reutilização a abordagem de sandboxing usada por trás do Claude Code.

O próximo ponto a acompanhar é como os desenvolvedores combinarão essas restrições de acesso com as ferramentas e os dados específicos de que seus agentes precisam em fluxos de trabalho reais.

[04:44] OpenAI lança a Decisions API para decisões objetivas em aplicativos

A OpenAI lançou a Decisions API, oferecendo aos desenvolvedores de aplicativos uma interface dedicada para escolhas automatizadas. A empresa a descreve como rápida, objetiva e de baixo custo, aplicável a diferentes tipos de aplicativos, em vez de se limitar a um único caso de uso.

Isso importa porque muitos produtos precisam tomar uma pequena decisão em um momento específico: qual opção apresentar, como encaminhar uma solicitação ou qual ação um aplicativo deve executar. A API oferece às equipes outro componente para testar nesses momentos, em vez de tratar cada decisão como parte de um fluxo de trabalho mais amplo.

Para os desenvolvedores, os próximos pontos de comprovação são práticos: quão rápido a API responde, se suas decisões permanecem consistentes em cargas de trabalho reais e quanto essas decisões custam quando incorporadas a um produto em funcionamento.

[05:29] O Flint da Recursive leva um agente de programação de 39,8B para ambientes locais

A Recursive lançou o Flint sob a licença Apache 2.0, e o repositório da Unsloth fornece seu checkpoint, configuração do modelo, tokenizador, template de chat e kit de serving. O Flint é um modelo mixture-of-experts de entrada e saída de texto, projetado para agentes de programação. Ele tem 39,8 bilhões de parâmetros totais, com aproximadamente 2,5 bilhões ativos por token. Cada camada mixture-of-experts contém 256 experts roteados, dos quais seis são selecionados por token, além de um expert compartilhado sempre ativo. O Flint oferece suporte a raciocínio, uso de ferramentas em múltiplas interações e chamadas de ferramentas compatíveis com OpenAI, podendo executar tarefas como investigar bases de código, corrigir bugs, implementar recursos e escrever testes. A Recursive relata 54,9% no Terminal-Bench 2.1, 89,7% no SWE-bench Pro v2 e 74,2% no SWE-bench Verified. O card alerta que as configurações de avaliação variam e que o resultado do Flint no Terminal-Bench considera como insucessas as soluções obtidas por meio de busca na web, enquanto algumas pontuações relatadas por desenvolvedores podem não aplicar esse ajuste. Os pesos sob a licença Apache 2.0 estão disponíveis no repositório GGUF da Unsloth, com variantes quantizadas preparadas para runtimes da NVIDIA e da Apple Silicon. Os resultados podem variar conforme a precisão do checkpoint e o runtime de inferência, portanto a configuração específica de implantação é importante. O Flint ainda pode gerar código com falhas ou chamadas de ferramentas inadequadas, de modo que os aplicativos precisam ter suas próprias permissões e limites de execução. O Flint é um modelo de agente de programação baseado em texto que oferece suporte a raciocínio, uso de ferramentas em múltiplas interações e chamadas de ferramentas compatíveis com OpenAI.

[06:45] O Timestral-209M da Mistral traz previsão probabilística local

A Mistral lançou o Timestral-209M, um modelo fundamental de séries temporais para previsão sem necessidade de retreinamento específico para cada tarefa. Ele é o maior dos quatro tamanhos documentados, que variam de 5 milhões a 209 milhões de parâmetros, e a publicadora afirma que seus resultados de previsão zero-shot lideram no GIFT-Eval, no TIME e no fev-bench. O modelo pode prever uma única série ou várias séries relacionadas. Ele também aceita entradas adicionais que já são conhecidas ou estão programadas para o futuro, o que pode ajudar um aplicativo a incorporar contexto além do histórico-alvo. Sua saída probabilística abrange 21 quantis, para que o software possa solicitar uma previsão mediana junto com limites inferiores e superiores, em vez de tratar uma única predição como certeza. O Timestral aceita até 32.768 passos temporais históricos e prevê até 1.024 passos em uma única passagem. Previsões mais longas são realizadas em blocos. Internamente, ele agrupa 32 passos em cada patch e incorpora tanto os valores quanto os indicadores de observações ausentes. Para os desenvolvedores, a mudança importante é a implantação local por meio do PyTorch em CPU ou GPU. A Mistral também afirma que está lançando o código-fonte para executar o modelo e reproduzir seus resultados de benchmark. Isso torna o Timestral um componente candidato para previsão em serviços locais e pilhas de agentes que precisam de intervalos de probabilidade, horizontes futuros ou vários sinais relacionados, em vez de uma única estimativa pontual. A Mistral lançou o checkpoint Timestral-209M e informou que está lançando o código-fonte. O Timestral oferece suporte a previsão univariada e multivariada, covariáveis apenas do passado e covariáveis conhecidas do futuro, além de predições probabilísticas em 21 quantis. A publicadora relata que, no GIFT-Eval, o Timestral-209M apresentou erros de MASE e CRPS menores que os do TimesFM-3. O checkpoint é executado por meio do PyTorch em CPU ou GPU, e os modelos são lançados sob uma licença Modified MIT.

[08:26] OpenAI e a NASK da Polônia se unem em torno da segurança de IA

A OpenAI e a NASK da Polônia anunciaram uma parceria em 23 de outubro de 2026, abrangendo segurança de IA, cibersegurança e pesquisa técnica. A NASK da Polônia está se juntando à OpenAI para reforçar as salvaguardas e apoiar um ecossistema digital mais resiliente.

Não se trata do lançamento de um produto, mas de uma colaboração entre uma empresa de IA e a instituição nacional de cibersegurança da Polônia. Sua Bedeutung imediata é institucional: a pesquisa sobre segurança e salvaguardas de IA agora se conecta diretamente a uma organização dedicada à segurança da infraestrutura digital polonesa.

Para os desenvolvedores de IA, o sinal útil a acompanhar é se a parceria produzirá salvaguardas concretas, métodos de segurança ou pesquisa técnica que as equipes possam aplicar ao proteger sistemas reais.

[09:06] Resumo da pesquisa: METTA permite que agentes se adaptem durante a tarefa

O METTA, um método de adaptação com memória aprimorada, ajuda um agente de IA a aprender enquanto já está tentando executar uma tarefa, em vez de depender apenas de aprendizados obtidos antes do início dela. Isso é importante para sistemas que precisam lidar com trabalhos desconhecidos e pouca experiência: eles podem atualizar seu comportamento a partir das interações recentes e carregar um resumo compacto de episódios anteriores para a próxima tentativa. Os pesquisadores testaram a abordagem em tarefas não vistas do Meta-World e em tarefas de PointMaze com contexto longo, nas quais a recompensa era rara. Nos ambientes Meta-World retidos para teste, o METTA superou uma taxa de sucesso de 50%, mantendo baixos os custos de treinamento e o tempo de execução. Nas tarefas do labirinto, ele superou baselines baseados em transformers e apresentou uma exploração mais estruturada. A consequência prática é que um agente pode se adaptar com um baixo orçamento de treinamento, mantendo histórico suficiente para orientar tentativas posteriores, em vez de reconstruir sua compreensão do zero a cada vez. A próxima questão é se esse equilíbrio entre aprender durante uma tarefa e lembrar entre diferentes tarefas se mantém fora dos ambientes de benchmark.

[10:07] SpaceX Super Intelligence abre uma rede de parceiros do Grok

A SpaceX Super Intelligence apresentou um programa oficial para empresas que constroem produtos, soluções e serviços com o Grok, com o objetivo de trabalhar em conjunto na prospecção de clientes. A SpaceX Super Intelligence Partner Network separa esse trabalho em Transformation Partners, que ajudam clientes a implantarem a plataforma Grok em toda a empresa, e Marketplace Partners, que criam plugins e integrações que conectam o Grok às ferramentas que os clientes já utilizam.

Mais de 130 empresas participaram da fase de acesso antecipado. Os Transformation Partners estão construindo capacidade de implantação por meio de um programa de certificação Forward Deployed Engineer, com engenheiros treinados em mais de 30 organizações. Os Marketplace Partners estão trabalhando em integrações de produtos para a suíte Grok.

Entre os parceiros de lançamento estão Bain & Company, Databricks, NVIDIA, Snowflake, Galatiq, Adapter Group, AHEAD e Alpha FMC. Suas funções declaradas vão da transformação e entrega empresarial às plataformas de dados, governança, trilhas de auditoria e contexto específico do negócio. A Galatiq, por exemplo, descreve um modelo de entrega no qual engenheiros definem o escopo e constroem sistemas de produção dentro dos fluxos de trabalho dos clientes. A Adapter descreve a Incorporação de toda a trajetória do cliente ao Grok Bot e ao Grok Build, para que cada interação comece a partir de um contexto de missão mais amplo, e não apenas da memória de trabalho.

Para os desenvolvedores, a oportunidade prática é o trabalho conjunto que abrange implantação, integrações, dados empresariais e controles operacionais. O próximo ponto de prova será o alcance da transição dessas parcerias de pilotos para o uso recorrente em produção.

[11:27] Resumo da pesquisa: Uma técnica de treinamento torna a inferência repetitiva de IA menos exigente em memória

Um novo método de pós-treinamento chamado BeNice! ajuda uma classe de modelos de IA que passam repetidamente informações pelas mesmas camadas, mantendo fixo o número de parâmetros aprendidos. Durante a inferência, cada passagem criava sua própria key-value cache — a informação armazenada de tokens anteriores —, fazendo com que o uso de memória crescesse linearmente com o número de repetições. BeNice! treina o modelo de modo que o cache da passagem final possa ser transmitido para a primeira, tornando as passagens repetidas compatíveis com um cache compartilhado. Os pesquisadores relatam que isso preserva a qualidade do modelo, equivalente à do ajuste fino padrão com caches separados. O resultado é importante porque arquiteturas baseadas em loops podem melhorar a qualidade sem simplesmente adicionar mais parâmetros, mas a demanda de memória durante a inferência limitava essa vantagem. BeNice! oferece uma maneira de manter o benefício de qualidade sem evitar caches duplicados ao longo da profundidade. Os pesquisadores também descobriram que a abordagem pode complementar outros métodos de sequência que economizam memória, sugerindo que as equipes poderiam combiná-la com técnicas de compressão existentes quando a eficiência de memória for especialmente importante.

[12:27] DeusData leva inteligência de código local a agentes de IA

A DeusData lançou o codebase-memory-mcp, um projeto local de inteligência de código para desenvolvedores e agentes de IA. Sua versão mais recente é a v0.12.1, datada de 16 de outubro de 2026, e o repositório recebeu um novo push em 24 de outubro. O GitHub informa 47.438 estrelas para o projeto.

O repositório conecta código, documentação e infraestrutura em um grafo persistente. Ele também inclui o CBM Lens, ferramentas MCP, integrações com agentes e seleção de testes ciente de mudanças. Juntas, essas peças visam ajudar desenvolvedores e agentes de IA a trabalhar com uma base de código como um conjunto conectado de informações, em vez de arquivos isolados ou prompts.

Para desenvolvedores, a oportunidade mais útil é uma camada de contexto local que possa apoiar fluxos de trabalho de agentes em código e documentação. O recurso de seleção de testes também pode ajudar as equipes a gastar menos esforço executando testes não relacionados a uma alteração. Algo importante a acompanhar é a eficácia das integrações com agentes e da seleção sensível a mudanças em projetos reais.

[13:21] O Agensh, da Microsoft, coordena 1.024 agentes sem um chefe central

A Microsoft Research abriu o código do Agensh, um framework para múltiplos agentes que executa até 1.024 agentes no ProgramBench sem um orquestrador central, ou controlador único que distribui o trabalho.

O mecanismo útil é a coordenação compartilhada. Os工作人员 se auto-organizam enquanto se comunicam por meio de um repositório Git compartilhado, um canal de chat e um quadro de descobertas. No experimento relatado, o Agensh escalou de um agente para 1.024, mantendo-se dentro de um orçamento de seis horas no ProgramBench.

Isso oferece aos desenvolvedores um framework de código aberto para explorar grandes equipes cooperativas de agentes e estudar como eles se coordinam por meio de código, conversas e descobertas registradas em conjunto. O número principal chama atenção, mas o espaço de trabalho compartilhado e os canais de comunicação são as peças concretas que as equipes podem adaptar.

A próxima questão é como a abordagem se comporta em tarefas além do ProgramBench e sob cargas de trabalho diferentes das do benchmark relatado.

[14:11] Cognition torna de código aberto um plugin de agente para correção de vulnerabilidades

A Cognition abriu o código do plugin Devin Vulnerability Fixes para ajudar as equipes a responder às falhas críticas de execução remota de código desta semana no PHP, no Node.js e em implantações do GitLab autogerenciadas.

A versão inclui três habilidades de agente com licença MIT. Elas inventariam os sistemas afetados, aplicam patches e os testam, e então abrem uma pull request para cada repositório. Isso transforma uma resposta ampla a vulnerabilidades em alterações separadas e revisáveis, em vez de deixar as equipes descobrirem e corrigirem manualmente cada repositório afetado.

O detalhe principal a acompanhar é se as pull requests geradas estão prontas para a revisão normal de engenharia depois que o plugin conclui seu trabalho de inventário, aplicação de patches e testes.

[14:49] Tutorial da Letta constrói copilotos de engenharia com estado

A MarkTechPost publicou um guia prático sobre como criar um copiloto de engenharia com estado usando o Letta. O objetivo é estender um assistente de IA além das informações presentes em seu prompt imediato, para que ele possa trabalhar com contexto persistente e conhecimento reutilizável do projeto.

No centro está a memória central inspecionável, que oferece um lugar visível para o copiloto reter informações. O tutorial também demonstra a recuperação vetorial de arquivos: uma forma de encontrar materiais mais antigos de acordo com seu significado, sem exigir uma correspondência exata de palavras.

Para trabalhos mais complexos, o copiloto pode usar ferramentas personalizadas e compartilhar estado com vários agentes, permitindo que agentes especializados se coordenem em torno do mesmo contexto. Ele também oferece suporte a respostas em streaming e fluxos de trabalho portáteis, que podem migrar entre ambientes.

Para desenvolvedores, o resultado útil é uma arquitetura concreta para um assistente de engenharia capaz de reter o contexto do projeto, recuperar informações relevantes, se conectar a ações especializadas e preservar um fluxo de trabalho reutilizável, em vez de começar do zero em cada sessão.