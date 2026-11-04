Episódio 126 — 29 de outubro de 2026

[00:00] Gancho do episódio

O Google anunciou o Gemini 4 Carbon como seu modelo mais avançado, criado para fluxos de trabalho contínuos de engenharia de software e para todo o ciclo de defesa cibernética, e informou que o Carbon encontrou vulnerabilidades. A OpenAI publicou resultados de modelos relacionados à conjectura de Kakeya, à Hipótese do Tempo Exponencial e à cromodinâmica quântica, expandindo seu trabalho em matemática e física. Segundo um estudo de caso da OpenAI publicado em 27 de outubro, os agentes de voz da Retell,.baseados em modelos da OpenAI, agora atendem a 100 milhões de chamadas por mês, com o GPT-6 Astra liderando o benchmark de agentes de voz da empresa. Os engenheiros da Anthropic Katelyn Lesse e Angela Jiang explicaram como a equipe da Claude Platform lançou o Opus 5.5 e opera agentes gerenciados separando a tomada de decisões do modelo de suas ações externas. Os desenvolvedores de hardware também receberam novas opções de IA local: a placa de trabalho compacta Radeon AI Pro R9700 da ASRock combina 32 GB de GDDR6 com 640 GB/s de largura de banda e suporte a FP8 da RDNA 4, enquanto a NVIDIA publicou o Nemotron-3.5-Bolt-E4B-4GB, um modelo quantizado de 8 bilhões de parâmetros e 4 GB, projetado para assistentes de voz locais, personas interativas e interfaces embarcadas.

[02:00] Gemini 4 Carbon visa à engenharia de longa duração e à defesa cibernética

O Google anunciou o Gemini 4 Carbon como seu próximo modelo de fronteira. De acordo com o Google, o Carbon pode funcionar por dias, persistir diante de becos sem saída, identificar as causas raiz de bugs sutis em grandes bases de código e produzir correções. Os resultados cibernéticos abrangem três etapas: encontrar vulnerabilidades, verificar se elas podem ser exploradas e corrigir a causa subjacente. O Google relata que o Carbon obtive 88,2% no SEC-bench Pro para descoberta de vulnerabilidades, 54,8% no ExploitGym para exploração e 71,0% no CWE-bench da Collinear para geração de correções de código. A publisher relata que, nos benchmarks internos do Google, o Carbon mais que dobrou a taxa de sucesso do Argon na geração de código seguro. Inicialmente, o Carbon estará disponível para um subconjunto de especialistas em defesa cibernética, com o acesso sendo ampliado gradualmente a parceiros de confiança por meio do Fairwind Program. Desenvolvedores, empresas e consumidores poderão acessar o modelo mais adiante. O preço inicial será de US$ 2 por milhão de tokens de entrada e US$ 10 por milhão de tokens de saída, com 95% de desconto para entradas em cache; depois, as taxas serão de US$ 4 e US$ 20. O próximo marco a observar é como os primeiros especialistas utilizarão o Carbon e se o acesso será ampliado. O Google afirma que o Carbon foi criado para fluxos de trabalho agentivos contínuos e pode funcionar por dias enquanto pursue tarefas complexas de engenharia com várias etapas.

[02:32] OpenAI compartilha resultados de modelos sobre três problemas científicos

A OpenAI compartilhou resultados de modelos relacionados à conjectura de Kakeya, à Hipótese do Tempo Exponencial e à cromodinâmica quântica, além de uma explicação sobre como pesquisadores acadêmicos podem verificar o trabalho e avançar a partir dele.

O resultado útil é o acesso a resultados produzidos por modelos em matemática, ciência da computação e física. Pesquisadores podem examinar o trabalho e desenvolver novasbeiten a partir dele, transformando a saída dos modelos em material para investigação científica, em vez de deixá-la como produto final.

A OpenAI está posicionando as comunidades acadêmicas como participantes ativas na verificação e no avanço dos resultados. O próximo teste é se esses pesquisadores conseguirão verificar o trabalho e convertê-lo em progresso científico adicional.

[03:11] Agentes de voz da Retell baseados em modelos da OpenAI chegam a 100 milhões de chamadas mensais

Em 27 de outubro, a OpenAI publicou um estudo de caso mostrando que a Retell está usando modelos da OpenAI para operar uma plataforma de agentes de voz que processa 100 milhões de chamadas por mês. A Retell relata que o GPT-6 Astra liderou seu benchmark de agentes de voz, enquanto o Codex ajudou a empresa a alcançar uma receita anualizada de US$ 1,6 milhão por funcionário.

O exemplo prático é um sistema de agentes de voz em escala de produção, e não uma pequena demonstração. O GPT-6 Astra lidera o benchmark da Retell, e a implantação processa volume mensal suficiente para que 100 milhões de chamadas representem uma métrica operacional relevante. O indicador de receita por funcionário acrescenta um sinal de negócio ao resultado de desempenho dos modelos.

Para quem está desenvolvendo agentes de voz, esse caso oferece uma referência concreta sobre a escala e os resultados associados a uma implantação baseada em modelos da OpenAI. O volume de chamadas e a receita por funcionário são os dois indicadores a acompanhar à medida que a Retell amplia o uso dos modelos.

[04:02] Anthropic separa o modelo das ações do agente

A equipe de plataforma da Anthropic tem uma maneira concreta de tornar os agentes mais controláveis: manter separado o modelo que realiza o raciocínio do sistema que executa as ações. Em uma entrevista ao Latent Space em 27 de outubro, Katelyn Lesse e Angela Jiang descreveram o lançamento do Opus 5.5 e a ampliação da Claude Platform por meio de agentes gerenciados, cujo cérebro, harness e sandbox são desacoplados. A camada de execução é contida por meio de isolamento, proteções de credenciais e controles de rede, enquanto os harnesses de longa duração são projetados para manter o progresso entre diferentes janelas de contexto.

Para os desenvolvedores, isso sustenta uma arquitetura de agentes capazes de continuar trabalhando sem conceder ao modelo de raciocínio controle irrestrito sobre ferramentas ou credenciais. A conversa também diferencia incidentes de treinamento das salvaguardas de produção e aborda classificadores de segurança e roteamento de modelos como parte da operação da plataforma.

Uma questão importante para as equipes que adotam esse padrão é se seus mecanismos de contenção e preservação do progresso continuam confiáveis à medida que as cargas de trabalho dos agentes se prolongam.

[04:57] Radeon AI Pro R9700 da ASRock visa à inferência em estações de trabalho locais

A ASRock está levando a plataforma de estações de trabalho da AMD com RDNA 4 aos desenvolvedores de IA local com a Creator Radeon AI Pro R9700. A placa combina 32 GB de memória GDDR6 com 640 GB/s de largura de banda e suporte a operações matriciais em FP8, um formato de menor precisão que comporta mais parâmetros de modelo dentro de um orçamento fixo de memória.

No centro está o processador Navi 48 da AMD, com 64 unidades de computação, 128 núcleos aceleradores de IA e clock máximo de 2,92 GHz. A ASRock estima uma vazão de matrizes densas em FP8 de 382,7 TFLOPS, o dobro desse valor ao usar sparsity. Modelos em FP6 e FP4 são processados em FP8, e não em seus formatos nativos. Um exemplo prático é um modelo de aproximadamente 30 bilhões de parâmetros funcionando com alguma VRAM sobrando.

O design，强调 o uso em estações de trabalho. É um blower com dois slots, com dimensões de 271 por 111 por 39 milímetros, e até quatro placas podem ser instaladas em um sistema ATX padrão. Usuários de Linux podem ativar manualmente o soft ECC para maior confiabilidade. A placa consome 300 watts, consumo que a análise descreve como administrável para um design do tipo blower.

A capacidade de memória é a principal limitação. A R9700 tem 32GB, menos que os 48GB da Radeon Pro W7900 da geração anterior. A próxima questão é como as melhorias de computação da RDNA 4 se traduzem em vazão prática de inferência e eficiência dentro desse orçamento de memória menor.

[06:16] O modelo Bolt de 4GB da NVIDIA visa a agent stacks locais

A NVIDIA publicou o NVIDIA-Nemotron-3.5-Bolt-E4B-4GB, um modelo de texto quantizado voltado a assistentes locais de voz e dispositivos, personas interativas e interfaces embarcadas. Segundo a NVIDIA, o modelo passou por um pós-treinamento adicional a partir do Gemma-4-E4B-it e foi projetado para funcionar com pouca memória e baixo tempo até o primeiro token. O modelo de texto tem 8B parâmetros, dos quais 4B são efetivos, utiliza precisão Q4_K_M, aceita entradas e saídas de até 64K tokens e oferece controles de raciocínio, modo conversacional e chamadas de ferramentas. Seus controles incluem pensamento ativado ou desativado, um orçamento de tempo de pensamento em execução e um modo conversacional que gera respostas mais concisas. Ele oferece suporte a chamadas de ferramentas no estilo de funções, incluindo um padrão documentado para confirmar um resultado de ferramenta pendente e retomar a conversa quando o resultado chega. A NVIDIA fornece instruções de download e de servidor llama.cpp, além de um drafter DFlash complementar para speculative decoding. A tabela própria de avaliação da NVIDIA em Q4_K_M registra uma pontuação de 55,60 no MultiChallenge para esse modelo, contra 39,36 do Gemma4 E4B-it, e informa que as medições foram realizadas com um harness consistente da NVIDIA. O model card afirma que o modelo está pronto para uso comercial ou não comercial e fornece comandos de download e de served por meio do llama.cpp. O model card alerta que alocações restritas de tokens podem truncar processos de pensamento no meio de uma frase, portanto continua sendo necessária uma avaliação específica para cada tarefa. A NVIDIA publicou o NVIDIA-Nemotron-3.5-Bolt-E4B-4GB como um modelo geralmente disponível em 23 de outubro de 2026. A publicadora relata que, nas avaliações Q4_K_M da NVIDIA, o Nemotron-3.5-Bolt-E4B-4GB obtive 55,60 pontos no MultiChallenge, comparado a 39,36 do Gemma4 E4B-it.

[07:39] Investimentos nos EUA aumentam a capacidade de chips e criam um campo de testes para armas autônomas

A Casa Branca detalhou um conjunto de investimentos industriais com implicações diretas para chips, hardware de computação e sistemas autônomos. A Carolina do Norte receberá até US$ 1,5 bilhão para expandir a produção de semicondutores, enquanto a Sibelco está ampliando, no condado de Mitchell, a produção de quartzo de alta pureza e materiais relacionados indispensáveis aos semicondutores.

O governo também está recorrendo ao Defense Production Act para liberar US$ 150 milhões para ampliar a capacidade de refino nos EUA, com o objetivo de aumentar a produção doméstica de diesel e gasolina. Em Montana, o Department of War está estabelecendo um novo campo para testar armas e tecnologias avançadas, incluindo armas autônomas e capacidades de guerra espacial e eletrônica.

Para quem desenvolve soluções, o investimento em semicondutores é um sinal concreto no upstream: mais capacidade planejada para chips e materiais essenciais pode apoiar uma base de hardware doméstica maior. O campo em Montana cria um espaço dedicado à avaliação de sistemas autônomos e de guerra eletrônica.

Um ponto a acompanhar é a rapidez com que os investimentos anunciados se transformarão em instalações operacionais na escala descrita.

[08:38] Resumo de pesquisas: a memória de grupo pode distorcer as evidências que preserva

Um grupo de modelos de linguagem pode perder a substância da própria discussão quando um modelo comprime o intercâmbio em uma memória curta. Duas regras tentadoras falham de maneiras diferentes. Selecionar as alegações mais raras às vezes funciona, mas, em média, não é melhor do que escolher ao acaso. Selecionar alegações que parecem relevantes para a decisão pode ser ainda pior, porque iscas plausíveis também tratam do assunto. O responsável final pela decisão acrescenta outra distorção: a prova social, ou seja, dar mais peso a um fato porque muitos agentes são creditados como seus autores. Remover ou reatribuir aleatoriamente essas atribuições, sem alterar a ordem da discussão, melhora a precisão. A transcrição completa também pode obter uma pontuação inferior à de não fazer anotações, o que mostra que a compressão não é automaticamente o problema; importa como as evidências são preservadas e enquadradas. Para um fluxo de trabalho que converte as pesquisas de um painel em uma única recomendação, a consequência prática é examinar o equilíbrio entre evidências que apoiam a decisão e evidências que a desviam na memória resultante, em vez de tratar um resumo conciso como um registro neutro.

[09:43] Anthropic treinou Claude com livros obtidos ilicitamente de professores de Stanford

Anthropic treinou Claude illegalmente com livros de professores de Stanford Anthropic treinou Claude illegalmente com livros de professores de Stanford Anthropic treinou Claude illegalmente com livros de professores de Stanford (Foto: JACK BERNARDO/The Stanford Daily) Publicado em 27 de out. de 2026, 2:46, atualizado pela última vez em 27 de out. de 2026, 3:19. Uma juíza federal decidiu, em maio de 2026, que a Anthropic raspar e pirateou illegalmente obras de mais de 10 professores de Stanford para treinar seus modelos Claude. Anteriormente, a Anthropic treinou Claude com textos obtidos ilicitamente dos professores Tobias Wolff, Abraham Verghese, Chang-Rae Lee, Daniel Mason, Hayagreeva Rao e Myra Strober. Em Bartz v. O mecanismo é um limite legal ou de política, não uma mudança na API. Os fatos com fonte definem o que foi proposto, decidido ou declarado, sem transformar isso em uma lei universal. Quem desenvolve produtos deve acompanhar a regra, a decisão judicial ou a mudança concreta no acesso e evitar alterar um produto com base apenas em uma manchete.

[10:37] Resumo de pesquisas: EnvSched busca execuções de treinamento de agentes mais úteis

O treinamento de um agente de linguagem pode se tornar caro rapidamente, porque cada execução de treinamento, ou rollout, pode envolver ferramentas, estados, transições e verificações de sucesso diferentes. EnvSched é um agendador de pesquisas projetado para tornar mais úteis um conjunto limitado dessas execuções.

O principal achado do artigo é que agendar tarefas junto com seus ambientes pode melhorar as informações contidas em cada lote de treinamento. EnvSched aprende com o histórico de rollouts, prioriza tarefas provavelmente reveladoras de diferenças significativa de recompensa e distribui o trabalho entre ambientes e padrões de interação que receberam menos atenção.

Para isso, ele organiza pares de tarefa e ambiente em um grafo. As conexões registram relaciones dentro de um ambiente, como ferramentas compartilhadas e estruturas de verificação, ou semelhanças mais amplas na execução e nas recompensas. Informações históricas de rollout são usadas para estimar quanto variar cada tarefa provavelmente produzirá. Cotas por ambiente e uma penalidade por similaridade limitam então a repetição.

A consequência prática é direta: com um orçamento de treinamento fixo, uma equipe de agentes pode concentrar as execuções onde é mais provável distinguir o bom comportamento do mau, em vez de gastar parte excessiva do orçamento com experiências redundantes.

[11:45] Greptile usa GPT-6 Astra para testar fluxos de trabalho de software

A Greptile está expandindo a detecção de bugs para além da revisão de código com o GPT-6 Astra. A empresa está usando o Astra para testar fluxos de trabalho de usuários, dando ao seu produto de revisão uma forma de examinar como um aplicativo se comporta em uso, em vez de se concentrar apenas no código proposto.

A Greptile também está usando o Daybreak para fortalecer a segurança. Isso acrescenta uma dimensão focada em segurança à mesma abordagem orientada por fluxos de trabalho, com o objetivo de ajudar equipes a identificar falhas além do ponto em que um desenvolvedor ou revisor poderia perceber manualmente.

O anúncio também destaca o papel do Codex na redução de retrabalho. Ao incorporar assistência de código ao processo, a Greptile está abordando trabalhos que, de outro modo, talvez precisem ser repetidos depois que problemas são encontrados.

O resultado prático é um fluxo de trabalho mais amplo de verificação de qualidade: o Astra testa o comportamento voltado ao usuário, o Daybreak oferece suporte à segurança e o Codex ajuda a limitar o trabalho corretivo. Para quem desenvolve, o próximo sinal a observar é o grau em que essas capacidades reduzem a depuração repetitiva e o retrabalho em aplicações reais.

[12:43] CodeRabbit usa GPT-6.1 Sol para revisar a segurança de bases de código

A CodeRabbit está usando o GPT-6.1 Sol para investigar riscos de segurança em bases de código complexas. Seu agente de segurança ajuda desenvolvedores a revisar constatações e correções propostas, conectando a investigação automatizada à avaliação humana de possíveis vulnerabilidades e remediações.

A mudança prática é que o modelo está sendo aplicado dentro de um fluxo de trabalho de segurança de bases de código. A CodeRabbit pode investigar riscos e apresentar correções propostas, enquanto os desenvolvedores revisam os resultados antes de decidir o que alterar.

Para quem desenvolve, o padrão é claro: combine a investigação de segurança em toda a base de código com a proposição de correções e mantenha o desenvolvedor responsável por revisar ambos. A evidência a observar é quão consistentes são as constatações e correções propostas pelo agente em revisões reais de segurança.

[13:23] Hermit ensina agentes de IA sem substituir seu núcleo

A Infini-AI-Lab lançou o Hermit, um framework adaptador de código aberto, sob a licença Apache-2.0, para agentes de IA. Sua ideia central é simples: em vez de alterar o modelo ou o harness que executa o agente, o Hermit treina uma camada externa com base no feedback de tarefas concluídas.

Essa camada contém instruções, habilidades, memória e ferramentas. Portanto, quem desenvolve pode melhorar o comportamento de um agente ensinando-o por meio do feedback das tarefas, sem alterar o modelo subjacente nem o harness.

Essa separação é importante para equipes que já possuem um ambiente de agente que não querem substituir. Elas podem trabalhar nas instruções do agente, no conhecimento retido e no comportamento das ferramentas por meio do adaptador, em vez de modificar o próprio modelo.

O principal aspecto a observar é se o Hermit consegue continuar melhorando essa camada externa a partir do feedback das tarefas sem exigir alterações no modelo principal do agente ou no harness.

[14:14] Legora incorpora agentes à análise de contratos jurídicos

A Legora está desenvolvendo um sistema operacional agêntico para o trabalho jurídico. Em um perfil publicado pela OpenAI, a empresa afirma que usa modelos da OpenAI, ChatGPT e Codex para acelerar fluxos de trabalho jurídicos e ampliar a análise de contratos.

O impacto imediato é uma maior capacidade de execução de trabalho jurídico, com a análise de contratos oferecendo um exemplo concreto de onde a IA pode assumir um volume maior de tarefas. O objetivo declarado pela Legora é liberar os advogados para se concentrarem em atividades de maior valor, em vez de gastarem seu tempo com análises rotineiras.

A próxima evidência relevante é até onde a análise de contratos se expande na prática e como isso altera a distribuição do tempo dos advogados. Para quem desenvolve, a Legora demonstra que modelos, ferramentas conversacionais e agentes de programação podem ser combinados em torno de um fluxo de trabalho profissional, em vez de serem implantados como recursos isolados.