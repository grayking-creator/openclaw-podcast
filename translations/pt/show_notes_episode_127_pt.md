Episódio 127 — 5 de novembro de 2026

### Abertura do episódio

A OpenAI criou correções para 948 vulnerabilidades do kernel Linux após construir um pipeline autônomo que encontrou, validou e gerou soluções para falhas de escalada local de privilégios. Cada problema poderia permitir que um invasor local obtivesse privilégios elevados, e o trabalho reúne descoberta, validação e geração de patches em um sistema automatizado. O Astra demonstrou um modelo de linguagem de ponta inspecionando e editando diretamente pesos de redes neurais por meio de instruções em linguagem natural, sem um ciclo de treinamento personalizado ou descida de gradiente; o experimento da equipe com Qwen3.5-0.8B aponta para outra maneira de modificar o comportamento de modelos. A OpenAI também lançou o Images 2.6, com geração mais rápida, criação de GIFs, edição mais precisa e novos controles de API em ChatGPT, Codex e na API. O Hermes Agent 0.22.7 acrescenta melhorias de colaboração, agendamento e controle na CLI, no aplicativo web, no Desktop, no Docker e no Hermes Cloud. O Ripple-65B de pesos abertos da Ricursive Intelligence traz chamada nativa de ferramentas, uma janela de contexto de 1.048.576 tokens e programação com agentes projetada para uso local, com resultado relatado de 80,52 no TerminalBench 2.1.

### Atualizações do Agent Stack: Hermes Agent v0.22.7 e v0.22.6

A Nous Research lançou o Hermes Agent v0.22.6 em 2 de novembro de 2026, seguido da v0.22.7 em 3 de novembro. Juntas, as versões ampliam substancialmente as formas de organizar o trabalho compartilhado de agentes, agendar seus resultados e controlar o que eles podem fazer.

O Hermes Agent v0.22.6 acrescenta um aplicativo web servido diretamente pelo gateway. A CLI pode abri-lo, e usuários do Desktop podem acessá-lo pelo painel Web Access na própria rede ou mediante login da Nous. Plugins do Desktop também podem ser carregados em uma aba do navegador. A versão acrescenta renomeação e encerramento de conversas em grupo, menções e colagem de anexos; cada perfil pode aparecer como uma seção na barra lateral do Desktop.

As ferramentas de agendamento também ficam mais fáceis de administrar. Usuários podem cancelar tarefas cron, escolher como uma tarefa reage quando uma execução é perdida e interrompê-la pelo editor de cron do Desktop. O Hermes Agent v0.22.7 passa a permitir que tarefas cron publiquem em conversas em grupo. Essa mesma versão acrescenta encaminhamento opcional a um agente líder nas conversas em grupo do Desktop, um selo de líder, objetivos de sala, notas compartilhadas, um layout de grupo em coluna única que mostra o estado de cada participante em tempo real e quadros Kanban fixados como abas de acesso rápido.

Duas proteções se destacam para desenvolvedores. Bloqueios por habilidade podem impedir que um agente faça gravações autônomas em uma habilidade selecionada, e um gancho anterior à inferência pode bloquear uma rodada antes da chamada ao modelo. O modelo fixado de uma sessão também pode ser redefinido sem apagar o histórico.

O próximo ponto a acompanhar é a v0.23.0, na qual o Hermes planeja publicar notas selecionadas sobre essas áreas de recursos e o histórico completo de mudanças desde a v0.22.0.

### Ripple-65B da RicursiveAI chega ao OpenRouter

O OpenRouter lista o Ripple-65B-Preview, um modelo de 65 bilhões de parâmetros da RicursiveAI com chamada nativa de ferramentas, servido em BF16. A chamada de ferramentas permite que um modelo solicite a um programa a execução de uma função específica, tornando-o relevante para fluxos que combinam documentos extensos com ações externas. O catálogo registra contexto de 1.048.576 tokens e arquitetura de texto para texto. Os preços listados pelo OpenRouter são US$ 0,0000002 por token de entrada, US$ 0,0000006 por token de saída e US$ 0,00000005 por token de entrada lido do cache. Isso oferece aos desenvolvedores uma opção concreta para aplicações de contexto longo que precisam usar ferramentas. A janela de um milhão de tokens é a capacidade de destaque, enquanto o preço do catálogo oferece uma base direta para estimar custos de uso. O modelo listado recebe texto e produz texto, com contexto de 1.048.576 tokens. Ele está disponível por meio de sua listagem no OpenRouter.

### Astra edita diretamente pesos de redes neurais

A equipe relata que o GPT-6 Astra consegue inspecionar pesos brutos de redes neurais, inferir o que uma rede aprendeu e editar diretamente pesos selecionados usando raciocínio em linguagem natural, em vez de um ciclo de treinamento. No experimento com Qwen3.5-0.8B, o Astra identificou um problema nos pesos que causava ciclos repetitivos de raciocínio e então alterou 0,016% deles. Com as mesmas configurações de amostragem, a correção elevou a precisão em MATH-500 de 7,9% para 48,1% e triplicou o desempenho de seguimento de instruções no IFEval.

A equipe chama isso de Weight-Space Programming, um método no qual um modelo de linguagem de uso geral trata pesos como artefatos numéricos editáveis e raciocina sobre o que cada parte calcula. Isso poderia permitir reparar modelos sem a otimização convencional baseada em gradientes e ampliar as ideias sobre o comportamento que pode ser inferido apenas dos parâmetros. Os resultados são explicitamente iniciais; portanto, o próximo ponto a acompanhar é se edições direcionadas conseguem melhorar modelos reais de forma consistente, para além dos exemplos relatados.

### OpenAI encontrou e gerou correções para 948 vulnerabilidades do kernel Linux

A OpenAI construiu um pipeline autônomo para encontrar e corrigir falhas graves do kernel Linux. Ele encontrou, validou e gerou patches para 948 vulnerabilidades de escalada local de privilégios, ou seja, defeitos que podem permitir que alguém com acesso limitado obtenha privilégios maiores na mesma máquina.

A mudança concreta está no tamanho da fila de correções candidatas. Em vez de deixar que as equipes do kernel descubram e reparem cada problema individualmente, o pipeline produz 948 casos validados de vulnerabilidades, com patches gerados que os mantenedores podem revisar. A OpenAI é a organização por trás do pipeline, e as equipes de segurança do kernel Linux são o público evidente de seus resultados.

O próximo ponto a acompanhar é se esses patches gerados passam pela revisão de especialistas e se tornam correções aceitas no Linux.

### OpenAI lança imagens mais rápidas, GIFs e edição mais precisa

A OpenAI lançou o Images 2.6 em 4 de novembro, acelerando a geração de imagens e acrescentando duas capacidades criativas visíveis: criação de GIFs e edição mais precisa.

A atualização está disponível em ChatGPT, Codex e na API. Isso oferece uma via interativa para criar e aperfeiçoar imagens, além de uma via por API para incorporar essas capacidades a aplicativos.

Para desenvolvedores, a oportunidade concreta é acrescentar geração de imagens, criação de GIFs ou edição precisa a produtos e fluxos de trabalho. A OpenAI também introduziu novos controles de API, ampliando o que pode ser configurado ao desenvolver com o modelo. Um próximo ponto a acompanhar é o desempenho desses controles em tarefas reais de edição de imagens e geração de GIFs.

### Ripple-65B leva programação com agentes e pesos abertos a máquinas locais

A Ricursive Intelligence lançou o Ripple-65B Preview, um modelo de uso geral e pesos abertos que, segundo a empresa, assume a liderança entre os modelos de pesos abertos dos Estados Unidos em programação com agentes. Ele obteve 80,52 no TerminalBench 2.1, à frente de Reflection Beam 501B, Meta Muse Spark Open 816B, Thinking Machines Inkling 975B e NVIDIA Nemotron 3 Ultra 550B.

O modelo foi pré-treinado com 12 trilhões de tokens e suporta contextos de até um milhão de tokens. A Ricursive projetou sua arquitetura densa para treinamento e execução eficientes em hardware NVIDIA, buscando viabilizar uma operação local robusta em sistemas como o NVIDIA DGX Spark. Ele está disponível no Hugging Face, Together AI, GMI Cloud e OpenRouter, com lançamento no Fireworks previsto para mais tarde naquele dia.

A Ricursive relata que o custo total de pesquisa e desenvolvimento do Ripple, incluindo trabalho com dados, avaliação, depuração e pós-treinamento, foi de US$ 32 milhões. Para melhorar a eficiência em programação, a empresa testou mudanças arquiteturais em modelos menores antes de ampliá-las e construiu seus próprios pipelines de dados sintéticos, em vez de comprar dados de pós-treinamento. O próximo ponto a acompanhar é o desempenho do modelo fora da avaliação de programação com agentes da Ricursive, enquanto o desenvolvimento avança para modelos de maior escala.

### ComfyUI lança nós de textura e dublagem

O ComfyUI lançou sua versão estável v0.44.0 em 4 de novembro de 2026, com novos componentes criativos para fluxos de trabalho. A versão acrescenta Partner Nodes para texturas Patina e dublagem VEED, ambos contribuídos por bigcat88.

Para quem desenvolve com ComfyUI, essas adições oferecem novas maneiras de incorporar criação de texturas e dublagem a um fluxo baseado em nós. A versão também atualiza os modelos de fluxo do ComfyUI para v0.11.98, oferecendo uma coleção renovada de pontos de partida.

A mudança restante é de manutenção interna: o projeto alterou a versão de Python usada pelo pylint para 3.1. O foco desta versão para criadores é o par de Partner Nodes; por isso, a próxima evidência útil virá de fluxos completos que mostrem como as etapas de textura e dublagem funcionam em conjunto.

### Eleitores impõem novas restrições a data centers de IA

Eleitores norte-americanos rejeitaram ou restringiram data centers em mais de 30 localidades de nove estados. As medidas incluíram moratórias, proibições totais e condições financeiras ou operacionais para grandes operadoras de nuvem que buscavam incentivos fiscais, com algumas votações respondendo diretamente a projetos já em andamento.

Os resultados foram especialmente claros em Edgewater, na Flórida, onde os moradores apoiaram amplamente a inclusão de uma proibição de data centers na carta municipal. Em Perry, Ohio, os eleitores aprovaram uma medida que impõe condições financeiras e operacionais às grandes operadoras que buscam incentivos fiscais.

A pressão política se amplia para além das votações locais. Segundo uma análise, democratas que disputavam mais de 130 eleições federais e para governos estaduais usaram publicidade contrária a empresas de tecnologia ou data centers. O governador do Texas, Greg Abbott, que vinha promovendo a IA e a expansão de data centers, prometeu uma regulamentação mais rígida, mas perdeu sua eleição.

Essa oposição já afeta o capital. Bancos e gestores de ativos que financiam data centers passaram a tratar a resistência local como risco de crédito, enquanto grandes operadoras contratam profissionais de relacionamento com as comunidades. Algumas empresas também tentam descrever suas instalações como “campi computacionais”, embora essa mudança de marca tenha produzido resultados variados.

O próximo teste é saber se essas restrições locais alteram onde a nova infraestrutura de IA será construída, quais projetos conseguem financiamento e incentivos e como as operadoras respondem quando as comunidades exigem mais do que uma nova marca.

### SambaNova e Supermicro planejam sistemas de inferência de IA com diferentes tipos de chips

A SambaNova e a Supermicro anunciaram uma colaboração estratégica para construir e vender sistemas de inferência de IA que combinam RDUs e GPUs. O planejamento inicial da Supermicro contempla 10 mil chips SN50 RDU para a iniciativa.

A SambaNova afirma que a parceria se destina à IA com agentes; o cofundador Rodrigo Liang a chama de “a próxima onda de inferência”, que precisa funcionar em todos os lugares. A proposta concreta é uma arquitetura mista, em vez de um único tipo de processador, combinando chips RDU da SambaNova e GPUs.

Para desenvolvedores, a novidade importante é a combinação de um parceiro de fabricação identificado, uma categoria de produto e uma meta inicial de volume de chips. O próximo ponto a acompanhar é se os 10 mil chips SN50 planejados se traduzem em sistemas de inferência disponíveis.

### OpenAI vincula novos campi computacionais à confiabilidade da rede elétrica

Em 2 de novembro, a OpenAI apresentou o Grid Protectors Program, que trabalhará com concessionárias para ajudar futuros campi computacionais a apoiar a confiabilidade da rede elétrica e proteger os consumidores quanto aos custos de eletricidade.

A iniciativa aborda os dois lados do crescimento da infraestrutura de IA: as necessidades de grandes instalações computacionais e seus efeitos sobre os consumidores de eletricidade que as sustentam. A OpenAI posiciona o programa em torno do trabalho direto com concessionárias, em vez de apresentar uma nova tecnologia computacional ou versão de software.

Para organizações que desenvolvem serviços de IA, a implicação prática é que acesso à energia, confiabilidade da rede e custos para consumidores fazem parte do planejamento de implantação, não são questões separadas. O detalhe a acompanhar é quais concessionárias e futuros campi participarão e quais proteções resultarão desses acordos.

### Resumo de pesquisa: IA de laboratório entende procedimentos, mas ainda falha nos detalhes físicos

Os modelos atuais de IA conseguem acompanhar as etapas gerais de um procedimento de laboratório mostrado em vídeo, mas ainda têm dificuldades com os detalhes físicos necessários para executá-las. O benchmark BEAKER avalia se os modelos conseguem relacionar uma ação pretendida à parte correta de um objeto e a um percurso de movimento viável dentro de um laboratório.

Os autores selecionaram manualmente perguntas sobre reconhecimento de equipamentos e estados experimentais, segurança, montagem de aparelhos, operação, ordem de procedimentos e raciocínio com imagens e vídeos. Os modelos atuais tiveram melhor desempenho em etapas gerais do que em tarefas que exigem relacionar ações a regiões manipuláveis e trajetórias viáveis, isto é, percursos que descrevem como uma máquina pode se mover ou agir.

Isso importa porque um laboratório químico autônomo precisa não apenas entender qual experimento está em andamento, mas também perceber a cena, respeitar restrições de procedimento e segurança e escolher ações que funcionem no mundo físico. Por exemplo, um sistema pode reconhecer que uma amostra precisa ser deslocada e ainda assim não identificar o que pode ser agarrado ou como alcançá-lo. O BEAKER oferece às equipes de pesquisa uma maneira concreta de expor e comparar essa lacuna antes de confiar o controle de laboratórios a modelos semelhantes.

### OpenAI construiu um backend Git para desenvolvimento na escala do Codex

A OpenAI construiu o Pando, um backend compatível com Git, projetado para a escala de desenvolvimento que o Codex torna possível.

A mudança importa porque aborda a camada de repositórios que sustenta a programação assistida por IA. Git é o sistema usado por desenvolvedores para acompanhar e administrar alterações no código, e o Pando foi projetado para oferecer um backend compatível com o desenvolvimento na escala impulsionada pelo Codex.

A evidência concreta no anúncio da OpenAI é o escopo e a autoria do sistema: a OpenAI o construiu, ele é compatível com Git e o desenvolvimento impulsionado pelo Codex define sua escala-alvo. Isso oferece a quem avalia ambientes de desenvolvimento intensivos em IA um padrão específico de infraestrutura a considerar: um backend compatível com Git, projetado em torno da carga de trabalho que o Codex torna possível.

O desempenho do Pando sob cargas reais de repositórios é o próximo ponto a acompanhar.

### OpenAI está adquirindo a Pierre para ampliar o Codex

A OpenAI anunciou em 4 de novembro que adquirirá a Pierre Computer Company. A empresa afirma que a aquisição amplia as ferramentas do Codex para criar, compreender e revisar código.

Isso dá à transação um foco claro de produto: fortalecer as formas pelas quais desenvolvedores criam software, inspecionam bases de código existentes e avaliam código. A OpenAI usa uma aquisição para ampliar o papel do Codex no processo de desenvolvimento de software, em vez de apresentar o anúncio como o lançamento isolado de uma funcionalidade.

Para desenvolvedores, isso sinaliza investimento contínuo no Codex como ambiente de trabalho prático. As capacidades mais úteis a avaliar conforme forem chegando são criação, compreensão e revisão de código.

### Together Compiler reotimiza a inferência conforme o tráfego muda

A Together AI lançou o Together Compiler, um sistema conduzido por agentes que continua reotimizando a passagem direta de um modelo de inferência conforme o tráfego muda. A passagem direta é o cálculo do modelo que produz sua saída. A Together AI relata que o compilador alcançou até 2,6 vezes o número de tokens por segundo das melhores configurações do InferenceX, com esse resultado obtido em menos de 24 horas por modelo.

Isso importa porque desenvolvedores de sistemas de inferência podem avaliar um processo de otimização que se adapta ao tráfego efetivamente atendido, em vez de deixar uma configuração ajustada inalterada. O mecanismo útil é o ciclo contínuo conduzido por agentes; a evidência concreta é a comparação relatada de vazão e o tempo de otimização. Um ponto a acompanhar é se o ganho relatado se mantém com diferentes modelos e padrões de tráfego.
