Episódio 113 — 11 de setembro de 2026

[00:00] Gancho do episódio

O DeepSeek lançou o V4.1 Flash hoje, o primeiro modelo construído sobre sua nova arquitetura Causal Encoder-Decoder — um design de mixture-of-experts esparso que ativa 8 bilhões de parâmetros por token enquanto mantém a computação de inferência bem abaixo de modelos densos comparáveis. O lançamento vem com um relatório técnico completo e pesos abertos sob uma licença permissiva, marcando a primeira mudança arquitetural do DeepSeek desde o V3. O lançamento também ocorre na mesma semana em que a OpenAI afirmou que um modelo interno não lançado resolveu o problema do Prêmio Millennium de Navier-Stokes, apenas para um matemático da NYU e um colaborador empleado na Anthropic afirmarem publicamente que chegaram ao mesmo resultado primeiro — uma disputa de prioridade que agora está vazando para fóruns abertos e levantando novas questões sobre como descobertas matemáticas devem ser creditadas quando o modelo por trás da afirmação é ele mesmo não revelado.

[02:00] DeepSeek Ships V4.1 Flash on a New Architecture

O DeepSeek lançou o V4.1 Flash, um modelo de mixture-of-experts esparso que é o primeiro construído sobre a nova arquitetura Causal Encoder-Decoder (CED) da empresa. O modelo roteia cada token através de apenas uma fatia de seus pesos — 8 bilhões de parâmetros ativos na entrada, 16 bilhões na saída — em vez de executar cada parâmetro em cada passagem, que é o movimento padrão de eficiência do MoE. Ele possui uma janela de contexto de um milhão de tokens, grande o suficiente para conter um livro longo ou uma base de código substancial em um único prompt, e limita as respostas geradas em 4.096 tokens por chamada. O V4.1 Flash está listado sob o próprio provedor do DeepSeek no OpenRouter, então integrações existentes do OpenRouter podem apontar para o novo id do modelo sem alterações no SDK. A pergunta interessante para os desenvolvedores é como o CED difere na prática dos designs baseados apenas em transformers que o DeepSeek lançou antes — o V4.1 Flash é o primeiro modelo na nova arquitetura, e como ele performará definirá expectativas para o que quer que seja lançado em seguida sobre ele.

[02:09] A afirmação de Navier-Stokes da OpenAI encontra uma contra-afirmação

A OpenAI afirma ter resolvido o problema de existência e suavidade de Navier-Stokes, um dos sete desafios do Prêmio Millennium de $1 milhão que estão em aberto desde maio de 2000. O resultado foi produzido por um modelo não lançado cujo nome a empresa não revelou.

Em poucos dias, uma afirmação concorrente surgiu. Tristan Buckmaster, professor de matemática na NYU, e Levent Alpöge, um matemático reconhecido agora na Anthropic, postaram um PDF descrevendo seu próprio esforço de quase um ano no mesmo problema, conduzido em grande parte através do Claude e do produto Codex da OpenAI, especialmente o modelo GPT-5.6 Sol. Eles dizem que atingiram seu avanço em 15 de agosto.

O que se seguiu foi uma disputa pública sobre procedência. Buckmaster escreve que depois que o rumor matemático os alertou, ele contatou a OpenAI e descobriu que a empresa tinha uma equipe paralela usando uma abordagem semelhante. Quando ele perguntou quando a OpenAI enviou seu primeiro prompt, foi-lhe dito eventualmente que foi depois que a notícia de seu trabalho chegou à empresa. Quando ele perguntou se o treinamento do modelo havia tocado em suas sessões do Codex — onde cada rascunho do projeto vivia — a OpenAI disse que o modelo não procurou dados do usuário, mas não respondeu à pergunta sobre treinamento.

A OpenAI ofereceu esperar Buckmaster publicar ou tê-lo como co-autor de seu artigo. O episódio, resumido esta semana pelo Simon Willison's Weblog, subiu acima de 1.300 upvotes no Hacker News.

Para matemáticos e desenvolvedores, a questão em aberto não é qual laboratório cruzou a linha primeiro. É se modelos de fronteira já podem conter vestígios das sessões de pesquisa privadas que os clientes acreditavam serem suas próprias.

[03:46] O aplicativo de IA pessoal Muse da Meta tem um começo lento

O aplicativo mais recente da Meta é o Muse, anunciado como um agente de IA pessoal — software que executa tarefas em seu nome em vez de apenas responder perguntas em uma janela de bate-papo. Segundo o TechCrunch AI, o lançamento está tendo um começo mais lento do que os outros lançamentos recentes de aplicativos da Meta, incluindo o assistente Meta AI e o Threads. Essa comparação tem peso porque a Meta passou os últimos anos tentando se posicionar como uma empresa de IA para consumidores confiável, e um aplicativo de agente pessoal é exatamente a categoria que toda a indústria tem corrido em direção.

O lançamento chamou a atenção das pessoas que prestam mais atenção a esse espaço. Uma discussão no Hacker News sobre a notícia subiu para 655 pontos, o que sinaliza curiosidade genuína de um público técnico, mesmo que a tração no mainstream pareça mais suave do que a Meta provavelmente queria. O aplicativo em si está em ai.meta.com/muse, o que sugere que a Meta está enquadrando-o como uma extensão de seu trabalho de IA em vez de um produto social independente.

Para desenvolvedores e observadores de IA, o movimento é marcar e esperar. As perguntas interessantes são se a Meta trata o Muse como uma jogada de plataforma real com ganchos profundos no Facebook, Instagram e WhatsApp, ou como outra barra lateral experimental. Vale revisitar em algumas semanas assim que revisores independentes o tenham usado e a curva de adoção inicial fique mais clara.

[05:09] Ahead of AI de Raschka diseca o raciocínio do GPT-6 Astra

A newsletter Ahead of AI de Sebastian Raschka publicou uma análise detalhada do GPT-6 Astra da OpenAI, e o artigo rapidamente subiu para 512 pontos no Hacker News. O Astra é o modelo mais capaz da OpenAI voltado para clientes empresariais, e Raschka se concentra em duas ideias técnicas que os profissionais continuam perguntando: transformers em loop e raciocínio oculto.

O artigo cai na lacuna entre o posicionamento da OpenAI e o que os engenheiros realmente querem saber sobre um novo modelo. Raschka apresenta o Astra como um sistema com raciocínio avançado, capacidades de uso de computador e julgamento de escrita e design mais forte, e então percorre os conceitos arquiteturais que podem explicar por que ele se comporta de forma diferente dos lançamentos anteriores do GPT. Essa apresentação importa porque 'raciocínio' e 'uso de computador' são exatamente os recursos que as equipes serão perguntadas para avaliar.

Para desenvolvedores, o valor está em ter uma análise cuidadosa em vez de folhear um comunicado de lançamento e uma dúzia de threads espalhados. Qualquer pessoa decidindo se roteia um fluxo de trabalho de produção através do Astra, ou simplesmente curiosa sobre o que um transformer em loop significa na prática, obtém uma leitura focada.

Raschka publicou o artigo em 9 de setembro, e a thread de discussão é um lugar útil para ver quais perguntas arquiteturais os profissionais estão pressionando. Vale combinar o artigo com qualquer plano de teste interno antes de comprometer um fluxo de trabalho com o novo modelo.

[06:27] Cohere Lança Modelo de Tradução Open-Weights de 218B em 50 Idiomas

A Cohere lançou o North Small Translate, um modelo de tradução automática com pesos abertos que pontua 83,6 na avaliação WMT26 da Cohere em 50 idiomas. O modelo utiliza um design de Mistura de Especialistas, uma forma de construir um modelo com 218 bilhões de parâmetros totais, mas ativando apenas cerca de 25 bilhões deles para qualquer token individual de texto. O restante dos parâmetros fica inativo até que o modelo precise deles, o que explica como um modelo tão grande pode rodar com o perfil de custo de um modelo muito menor.

Os pesos são gratuitos para uso não comercial, e o licenciamento comercial é feito através do Cohere Model Vault ou RWS Language Weaver. Para desenvolvedores, isso significa que qualquer pessoa pode baixar e hospedar o modelo para pesquisa ou ferramentas internas, enquanto empresas que desejam implementar tradução em um produto têm um caminho de fornecedor para direitos de produção.

A conclusão prática: tradução em 50 idiomas em um único modelo, e a primeira opção credível de pesos abertos nessa escala que também vem com uma rota comercial clara. Se você estava juntando APIs de tradução separadas para cobrir um portfólio amplo de idiomas, um modelo que cuida de todos é uma arquitetura significativamente mais simples.

[07:37] BioIR da NVIDIA Quase Triplica a Capacidade de Dobramento de Proteínas em H100s

A NVIDIA detalhou o BioNeMo Inference Runtime, ou BioIR, em 10 de setembro — uma biblioteca Python que acelera modelos de previsão de estrutura biomolecular em GPUs NVIDIA mantendo-se dentro do PyTorch padrão.

O número principal vem de um benchmark pareado em 1.000 alvos diméricos humanos executados em sistemas 8xH100. O Boltz-2 acelerado pelo BioIR dobrou 58,5 mil resíduos dobrados com sucesso por GPU-hora, comparado com 20,2 mil para uma implementação open-source compilada com torch no mesmo hardware. Isso representa um ganho de 2,90x na capacidade.

O BioIR funciona empilhando três otimizações. Primeiro, ele escolhe kernels personalizados ajustados para a carga de trabalho. Segundo, usa captura de CUDA Graph, que registra operações repetidas da GPU como um único gráfico reproduzível. Terceiro, ele escala réplicas com Ray de uma forma que coloca uma cópia completa do modelo por GPU, para que cada acelerador execute uma instância completa do Boltz-2 em vez de uma fatia.

O runtime não é apenas uma demonstração de pesquisa. A NVIDIA diz que o BioIR já impulsionou a expansão recente do Banco de Dados AlphaFold, produzindo cerca de 31 milhões de candidatos a complexos proteicos extraídos de 4.777 proteomas. Esse é o tipo de carga de trabalho onde um ganho de 2,90x muda a frequência com que um laboratório pode atualizar um banco de dados estrutural.

Para quem executa Boltz-2 ou modelos similares de dobramento em hardware H100, o BioIR é um substituto drop-in em Python, não um novo framework. Ele mantém o fluxo de trabalho PyTorch que desenvolvedores já usam enquanto obtém mais estruturas dobradas de cada GPU-hora. A questão em aberto é se os mesmos ganhos aparecem em outros backbones de previsão estrutural além do Boltz-2, e se o padrão BioIR chegará a mais modelos BioNeMo em breve.

[09:10] V4.1-Flash da DeepSeek Comprime Memória de Million-Token em Cache FP4

A DeepSeek AI lançou o V4.1-Flash em 10 de setembro de 2026, e o lançamento é voltado para a carga de trabalho que tem dado dor de cabeça em todos: execuções de agentes com million-token.

O V4.1-Flash é um modelo multimodal de mistura de especialistas. O backbone carrega 552 bilhões de parâmetros, com 196 bilhões de parâmetros adicionais que a DeepSeek rotula como Engram, e o modelo aceita uma janela de contexto de um milhão de tokens. Em termos simples, ele é construído para ler o conteúdo de uma pequena biblioteca em texto, código ou imagens em uma única chamada.

A engenharia interessante está em dois lugares. Primeiro, compressão de cache KV em FP4. Todo transformador mantém uma área de rascunho chamada cache KV, essencialmente um registro do que cada token de entrada atendeu até agora. FP4 comprime cada número nesse rascunho em 4 bits, cortando dramaticamente a memória e largura de banda necessárias para manter prompts de million-token em execução na GPU. Segundo, o reaproveitamento de atenção entre camadas permite que camadas adjacentes compartilhem partes desse rascunho em vez de recalculá-las do zero.

Por que isso importa agora: agentes de longo horizonte transformaram o atendimento de LLMs em um trabalho intensivo de entrada. Pré-preenchimentos repetidos, onde o modelo rele o prompt inteiro de million de tokens a cada turno, acumulam entradas de cache KV que sobrecarregam a memória da GPU, a capacidade de SSD e a largura de banda de interconexão. A DeepSeek está apostando que comprimir o cache e deixar as camadas compartilharem o estado de atenção é uma resposta mais barata do que comprar mais memória.

Para desenvolvedores, a questão prática é se o cacheamento em FP4 junto com atenção compartilhada mantém a capacidade em traces de agentes reais, coisas como repositórios de código, sessões de navegação de várias horas e revisões de documentos longos, em vez de apenas benchmarks sintéticos de contexto longo. Se funcionar, espere uma onda de receitas da comunidade que portam o mesmo truque para outros modelos com pesos abertos.

[10:51] OpenAI e GSA Eliminam Custos de IA para o Governo

A OpenAI e a Administração de Serviços Gerais dos EUA estão lançando um novo acordo para governos federais, estaduais, locais e tribais elegíveis. Sob o arranjo anunciado em 10 de setembro, agências qualificadas pagam $0 em taxas de licença e recebem 50% de desconto nos custos de uso, além de suporte.expandido de defesa cibernética da OpenAI.

A parceria é projetada para ampliar o acesso à IA no setor público, enquanto aborda as preocupações de segurança que têm retardado a adoção pelo governo. O suporte de defesa cibernética é explícito no anúncio, o que significa que a OpenAI está empacotando salvaguardas técnicas junto com o acesso com desconto, em vez de tratar a segurança como uma aquisição separada.

Para desenvolvedores no espaço govtech, isso reduz a barreira de custo para prototipar serviços alimentados por IA que precisam se integrar com sistemas governamentais. Agências estaduais, locais e tribais que anteriormente não conseguiam justificar orçamentos de IA empresarial agora têm um caminho financiado para experimentar, e fornecedores que trabalham com essas agências ganham uma linha de base de preços mais clara para propostas.

O que vale a pena assistir a seguir: como a elegibilidade é definida na prática em milhares de jurisdições, o que o "suporte expandido de defesa cibernética" realmente cobre na entrega, e se provedores concorrentes como Anthropic, Google ou fundações de código aberto respondem com ofertas semelhantes para defender seus próprios pontos de apoio governamentais.

[12:03] OpenAI transforma o Codex harness em uma Agents API gerenciada

Em 10 de setembro, a OpenAI apresentou a Agents API, um serviço de nuvem gerenciado para construir e lançar agentes. Ela é alimentada pelo Codex harness, que a OpenAI agora está expondo como um produto hospedado em vez de algo que os desenvolvedores executam em suas próprias máquinas.

A Agents API faz três coisas para os desenvolvedores. Primeiro, orquestração: o serviço sequencia os passos do agente e roteia o trabalho entre chamadas, para que o desenvolvedor não precise configurar seu próprio agendador ou máquina de estados. Segundo, sessões de longa duração: um agente pode persistir entre interações separadas em vez de redefinir cada vez que um usuário volta. Terceiro, uso de ferramentas: o agente pode chamar ferramentas e sistemas externos, com o serviço gerenciado mediando essas chamadas em vez do desenvolvedor proxyando-as.

O argumento é direto. Em vez de configurar uma infraestrutura de orquestração para executar um agente, você chama a Agents API e envia um agente baseado em nuvem. A OpenAI opera o harness; o desenvolvedor se concentra no que o agente deve fazer e em quais ferramentas ele pode acessar. O lançamento posiciona a OpenAI na mesma faixa de outras plataformas de agentes gerenciados, mas com o Codex como mecanismo subjacente em vez de um tempo de execução genérico.

O que vale a pena assistir a seguir é como as permissões de uso de ferramentas são definidas e como o serviço lida com a autenticação entre o agente e os sistemas externos que ele chama. A Agents API está ativa desde 10 de setembro, e é a primeira vez que o Codex harness é oferecido como um produto gerenciado de propósito geral no qual qualquer pessoa pode construir.

[13:35] Resumo de pesquisa: Uma Nova Receita para Detectar Alucinações de IA, e Reduzi-las pela Metade

Pesquisadores desenvolveram uma nova forma de sinalizar quando um modelo de IA inventa fatos. O pipeline deles verifica uma resposta de vários ângulos ao mesmo tempo: um classificador treinado julga se cada afirmação é fiel, uma pontuação de incerteza sinaliza partes sobre as quais o modelo em si não tem certeza, e uma etapa de calibração coloca esses sinais em uma escala comparável. No benchmark padrão HaluEval, o sistema identificou declarações falsas com precisão em resposta a perguntas, sumarização e diálogo.

A equipe também mostrou o que fazer uma vez que você consegue detectar uma alucinação. Eles fizeram o ajuste fino de um pequeno modelo de código aberto chamado Qwen2.5-0.5B com uma técnica de treinamento de preferência que recompensa o modelo por escolher respostas verdadeiras em vez de respostas inventadas. Isso reduziu a taxa de alucinação do modelo quase pela metade.

Para construtores, esta é uma receita prática: combine um detector com treinamento de preferência, e você obtém um modelo que tanto admite quando está adivinhando quanto aprende a adivinhar menos.

[14:30] GitHub Copilot adiciona integração com Jira e um CLI adaptativo

O GitHub publicou um resumo semanal do Copilot em 10 de setembro, cobrindo alterações enviadas por volta de 7 de setembro. Três itens aparecem na postagem. O aplicativo Copilot ganha integração com Jira, trazendo contexto do rastreador de problemas para o espaço de trabalho do Copilot. O Copilot CLI envia "orquestração adaptativa de modelos" sob o nome Project HydraFusion, dando ao CLI uma forma de coordenar modelos adaptativamente conforme o trabalho muda em vez de bloquear usuários em um único modelo. A postagem também anuncia nova automação de agentes dentro do Visual Studio Code, embora o resumo do changelog seja cortado antes das capacidades específicas serem listadas. Juntos, o GitHub está posicionando o Copilot além de sua superfície original de chat único e para conexões mais profundas com ferramentas de rastreamento de projetos e escolha de modelos dentro do CLI. Os detalhes completos sobre a peça do VS Code permanecem a serem vistos na postagem vinculada.

[15:18] A Agents API da OpenAI Vai ao Ar em Beta Público

A OpenAI colocou a Agents API em beta público em 10 de setembro, e todo desenvolvedor pode usá-la agora. O argumento é direto: este é o mesmo harness e infraestrutura que alimenta o Codex, aberto para que qualquer pessoa possa conectá-lo ao seu próprio produto.

A divisão que importa é quem é dono do quê. A OpenAI hospeda e mantém o harness em si, então a equipe lida com atualizações, patches de runtime e a camada de orquestração. Os desenvolvedores decidem onde a computação real do agente é executada. Existem três opções: um sandbox gerenciado pela OpenAI, a própria infraestrutura do desenvolvedor, ou um sandbox de parceiro. Esse último botão é aquele com o qual as equipes de dados se importarão — se você precisa que a computação fique dentro de um ambiente específico, pode apontá-la para sua própria stack em vez do caminho gerenciado.

É um produto implantável e ao vivo hoje, não uma lista de espera. Essa é a mudança significativa: o harness que os construtores estavam executando agora é alcançável através de uma chamada de API, com a OpenAI assumindo a responsabilidade de mantê-lo atualizado.

Uma coisa vale a pena acompanhar: como a OpenAI lida com atualizações do harness uma vez que os desenvolvedores têm agentes em produção. Se a orquestração por baixo dos agentes ativos mudar, isso se torna uma questão de estabilidade que vale a pena acompanhar à medida que mais equipes lançam contra o beta público.

[16:33] Uma API Auto-hospedada de Download do TikTok e Douyin Acaba de Atingir a v5.0.3

Um scraper auto-hospedado para TikTok e Douyin acabou de enviar uma nova versão, e a amplitude das formas de usá-lo é a novidade. Evil0ctal enviou o Douyin_TikTok_Download_API v5.0.3 em 11 de setembro de 2026. O repositório agora está acima de 20.000 estrelas no GitHub.

O argumento da ferramenta é simples: baixe vídeos do TikTok e Douyin sem a marca d'água, e extraia dados estruturados sobre postagens, perfis, comentários e playlists enquanto isso. O que torna a v5.0.3 interessante é quantas superfícies esses dados são expostos. Nos bastidores, uma API REST assíncrona lida com as solicitações. Em cima disso, o projeto envia um servidor Model Context Protocol (MCP), uma CLI e um console web. Isso significa que o mesmo arquivo pode ser consultado por um agente, script de um terminal, ou examinado em uma aba do navegador.

O deploy é deliberadamente sem fricção: um único `docker compose up` ativa a API junto com um archive PostgreSQL, então vídeos buscados e metadados permanecem entre as execuções. O projeto também depende de um pool de identidade auto-regenerativo, que rotaciona os cookies ou fingerprints que o scraper usa para se identificar nas plataformas. Na prática, essa rotação é o que permite que a ferramenta sobreviva ao constante jogo de gato e rato do TikTok e Douyin contra scrapers — a camada de contribuição própria do projeto absorve novos bloqueios em vez de deixar cada usuário corrigir credenciais manualmente.

Para desenvolvedores, o que se destaca é o servidor MCP. Qualquer agente ou cliente de chat que já fala MCP pode agora tratar contas do TikTok e Douyin como fontes de dados estruturados — extraindo posts, perfis, comentários e playlists sob demanda — sem escrever um scraper do zero. Criadores e pesquisadores que querem seu próprio arquivo privado em vez de uma conta mensal de um scraper hospedado obtêm um único comando Docker como ponto de entrada. Uma coisa para observar a seguir: quanto tempo o pool de identidade auto-regenerativo conseguirá acompanhar agora que ambas as plataformas continuam apertando o acesso automatizado.

[18:31] O Data Agent da OpenAI transforma arquivos da empresa em dashboards por chat

A OpenAI adicionou um Data Agent ao ChatGPT Work, anunciado em 10 de setembro através do canal de notícias da empresa. O propósito declarado do agente é direto: conectar aos dados da empresa, revelar insights e montar dashboards interativos a partir de um prompt em linguagem natural em vez de uma planilha ou consulta SQL.

Esse último ponto é a mudança significativa. O público que o anúncio nomeia é 'todos,' não analistas, o que significa que o produto é posicionado para a pessoa mais próxima da questão de negócio que geralmente tem que enviar uma solicitação e esperar. Uma interface em linguagem natural que produz tanto uma resposta quanto um artefato visual colapsa o típico接力 entre quem pergunta, analista e ferramenta de dashboard.

O que o anúncio realmente confirma é restrito: um produto chamado Data Agent, um lugar dentro do ChatGPT Work, três capacidades (conectar, descobrir e construir dashboards) e uma interface em linguagem natural. O que não especifica é quais fontes de dados se conectam nativamente, se os dashboards são artefatos editáveis ou saídas únicas, ou como os controles de acesso funcionam.

Para desenvolvedores e operadores, a questão prática é se isso substitui um fluxo de trabalho ou adiciona um novo. A leitura honesta do anúncio é que a OpenAI está marcando território na camada de analytics conversacional antes que os concorrentes fechem a mesma porta. Vale observar a seguir: como o agente lida com citações de fontes, e se os dashboards sobrevivem à conversa como entregas autônomas.