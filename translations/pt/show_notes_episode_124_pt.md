Episódio 124 — 21 de outubro de 2026

[00:00] Gancho do episódio

A MiniMax lançou oficialmente o M3.1 Flash, um modelo projetado para trabalho agentivo que envolve tarefas em várias etapas e uso de ferramentas, além de aplicações adicionais em programação, uso de computadores e segurança cibernética. Google, Red Hat e IBM também lançaram o llm-d 1.0, uma stack open source, nativa de Kubernetes, para inferência distribuída de grandes modelos de linguagem em TPUs e GPUs; o lançamento adiciona controle de fluxo multitenant e roteamento consciente de cache para grandes implantações de IA. O SGLang ampliou seu ecossistema de serving com suporte a Clef e Clef Flash, PPLX-Decider v1 e v1.1 e EmbeddingGemma 2, além de exemplos de cookbook para cada modelo. A Microsoft publicou um model card para o Sentiment-Analysis-7B, um modelo de linguagem com 7 bilhões de parâmetros que classifica mensagens de usuários direcionadas a serviços, produtos ou agentes como Negative, Neutral ou Positive. A Mistral apresentou o Timestral, sua primeira família de modelos pré-treinados para séries temporais, ampliando a previsão de leituras de sensores, demanda, volatilidade e outros dados sequenciais para cargas de trabalho que usam apenas CPU.

[02:00] MiniMax M3.1 Flash tem como foco agentes mais rápidos e baratos

A MiniMax lançou oficialmente o M3.1 Flash como um modelo de próxima geração para tarefas agentivas, programação, uso de computadores e segurança cibernética. A MiniMax relata que a inferência online é quase três vezes mais rápida e que os custos de uso para tarefas agentivas são 70% menores do que os de seu antecessor. Segundo a empresa, o modelo consegue concluir fluxos de trabalho SaaS completos nas áreas de vendas, marketing, operações, atendimento ao cliente, finanças e RH. O modelo pode compreender código de forma independente, desenvolver recursos, corrigir problemas, validar seu trabalho por meio de testes e usar ferramentas ao longo de longas sequências de tarefas. Em operações em computadores, ele obtém 61,7 pontos no OSWorld V2 e 29,6 pontos no Agents’ Last Exam, um benchmark para trabalho profissional e tarefas complexas. A MiniMax atribui parte do ganho de eficiência a uma esparsidade mais agressiva, que reduz o cálculo ativo. No uso cotidiano, o modelo reportedly alcança velocidades de saída superiores a 200 tokens por segundo e velocidades medianas superiores a 170. O preço fixo é de US$ 0,15 por milhão de tokens de entrada, US$ 0,60 por milhão de tokens de saída e US$ 0,015 por milhão de tokens de entrada em cache. O M3.1 Flash está disponível por meio da API da MiniMax, do M Plan e do MiniMax Code. A MiniMax afirma que os pesos do modelo serão liberados mais adiante.

[02:23] llm-d 1.0 adiciona roteamento consciente de cache para frotas de IA

Google, Red Hat e IBM lançaram o llm-d 1.0, uma stack open source construída sobre o Kubernetes para distribuir a inferência de grandes modelos de linguagem em TPUs e GPUs.

O lançamento combina vários recursos operacionais em uma única camada: roteamento consciente de cache e de agentes, controle de fluxo multitenant e atualizações sem indisponibilidade. O roteamento consciente de cache significa que as solicitações podem ser direcionadas considerando o cache de inferência; o roteamento consciente de agentes adiciona conhecimento sobre cargas de trabalho agentivas. O controle de fluxo multitenant oferece gerenciamento de tráfego quando vários usuários ou cargas de trabalho compartilham a frota de serving.

A stack abrange vLLM e SGLang, oferecendo às equipes uma forma comum de operar a inferência distribuída entre esses mecanismos e as duas famílias de aceleradores. Isso é importante para organizações que não querem tratar cada componente de serving de forma independente, especialmente quando aplicações agentivas precisam de roteamento coordenado de solicitações e atualizações em produção devem evitar a interrupção do tráfego ativo.

O próximo ponto a observar é quão bem esses controles funcionam em frotas reais de produção à medida que as equipes começam a adotar o llm-d 1.0.

[03:20] SGLang adiciona três novas famílias de modelos

O SGLang v0.5.22 amplia o conjunto de modelos que as equipes podem usar por meio de sua stack de serving. As notas de lançamento listam Clef e Clef Flash, PPLX-Decider v1 e v1.1 e EmbeddingGemma 2 como novos modelos, com uma entrada separada no cookbook vinculada para cada um.

Isso importa porque o trabalho prático de implantação de um modelo vai além de baixar seus pesos: os desenvolvedores também precisam de um caminho testado para servi-lo. As novas entradas oferecem aos aplicativos auto-hospedados e às stacks agentivas mais opções documentadas de modelos para avaliação, incluindo cargas de trabalho com modelos de linguagem e modelos de linguagem e visão.

O lançamento também demonstra uma atividade substancial de manutenção, com 950 pull requests de 245 colaboradores. A próxima questão para quem está avaliando a atualização é quais dos novos modelos atendem aos requisitos de serving e às cargas de trabalho da organização.

[04:06] Modelo de 7 bilhões de parâmetros da Microsoft adiciona classificação local de sentimento

O model card da Microsoft descreve o Sentiment-Analysis-7B como um modelo de linguagem com 7 bilhões de parâmetros, ajustado por fine-tuning para classificar o sentimento de mensagens direcionadas a um serviço, produto ou agente. O modelo foi treinado com reinforcement learning e um LLM judge em um pequeno conjunto interno de aproximadamente 300 exemplos. O modelo gera Negative, Neutral ou Positive como seu primeiro token, seguido de uma breve explicação. Um limite de geração de três tokens retorna somente o rótulo, enquanto o exemplo da editora em Transformers mostra como carregar o modelo causal e gerar uma resposta mais detalhada. A editora relata 72,8% de precisão para o Sentiment-Analysis-7B, em comparação com 62,0% para o Mistral-7B-Instruct-v0.2. O tamanho reduzido do conjunto de treinamento e a ênfase do model card em reinforcement learning são contextos importantes para quem considera utilizar o modelo como um componente local de análise de sentimento em uma stack agentiva. O fluxo de trabalho publicado carrega o modelo causal com o AutoModelForCausalLM do Transformers.

[04:57] Resumo de pesquisas: projetos de busca evoluídos por IA proporcionam ganho mensurável na recuperação

Pesquisadores demonstraram que um modelo de linguagem pode ajudar a projetar a recuperação generativa, uma abordagem de busca e recomendação que gera rótulos semânticos compactos para documentos, em vez de depender apenas da correspondência de palavras-chave. Um modelo open-weight servido localmente gerou e testou alterações em partes executáveis do sistema, incluindo a construção de rótulos semânticos e o tratamento de colisões, sem utilizar um serviço proprietário de IA.

O projeto evoluído melhorou a recuperação em conjuntos de dados de busca geral na web, busca na web e comércio eletrônico multilíngue. Em um benchmark, a métrica que verifica se o resultado correto aparece primeiro aumentou de 55,8% para 59,3%. Um decodificador proxy menor ofereceu feedback rápido ao sistema enquanto os pesquisadores buscavam projetos melhores, em vez de treinar repetidamente o gerador completo.

O limite importante é que o proxy previu melhora para alterações no índice semântico, mas não de forma confiável para alterações no objetivo de treinamento do gerador ou no pipeline completo. Isso torna o método promissor para o projeto de sistemas de busca, mas também torna a validação por proxy essencial antes de aplicá-lo em outros contextos.

[05:56] O Timestral da Mistral traz previsões pré-treinadas para cargas de trabalho somente em CPU

A Mistral lançou o Timestral, uma família de quatro modelos fundacionais para séries temporais com 5 milhões, 28 milhões, 123 milhões e 209 milhões de parâmetros. Os modelos oferecem previsões zero-shot, ou seja, conseguem fazer previsões para dados nunca vistos antes sem treinamento específico para a tarefa, e podem ser ajustados por meio do Mistral Forge para um determinado domínio.

Segundo a Mistral, o Timestral ficou em primeiro lugar entre os modelos pré-treinados e zero-shot em cinco métricas do GIFT-Eval, do TIME e do fev-bench. A empresa afirmou que seus resultados vieram de um único checkpoint, sem combinar múltiplos modelos. A versão com 28 milhões de Parameters superou o Chronos-2 no GIFT-Eval e no TIME, usando aproximadamente um quarto dos parâmetros, enquanto o modelo com 209 milhões de parâmetros superou o TimesFM-3 e o Falcon-2.0 com menos parâmetros.

Os modelos podem prever várias séries relacionadas em conjunto e produzir um conjunto completo de quantis, permitindo que as equipes expressem a incerteza em vez de depender de um único valor previsto. Também aceitam diretamente entradas categóricas, como se uma máquina está em funcionamento, ociosa ou em manutenção, além de entradas conhecidas para o futuro, como cronogramas de produção, paradas programadas e previsões meteorológicas. O Timestral diferencia essas entradas da série-alvo, evitando que valores futuros da série-alvo sejam incluídos inadvertidamente em suas previsões.

A implantação não exige uma placa de vídeo. Em um processador de servidor com oito threads, a previsão de um dia adiante com base em três semanas de histórico em intervalos de 15 minutos levou 10 milissegundos com o modelo de 5 milhões de parâmetros e 140 milissegundos com o modelo de 209 milhões de parâmetros.

Isso torna o Timestral uma opção prática para monitorar fluxos que abrangem sensores industriais, movimentações financeiras e outros dados operacionais. O Mistral Forge oferece ajuste fino, extensões específicas para cada domínio, geração de dados sintéticos e implantação no hardware do cliente, inclusive em ambientes isolados da internet. O principal teste restante é verificar se a adaptação preserva o desempenho útil à medida que os dados de produção mudam ao longo do tempo.

[07:40] O Mercury 3 leva LLMs de difusão à velocidade de produção

A Inception Labs lançou o Mercury 3, um modelo de linguagem baseado em difusão voltado a aplicações em que o tempo de resposta afeta a experiência do usuário. Segundo a empresa, o modelo supera o GPT-6 Luna e o Claude Haiku 5.5 em sua suíte de benchmarks, gera 1.068 tokens por segundo em GPUs NVIDIA e oferece suporte a uma janela de contexto de 1 milhão de tokens, contra 260 mil do Mercury 2.5.

Em um ambiente de testes de agentes web em produção, o Mercury 3 concluiu 50% de 50 tarefas ao vivo de navegação no Mind2Web, resultado que, de acordo com a Inception, foi superior ao do GPT-6.1-Sol, usando o mesmo volume de tokens e o mesmo número de etapas do agente. A empresa também registra um tempo mediano de geração de 0,9 segundo e um tempo mediano de resposta de ponta a ponta de 2,2 segundos nos testes de busca com os óculos inteligentes da Octen.

O Mercury 3 custa US$ 0,20 por milhão de tokens de entrada e US$ 0,70 por milhão de tokens de saída, com 50% de desconto no preço de lançamento e 90% de desconto para tokens de entrada em cache. A Inception e seus parceiros estão usando o modelo em suporte por voz e chat, tutoria, busca, engenharia de dados e navegação web. O modelo está disponível por meio da API da Inception, do OpenRouter, do Basetan e da Vercel, com compatibilidade com a API da OpenAI. O próximo teste é verificar se a velocidade e a qualidade relatadas se mantêm em cargas de trabalho de produção contínuas.

[08:51] Resumo de pesquisas: robôs aprendem a usar a linguagem como memória

Pesquisadores apresentaram o UniWALM, um modelo criado para conectar vídeo, ações e linguagem em uma representação compartilhada. O resultado mais importante é que a geração conjunta da linguagem parece melhorar a manipulação robótica e ajudar em tarefas que dependem da lembrança do que aconteceu antes.

Em vez de transmitir informações por etapas separadas de percepção, planejamento e ação, o UniWALM gera uma ação e uma memória textual simultaneamente. A linguagem gerada é então utilizada na etapa seguinte, oferecendo ao robô um mecanismo leve de memória sem a necessidade de um planejador externo ou de um banco de memórias. Na parte do RMBench que depende de memória, o sistema alcançou 34,5%, sem utilizar um modelo pré-treinado de linguagem ou raciocínio.

Os pesquisadores também treinaram o modelo para se recuperar de trajetórias de ação perturbadas, adicionando essa capacidade sem aumentar o custo da inferência. Uma consequência concreta é um robô capaz de dar continuidade a uma tarefa por meio do movimento e da linguagem: ele pode agir, registrar uma breve observação sobre a tarefa e usar essa observação para orientar sua próxima ação.

[09:50] O Concat oferece uma alternativa local ao CapCut, com suporte a scripts

O Concat é um editor de vídeo de código aberto, com abordagem local e disponível em várias plataformas, apresentado como uma alternativa gratuita ao CapCut. Seu principal recurso面向 pessoas que criam conteúdo é a possibilidade de usar scripts por meio de uma API JSON-RPC e do MCP, que oferecem interfaces estruturadas para que softwares interajam com o editor.

Essa distinção é importante porque abre caminho para conectar a edição de vídeo a fluxos de trabalho automatizados, em vez de tratar cada edição como uma tarefa manual na interface. O repositório no GitHub registra 10.199 estrelas, evidenciando um interesse considerável pelo projeto.

Por isso, o Concat vale a pena ser acompanhado como uma base local para ferramentas e fluxos de trabalho de edição. A próxima evidência útil seriam exemplos concretos das funções de edição expostas por suas interfaces e de quão confiavelmente essas funções executam trabalhos reais de edição.

[10:33] O Terminal X usa o GPT-6.1 Sol para avaliar julgamentos de investimentos

O estudo de caso da OpenAI de 20 de outubro destaca o Eval Agent do Terminal X, que avalia as respostas de acordo com uma rubrica de 54 critérios. Na configuração relatada, segundo a OpenAI, o GPT-6.1 Sol correspondeu ao julgamento de investidores seniores em 88,6% dos casos e identificou 25% mais desvios em relação ao mandato do fundo.

Isso transforma a revisão baseada em rubricas em um padrão concreto de construção: definir os critérios que uma resposta deve atender, avaliá-la de acordo com esses critérios e inspecionar onde ela se afasta das regras ou do julgamento de especialistas. O valor está em fazer com que a avaliação se torne uma etapa separada, orientada por critérios, em vez de depender apenas de uma leitura humana final.

A próxima coisa a acompanhar é se a concordância relatada e a detecção de desvios são transferíveis para outros modelos, mandates e tipos de resultado de investimento. O resultado de 88,6% se aplica à configuração relatada pela Terminal X.

[11:22] Exa 3.0 adiciona um modelo de embeddings maior e a opção $4 Lite

A Exa lançou a versão 3.0 de sua Search API, adicionando um modelo de embeddings maior, uma opção Exa Lite com preço de $4 por 1.000 requisições e o Dynamic Highlights.

O modelo de embeddings maior altera o sistema de representação usado para relacionar consultas ao conteúdo relevante, enquanto o Exa Lite introduz uma opção de API com custo mais baixo. O Dynamic Highlights é outro novo recurso disponibilizado por meio da API aprimorada.

A Exa tambémconductiu uma comparação com a Perplexity, a Brave e a Parallel e afirma que seu sistema superou as três empresas em todos os oito benchmarks. Como a Exa conductiu esses testes por conta própria, os desenvolvedores devem considerar o resultado uma forte alegação do fornecedor, e não uma validação independente.

A questão prática é como o Exa 3.0 se comporta nas próprias buscas de uma equipe e como as novas opções afetam o orçamento. Resultados de benchmarks independentes e o comportamento do Dynamic Highlights em cargas de trabalho reais são as próximas coisas a acompanhar.

[12:13] ChatGPT Work acelera a redefinição de preços de cardápios de restaurantes

Uma franqueada independente da Schlotzsky’s e da Cinnabon reduziu em 95% o tempo necessário para redefinir os preços de seus cardápios usando um fluxo de trabalho criado com o ChatGPT Work. A operadora estima que a mudança pode liberar US$ 100 mil em fluxo de caixa, tornando esse um exemplo concreto de IA indo além da geração de conteúdo e entrando nas operações recorrentes dos negócios.

O resultado importante não é simplesmente a edição mais rápida dos cardápios. Ao transformar o processo de redefinição de preços em um fluxo de trabalho repetível, a franqueada conectou uma tarefa operacional cotidiana a um possível benefício em capital de giro. A redução relatada de 95% oferece a evidência mais clara do impacto.

Para outros grupos de restaurantes e empresas com múltiplas unidades, a oportunidade é identificar trabalhos frequentes de precificação e testar se um fluxo de trabalho semelhante no ChatGPT Work pode reduzir o tempo da equipe, ao mesmo tempo em que melhora o fluxo de caixa. O próximo teste é verificar se outras operadoras conseguem reproduzir tanto a economia de tempo quanto o benefício financeiro em suas próprias unidades.

[13:07] OpenAI adquire a Orchestra Bio para P&D de ciências da vida

A OpenAI está adquirindo a Orchestra Bio para llevar operações|DE IA para a pesquisa e o desenvolvimento de ciências da vida. Os usuários pretendidos são equipes de biofarmacologia que trabalham no desenvolvimento de medicamentos, com o objetivo de ajudá-las a acelerar o desenvolvimento e avançar no estudo de novos tratamentos.

O que importa agora é o contexto: o anúncio se concentra na aplicação de IA dentro das operações de P&D de ciências da vida, em vez de apresentar mais um chatbot de uso geral ou um resultado de pesquisa definido de forma restrita. Isso torna o anúncio relevante para equipes que pensam em como a IA pode apoiar fluxos de trabalho cotidianos de biofarmacologia.

A próxima evidência útil será concreta: quais processos de pesquisa e desenvolvimento se tornarão orientados por IA, como essas capacidades serão disponibilizadas e se elas ajudarão as equipes a operar mais rápido.

[13:48] OpenAI adiciona avaliações do ChatGPT para idiomas com menos recursos

A OpenAI está aprimorando o ChatGPT em linguagens de programação com poucos recursos — idiomas com menos exemplos digitais e recursos disponíveis para ferramentas de software. A empresa anunciou novas avaliações que abrangem engenharia de software, SQLite e migração de COBOL.

A mudança importa para equipes cujo trabalho não está centrado nas linguagens de programação mais amplamente representadas. As tarefas de SQLite envolvem trabalho orientado a bancos de dados, enquanto a migração de COBOL se concentra na transferência de código de uma linguagem de programação empresarial mais antiga. Esses são contextos concretos em que os limites de um assistente de programação com IA podem afetar projetos reais.

Para os desenvolvedores, as novas avaliações oferecem uma base mais relevante para avaliar o ChatGPT do que perguntas gerais de programação. Uma equipe pode examinar como o modelo lida com uma tarefa de engenharia de software, um cenário de SQLite ou uma migração de COBOL antes de decidir onde a assistência da IA deve entrar em seu fluxo de trabalho.

Uma coisa a acompanhar é o que as avaliações ampliadas revelam sobre o desempenho à medida que a OpenAI amplia a atuação do ChatGPT em ambientes com linguagens de poucos recursos.