OPENCLAW DAILY - EPISODE 035 - April 20, 2026

[00:00] GANCHO
A maioria das pessoas que estão comprando uma máquina de IA local agora está buscando o dispositivo mais impressionante, não aquele menos passível de arrependimento.
Este episódio reformula toda a decisão em torno de um comprador:
alguém que já vive no macOS, já usa dois Macs, e quer uma IA local séria sem comprar uma máquina que é incrível no papel e irritante na vida real.

[02:30] AS MÁQUINAS NA MESA
- Nvidia DGX Spark como a menor caixa de mesa séria compatível com CUDA
- DGX Station / hardware Nvidia de mesa da classe Thor como a grande máquina de referência
- AMD Strix Halo / Ryzen AI Max+ 395 como a opção x86 intermediária promissora
- Mac mini e Mac Studio da Apple como o caminho de menor fricção para quem prefere Mac
- Rumores sobre desktops M5 como contexto de timing, não como lógica de compra

[07:00] A LENTE DOS BENCHMARKS QUE REALMENTE IMPORTA
A hierarquia para compra de LLM local é geralmente:
1. capacidade do modelo em memória rápida
2. largura de banda da memória
3. maturidade do ecossistema de software
4. computação bruta

Limiares aproximados práticos para inferência local:
- 7B a 8B: aproximadamente 4 a 6GB
- 13B a 14B: aproximadamente 8 a 12GB
- 32B: aproximadamente 18 a 24GB
- 70B: aproximadamente 35 a 45GB
- Classe 120B+: frequentemente 60GB e acima antes de overhead

Ponto principal:
memória utilizável e compatibilidade de software vencem o drama de marketing.

[14:30] O CAMINHO DA APPLE
O Mac mini continua sendo o ponto de entrada mais simples e com menor fricção se o objetivo é ter IA local útil em uma máquina que ainda parece apenas um Mac.

O Mac Studio é o verdadeiro centro de gravidade:
- a resposta equilibrada é o nível Studio que oferece memória unificada suficiente para trabalho local verdadeiramente sério sem sacrificar o resto da experiência Mac
- a configuração Studio com mais memória é a opção Apple mais forte para o ouvinte que quer os maiores modelos possíveis em memória enquanto permanece no macOS

A vantagem da Apple não é "vencer todo benchmark de CUDA."
É:
- hardware silencioso
- grandes pools de memória unificada
- largura de banda forte
- um fluxo de trabalho diário familiar
- suporte crescente de MLX / LM Studio / Ollama no Mac

O caso de esperar pelo M5 é razoável apenas se os Macs atuais ainda estão bons e o gargalo real é ansiedade de timing, não capacidade real.

[22:00] O CAMINHO DA NVIDIA
O DGX Spark importa porque a pilha de software é o produto.
Se a carga de trabalho especificamente precisa de compatibilidade nativa com CUDA, repositórios Nvidia-first, caminhos estilo TensorRT, ou continuidade local-datacenter, o Spark faz sentido imediato.

O DGX Spark é mais forte como uma compra de compatibilidade, não automaticamente como uma compra de valor.

O DGX Station e a ideia mais ampla de hardware Nvidia de mesa da classe Thor são impressionantes, mas principalmente úteis como ponto de referência.
Eles mostram como é o alto desempenho, mas não são a recomendação sensata padrão para a maioria dos indivíduos.

Alternativas Nvidia de menor custo ainda importam:
- boxes RTX 3090 usados
- builds GeForce mais recentes
- rotas de GPU workstation de 48GB

Essas frequentemente vencem o argumento de CUDA-por-dólar enquanto perdem o argumento de estilo de vida em ruído, energia e fricção.

[29:30] A AMD E O VEREDITO FINAL
Sistemas da classe Ryzen AI Max+ 395 / Strix Halo são atraentes porque apontam para:
- sistemas x86 compactos
- gráficos integrados fortes
- uma filosofia de design mais semelhante à memória unificada
- valor potencialmente muito atraente

Mas a AMD ainda parece mais a escolha inteligente do entusiasta do que o padrão entediante para o público geral.

Recomendação final:
- espere a menos que haja um gargalo real de IA local
- se comprando agora como generalista que prefere Mac, escolha Mac Studio
- compre DGX Spark apenas se compatibilidade com CUDA for o motivo
- mantenha AMD Strix Halo na lista de observação
- ignore hardware de fantasia de DGX station gigante a menos que o orçamento e o caso de uso sejam realmente extremos

Resumo em uma linha:
Se você já está feliz no Mac, compre mais Mac por conveniência, compre Nvidia apenas para CUDA, e mantenha a AMD na lista de observação.