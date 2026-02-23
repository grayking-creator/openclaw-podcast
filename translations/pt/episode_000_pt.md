# Episode 0: Hardware Deep Dive - Corrigindo Falhas de Modelos Locais
**Data:** 18 de fevereiro de 2026
**Duração:** 11:45
**Apresentadores:** Nova & Alloy

---

## TRANSCRIÇÃO COMPLETA

*Nota: Episode 0 é um relatório técnico solo. As atribuições de locutor abaixo refletem o formato padrão de dois hosts do programa baseado no fluxo de conteúdo — o trailer pré-show é compartilhado, o relatório principal é apresentado pela Nova.*

---

**[TRAILER PRÉ-SHOW]**

[NOVA]: A maioria das coberturas de IA te diz o que ficar animado. Este programa te diz o que realmente funciona — e o que não funciona — quando você está rodando modelos de linguagem no seu próprio hardware, nos seus próprios termos.

[ALLOY]: OpenClaw Daily é para pessoas que passaram da fase de demo na nuvem. Você está rodando agentes locais, você se importa para onde seus dados vão, e você é cético em relação a benchmarks publicados pela mesma equipe que treinou o modelo.

[NOVA]: Mesmo.

[ALLOY]: Cada episódio vem de sistemas reais, falhas reais e correções reais. Não comunicados de imprensa. Se algo quebra no meio de uma tarefa, investigamos. Ao vivo. Sem limpeza editorial, sem polimento retroativo.

[NOVA]: Este é o programa para construtores que rodam sua própria infraestrutura. Vamos lá.

---

**[EPISÓDIO PRINCIPAL]**

[NOVA]: Meu agente de codificação, Clarity, rodando Qwen3-Coder 30B, 계속 getting context overflow errors right in the middle of tasks. Não ocasionalmente. Consistentemente.

Então eu comecei a investigar — talvez seja um teto de hardware, talvez eu precise de um DGX Spark ou um M3 Ultra para rodar isso direito. Essa questão virou uma imersão completa em hardware: especificações reais, custos reais, largura de banda de memória, e tudo mais.

A reviravolta? Não era problema de hardware nenhum. Era um rótulo de configuração. E eu encontrei e corrigi ao vivo enquanto fazia a pesquisa.

Você vai ver os números, as trocas honestas, e uma recomendação real.

---

Os estouros de contexto que você estava tendo? Não é problema de hardware.

O modelo que você está rodando — Qwen3-Coder 30B — suporta realmente 262.144 tokens de contexto. 262.000.

OpenClaw estava limitando a 131.072 por causa de como o modelo Ollama foi nomeado na criação. O rótulo `v-128k` não era um teto de capacidade — era só uma string. Um rótulo do dia de configuração que virou um limite rígido por acidente.

A correção foi um patch de configuração e uma nova definição de modelo Ollama. Feito. Ao vivo. Grátis.

Você não precisava de hardware novo. Você precisava de uma correção de uma linha. Essa é a reviravolta.

---

Então vamos ver o que realmente aconteceu em 18 de fevereiro às 11:15.

Você pediu 146.760 tokens contra um limite de 131.072.

Those five-minute timeouts weren't crashes — the model wasn't dying. It was pre-filling.

Com velocidade de pré-preenchimento de ~400 tokens por segundo, processar 146.000 tokens leva 6+ minutos. Seu limite de timeout era 5 minutos. Então o sistema bateu na parede no minuto 5, três vezes seguidas.

Três timeouts consecutivos, perfeitamente explicados pela matemática. Isso não é instabilidade. É um valor de timeout curto demais para uma janela de contexto grande demais para um limite configurado que estava errado desde o início. Três camadas de erro, empilhadas uma sobre a outra.

---

Agora a matemática da memória.

Qwen3-Coder é uma arquitetura Mixture-of-Experts com apenas quatro heads de atenção KV. Compare com LLaMA-3 8B, que tem oito. Metade. Essa é uma escolha de design intencional que a torna dramaticamente mais eficiente em memória para contexto longo.

Em contexto 262K: 15 GB para pesos do modelo, 24 GB para cache KV, overhead do SO — considere 44 GB no total.

Você tem 64 GB de memória unificada. Isso é 20 GB de folga.

O modelo que estava estourando cabe na sua máquina atual no contexto nativo completo, com espaço de sobra. O hardware estava fino o tempo todo.

---

Você pediu um relatório de hardware — então aqui está ele. Quatro opções, porque há uma nova que vale a pena adicionar à conversa.

**Opção 1: NVIDIA DGX Spark — $3.000**

Chip GB10 Grace Blackwell. 128 GB de memória unificada LPDDR5X. 1 petaflop de computação FP4.

O número que salta: 273 GB/s de largura de banda de memória.

Isso é na verdade menor que seu Mac Studio atual, que entrega cerca de 800 GB/s. Então a máquina que a NVIDIA está vendendo como um supercomputador de IA tem um terço da largura de banda de memória da máquina na sua mesa.

Geração de tokens é limitada por largura de banda de memória. Largura de banda é o gargalo.

Onde a Blackwell compensa são os núcleos tensores FP4. Benchmarks colocam em 25-50 tokens por segundo em um modelo 70B, versus seus atuais 10-15. Melhoria real.

Mas: Linux apenas, é um sidecar — não um substituto. Vincule duas unidades por $6.000 e você pode rodar modelos 405B+.

---

**Opção 2: Mac Studio M3 Ultra**

$4.000 para 192 GB. $8-10.000 para 512 GB.

Largura de banda: 819 GB/s — um passo modesto.

A Apple mediu M3 Ultra como 2,1× mais rápido que M2 Ultra para throughput de LLM, devido a melhorias arquiteturais no motor neural e unidades de multiplicação de matrizes.

Em um modelo 70B: 20-32 tokens por segundo. O dobro de onde você está agora.

A configuração de 192 GB desbloqueia carregamento simultâneo de modelos — seu modelo de codificação 30B, um modelo geral 70B, e o SO, tudo na RAM de uma vez. Sem swapping. Fluxo de trabalho diferente.

A configuração de 512 GB existe por um motivo: LLaMA 3.1 405B em Q4 pesa 230 GB. Esse é o único caminho de consumidor para rodar um modelo de classe 400B localmente. Mesmo macOS, mesma mesa, zero fricção.

---

**Opção 3: AMD — e isso são duas histórias muito diferentes.**

O caminho do consumidor: Threadripper mais duas placas RX 7900 XTX — custa cerca de $5.000-6.000. Cada placa tem 24 GB de VRAM.

O problema de VRAM dividido significa que você não obtém 48 GB limpos de memória endereçável — você obtém 24 com overhead caro de sincronização entre GPUs. ROCm ainda atrasa CUDA para inferência de LLM. Você gastaria $5.000 para obter os mesmos tokens por segundo que está obtendo agora.

Recusa veemente.

---

Mas a AMD tem uma carta selvagem que merece atenção séria — especialmente se seu teto de orçamento está mais perto de $2.500 do que de $25.000.

O Ryzen AI Max+ 395, codinome Strix Halo.

16 núcleos Zen 5. 40 unidades de computação RDNA 3.5 para a iGPU. Um NPU de 50 TOPS. E suporte para até 128 GB de LPDDR5X em um pool de memória completamente unificado — CPU, GPU e NPU todos desenhando do mesmo espaço de endereço.

Soa familiar?

Essa é a resposta da AMD à arquitetura Apple Silicon, em um chip de laptop, em preços de consumidor.

Um Framework Desktop AMD Edition completo custa cerca de $2.000-2.500. O ASUS ROG Flow Z13 sai por $2.499. Esse é o caminho mais barato, por uma margem significativa, para 128 GB de memória unificada em qualquer fator de forma.

Por que não é o vencedor óbvio? Largura de banda. Sempre largura de banda.

O barramento de memória aqui é de 256 bits, entregando cerca de 256 GB/s. Compare com seu M2 Ultra em 800 GB/s — isso é um déficit de três vezes. Mais capacidade de memória não ajuda se os tokens não podem se mover rápido o suficiente.

Na prática, via backend CPU do llama.cpp: cerca de 60-80 tokens por segundo em um modelo 7B, 15-20 em um 30B, e 5-8 tokens por segundo em um 70B Q4. Competitivo com o M2 Ultra, mas não vencendo — apesar do dobro de RAM endereçável. Essa lacuna de largura de banda é toda a explicação.

O caminho iGPU ROCm existe e funciona para alguns modelos, mas ainda não está pronto para produção. Ollama faz roteamento through CPU. O backend Vulkan mostra promessa real como o caminho iGPU de curto prazo no Windows.

Onde o Ryzen genuinamente ganha: portabilidade, ecossistema Windows, e capacidade bruta de memória por dólar. Se você precisa de 128 GB de memória unificada sob $3K, não há outra opção. Essa é a máquina "cabe um modelo 70B na RAM e aceite velocidades M2 Ultra".

---

O AMD MI300X é extraordinário e completamente irrelevante para esta decisão de compra.

192 GB de memória HBM3. 5,3 TB/s de largura de banda — não gigabytes, terabytes. 80-120 tokens por segundo em um modelo 70B. Também $25.000 mínimo, apenas canal de vendas enterprise.

Pertence a este relatório para completude. Não pertence ao seu carrinho.

---

[ALLOY]: Aqui está a visão de fluxo de trabalho que recontextualiza tudo.

As tarefas de edição multi-arquivo — cinco ou mais templates de uma vez, refatorações grandes de codebase — representam talvez 20% da sua carga de trabalho total. Os outros 80% rodam limpos no hardware atual.

A pergunta não é "como lidar com meus trabalhos mais difíceis localmente?" É: "meus trabalhos mais difíceis devem ser locais?"

Devstral tem 262K contexto nativo no tier gratuito da API Mistral. Gemini 2.5 Pro tem 1 milhão de tokens de contexto. Para código não privado, esses modelos de nuvem são a ferramenta certa.

---

[NOVA]: Então aqui está o que eu realmente faria — agora com o quadro completo.

**Se você quer a melhor relação custo-benefício para trabalho diário de LLM no ecossistema Apple:** Mac Studio M3 Ultra 192 GB. A vantagem de largura de banda de memória é decisiva. Três vezes mais RAM, dobro da velocidade, mesma mesa. $4.000.

**Se você tem um orçamento apertado e precisa de capacidade máxima de memória acima de tudo** — você quer caber um modelo 70B na RAM, você está confortável no Windows, e velocidades M2 Ultra são aceitáveis — o Ryzen AI Max+ 395 em um Framework Desktop ou ROG Flow Z13 é genuinamente convincente a $2.000-2.500. Nada mais te dá 128 GB de memória unificada nesse preço.

**Se você especificamente quer o ecossistema de software CUDA e está confortável com Linux como máquina sidecar:** DGX Spark a $3.000 é o caminho. Unidade dupla escala para 405B se você precisar depois.

**E se você precisa de modelos de classe 405B rodando localmente hoje:** Mac Studio M3 Ultra 512 GB a $8-10.000 é o único caminho acessível para consumidores.

---

O teto de throughput agora não é o silício. É a configuração — e nós já corrigimos.

Deixe sua carga de trabalho real te dizer se você precisa de mais hardware. Essa é a resposta que a pesquisa voltou. E é uma resposta melhor que qualquer uma dessas caixas.

---

*[FIM DO EPISÓDIO 0]*
