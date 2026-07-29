Episódio 094 — 28 de julho de 2026

[00:00] Vinheta do episódio

A OpenAI transferiu sua experiência dedicada ao Codex para o aplicativo ChatGPT para desktop em 9 de julho, onde o Codex agora fica ao lado de Chat e Work em um único espaço de trabalho, e o carro-chefe atual da empresa para tarefas complexas de codificação é o GPT-5.6 Sol. A Microsoft adicionou MAI-Cyber-1-Flash ao MDASH, seu sistema multiagente para encontrar e corrigir vulnerabilidades de software, posicionando o novo modelo como um defensor especializado conectado diretamente ao pipeline existente, com o objetivo de comprimir o tempo entre a descoberta de vulnerabilidades e o patch. Um projeto do GitHub com licença MIT chamado esp32-ai foi lançado esta semana, executando um modelo de linguagem de 28,9 milhões de parâmetros em um microcontrolador ESP32-S3 que custa cerca de oito dólares, colocando um gerador de texto funcional no dispositivo em um hardware pequeno o suficiente para perder em uma gaveta de cozinha.

[02:00] Microsoft Adiciona um Modelo Especialista em Defesa Cibernética ao Seu MDASH

A Microsoft acabou de lançar um novo modelo chamado MAI-Cyber-1-Flash e o conectou ao MDASH, o sistema multiagente da empresa para encontrar e corrigir vulnerabilidades de segurança. A forma como é apresentado é importante: este não é um chatbot geral vestindo uma fantasia de segurança. A Microsoft está tratando a defesa cibernética como um pipeline de tarefas discretas — descubra o bug, classifique-o, escreva uma correção — e inserindo um modelo construído especificamente nesse fluxo de trabalho.

O argumento da Microsoft é direto. A empresa afirma que o MAI-Cyber-1-Flash, executando dentro do MDASH, iguala o desempenho dos principais modelos em trabalho de vulnerabilidade a cerca de metade do custo, e que o sistema atinge até 90 por cento em sua própria suíte de tarefas. Ambos os números são fornecidos pelo fornecedor e devem ser tratados como marketing até que equipes independentes os reproduzam em trabalho real de busca de bugs.

O que isso sinaliza para os desenvolvedores é maior do que o modelo único. Configurações multiagente — onde um coordenador atribui tarefas especializadas a modelos menores e focados — têm sido principalmente uma história de pesquisa há dois anos. Colocar um modelo nomeado e disponível por trás de um para trabalho de segurança é um pequeno passo para que esse padrão se torne uma categoria de produto que os defensores podem realmente comprar.

Para uma equipe de segurança que está avaliando, as perguntas relevantes são familiares: a economia de custo se mantém na sua carga de trabalho, a afirmação de 90 por cento sobrevive ao contato com sua base de código, e o design multiagente torna o pipeline auditável em vez de opaco? O anúncio da Microsoft dá um nome e um ponto de preço; as evidências ainda precisam vir de implantações reais.

[02:39] Um Modelo de 28,9M Parâmetros Agora Executa em uma Placa de $8

Um novo projeto de código aberto chamado esp32-ai está executando um modelo de linguagem de 28,9 milhões de parâmetros em um microcontrolador ESP32-S3 que custa cerca de oito dólares, e o lançamento no Hacker News chamou a atenção de 282 pontos. O repositório é licenciado pelo MIT, o que significa que qualquer pessoa pode fazer um fork e enviar um dispositivo baseado nele.

O que torna isso interessante é o fator de forma. O ESP32-S3 é o tipo de chip que já existe dentro de sensores de baixo custo, luzes inteligentes e kits de robótica para hobiastas. Executar um modelo de linguagem nele diretamente significa que um dispositivo pode interpretar solicitações em linguagem simples, resumir leituras de sensores ou responder perguntas simples sem nunca ligar para casa para um servidor. Para desenvolvedores, isso abre interfaces de comando offline para oficinas, explicadores de sensores para kits industriais, robôs de brinquedo conversadores e dispositivos de sala de aula que demonstram como um modelo realmente executa em hardware limitado.

Os limites são reais e merecem ser mencionados. Um modelo de 28,9 milhões de parâmetros em uma placa de oito dólares está longe de ser um assistente de escala de laptop. As respostas são curtas, o raciocínio é superficial e o dispositivo não manterá uma conversa longa. Pense nele como uma peça inteligente de cola local entre sensores e pessoas, não como uma substituição de um assistente em nuvem.

O sinal útil aqui é que os modelos de linguagem continuam diminuindo para silício cada vez mais barato. Cada geração de construções pequenas e locais como esta torna mais realista colocar um pouco de inteligência conversacional em objetos comuns, e fazê-lo sem uma assinatura ou uma conexão de rede.

[04:09] Nanbeige 4.2 traz um modelo de agente de três bilhões de parâmetros para runtimes locais

NOVA: A Nanbeige lançou um modelo de três bilhões de parâmetros chamado Nanbeige4.2-3B no Hugging Face, e é licenciado sob Apache 2.0, então qualquer pessoa pode usá-lo comercialmente.

ALLOY: O número principal aqui é o tamanho. Três bilhões de parâmetros é pequeno o suficiente para rodar em um laptop decente, e o card do modelo lista suporte para Transformers, vLLM, llama.cpp, GGUF quantization, MLX, LM Studio e Ollama — basicamente todos os runtimes de IA local que as pessoas realmente usam.

NOVA: Ele também vem com templates de chat de uso de ferramentas e raciocínio incluídos, além de uma janela de contexto de 256K, que é enorme para um modelo desse tamanho.

ALLOY: Para os desenvolvedores, o argumento prático é um assistente privado e no dispositivo que pode puxar documentos longos ou uma base de código inteira sem enviar nada para a nuvem. Pense em redigir um contrato, resumir uma pilha de PDFs ou conectá-lo a um fluxo de trabalho de codificação que roda localmente.

NOVA: Uma ressalva: a Nanbeige afirma que o modelo supera o Qwen3.5-4B e o Qwen3.5-9B em seis benchmarks — isso é uma afirmação do editor, não verificação independente, então espere pelos testes da comunidade antes de apostar um projeto nele.

ALLOY: Vale a pena observar a seguir: como ele realmente performa em tarefas reais de chamada de ferramentas uma vez que as pessoas comecem a implementá-lo em agentes.

[05:21] A CPU Vera da NVIDIA agora ajuda a projetar a próxima geração de chips da NVIDIA

A NVIDIA diz que sua CPU Vera tem um segundo trabalho: ajudar a projetar a próxima rodada de chips da NVIDIA. A empresa anunciou em 27 de julho que está trabalhando com a Cadence e a Synopsys — os dois fornecedores cujas ferramentas praticamente todo projetista de chips usa para layout, simulação e verificação — para ajustar essas toolchains de EDA para a Vera. A NVIDIA também está rodando a Vera internamente para fazer seu próprio trabalho de projeto de chips.

Esse é um loop recursivo que vale a pena pausar. O tipo de tarefa de engenharia que mais se beneficia de largura de banda de memória e throughput de CPU — as longas simulações que verificam se um novo processador realmente se comporta da forma que a especificação diz — acontece de ser exatamente o que a Vera foi ajustada para fazer. GPUs podem acelerar partes disso, mas a verificação ainda depende fortemente do lado da CPU, onde os dados precisam fluir de forma limpa sem causar gargalos.

A Cadence e a Synopsys são a razão prática pela qual esta história vai além da NVIDIA. Se os dois fornecedores de EDA lançarem versões reais otimizadas para a Vera, os mesmos ganhos que encurtam os ciclos de verificação da NVIDIA podem chegar a qualquer empresa de chips que já paga por essas ferramentas.

O que observar em seguida: um número público de speedup da Cadence ou da Synopsys rodando um fluxo de verificação de cliente real na Vera, não apenas um benchmark interno da NVIDIA.

[06:39] Oito projetos de computação científica mostram o que os fluxos de trabalho do Codex podem fazer agora

A experiência standalone do Codex desktop agora vive dentro do app ChatGPT, ao lado de Chat e Work, para que um único workspace possa lidar com uma conversa, um job de longa duração e uma sessão de codificação. Essa é a forma prática da consolidação desktop de 9 de julho da OpenAI.

Por baixo está o GPT-5.6 Sol, o flagship atual para codificação complexa, uso de computador, pesquisa e trabalho de segurança. A orientação oficial do modelo destaca menos tokens de saída em performance de fronteira, compreensão de design frontend e intenção mais afiadas, Programmatic Tool Calling, e um beta multi-agent. O Programmatic Tool Calling permite que um modelo passe para uma ferramenta um pequeno script em vez de encadear dezenas de chamadas de um lado para outro, o que importa quando um agent precisa coordenar uma corrida de pesquisa multi-step ou uma interface gerada. O beta multi-agent permite que uma sessão do Codex delegue subtarefas paralelas a sessões de trabalho novas.

Como isso fica em laboratórios reais? O relatório de computação científica de 28 de julho da OpenAI percorre oito projetos. Cinco rodam apenas no Codex; três emparelham o Codex com o Claude Code. O exemplo de variantes genômicas cyvcf2 usou o GPT-5.5, então não é um benchmark do Sol e aclaim de codificação deve ser lido como um sinal direcional em vez de um número para citar. Os outros sete percorrem fluxos de trabalho concretos: construção de pipelines de variantes, design de UIs de experimentos e orquestração de longos jobs de análise de dados a partir de uma única superfície desktop.

Um builder agora pode apontar um agent para um notebook bagunçado, receber de volta uma interface projetada mais o script que a alimenta, e rodar tudo em um workspace sem ter que alternar entre abas do navegador.

[08:12] PNNL e AWS planejam ferramentas de decisão de IA para interrupções na rede elétrica

O Pacific Northwest National Laboratory do Departamento de Energia dos EUA e a Amazon Web Services estão se unindo para explorar ferramentas de suporte à decisão com IA para a rede elétrica. A parceria, anunciada em 27 de julho pela HPCwire, visa os momentos que operadores mais temem: clima severo passando pela região, demanda oscilando inesperadamente, ou um ataque cibernético ou físico atingindo a infraestrutura.

Por enquanto, isso é trabalho de planejamento e validação, não uma implantação em rede elétrica ao vivo. O PNNL e a AWS disseram que o objetivo é construir e testar ferramentas que deem aos operadores da rede uma consciência situacional mais rápida e melhores opções durante essas janelas de alta pressão, com humanos permanecendo no controle das decisões reais de manobra. Essa é uma escolha deliberada para infraestrutura crítica, onde você não entrega as chaves de uma subestação para um sistema autônomo enquanto ainda está validando como ele raciocina sob pressão.

O ângulo federal importa porque a resiliência da rede cruza linhas estaduais, utilitários e regimes regulatórios, e o PNNL historicamente conduziu o tipo de modelagem em grande escala e testes de hardware-in-the-loop que operadores menores não conseguem fazer sozinhos. A AWS traz a computação escalável que torna a simulação de cenários sérios viável. Juntos, o objetivo declarado é fazer stress-test das sugestões de IA contra as falhas em cascata que já desligaram redes regionais em eventos anteriores.

O que vale a pena observar em seguida é se a parceria produz benchmarks ou cenários de teste revisáveis publicamente. Até lá, isso é um sinal crível de que a IA para infraestrutura crítica está passando de decks de slides para validação estruturada, não um produto que alguém possa plugar em uma sala de controle ainda.

[09:44] Black Forest Labs Explora Um Modelo Para Múltiplos Tipos de Mídia

A Black Forest Labs acabou de publicar o Self-Flow, um artigo de pesquisa e código público explorando se um único modelo foundation poderia aprender a gerar através de múltiplos tipos de saída usando uma abordagem compartilhada de auto-supervisão. A direção interessante é um sistema adaptável que lida com diferentes mídias em vez de especialistas separadamente projetados para cada modalidade.

A história prática aqui é a direção, não a matemática. O panorama generativo de hoje muitas vezes parece uma pilha de ferramentas estreitas, uma por tipo de saída, coladas com código de orquestração. O Self-Flow pergunta se essa fragmentação é realmente necessária, ou se um foundation unificado poderia substituí-la.

Para builders, a conclusão é paciência mais curiosidade. Nada é lançado hoje. Isso é pesquisa e código público, não um produto que você pode plugar em um fluxo de trabalho. Mas se a direção se mantiver, pipelines multimodais podem ficar mais baratos e simples depois, porque equipes não precisariam de stacks separadas para cada modalidade. A página de pesquisa vale um bookmark para você poder acompanhar o que eventualmente chega como um release real.

O que torna isso vale a pena dar uma olhada é quem está fazendo o trabalho. A Black Forest Labs é um dos grupos de pesquisa generativa mais ativos, então um follow-up unificado carregaria peso real de engenharia em vez de permanecer puramente acadêmico. Por enquanto, trate como um sinal de para onde ferramentas multimodais podem ir, não uma coisa para integrar.

[11:06] O que realmente é necessário para operar um rack HGX B300 de 8 GPUs

O ServeTheHome publicou uma análise prática em 27 de julho sobre o 4U16X-GNR2 da ASRock Rack, um servidor de quatro unidades de rack que acomoda oito aceleradores NVIDIA HGX B300 em um único chassi. Este é o tipo de máquina com a qual um cluster sério de treinamento ou inferência de grande contexto é construído, e a análise é uma janela útil para entender o que um rack de IA denso realmente é quando você olha além do slide de marketing.

A referência ao HGX aqui é importante. HGX é o design de placa base altamente acoplado da NVIDIA, onde as GPUs ficam próximas o suficiente para se comunicarem por links de altíssima largura de banda em vez de PCIe comum. É por isso que a análise dedica mais tempo ao encanamento do que aos gráficos de benchmark. Oito aceleradores trabalhando juntos geram muito calor e muito tráfego entre chips, e o chassi precisa lidar com ambos.

Duas abordagens de refrigeração líquida se destacam, porque a escolha muda o que o restante do data center precisa ter. A refrigeração líquida direta faz o líquido de refrigeração circular próximo aos chips, o que é eficiente, mas pressupõe que a sala já tenha a infraestrutura para isso. O outro caminho aceita uma carga de refrigeração de instalação mais alta em troca de uma implementação mais convencional. De qualquer forma, a decisão de refrigeração é tomada no rack, não na mesa.

A outra lição é largura de banda. A velocidade de interconexão entre GPUs, e para a rede, decide se um nó denso se comporta como um grande computador ou oito pequenos esperando uns pelos outros. A ASRock Rack emparelhou os oito B300s com uma estrutura dimensionada para esse tráfego, o que transforma a contagem bruta de GPUs em throughput utilizável para treinamento e inferência de grande contexto.

Para construtores, a conclusão é que o servidor em si faz parte da arquitetura. Escolha primeiro o envelope de refrigeração e energia, depois escolha o modelo.

[12:52] A Verizon aposta um bilhão em fibra escura para IA de borda

A Verizon quer que Wall Street a veja como uma empresa de infraestrutura de IA, e seu argumento se divide em duas partes: uma frota de mini data centers e um acordo de aproximadamente um bilhão de dólares com o Google para fibra escura. Fibra escura significa fios ópticos já instalados no subsolo que ninguém está iluminando com sinais atualmente. Em vez de comprar largura de banda pronta de uma operadora, a Verizon arrenda os fios brutos e os opera ela mesma.

Por que se incomodar? Porque executar inferência de IA perto do usuário é importante para qualquer coisa sensível à latência — assistentes de voz em tempo real, compreensão de vídeo ao vivo, verificações de fraude, malhas de controle de robótica. Mover a computação de uma nuvem regional distante para um prédio na mesma rua só funciona se você já controla a fibra dessa rua. Fibra escura é como uma operadora controla essa rota.

Também é uma questão de custo. Fios brutos geralmente são mais baratos por gigabit do que transporte comercial, e operá-los permite que uma operadora decida como a capacidade é dividida, em vez de competir em largura de banda commodity.

O que observar: se compromissos de clientes nomeados acompanham o anúncio, e o que o próprio Google planeja transmitir por esses novos links. Por enquanto, isso é principalmente o argumento comercial da Verizon — a demanda real de IA de borda ainda precisa aparecer para justificar a construção.

[14:09] A Enigma levanta $71M para tornar o ajuste de robôs algo como um controle de volume

Uma startup de robótica chamada Enigma acabou de fechar uma rodada seed de setenta e um milhões de dólares, com Index Ventures e Ribbit Capital liderando o investimento, e o argumento é um pouco diferente da história usual de robótica. Em vez de vender uma pilha de autonomia melhor, a empresa quer tornar o comportamento do robô ajustável, mais como girar um botão de volume do que reescrever software.

A premissa do relato da TechCrunch: uma equipe de armazém ou fábrica deveria ser capaz de escolher quanto uma pessoa especifica e quanto o robô descobre sozinho, e mudar essa proporção conforme as condições mudam. Pense em uma célula de picking e embalagem onde o líder de piso quer que o robô pergunte antes de pegar uma caixa de formato estranho esta manhã, mas funcione totalmente sozinho esta noite. Hoje, esse tipo de mudança de comportamento geralmente significa que um engenheiro edita a camada de autonomia; a Enigma está apostando que deveria significar um dial.

Essa é uma dor real em robótica industrial, onde cada ajuste de comportamento atualmente passa por uma pequena equipe de autonomia e lançar uma nova garra ou um novo SKU pode levar semanas de ciclos de ajuste. A proposta de valor é concreta mesmo antes de qualquer vídeo de demonstração.

O aviso honesto é que as alegações do produto são de estágio inicial de startup. Os relatórios públicos não mencionam clientes piloto, hardware suportado ou exatamente o que os controles ajustam nos bastidores. Para qualquer pessoa apostando equipamento físico nisso, a evidência a solicitar é simples. Quais comportamentos de autonomia a interface realmente expõe, e quais ainda são pré-programados? Como fica o registro de auditoria quando o robô faz algo inesperado, e quem é responsável quando isso acontece? Até que essas perguntas tenham respostas públicas, trate os setenta e um milhões como um voto de confiança na ideia do controle em vez de um veredito sobre o produto em si.

[16:00] Vinte agências dos EUA aderem à Missão Genesis do DOE para ciência orientada por IA

A Missão Genesis do Departamento de Energia cresceu para um esforço genuinamente multiagências. Vinte departamentos e agências federais agora participam, com representantes do NIH, NASA, NSF e outros apresentando objetivos compartilhados na Cúpula da Missão Genesis desta semana. Os primeiros prêmios já começaram a fluir para equipes em laboratórios nacionais e universidades.

O que torna isso digno de atenção é o ângulo de acesso. Agora, um cientista procurando computação de IA tipicamente compete por bolsas de uma agência — NSF, DOE, NIH — e trabalha dentro das regras de dados e cronogramas de revisão dessa agência. Um programa de IA de todo o governo promete algo diferente: recursos computacionais agrupados em laboratórios nacionais, acesso compartilhado a conjuntos de dados científicos que costumavam ficar em silos separados e caminhos de financiamento que podem atravessar limites de agências. Para equipes construindo ferramentas de IA para genômica, modelagem climática, ciência de materiais ou astronomia, isso poderia significar caminhos mais rápidos do protótipo ao experimento em escala.

Também levanta questões reais de governança. Quando vinte agências compartilham modelos, dados e prioridades, alguém tem que decidir quais questões de pesquisa vêm primeiro, como funciona a atribuição quando vários departamentos financiam um único modelo, e o que acontece quando a missão de uma agência conflita com a de outra. A cúpula trouxe essas tensões à tona sem resolvê-las. Observe a próxima rodada de prêmios para ver quem realmente é financiado entre linhas de agências, não apenas dentro de um único departamento.

[17:22] Anthropic Traça uma Linha na Fronteira dos Pesos Abertos

A Anthropic publicou esta semana uma página oficial de posicionamento delineando sua posição sobre modelos de IA de pesos abertos — as versões que fornecem seus parâmetros treinados para que qualquer pessoa possa baixar e executar. O CEO Dario Amodei deixou claro que não é contra os pesos abertos como categoria. Sua preocupação está na ponta da fronteira: os lançamentos mais capazes, em sua visão, poderiam fortalecer o desenvolvimento de IA chinês e desequilibrar o balanço competitivo entre EUA e China.

A página lê-se menos como uma atualização de produto e mais como uma contribuição para uma conversa política. A Anthropic nomeia o que os lançamentos abertos realmente proporcionam: pesquisadores independentes examinando o comportamento dos modelos, startups construindo sobre pesos públicos, e desenvolvedores de implantação local executando modelos em seu próprio hardware. Junto desses benefícios, a empresa destaca a questão não resolvida com a qual todos os laboratórios de fronteira estão lidando — onde traçar a linha entre abertura útil e risco de proliferação em nível de pesos.

Essa distinção importa porque a manchete pode facilmente ser lida como uma proibição. Não é. Amodei está pedindo por limites de lançamento escalonados e baseados em tiers, em vez de restringir pesos abertos em todo o espectro. O posicionamento é um comentário da indústria, não uma nova lei. Os controles reais sobre o que os desenvolvedores podem implantar permanecem como controles de exportação no compute circundante, restrições de hospedagem específicas por jurisdição, e os termos de licenciamento anexados a cada lançamento de modelo.

Para quem escolhe modelos abertos hoje, o mapa prático não mudou. Termos de licença, onde você hospeda, e quaisquer regras de exportação sobre hardware ou compute ainda determinam o que você pode implantar. O que mudou esta semana é que um grande laboratório de fronteira agora tem uma posição registrada por escrito, aguçando um debate que até agora vivia principalmente em briefs de think tanks e audiências governamentais.

[19:02] Caso de Scraping do Google Contra SerpApi Decidido por Falta de Legitimidade, Não por Mérito

O processo do Google contra SerpApi, o serviço de scraping que permite desenvolvedores extraírem resultados de busca estruturados, foi encerrado em 20 de julho. Mas o tribunal não decidiu que scraping é legal. Decidiu que o Google não podia apresentar esta alegação específica sob este estatuto específico. O motivo é a legitimidade do DMCA. Para processar sob as disposições anti-circumvenção que o Google invocou, um reclamante precisa ser proprietário de direitos autorais, licenciador exclusivo, ou agente autorizado do material em questão. O tribunal concluiu que o Google não estabeleceu esse papel.

Isso é uma derrota processual, não uma derrota substancial. A decisão não diz aos scrapers que eles estão livres para extrair qualquer página que quiserem. O Reddit entrou com um processo similar contra SerpApi, e截至as reportagens de 27 de julho citadas, aquele processo ainda estava pendente. Portanto, a questão subjacente de se extrair resultados públicos da web viola o DMCA permanece genuinamente não resolvida.

O que ficou mais claro é quantos portões legais diferentes um scraper pode encontrar. Robots.txt é um sinal de preferência de rastreador, um pedido educado que rastreadores compatíveis respeitam, não um bloqueio técnico e não automaticamente uma lei vinculante. Além disso, contratos (termos de serviço), controles de acesso técnico (limites de taxa, paredes de autenticação), propriedade de direitos autorais da saída específica, e legitimidade do DMCA são questões separadas. Um scraper que respeita robots.txt ainda pode perder em uma alegação contratual, e uma plataforma que perde na legitimidade do DMCA ainda pode vencer em teoria contratual ou de trespass.

Para pessoas construindo camadas de recuperação de busca, conjuntos de dados de treinamento de IA, ou ferramentas de inteligência competitiva, o quadro prático permanece inalterado: cautela. A manchete lendo "tribunal aprova scraping" está errada, e também está "scraping está morto." O que é verdade é que a questão está se movendo pelos tribunais lentamente, em trilhas processuais, e ninguém tem uma resposta definitiva ainda.

[20:51] ChatGPT Permite Trabalhadores Cruzarem Limites de Função, Descobre OpenAI

A OpenAI lançou uma peça de pesquisa em 28 de julho que inverte a pergunta usual "IA substitui empregos". Em vez de perguntar quais funções serão automatizadas, a equipe perguntou o que as pessoas estão realmente fazendo com o ChatGPT no trabalho. A descoberta principal: trabalhadores regularmente ultrapassam suas descrições formais de cargo. A mesma pessoa redige, analisa, programa e se comunica em áreas que antes exigiam um especialista diferente na equipe.

O exemplo prático que a OpenAI destaca é uma pequena equipe de marketing onde uma pessoa cuida de textos, análise básica de dados, scripting leve e e-mails para clientes em uma única tarde, com o ChatGPT suavizando as costuras entre essas tarefas. Nenhuma dessas é a função oficial dessa pessoa, ainda assim o trabalho é feito.

Por que importa agora: muito da narrativa de produtividade para IA tem sido sobre automação substituindo uma tarefa. Este estudo recategoriza como expansão. Um trabalhador pode cobrir mais terreno, o que muda como pequenas equipes dividem o trabalho, o que é contratado, e onde os gerentes passam seu tempo de revisão. Para desenvolvedores, o padrão de cruzamento de funções é um sinal para projetar ferramentas e prompts que suportem múltiplos tipos de tarefa em uma sessão, em vez de forçar o usuário a pular entre aplicativos especializados.

A OpenAI é a publicadora e financiadora, o que vale a pena manter em mente. A pesquisa descreve comportamento observado, não ganhos de qualidade medidos, e explicitamente não afirma que maior variedade de tarefas equivale a trabalho melhor ou menos empregos. O que ela sugere é que a pergunta para gerentes e desenvolvedores de ferramentas está mudando de "qual função esta ferramenta substitui" para "como reorganizamos quando uma pessoa pode fazer mais de forma crível."