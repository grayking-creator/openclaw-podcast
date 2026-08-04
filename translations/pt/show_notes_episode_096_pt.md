Episódio 096 — 31 de julho de 2026

[00:00] Gancho do episódio

Leitura de Lançamentos do Agent Stack: Hermes Agent v2026.7.30 lidera o dia: v2026.7.30 traz mudanças concretas nas superfícies que os desenvolvedores executam todos os dias, com os detalhes abaixo. Também na programação de hoje: Gemini Robotics 2 traz inteligência de corpo inteiro para robôs, GitHub Models Descontinuado: Playground, API e BYOK extintos, Kimi K3 da Moonshot chega como uma versão local de IA quantizada, além do restante de um ciclo de notícias denso entre modelos, ferramentas e infraestrutura. Cada história recebe o mesmo tratamento — o que foi lançado, o mecanismo por trás e o que muda para os desenvolvedores que trabalham na prática.

[02:00] Leitura de Lançamentos do Agent Stack: Hermes Agent v2026.7.30

Um lançamento estável chegou neste ciclo, moldando como os harnesses de agentes estão sendo montados agora. Hermes Agent v2026.7.30: Data de Lançamento: 30 de julho de 2026 > Lançamento de correção. Esta tag consolida os ~1.000+ PRs mesclados desde v0.19.0 em um lançamento estável para consumidores downstream (imagens Docker, implantações hospedadas, instalações novas). Desde (v0.19.0, 20 de julho): ~2.789 commits · ~4.748 arquivos alterados · ~442.000 inserções · ~392.300 exclusões no main. Esta janela é dominada por ondas de correção de bugs e resgate no gateway, subsistema de voz, aplicativo desktop e instalador, além de trabalho contínuo na plataforma (canal Buzz/Nostr, geração e entrega de vídeo FLUX3, confiabilidade de mídia no Telegram, regressões no modo de voz). As notas de lançamento completas curadas para esta janela serão lançadas com v0.20.0, que documentará tudo desde v0.19.0 — destaques, áreas de funcionalidades e créditos completos dos contribuidores. Nada nesta janela será pulado. hermes update curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash Registro de Alterações Completo: [..v2026.7.30](https://github.com/NousResearch/hermes-agent/compare/..v2026.7.30) Na camada de API e runtime, essas alterações modificam o que os desenvolvedores podem configurar e usar por padrão; a questão para qualquer workflow de agente em produção é se os novos padrões melhoram ou quebram o caminho que você estava executando esta semana. As notas de lançamento completas para cada harness — incluindo orientação de implantação, lista de pull requests mesclados e créditos dos contribuidores — estão linkadas na fonte primária, e o contexto do changelog para cada tag é o que os desenvolvedores devem comparar com sua versão fixada atual antes de ativar o padrão em produção. Hermes Agent v2026.7.30, publicado em 30/07/2026, é uma tag estável: fixe-a explicitamente em vez de acompanhar um canal em movimento, reproduza uma sessão de agente representativa contra a nova build e compare latência de chamadas de ferramentas, comportamento de reconexão e tratamento de aprovações com a versão atualmente em execução antes de promover o novo padrão.

[02:42] Gemini Robotics 2 traz inteligência de corpo inteiro para robôs

O DeepMind publicou o Gemini Robotics 2 em 30 de julho, enquadrando o trabalho como trazendo 'inteligência de corpo inteiro' para robôs. A alegação principal é que um sistema agora pode lidar com percepção, planejamento e uso de ferramentas em todo o corpo de um robô, em vez de tratar braços, garras e movimento da base como problemas separados. O lançamento são na verdade dois modelos: Gemini Robotics 2 e um companheiro chamado Gemini Robotics ER 2. De acordo com o blog, ER 2 é a variante construída para raciocínio, colaboração e resolução de tarefas do mundo real. O DeepMind destacou três áreas concretas onde os novos modelos superam trabalhos anteriores. Primeiro, compreensão de vídeo: os modelos podem assistir demonstrações longas e identificar os passos que importam. Segundo, orquestração de ferramentas: em vez de apenas mover os próprios braços, o robô pode decidir buscar uma ferramenta diferente ou chamar um agente separado. Terceiro, colaboração multi-robô: vários robôs podem dividir um trabalho sem um humano coreografando cada transição. O post do DeepMind enquadrou o trabalho em torno de tarefas do mundo real em vez de picking and placing em superfície plana. A thread do Hacker News atingiu uma pontuação de 561 em um dia, o que é incomumente alto para um tópico de robótica e sugere que a comunidade de desenvolvedores acha que o trabalho está fazendo coisas reais desta vez.

[03:56] GitHub Models Descontinuado: Playground, API e BYOK Extintos

O GitHub Models foi descontinuado. A partir de 30 de julho de 2026, o playground, o catálogo de modelos, a API de inferência e a opção de trazer sua própria chave não estão mais disponíveis para nenhum cliente.

Para desenvolvedores, o impacto prático é direto. Se você usava o GitHub Models como uma forma rápida de experimentar diferentes modelos no navegador, esse ponto de entrada desapareceu. Se você chamava o endpoint de inferência do GitHub Models do seu código, esse endpoint desapareceu. Se você conectou chaves de provedores externos através do fluxo BYOK para poder rotear solicitações para OpenAI, Anthropic ou outros a partir de uma única superfície no lado do GitHub, essa conexão também desapareceu.

A descontinuação é total em vez de parcial. O GitHub não está desativando uma parte enquanto mantém o resto vivo; o playground, catálogo, inferência e BYOK desaparecem juntos. Clientes que tratavam o GitHub Models como uma fina camada de conveniência sobre provedores externos agora têm que conversar diretamente com esses provedores.

O próximo passo razoável é migrar qualquer uso ativo. SDKs de provedores diretos e chaves de API substituem os caminhos de inferência e BYOK. A navegação de modelos muda para o catálogo de cada provedor ou para diretórios de terceiros. Superfícies de prototipagem como o playground da OpenAI, Console da Anthropic ou interfaces de chat específicas de fornecedores cobrem o caso de uso do playground.

Uma coisa a observar: o post do changelog deixa a cláusula de escopo do cliente truncada, então não está claro se clientes de nível pago ou empresarial recebem algum caminho de continuação ou acesso herdado. Se você dependia do GitHub Models para um workflow de produção, verifique se seus relacionamentos existentes com provedores permitem absorber as chamadas sem re-arquitetar.

[05:32] GPUs Ociosas Estão Custando Caro — Uma Nova Visão sobre Gestão de Frota

[07:13] GPUs Ociosas Estão Custando Caro — Uma Nova Visão sobre Gestão de Frota

Uma nova postagem no blog da Hugging Face, publicada em 30 de julho pela Dharma-AI, usa uma metáfora da aviação para fazer um argumento orçamentário: um GPU ocioso é como uma aeronave em solo — um ativo que se deprecia e custa o mesmo seja quando voa ou quando fica na pista.

A estrutura importa porque equipes de IA tendem a orçar com base na computação bruta adquirida, não na computação realmente consumida. O claim principal da postagem é que o tempo ocioso se tornou silenciosamente o custo dominante para organizações que executam mais do que alguns aceleradores, porque GPUs se depreciam por hora independentemente da carga de trabalho.

Para construtores, o aprendizado é mais conceitual do que mecânico. O material disponível não documenta sistemas específicos de agendamento, políticas de recuperação ou benchmarks de utilização, então a evidência útil é a própria estrutura: trate a capacidade dos aceleradores como uma frota gerenciada, meça a utilização e projete trabalhos que preencham lacunas em vez de reservar hardware indefinidamente.

O que observar a seguir: se a Dharma-AI vai acompanhar com ferramentas concretas ou estudos de caso que coloquem números no argumento do custo do tempo ocioso.

[08:16] Jetson como o Accessório 'Clutch': Sarah Guo Destaca IA de Borda

A NVIDIA colocou um holofote promocional em sua plataforma de IA de borda Jetson esta semana, e a empresa recorreu a uma metáfora da moda para isso. A postagem, publicada em 28 de julho no blog da NVIDIA sob o título "Compute Poderoso Tão Compacto Que É Clutch — Construa IA em Qualquer Lugar Com o NVIDIA Jetson," apresenta a investidora Sarah Guo em um vídeo curto enquadrando o kit de desenvolvedor compacto como um "clutch" — o tipo de acessório pequeno e elegante que cabe na sua mão e ainda assim chama atenção.

Guo dirige a Conviction, uma empresa de capital de risco nativa de IA, e co-apresenta o podcast No Priors. No vídeo, ela destaca como o Jetson funciona como uma plataforma para construções de IA de borda.

Para construtores, a ideia subjacente é direta: "borda" significa que o modelo é executado no próprio dispositivo em vez de pingar um servidor remoto. É isso que permite que um robô, câmera, drone ou gadget de mão processe inferência localmente. O enquadramento aqui é menos sobre números brutos de benchmark e mais sobre como um investidor-operador como Guo fala sobre IA de borda quando está tentando convencer outros fundadores de que é um alvo de implantação real, não uma demo de pesquisa.

A postagem em si é leve em detalhes técnicos — sem novo SKU, sem lançamento de SDK, sem preços, sem changelog de nenhum tipo. O interessante é o mensageiro: uma capitalista de risco que financia empresas nativas de IA endossando uma plataforma de hardware específica no próprio marketing da NVIDIA. Esse é um sinal de para onde o capital acha que a IA de borda está indo a seguir, e vale a pena uma rápida olhada se você está pesando APIs de nuvem versus inferência no dispositivo para uma construção futura.

[09:55] OpenAI Esboça Seu Playbook de IA Responsável para a Europa

Em 31 de julho, a OpenAI publicou um artigo intitulado 'Avançando IA responsável através da Europa,' delineando como suas práticas atuais apoiam a governança de IA responsável no continente. O post agrupa o trabalho em quatro áreas: segurança, proteção, transparência e procedência. A OpenAI diz que esses esforços continuarão rodando ao lado do EU AI Act à medida que a lei passar por suas fases de implementação.

Para construtores, o sinal prático é que procedência, significando os metadados que marcam imagens e texto gerados por IA, e divulgações de transparência estão cada vez mais fazendo parte da linha de base europeia. A OpenAI está enquadrando suas práticas existentes como o scaffolding para essa conformidade em vez de introduzir novos compromissos específicos para a Europa neste post. O artigo posiciona o trabalho como um programa contínuo que acompanha o lançamento do AI Act.

O EU AI Act está sendo implementado gradualmente, com diferentes obrigações entrando em vigor em diferentes cronogramas. O post da OpenAI sinaliza investimento contínuo em manter suas divulgações de segurança e proteção alinhadas com essas obrigações à medida que forem implementadas. Também aponta para transparência e procedência como áreas onde usuários europeus podem esperar ver mais visibilidade em como conteúdo gerado por IA é identificado e rotulado.

O que observar a seguir: à medida que as provisões de maior risco do AI Act entrarem em vigor, espere requisitos de documentação mais concretos em torno de procedência, documentação de modelos e divulgações de segurança para qualquer sistema implantado no mercado europeu.

[11:18] Resumo de pesquisa: PhiZero Constrói uma 'Linguagem Física' para Prever Como o Mundo se Move

PhiZero é um novo modelo de pesquisa que prevê como o mundo se comporta aprendendo uma linguagem física, um vocabulário discreto e compacto de mudanças de estado, em vez de prever pixels de vídeo brutos. Modelos de mundo existentes tendem a renderizar quadros futuros diretamente, o que deixa a física subjacente enterrada dentro de um preditor visual de alta dimensionalidade. Os autores do PhiZero argumentam que humanos fazem algo diferente: observamos, abstraímos as regras do movimento e armazenamos essas regras em representações semelhantes à linguagem sobre as quais podemos raciocinar. O PhiZero tenta reproduzir esse truque aprendendo tokens físicos da experiência de vídeo em ambiente natural, então usando esses tokens para avançar estados do mundo. A esperança prática é um modelo que planeja e raciocina sobre resultados mais como uma pessoa do que um gerador de vídeo. É um preprint de pesquisa, não um produto, então o aprendizado é a ideia: tokens discretos para física podem ser um substrato mais útil do que pixels para modelos de mundo.

[12:13] Resumo de pesquisa: Frontis-MA1: Treinando IA para Melhorar o Processo de Construção de IA

Uma equipe está testando se IA pode melhorar significativamente o processo de construção de IA — e publicando o sandbox para que qualquer pessoa possa assistir. O artigo apresenta o Frontis-MA1, um modelo de 35 bilhões de parâmetros pós-treinado como um agente de meta-evolução para engenharia de aprendizado de máquina. Os pesquisadores construíram o OpenMLE, uma stack aberta que transforma engenharia de ML em um jogo mensurável com feedback de execução.

O OpenMLE tem três camadas. O OpenMLE-Gym executa ambientes de tarefas verificáveis onde mudanças propostas realmente são executadas. O OpenMLE-RL lida com aprendizado de operador — ensinando o modelo como direcionar edições e buscas. O OpenMLE-Evo executa busca de longo horizonte para que melhorias possam se composta. O Frontis-MA1 fica no topo, propondo mudanças de engenharia de ML e vendo quais realmente funcionam.

O headline não é que IA melhorou a si mesma — é que melhoria autorregressiva recursiva agora tem um testbed concreto e aberto. A maior parte do trabalho anterior permaneceu teórica ou viveu atrás de demos fechadas; aqui o gym, loop de treinamento e harness de busca são todos públicos, então outros laboratórios podem repetir ou estender o mesmo setup. O artigo está em alta no feed diário do HuggingFace.

[13:15] Uma Tour pela Árvore Genealógica das Variantes de Atenção do DeltaNet

A Doubleword publicou um tutorial no blog rastreando a família DeltaNet de variantes de atenção linear e argumentando, como diz o título, que Kimi Delta Attention é uma extensão natural que um leitor cuidadoso poderia ter chegado sozinho. O post chegou ao Hacker News em 28 de julho de 2026, gerou uma discussão de 297 pontos que permaneceu ativa, e também apareceu na tag de IA do Lobsters.

O post apresenta o campo como uma árvore genealógica em vez de um amontoado de truques independentes. Suaclaim principal é que variantes de atenção recentes parecem menos exóticas quando você alinha seus predecessores, e que seguir a linhagem é suficiente para prever para onde a próxima provavelmente irá.

Por que importa agora: anúncios de modelos frontier continuam sendo lançados com mecanismos de atenção que parecem um salto de fé numa primeira olhada, e o aprendizado prático para engenheiros é que a linhagem importa mais do que qualquer artigo individual. Ler a árvore genealógica primeiro muda como cada nova variante chega.

Para construtores que querem realmente entender o que está rodando dentro de modelos como o Kimi, o post é uma útil rampa de entrada. É uma leitura de fim de semana, não um projeto de pesquisa, e as discussões do Hacker News e Lobsters ao lado dele preenchem o contexto.

[14:31] Habilidades de Agente e Suporte MCP do Copilot Code Review Chegam ao GA

A GitHub moveu as habilidades de agente e suporte a servidor MCP do Copilot code review para disponibilidade geral em 29 de julho. Ambas as capacidades agora estão abertas para todos os usuários do Copilot Pro, Pro+, Business e Enterprise, tendo saído da pré-visualização pública.

O post de changelog tem poucos detalhes. MCP — o Model Context Protocol — é a forma padrão para assistentes de IA se conectarem a ferramentas e fontes de dados externas. O post não define o que "habilidades de agente" significa nesse contexto nem lista quais habilidades estão incluídas. Também não especifica integrações MCP específicas, mudanças de comportamento, ou o que construtores devem esperar de diferente da pré-visualização.

Para construtores nos níveis pagos listados, a mudança é que esses recursos estão prontos para produção em vez de pré-visualização. O Copilot do tier gratuito não é mencionado no lançamento. O próximo monitoramento honesto é como as equipes realmente os configuram uma vez disponíveis, mas o anúncio em si é fino o suficiente para que qualquer pessoa planejando um rollout precisará mergulhar nos docs do GitHub em vez de confiar no changelog.

[15:33] Spec 2026-07-28 do MCP Vai Stateless, Promete Sem Remoções Súbitas

O Model Context Protocol, o padrão aberto que permite assistentes de IA se plugarem a ferramentas e fontes de dados externas, recebeu uma atualização de especificação em 30 de julho. A mudança principal: a camada de transporte está se tornando stateless, significando que servidores não precisam mais manter estado de sessão entre requisições do cliente. Junto com isso, o projeto adotou uma nova política que impede que recursos sejam removidos sem aviso.

Em termos simples, stateless significa que cada requisição é independente em vez de depender de uma sessão recordada no servidor. Para construtores rodando servidores MCP, isso muda o design para conexões mais simples e previsíveis — e igualmente importante, remove uma classe de modos de falha que vêm de estados de sessão perdidos ou descartados.

A política de deprecação é a metade mais silenciosa do lançamento mas carrega peso próprio. Recursos do protocolo agora passarão por um ciclo de deprecação documentado com aviso antes de poderem ser removidos, dando tempo para autores de servidores e clientes migrarem. É o tipo de promessa de previsibilidade que ajudou padrões web a se estabilizarem, e responde diretamente a uma preocupação real de qualquer pessoa investindo em integrações MCP hoje.

A atualização foi publicada no blog do MCP em 30 de julho e chamou atenção rápida no Hacker News, onde alcançou uma pontuação de 127.

[16:52] Avatarin Lança Agente de Voz 24/7 para Varejo com GPT-Realtime

A avatarin colocou o GPT-Realtime da OpenAI para trabalhar como um agente de voz multilíngue 24/7 para compradores na Yamada Denki, uma varejista de eletrônicos japonesa. Clientes podem chegar e fazer perguntas em seu próprio idioma, e o assistente responde em tempo real.

As primeiras duas semanas produziram números impressionantes: 30.000 pessoas usaram o agente, e 92% das respostas da pesquisa voltaram positivas. Para um assistente de voz implantado em escala de consumidor em um ambiente de varejo movimentado, esse é um sinal inicial significativo de que modelos de voz em tempo real podem funcionar sob tráfego real.

GPT-Realtime é o modelo de speech-to-speech da OpenAI, significando que áudio entra e áudio volta sem uma etapa intermediária separada de transcrição de texto. Esse caminho direto de voz é o que torna possível uma conversa fluida de ida e volta, e é a mesma família de capacidades que a avatarin agora apontou para uma carga de trabalho de varejo de alto volume.

Para construtores, a história é um ponto de dados concreto em vez de um anúncio de recurso. Um agente de voz que sobreviveu a 30.000 interações ao vivo com compradores e feedback esmagadoramente positivo está mais próximo de pronto para produção do que de demo. Cobertura multilíngue e disponibilidade 24 horas são diferenciais óbvios para uma implantação no varejo, e ambos parecem estar funcionando.

Uma coisa vale a pena acompanhar: se a avatarin e a Yamada Denki expandem o escopo do agente além de perguntas sobre produtos para devoluções, reclamações ou upsells, onde as conversas ficam mais difíceis e os números de satisfação serão mais difíceis de manter.

[18:17] Google DeepMind Lança Três Modelos de IA Física Para Controle de Corpo Inteiro, Destreza e Colaboração Multi-Robô

O Google DeepMind lançou o Gemini Robotics 2, a camada de inteligência para sua próxima geração de robôs. O lançamento ships três modelos: um modelo de visão-linguagem-ação para controle humanoide de corpo inteiro, o Gemini Robotics ER 2 para raciocínio incorporado e orquestração de tarefas, e um VLA on-device que se adapta a novos corpos de robôs em horas. Um checkpoint controla o Apptronik Apollo 2 e um Franka Duo. Apenas o ER 2 está disponível publicamente. O post Google DeepMind Ships Three Physical AI Models For Whole Body Control, Dexterity And Multi Robot Collaboration apareceu primeiro no MarkTechPost. A fonte primária suporta a mudança específica de produto ou fluxo de trabalho acima; ela não suporta alegações mais amplas sobre desempenho, compatibilidade ou implantação. Teste a mudança da fonte contra um fluxo de trabalho real antes de depender dela.