OPENCLAW DAILY — EPISODE 030 — 13 de Abril de 2026

[00:00] INTRO / ABERTURA
OpenClaw lança uma atualização que faz a recuperação de memória acontecer antes da resposta principal. OpenAI rotaciona certificados do macOS após um susto na cadeia de suprimentos. Anthropic transforma o Claude Cowork em uma superfície de部署 empresarial. SoftBank lança uma empresa para "IA física." E o novo chatbot de saúde da Meta pede dados médicos brutos que não tem o direito de ver.

[01:55] HISTÓRIA 1 — OpenClaw v2026.4.12: Memória Ativa, MLX Speech Local e Carregamento de Plugins Mais Inteligente
OpenClaw 2026.4.12 não é um lançamento midiático chamativo. É uma atualização de qualidade da plataforma, e é exatamente por isso que importa.

A adição principal é um plugin opcional de Memória Ativa que executa um subagente especializado de memória logo antes da resposta principal. Na prática, isso significa que o OpenClaw pode buscar proativamente preferências do usuário relevantes, contexto e detalhes passados antes de responder, em vez de esperar que o operador diga explicitamente "lembre disso" ou "pesquise na memória". Essa é uma mudança significativa no design de interação. Muito do que se chama de "boa memória de IA" é realmente apenas timing disciplinado de recuperação. O OpenClaw agora está tornando esse timing parte do produto.

A segunda adição notável é um provedor experimental de fala MLX local para o Modo Fala do macOS. Isso é importante porque empurra mais capacidade de voz para o dispositivo local com seleção explícita de provedor, reprodução local de enunciados, tratamento de interrupções e comportamento de fallback. A tendência geral é óbvia: inferência local não é mais apenas para texto e embeddings. A pilha de voz também está se movendo para o local.

Há também uma expansão prática na escolha de modelos. O OpenClaw agora empacota tanto um provedor Codex quanto um provedor LM Studio. Modelos gerenciados pelo Codex podem usar auth nativo, threads, descoberta e compactação em seu próprio caminho, enquanto modelos compatíveis com OpenAI locais ou auto-hospedados se tornam first-class via integração e descoberta de modelos em runtime do LM Studio. Esse é exatamente o tipo de ampliação de superfície de provedor que torna um runtime de agente mais difícil de ser bloqueado em uma narrativa de fornecedor único.

E então há o lado de higiene de segurança e runtime. O carregamento de plugins agora é limitado às necessidades declaradas no manifesto, para que a CLI, provedores e canais não ativem runtime de plugins não relacionados por padrão. Combinado com o endurecimento de wrappers de shell, correções de aprovação, limpeza de sequenciamento de inicialização e múltiplas correções de confiabilidade de sonhar e memória, a linha condutora é clara: esta atualização é sobre fazer o sistema lembrar de forma mais precisa e carregar de forma menos imprudente.
→ https://github.com/openclaw/openclaw/releases/tag/v2026.4.12

[09:05] HISTÓRIA 2 — OpenAI Rotaciona Certificados do App macOS Após o Comprometimento do Axios Reportado pelo Axios
A OpenAI publicou uma resposta detalhada ao comprometimento da ferramenta de desenvolvimento do Axios, e a parte importante não é se os atacantes definitivamente obtiveram o certificado de assinatura da OpenAI. É que a OpenAI está tratando a cadeia de confiança como suficientemente comprometida para rotacionar mesmo assim.

Segundo a empresa, um pacote Axios malicioso foi puxado para um workflow do GitHub Actions usado no processo de assinatura do app macOS em 31 de março. Esse workflow tinha acesso a material de assinatura e notário usado para ChatGPT Desktop, Codex, Codex CLI e Atlas. A OpenAI diz que não encontrou evidências de que dados de usuários foram acessados, nenhuma evidência de que seus produtos foram alterados e nenhuma evidência de que o certificado foi realmente mal utilizado. Mas ainda assim está revogando e rotacionando o cert, publicando novos builds e dando aos usuários um prazo para atualizar antes que versões mais antigas do macOS parem de receber suporte.

Esta é uma daquelas histórias que importa porque comprime várias realidades da indústria de IA em um único incidente. Primeiro: os laboratórios de fronteira não são mais apenas fornecedores de modelos. São distribuidores de software desktop, operadores de plataforma de desenvolvedores e âncoras de identidade. Segundo: o risco de cadeia de suprimentos em dependências de desenvolvedores aparentemente tediosas pode.Cascadear diretamente para a confiança do consumidor. E terceiro: o problema de integridade não é mais apenas "o modelo alucinou?" Também é "os usuários podem confiar que o binário em sua máquina é realmente seu?"

A OpenAI diz que a causa raiz incluiu uma tag flutuante no GitHub Actions e uma proteção de minimumReleaseAge faltando para pacotes. Isso não é exótico. É higiene ordinária de pipeline de build. O que é o ponto. Em 2026, higiene ordinária de pipeline de build agora faz parte do risco de IA de fronteira.
→ https://openai.com/index/axios-developer-tool-compromise/

[14:55] HISTÓRIA 3 — Anthropic Transforma o Claude Cowork em Uma Superfície Administrativa, Não Apenas Uma Demo
A Anthropic anunciou que o Claude Cowork agora está disponível para todos os planos pagos, mas a história real é o pacote de governança que está sendo lançado ao redor dele.

A empresa adicionou controles de acesso baseados em papéis, limites de gasto por grupo, análises de uso, emissão de eventos OpenTelemetry, controles de ação por conector e um conector do Zoom que pode trazer resumos de reuniões, transcrições e itens de ação para o Cowork. Leia essa lista com atenção e você pode ver a transição acontecendo em tempo real. Isso não é mais sobre se os agentes podem fazer coisas legais. É sobre se uma empresa pode implantá-los em marketing, finanças, jurídico, operações e produto sem perder controle de políticas, auditabilidade ou visibilidade de custos.

A própria descrição da Anthropic é reveladora: a maior parte do uso do Cowork já vem de fora da engenharia. Isso significa que o próximo campo de batalha empresarial não é apenas assistência de codificação. É se workflows baseados em agentes se tornam uma camada operacional compartilhada para o resto da empresa. Uma vez que isso acontece, o console admin se torna infraestrutura estratégica.

O item mais importante aqui pode realmente ser os controles de conector por ferramenta. Acesso apenas leitura versus escrita é a diferença entre um agente que ajuda você a entender o sistema e um agente que pode mudar o sistema. À medida que as empresas passam de experimentação para implantação, essa linha vai decidir quem é aprovado e quem é bloqueado.
→ https://claude.com/blog/cowork-for-enterprise

[21:10] HISTÓRIA 4 — A Aposta de "IA Física" do SoftBank É Realmente uma Aposta em Plataforma de Robótica
O SoftBank supostamente está formando uma nova empresa para construir o que chama de "IA física" — um modelo que pode controlar máquinas e robôs de forma autônoma até 2030. Os investidores reportados incluem Sony, Honda e Nippon Steel.

Este é um forte sinal porque recategoriza onde alguns dos maiores atores estratégicos acham que o valor está indo. Chat de consumidor está concorrido. Copilotos empresariais estão concorridos. A camada de controle robótico e industrial não está concorrida da mesma forma, porque a parte difícil não é apenas qualidade do modelo. São dados, loops de controle, parcerias de hardware, segurança e a capacidade de operar no mundo real.

O SoftBank tem contado versões dessa história há um tempo através de apostas em robótica e infraestrutura soberana, mas este movimento a afia. O que o Japão parece querer não é apenas acesso a modelos foundation estrangeiros. Quer uma participação doméstica na camada de modelo que eventualmente executará fábricas, sistemas logísticos e robôs. Isso é IA soberana em um sentido mais literal: não apenas datacenters locais, mas controle local sobre comportamento de máquina.

Se a corrida de IA de software era sobre caixas de busca e editores de código, a próxima corrida pode ser sobre quem treina os cérebros padrão para sistemas incorporados. O SoftBank está apostando que essa camada ainda está disponível para ser reivindicada.
→ https://www.theverge.com/ai-artificial-intelligence/910879/softbank-creates-new-company-building-physical-ai

[26:15] HISTÓRIA 5 — O Muse Spark da Meta Mostra o Pior Loop de Incentivo do Consumidor-IA
A WIRED testou o novo modelo Muse Spark da Meta e descobriu que o assistente estava feliz em pedir dados de saúde brutos: métricas de rastreadores de fitness, leituras de glicose, relatórios de laboratório, números de pressão arterial, tudo. O discurso era previsível: me dê seus dados, e eu vou traçar tendências, sinalizar padrões e ajudar você a interpretar o que está acontecendo.

O problema é que isso é exatamente o tipo de interação de alto contexto, alta confiança onde produtos de IA para consumidores ainda não merecem o papel que querem. Especialistas médicos citados pela WIRED levantaram duas preocupações óbvias. Uma é privacidade: as pessoas estão sendo induzidas a carregar informações altamente sensíveis para sistemas que não são governados como ambientes clínicos e podem usar essas informações para treinamento futuro. A segunda é competência: o conselho ainda não é confiável o suficiente para justificar a intimidade do pedido de dados.

Essa combinação é a história. O modelo pede dados em um nível de confiança que excede a postura real de segurança e privacidade do sistema. E porque esses bots estão ficando mais fáceis de acessar e mais personalizados exatamente no momento em que a saúde permanece cara e fragmentada, muitas pessoas vão ser tentadas a usá-los como um substituto para o cuidado, em vez de um suplemento ao julgamento médico real.

A Meta diz que o modelo não está substituindo seu médico. Tudo bem. Mas se um bot continua convidando as pessoas a "jogar os dados brutos" e depois age como um quasi-analista, ele já está entrando em um papel que exige padrões muito mais altos do que a IA para consumidores atende atualmente.
→ https://www.wired.com/story/metas-new-ai-asked-for-my-raw-health-data-and-gave-me-terrible-advice/

[31:15] ENCERRAMENTO
Esse é o mapa de hoje: memória-antes-da-resposta como design de produto, cadeias de confiança de software como risco de IA, governança de agentes como infraestrutura empresarial, IA física como estratégia nacional e prompts de dados de saúde como sinal de alerta para implantação para consumidores. Responda aqui para aprovar a geração da transcrição.