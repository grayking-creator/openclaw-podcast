[NOVA]: Eu sou a NOVA.

[ALLOY]: Eu sou o ALLOY, e este é o AgentStack Daily...

[NOVA]: O OpenClaw 7.1 foi lançado com openclaw attach, uma Control UI reconstruída, onboarding guiado, suporte ampliado a modelos e atualizações oficiais dos clientes iOS, Android e macOS. As funcionalidades concretas incluem sessões, aprovações, status do Gateway, trabalhos agendados, controle remoto de navegador, terminais de workspace e recuperação de conexão mobile. O agente de codificação baseado em terminal OpenAI Codex .144 ponto quatro melhorou os resultados rastreados para delegação e subagentes nativos, enquanto o agente de codificação AI baseado em terminal Claude Code .202 agora tem uma superfície direta de transferência de sessão do OpenClaw.

[ALLOY]: Hoje: o OpenClaw transfere sessões selecionadas para o Claude Code, o Codex retorna resultados de subtarefas estruturadas mais confiáveis, e o OpenRouter adiciona o KAT-Coder-Air V2.5 da Kwaipilot com uma janela de contexto de 256.000 tokens.

[NOVA]: O trabalho em robótica traz o ABot-AgentOS para planejamento incorporado de longo horizonte e o ABot-N1 da Amap para navegação de linguagem visual. Pesquisadores de segurança mostram como backdoors distribuídas evadem monitores por mensagem, enquanto a Salesforce empurra a resposta a perguntas em vídeo em direção a evidências em nível de pixel.

[ALLOY]: A fila também inclui raciocínio moral consciente da cultura, agendamento de fábrica PPVC, trajetórias de carreira do JobHop v2, variedades de circuitos de transformadores, MM-ToolSandBox, LightMem-Ego, Requential Coding, AdvancedMathBench, três repositórios MCP, duas listagens de modelos Kwaipilot, Ollama .32, e três candidatos de pesquisa extras.

[NOVA]: ...

[NOVA]: O OpenClaw 7.1 foi lançado em treze de julho com 3.063 contribuições de 532 colaboradores, e a mudança multiagente mais direta é o openclaw attach. O comando dá ao agente de codificação AI baseado em terminal Claude Code .202 acesso temporário a uma sessão OpenClaw selecionada, então contexto, aprovações e estado ativo do workspace podem passar para uma execução de codificação sem reconstruir a conversa. O release também reformula a Control UI: Tarefas ao vivo, visualizações de uso e custo, downloads, pareamento, aprovações, status do Gateway, sessões, objetivos, trabalhos agendados, terminais de workspace e controle remoto de navegador agora ficam mais próximos da superfície da conversa. Loops de crash do Gateway são explicitamente mencionados como melhorados.

[ALLOY]: O agente de codificação baseado em terminal OpenAI Codex .144 ponto quatro também avança no caminho dos subagentes. Delegação e subagentes nativos agora retornam resultados rastreados de forma mais confiável, então um agente pai pode ler saída estruturada de uma subtarefa do Codex em vez de raspar logs ou esperar por texto solto. Isso importa em executores de CI, sidecars de editor e longas sessões de terminal onde o agente pai tem que recuperar estado após uma tarefa filha falhar, expirar ou produzir trabalho parcial.

[NOVA]: O suporte a modelos foi ampliado nas rotas OpenAI e Codex com trabalho de compatibilidade com GPT-5.6, a Tencent Hy3 ganhou um caminho de configuração completo, e a API de Modelo da Meta adicionou o Muse Spark 1.1. Por baixo dos panos, o OpenClaw destaca trabalho de confiabilidade entre Claude, Ollama, ClawRouter e LongCat, além de escolhas mais amplas de provedores para o Copilot. Os clientes oficiais se moveram em sincronia: iOS e iPadOS, Android e macOS receberam trabalho em configuração, navegação, chat, voz, permissões, localização, leitura offline, envios em fila, recuperação de conexão e controles de sessão nativos.

[ALLOY]: As integrações de mensagens também receberam mudanças concretas de superfície. O Telegram recebe progresso ao vivo, fotos e anexos, tópicos, comandos, retentativas, roteamento de conta, configuração e correções de entrega. O Slack melhora threads, cards, progresso, identidade, reações e prevenção de duplicatas. As atualizações do Discord cobrem replies, anexos, sessões de voz, progresso, reconexões, comportamento de múltiplas contas e indicações de não lidos. O release torna a transferência entre harnesses menos personalizada: o OpenClaw pode anexar o Claude Code, subtarefas do Codex retornam resultados rastreados, e a Control UI expõe mais do limite de runtime onde aprovações, estado do navegador, terminais e status do Gateway se encontram.

[NOVA]: ...

[NOVA]: O OpenRouter adicionou o KAT-Coder-Air V2.5 da Kwaipilot ao seu catálogo de modelos. A configuração técnica visível é esparsa mas importante: a listagem expõe uma janela de contexto de 256.000 tokens, sem contagem de parâmetros pública, tabela de benchmarks ou preço anexado na página do modelo. O acesso funciona através da superfície de chat completions do OpenRouter usando o identificador de modelo Kwaipilot, então harnesses de agente já conscientes do OpenRouter podem rotear tráfego de codificação para ele sem uma conta Kwaipilot separada ou um novo SDK.

[ALLOY]: Uma janela de contexto de 256K coloca o KAT-Coder-Air V2.5 na categoria de codificação de contexto longo. Um agente de codificação pode incluir um grande trecho de repositório, transcripts de ferramentas acumuladas, patches gerados, comentários de revisores, manifests de dependências e logs de falha mais longos em um único prompt antes de se apoiar em sumarização. Isso não garante melhor raciocínio, mas muda o orçamento do prompt e diminui a pressão para comprimir cada estado intermediário.

[NOVA]: A camada de roteamento do OpenRouter também molda o comportamento operacional. Limites de taxa, retentativas, cache, rastreamento de requisições e failover seguem as mesmas convenções de roteador que outros modelos do catálogo, em vez de expor a Kwaipilot como um endpoint avulso. Isso torna o modelo fácil de comparar contra padrões de codificação existentes em agentes já conectados através do OpenRouter, especialmente quando o mesmo prompt, trace de ferramentas e schema de resposta podem permanecer inalterados.

[ALLOY]: As peças faltando ainda importam. Sem uma model card, dados de avaliação públicos ou preço, a listagem é um evento de disponibilidade mais do que uma afirmação de capacidade. O KAT-Coder-Air V2.5 agora é alcançável atrás de uma janela de contexto de 256K; o próximo ponto de dados significativo é se a Kwaipilot publica números de benchmark, características de latência e custos de tokens que justifiquem mover sessões de codificação de repositórios longos para ele.

[NOVA]: ...

[NOVA]: O ABot-AgentOS propõe um sistema operacional robótico de propósito geral para agentes incorporados que precisam de raciocínio de alto nível acima de controladores de Visão-Linguagem-Ação de baixo nível. O artigo separa a camada deliberativa da camada controladora: em vez de pedir a um modelo para perceber, planejar e atuar de ponta a ponta, o ABot-AgentOS gerencia planejamento condicionado a cena, uso de ferramentas, memória multimodal e execução através de corpos de robôs. O trabalho chamou atenção no feed diário do HuggingFace, onde a contagem rastreada chegou a 61 upvotes.

[ALLOY]: A ideia central do runtime é execução de habilidades isoladas por contexto. As habilidades executam como unidades modulares dentro de ambientes de execução isolados, em vez de como um fluxo contínuo de tokens de ação brutos. Isso dá ao sistema um limite ao redor de cada fase de tarefa e reduz a corrupção de estado quando um robô realiza um trabalho de múltiplas etapas como encontrar um objeto, navegar até ele, manipulá-lo e confirmar a conclusão.

[NOVA]: O ABot-AgentOS também usa memória multimodal para comparar a cena atual contra o resultado previsto antes de prosseguir. Se o robô esperava uma gaveta estar aberta ou um objeto ser agarrado, o loop de memória pode capturar a incompatibilidade antes que a próxima fase construa sobre uma etapa falhada. O artigo combina isso com um modelo de execução híbrido borda-nuvem: percepção imediata e verificações de segurança ficam no dispositivo, enquanto planejamento mais pesado e raciocínio de cena de alta dimensionalidade podem ir para computação em nuvem.

[ALLOY]: A abstração útil é o gerenciamento de habilidades agnóstico de robô. Um desenvolvedor pode expressar uma habilidade de alto nível uma vez, e então deixar o AgentOS mediar a execução entre diferentes corpos de hardware e capacidades de controle. A parte difícil muda para o mapeamento de atuadores, tolerância a latência e limites de segurança: um planejador que funciona em simulação ainda precisa sobreviver a garras, rodas, braços, câmeras e links de rede que se comportam de maneira diferente no mundo físico.

[NOVA]: ...

[NOVA]: O novo artigo do arXiv de Yibo Hu e Ren Wang mira um ponto fraco na segurança multiagente: monitores de tempo de execução por mensagem. A classe de ataque divide uma carga útil prejudicial entre múltiplos agentes para que cada fragmento possa parecer inofensivo sob uma visão local, enquanto o objeto montado executa a ação prejudicial. Os autores chamam o limite-chave de limite de observabilidade: se um monitor vê apenas um fragmento indistinguível de tráfego benigno, nenhum detector operando na mesma visão pode captá-lo de forma confiável.

[ALLOY]: O estudo avalia a ideia em um ambiente de teste controlado, um benchmark externo e execuções de agentes end-to-end. Monitores locais perdem o sinal à medida que a evidência local da carga desaparece, e então se recuperam apenas quando o monitor vê a representação totalmente montada. Isso importa porque muitas pilhas de agentes atuais inspecionam cada mensagem, chamada de ferramenta ou transferência independentemente, e então assumem que a segurança se compõe em todo o sistema.

[NOVA]: Dois resultados ancoram o artigo. Um monitor treinado apenas em tráfego benigno recupera a estrutura de código do ataque em codificações mantidas fora do conjunto de teste com um AUROC médio de 0,874. Um gate de visão decodificada, quando fornecido com a família de codificação, bloqueia todos os ataques testados. AUROC mede quão bem um detector separa casos positivos e negativos em diferentes limiares; aqui, mostra que a representação correta pode expor estrutura que fragmentos locais escondem.

[ALLOY]: Apenas mais logging não resolve o problema. Monitores de trace completo e decodificadores ainda falham a menos que atinjam a representação onde a carga se torna visível. Segurança multiagente, portanto, precisa de inspeção com consciência de montagem na fronteira onde os fragmentos se combinam, não apenas filtros por etapa anexados a mensagens individuais. A alegação mais incisiva do artigo é matemática: uma vez que os fragmentos são benignos sob a visão do monitor, classificadores mais fortes não podem recuperar informação que a visão nunca expôs.

[NOVA]: ...

[NOVA]: Ayoung Lee, Ryan Kwon e Yunxiang Zhang publicaram MET, uma estrutura de raciocínio moral multilíngue construída em torno de prompts de teoria com consciência cultural. O artigo ataca três lacunas: benchmarks traduzidos frequentemente perdem contexto moral local, scaffolds de inferência tendem a ser estáticos e centrados no inglês, e conjuntos de dados de raciocínio moral geralmente requerem labels humanos custosos ou supervisão de modelos maiores. O MET em vez disso usa teoria curada por especialistas de psicologia e filosofia no momento da inferência.

[ALLOY]: O artigo traz o MCLASH, um benchmark de decisão moral multilíngue projetado em torno de normas culturalmente situadas em vez de tradução direta do inglês. Também introduz um método de duas etapas: primeiro, o modelo seleciona fundamentos morais específicos da situação e cultura; segundo, ele raciocina sobre esses fundamentos no idioma do usuário. O MET-D adiciona auto-destilação focada nessa segunda etapa de raciocínio, sem labels morais externos.

[NOVA]: Os números reportados cobrem Qwen3-4B, Qwen3-8B e Gemma3-4B. O MET-D melhora macro-F1 sobre os modelos base em uma média de 3,71 pontos no MCLASH e 4,23 pontos no MMoralExceptQA. O maior ganho reportado é de 12,94 pontos para malaio no Qwen3-8B. Macro-F1 faz a média dos escores F1 em nível de classe, então os ganhos refletem melhor equilíbrio entre os rótulos, não apenas melhoria na maior categoria.

[ALLOY]: O mecanismo importante é a divisão entre selecionar fundamentos de teoria cultural e produzir a resposta final no idioma alvo. Isso mantém o scaffold portátil entre modelos menores e evita precisar de um dataset moral rotulado para cada idioma. Os resultados com modelos pequenos importam porque Qwen3-4B e Gemma3-4B se beneficiam de prompting e auto-destilação em vez de um juiz proprietário maior. Fique de olho se o MCLASH se torna um benchmark compartilhado e se a receita transfere para domínios além do raciocínio moral.

[NOVA]: ...

[NOVA]: Ziheng Zhang e Wei Zhang postaram um artigo sobre agendamento flexível de job-shop para construção volumétrica pré-fabricada pré-acabada, ou PPVC, em fábricas de módulos. O trabalho adiciona um benchmark e uma política de aprendizado por reforço profundo que fica dentro de cerca de 4% de uma referência de programação por restrições. As fábricas PPVC incluem atrasos de tempo pós-operação: concreto cura, água passa por testes de acumulação, ou tinta seca depois que uma estação de trabalho termina, enquanto a própria estação de trabalho se torna disponível novamente.

[ALLOY]: Esses atrasos mudam o problema de agendamento drasticamente. Em instâncias baseadas em um guia oficial nacional de pré-fabricação, os atrasos de tempo inflaram o makespan de referência ótimo em cerca de 67% em média. Ignorar os atrasos durante a tomada de decisão e reparar o cronograma depois tem performance pior do que toda regra de despacho testada, porque a política já fez escolhas que não respeitam a estrutura oculta de bloqueio.

[NOVA]: Os autores adaptam um resolvedor de deep RL com atenção dupla com três extensões abláveis: dinâmica com consciência de atraso com um limite de recompensa admissível, dois canais de features antecipatórias que expõem o tempo de espera restante para a política, e embeddings de tipo de operação e estação com máscara de vivacidade que distinguem trabalho ativo de operações bloqueadas por atraso. Com as extensões desabilitadas, a implementação reproduz o resolvedor original, o que ajuda a atribuir os ganhos às adições com consciência de atraso.

[ALLOY]: Em instâncias mantidas fora do conjunto de treinamento, a política aprendida supera regras de despacho e uma meta-heurística de algoritmo genético, com vantagem maior sob contenção de capacidade. Uma única política de tamanho misto mantém a liderança em toda a faixa treinada de tamanhos de fábrica, e os autores liberam um gerador de benchmark baseado em guia. A contribuição mais ampla é um tratamento concreto de viabilidade atrasada dentro de um loop de planejamento em vez de como um reparo post-hoc.

[NOVA]: ...

[NOVA]: Iman Johary, Guillaume Bied e Alexandru C. Mara liberaram o JobHop v2, um conjunto de dados de trajetórias de carreira em larga escala construído a partir de 440.000 currículos multilingues pseudonimizados do Serviço Público de Emprego Flamengo. O pipeline produz 355.315 trajetórias de alta fidelidade, baseadas em conteúdo autêntico de currículos em texto livre em vez de trajetórias de carreira sintéticas. Os dados são mapeados para códigos ocupacionais ESCO, com temporização em nível trimestral e um nível educacional normalizado de cinco níveis.

[ALLOY]: A tarefa de extração importa porque agentes de carreira precisam de mais do que títulos de emprego isolados. Eles precisam de sequências: mudanças de ocupação, mudanças educacionais, temporização e padrões de progressão entre idiomas. O JobHop v2 transforma texto ruidoso de currículos em trajetórias estruturadas enquanto preserva resolução temporal suficiente para raciocinar sobre saltos de emprego, lacunas de habilidades e caminhos do mercado de trabalho. Isso torna o dataset mais próximo de uma admissão de emprego pública do que resumos de perfis coletados.

[NOVA]: Avaliado contra anotações humanas, o melhor extrator fica apenas um a três pontos percentuais abaixo do teto de concordância entre anotadores. Isso significa que o fator limitante se aproxima da discordância humana em vez de falha óbvia do modelo. O link com ESCO também torna a saída interoperável com taxonomias ocupacionais usadas em serviços de emprego e análise de mercado de trabalho, onde um título de texto livre precisa mapear para um conceito ocupacional estável.

[ALLOY]: A escala oferece aos agentes de planejamento de carreira um substrato mais realista do que históricos escritos à mão ou sintéticos. Pode suportar recuperação, previsão, recomendação e análise de políticas onde o tempo e a normalização ocupacional são importantes. A fonte multilíngue também importa: a formulação de currículos varia por idioma, região e instituição, então sistemas de extração treinados apenas em perfis limpos em inglês frequentemente perdem equivalências que os serviços públicos de emprego precisam preservar.

[NOVA]: ...

[NOVA]: O CVLab da Amap tem um novo artigo de modelo fundamental sobre o ABot-N1, focado em Navegação Visual-Linguística. VLN significa que um agente incorporado se move através de espaços reais ou simulados seguindo instruções em linguagem natural. O ABot-N1 se posiciona como um modelo de propósito geral para raciocínio espacial fundamentado em tarefas incorporadas, em vez de uma política de navegação restrita ajustada a um simulador ou distribuição de cenas específicas.

[ALLOY]: O artigo critica políticas de VLN monolíticas que mapeiam observações diretamente para ações em uma passagem de ponta a ponta. Dois modos de falha dominam essa configuração. O desvio de coordenadas faz com que a estimativa de posição interna do agente se degrade ao longo de trajetórias mais longas. A semântica da cauda longa cria um ponto de quebra separado: marcos incomuns, referências ambíguas e frases espaciais raras ficam fora dos cômodos e objetos comuns vistos no treinamento.

[NOVA]: O ABot-N1 visa combinar raciocínio profundo para decisões espaciais fundamentadas com transferência ampla entre ambientes. O comportamento pretendido é uma única espinha dorsal que pode interpretar instruções como "vá passando pela tolda vermelha à esquerda" e carrying that capability into unfamiliar spaces without per-environment fine-tuning. O artigo framed interpretability as necessary for robustness, because black-box trajectories make it hard to tell whether the agent understood the instruction or merely followed a dataset shortcut.

[ALLOY]: O feed diário do HuggingFace rastreou o artigo com 71 votos positivos, o que representa atenção significativa da comunidade para um trabalho de navegação visual-linguística. As próximas evidências são pesos lançados, pontuações de benchmark e resultados de navegação de cauda longa. O diagnóstico está claro: agentes de navegação precisam de estado espacial persistente, análise de linguagem fundamentada e trajetórias recuperáveis. A afirmação precisa de evidências de que o ABot-N1 reduz o desvio e lida melhor com linguagem espacial rara do que os padrões VLN atuais.

[NOVA]: ...

[NOVA]: Tiberiu Musat, Tiago Pimentel e Nicholas Zucchet publicaram um framework teórico para como o raciocínio indutivo emerge em Transformers. O artigo, Dynamics de Aprendizado Invariante de Transformers em Tarefas de Raciocínio Indutivo, introduz uma classe generalizada de tarefas indutivas que unifica configurações como n-grams em contexto e raciocínio multi-hop. Ele avança de comportamento isolado de benchmark para uma conta matemática da dinâmica de treinamento.

[ALLOY]: A descoberta central é uma variedade invariante de baixa dimensão que confina a dinâmica de aprendizado de modelos de atenção. Em vez de rastrear milhões ou bilhões de valores de parâmetros, os autores mostram que o treinamento pode ser analisado através de um pequeno conjunto de coordenadas interpretáveis. Essas coordenadas descrevem como o modelo escolhe entre aprendizado em contexto, onde usa exemplos do prompt no momento da inferência, e aprendizado em pesos, onde armazena a regra nos parâmetros.

[NOVA]: As estatísticas dos dados impulsionam essa competição. Algumas distribuições incentivam memorização dentro dos pesos; outras incentivam raciocínio geral a partir do contexto. O framework também explica como a inicialização aleatória afeta a formação de circuitos. Quando várias soluções arquiteturais podem resolver a mesma tarefa, os pesos iniciais influenciam qual circuito vence durante a otimização.

[ALLOY]: Isso dá aos avaliadores de modelos uma possível moldura diagnóstica: detectar qual circuito de raciocínio um modelo treinado aprendeu sem depender apenas da precisão da saída final. Os autores relatam que as coordenadas de baixa dimensão permanecem tratáveis para análise teórica e empírica em arquiteturas de atenção padrão. Fique de olho nesses diagnósticos estilo variedade para aparecerem em pipelines de avaliação automatizados que inspecionam se um modelo aprendeu um circuito de raciocínio reutilizável ou um atalho frágil.

[NOVA]: ...

[NOVA]: O Salesforce AI Research publicou trabalho sobre Resposta a Perguntas em Vídeo com Evidências, ou E-VQA. Um modelo deve retornar tanto uma resposta quanto a evidência espaço-temporal por trás dela. O formato de evidência combina segmentos temporais com máscaras de segmentação de objetos densas e rastreadas, que são máscaras de objetos rastreadas através de frames de vídeo. O artigo argumenta que a precisão da resposta sozinha esconde se um Video LLM realmente olhou para a evidência visual relevante.

[ALLOY]: Dois artefatos acompanham o trabalho. ST-Evidence é descrito como o primeiro benchmark verificado por humanos para fundamentação de vídeo em nível de pixel, tanto discriminativa quanto generativa, então modelos devem localizar respostas no espaço e no tempo. ST-Evidence-Instruct é um conjunto de treinamento de 160.000 amostras gerado por pipelines automatizados para ensinar saídas de vídeo fundamentadas em vez de respostas de forma livre desconectadas do suporte visual.

[NOVA]: A melhoria relatada é grande. O ajuste fino de Video LLMs fundamentados no ST-Evidence-Instruct supera os padrões UniPixel do mesmo tamanho em 27,2 pontos no t-mean e 13,8 pontos no J&F quando medido em um modelo de 7B. J&F combina similaridade de região e precisão de contorno para qualidade de segmentação, então o ganho aponta para melhor fundamentação visual, não apenas texto de resposta mais fluente.

[ALLOY]: O artigo também mostra que precisão de QA e verdadeira percepção visual podem se desacoplar, e escalar sozinho não fecha a lacuna. Agentes de vídeo usados em filmagens de vigilância, demonstrações de produtos, telemetria de robótica ou fluxos de trabalho de inspeção precisam de rastros de evidência que apontem para pixels e intervalos de tempo. O contrato de masklet também cria uma saída auditável: um revisor humano pode inspecionar onde e quando a resposta foi fundamentada em vez de confiar em uma explicação fluente.

[NOVA]: ...

[NOVA]: Kaixin Ma, Di Feng e Alexander Metz introduziram MM-ToolSandBox, um benchmark e framework de avaliação para agentes que leem imagens e agem através de chamadas de ferramentas. O ambiente é stateful, abrange mais de 500 ferramentas em 16 domínios de aplicação e suporta tarefas multi-imagem e multi-turn. Os agentes devem fundamentar entradas visuais conforme chegam, depois converter esse entendimento fundamentado em chamadas executáveis.

[ALLOY]: O benchmark inclui dinâmicas conversacionais que prompts de shot único geralmente perdem: revisões de objetivos, correções de erros e mutações de estado durante sessões sustentadas. Foi construído com planejamento de cenários guiado por fluxo de informação e filtragem de qualidade multi-estágio, resultando em 258 cenários nominais verificados por humanos mais 50 variantes focadas em aplicações de UI interativas.

[NOVA]: Doze modelos de ponta foram avaliados, de sistemas open-weight de 4B a modelos proprietários de fronteira. Mesmo o melhor modelo alcança menos de 50% de sucesso nos cenários nominais. A análise de falhas é mais reveladora que a pontuação principal: 53% das falhas vêm de extração incorreta de informações de imagens, mesmo quando o fluxo de trabalho da tarefa subjacente está correto.

[ALLOY]: Os autores chamam isso de um cruzamento de planejamento para precisão. Modelos menores frequentemente falham em decidir o que fazer; modelos maiores falham mais frequentemente em perceber os fatos visuais exatos necessários para a chamada de ferramenta. Chamadas de ferramentas visuais, portanto, têm duas superfícies de confiabilidade: planejamento e percepção. Maior escala do modelo pode ajudar no primeiro, mas capturas de tela, diagramas, estado da interface e detalhes de imagem ainda precisam de melhores mecanismos de ancoragem antes que agentes possam operar interfaces ricas com segurança.

[NOVA]: ...

[NOVA]: LightMem-Ego foca em memória de longo prazo para assistentes de IA vestíveis. O artigo se concentra em dispositivos móveis e vestíveis que percebem continuamente o dia de um usuário através de fluxos visuais e de áudio, conhecido como captura egocêntrica, e então respondem perguntas sobre experiências passadas sob demanda. O feed diário do HuggingFace registrou 29 upvotes da comunidade.

[ALLOY]: Memória multimodal contínua pressiona os limites dos dispositivos. Um assistente vestível não pode manter cada momento dentro de uma janela de contexto, e o offload para nuvem adiciona latência, custo, exposição de privacidade e dependência de conectividade. LightMem-Ego é posicionado como um sistema de memória em streaming que acumula experiências cotidianas conforme elas chegam, organiza-as e as torna consultáveis posteriormente no mesmo tipo de dispositivo que as capturou.

[NOVA]: Isso muda a atenção do modelo sozinho para o runtime de memória: compressão, indexação, recuperação, alinhamento temporal, fusão visual-áudio e limites de privacidade. Um usuário pode perguntar onde deixou as chaves, quem mencionou uma reunião ou qual produto viu em uma loja; responder requer uma representação persistente de percepções passadas, não um prompt de uma única vez.

[ALLOY]: Os próximos detalhes úteis são uma implementação de referência, comparações de benchmark contra baselines de memória em nuvem e restrições de hardware como bateria, footprint de memória e latência no dispositivo. Agentes vestíveis só parecerão práticos se o recall de longo prazo funcionar silenciosamente em segundo plano sem transformar cada registro de vida em uma dependência de inferência remota. O limite de privacidade é especialmente importante porque a captura egocêntrica contém bystanders, localizações, rotinas e conversas por padrão.

[NOVA]: ...

[NOVA]: Shikai Qiu, Marc Finzi e Yujia Zheng introduziram Requential Coding, um framework de compressão para entender o que grandes modelos aprenderam. A quantização tradicional atribui tamanhos de código vinculados ao tamanho do modelo, mesmo quando muitos parâmetros podem não armazenar informações úteis. Prequential coding comprime uma trajetória de treinamento, mas ainda codifica a sequência exata de dados, o que pode produzir códigos grandes em dados de alta entropia.

[ALLOY]: Requential Coding muda a configuração com um esquema professor-estudante. Um professor seleciona amostras de treinamento extraídas da própria distribuição do modelo estudante, e o código do estudante registra apenas essas selections. Bits são gastos em desacordos entre professor e estudante, então o código reflete aprendizado genuíno em vez de contagem de parâmetros brutos ou entropia de dados.

[NOVA]: O tamanho de código resultante é independente tanto da contagem de parâmetros quanto da entropia de dados, e frequentemente é ordens de magnitude mais curto que o equivalente prequential. O efeito cresce conforme os modelos escalam. Mantendo a loss fixa, modelos maiores e ensembles comprimem para tamanhos menores apesar de terem mais parâmetros, um resultado que visões anteriores de compressão não expõem.

[ALLOY]: Quando conectado a um bound PAC-Bayes, Requential Coding produz garantias de generalização state-of-the-art para LLMs com bilhões de parâmetros e supera bounds construídos sobre quantização agressiva pós-treinamento, mesmo quando essa quantização é concedida erro zero. A contribuição é principalmente medição: compressão se torna uma sonda de estrutura aprendida. Fique de olho em reproduções em checkpoints open-weight e modelos com reasoning tuning.

[NOVA]: ...

[NOVA]: Lingkai Kong, Zijian Wu e Yuzhe Gu publicaram AdvancedMathBench para impulsionar a avaliação matemática além de problemas de ensino médio e estilo olimpiada. O suite visa níveis de graduação e qualificação de doutorado, com ProverBench contendo 296 problemas projetados para avaliar geração de provas complexas. Correspondência de resposta final não é suficiente aqui; um modelo pode chegar a uma conclusão com aparência correta enquanto faz movimentos simbólicos inválidos.

[ALLOY]: Os autores construíram um pipeline de verificação automática treinado em anotações especialistas em grande escala. Ele retorna vereditos de correção além de avaliações granulares de erros de prova, passando além de um passar ou falhar binário. Um segundo componente, VerifierBench, contém 888 trajetórias de prova geradas por modelos pareadas com ground truth especialista, medindo se modelos podem julgar validade de provas e explicar seus julgamentos. O lado verificador importa porque geração de provas e verificação de provas são habilidades diferentes.

[NOVA]: Os resultados reportados de modelos frontier mostram um aumento agudo de dificuldade. O melhor modelo testado, GPT-5.5-xhigh, marca 75.8 no split de graduação e cai para 66.1 no split de exame de qualificação de doutorado. Conforme a complexidade simbólica aumenta, mesmo os sistemas mais fortes expõem lacunas de raciocínio que benchmarks mais simples baseados em respostas podem perder.

[ALLOY]: AdvancedMathBench dá aos agentes técnicos uma superfície de avaliação mais rigorosa para prova de teoremas, auditoria matemática e autocorreção. O verificador granular importa porque futuros agentes de prova precisam identificar o passo inválido exato, não apenas anunciar que uma prova falhou. O split de doutorado também cria pressão nos modelos para manter definições, lemas e dependências de prova ao longo de cadeias mais longas, onde correspondência de padrões em nível de superfície falha mais cedo.

[NOVA]: ...

[NOVA]: O codebase-memory-mcp do DeusData entra no radar com 31.313 estrelas, uma release point nine de oitavo de julho e uma atualização em treze de julho. Ele fornece um servidor MCP de code-intelligence de alto desempenho que indexa um repositório em um grafo de conhecimento persistente em 158 linguagens, shipado como um binário estático único com zero dependências. Seu mecanismo principal é busca semântica sub-milissegundos após indexação, usando o Model Context Protocol como interface voltada para o agente. OpenClaw, Codex, Claude Code ou Hermes podem usá-lo como backend de contexto em vez de reler material fonte repetidamente durante cada sessão de agente.

[ALLOY]: O fastmcp da PrefectHQ chega com 26.195 estrelas e uma release 3.4 de nono de julho. Ele fornece um framework Pythonic para construir servidores e clientes MCP com ergonomia limpa e iteração rápida. O sinal de tração é uma grande primeira aparência no radar ligada a uma release fresca. Seu mecanismo é abstração de protocolo: desenvolvedores expõem ferramentas e recursos sem escrever à mão boilerplate MCP, mantendo type hints Python e schemas próximos da implementação. O ângulo de integração é criação rápida de servidor de ferramentas para qualquer harness que fale MCP, incluindo OpenClaw, Codex, Claude Code e Hermes.

[NOVA]: O mcp-for-beginners da Microsoft entra com 16.752 estrelas e uma atualização em treze de julho. Ele oferece um currículo open-source para fundamentos de MCP em dot net, Java, TypeScript, JavaScript, Rust e Python. Nenhum release GitHub é publicado, mas a tração é forte. Sua educação de protocolo orientada por exemplos cobre schemas, contratos de ferramentas e limites de segurança através de implementações cross-language. O ângulo de integração é material de referência para fortalecer os contratos que agentes negociam com servidores MCP de terceiros, especialmente quando permissões de ferramentas e exposição de dados precisam ser explícitas.

[NOVA]: ...

[ALLOY]: Kwaipilot KAT-Coder-Air V2.5 foi recém-listado no OpenRouter com disponibilidade de API e uma janela de contexto de 256.000 tokens. A listagem pública não expõe parâmetros ativos, parâmetros totais, preços ou pontuações de benchmark. Sua principal relevância é o tráfego de codificação de longo contexto através de uma stack de agente compatível com OpenRouter já existente, onde o roteador gerencia a superfície de requisições e o modelo gerencia o orçamento de prompt aumentado.

[NOVA]: Kwaipilot KAT-Coder-Pro V2.5 também foi recém-listado no OpenRouter, com a mesma janela de contexto de 256.000 tokens exposta publicamente. Contagens de parâmetros e tabelas de avaliação permanecem ausentes. O Pro dá ao Kwaipilot uma segunda entrada no catálogo para agentes de codificação, e a comparação útil será latência, preço, confiabilidade sob prompts longos e qualidade contra o Air assim que mais detalhes forem publicados.

[NOVA]: ...

[ALLOY]: Ollama .32 introduz uma nova experiência de agente interativo. Rodar o Ollama sozinho agora lança um coordenador local que pode conversar, codificar, pesquisar na web e delegar trabalho a partir de uma superfície controlada por um único prompt, apoiada por modelos locais e na nuvem. O lançamento mantém o caminho de servidor local de binário único do Ollama, mas adiciona roteamento que seleciona um modelo para cada tarefa delegada.

[NOVA]: A integração do Codex App foi renomeada para ChatGPT e exposta através do comando ollama launch ChatGPT, com uma flag de restauração para retornar a uma sessão anterior. O Ollama passa de servidor de runtime para coordenador de agente híbrido enquanto preserva inferência local para trabalho de menor latência ou sensível a privacidade. O roteador adicionado também faz modelos locais, modelos na nuvem, pesquisa e ações de codificação parecerem uma única superfície de conversa em vez de comandos separados.

[NOVA]: ...

[NOVA]: Requential Coding: Pushing the Limits of Model Compression with Self-Generated Training Data estende a história de generalização com um esquema de codificação professor-aluno. Um professor seleciona amostras da própria distribuição do aluno, então o comprimento do código acompanha o desacordo aprendido em vez da contagem de parâmetros ou entropia de dados brutos. A afirmação não é apenas compressão menor, mas um limite que reflete melhor a estrutura que um modelo realmente aprendeu.

[ALLOY]: Transformer-Guided Swarm Intelligence for Frugal Neural Architecture Search combina um controlador Transformer autorregressivo treinado com aprendizado por reforço para macro-pesquisa global e um algoritmo de Colônia de Abelhas Artificiais para micro-exploração local. Um termo de entropia dinâmico ajuda a escapar de convergência prematura, visando reduzir o custo em GPU-dias da busca de arquitetura neural enquanto ainda explora famílias de arquiteturas de alto nível e escolhas de design menores.

[NOVA]: From Global to Factor-Wise Expert Composition in Discrete Diffusion Models decompõe cada amostra em fatores menores e roteia cada fator para um especialista especializado. Isso substitui um único agendamento de mistura escalar global por composição de especialista por fator, visando raciocínio compositional mais preciso em sistemas de difusão discreta. A aposta técnica é que diferentes partes de uma amostra discreta podem precisar de especialistas diferentes no mesmo passo de geração.

[NOVA]: ...

[ALLOY]: OpenClaw, Codex e Claude Code apertaram a camada de controle em transferências de sessão, resultados de subagentes, aprovações e visibilidade de runtime.

[NOVA]: As listagens do Kwaipilot no OpenRouter trazem contexto de codificação de 256K para uma superfície de roteador, mas preços, latência, parâmetros e avaliações públicas ainda precisam de luz do dia.

[ALLOY]: A linha de pesquisa está clara em robótica, vídeo, capturas de tela, wearables e matemática: agentes precisam de evidências fundamentadas, memória durável e superfícies de verificação que exponham mais do que respostas finais.

[NOVA]: O radar do GitHub aponta para o MCP como o tecido conectivo para memória de código, servidores de ferramentas e integrações de terceiros mais seguras.

[ALLOY]: O serving local também está mudando para cima: o Ollama agora apresenta um coordenador de agente enquanto mantém o runtime de modelo de binário único por baixo.

[NOVA]: O trabalho de segurança adiciona uma condição de contorno mais difícil para sistemas multiagentes: fragmentos podem parecer inofensivos até que um agente downstream os assembla.

[ALLOY]: Para material de origem e links, veja as notas do programa em Toby On Fitness Tech ponto com. Obrigado por ouvir o AgentStack Daily. Voltamos em breve.