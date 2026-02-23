# Episode 0: Hardware Deep Dive - Corrigindo Falhas de Modelos Locais
**Data:** 18 de fevereiro de 2026
**Duração:** 11:45
**Apresentadores:** Nova & Alloy

---

## NOTAS DO PROGRAMA

### Tópicos Abordados

1. **O Bug de Estouro de Contexto** — Clarity (agente de codificação, Qwen3-Coder-30B) repetidamente encontrou erros de estouro de contexto no meio das tarefas. Causa raiz: uma definição de modelo Ollama rotulada `v-128k` que limitava o contexto a 131.072 tokens, enquanto o modelo suporta nativamente 262.144 tokens. Um rótulo de configuração do dia de configuração tornou-se um limite rígido por acidente.

2. **A Matemática do Timeout** — Em 18 de fevereiro às 11:15, 146.760 tokens foram solicitados contra um limite de 131.072 tokens. Com velocidade de pré-preenchimento de ~400 tokens/seg, processar 146K tokens leva 6+ minutos. O limite de timeout era 5 minutos. Três hits consecutivos — não travamentos, não instabilidade — perfeitamente explicados pela aritmética.

3. **Arquitetura de Memória do Qwen3-Coder** — Qwen3-Coder 30B é um modelo Mixture-of-Experts com apenas 4 heads de atenção KV (vs. 8 para LLaMA-3 8B). Em contexto 262K: ~15 GB de pesos do modelo + ~24 GB de cache KV + overhead do SO ≈ 44 GB no total. Uma máquina com 64 GB de memória unificada tem 20 GB de folga. O hardware estava fine o tempo todo.

4. **Opção de Hardware 1: NVIDIA DGX Spark ($3.000)** — Chip GB10 Grace Blackwell, 128 GB LPDDR5X, 273 GB/s de largura de banda de memória. Contrariamente à intuição, menor largura de banda que um Mac Studio M2 Ultra (~800 GB/s). Compensa via núcleos tensores FP4 (25-50 tok/s em 70B vs. 10-15 atualmente). Linux apenas como sidecar; vincule duas unidades por $6K para rodar modelos 405B+.

5. **Opção de Hardware 2: Mac Studio M3 Ultra** — $4.000 (192 GB) a $8-10K (512 GB). Largura de banda: 819 GB/s — 2,1× mais rápido que M2 Ultra segundo benchmarks da Apple. 20-32 tok/s em modelos 70B. Configuração de 192 GB permite carregamento simultâneo de modelos 30B + 70B sem swapping. Configuração de 512 GB é o único caminho de consumidor para rodar LLaMA 3.1 405B localmente.

6. **Opção de Hardware 3: AMD** — duas histórias muito diferentes:
   - *Threadripper + dual RX 7900 XTX ($5-6K)*: Problema de VRAM dividido, ROCm atrasado em relação a CUDA. Recusa veemente.
   - *Ryzen AI Max+ 395 "Strix Halo" ($2.000-$2.500)*: A resposta da AMD à arquitetura Apple Silicon — CPU/GPU/NPU memória unificada até 128 GB LPDDR5X. Framework Desktop AMD ou ASUS ROG Flow Z13. Largura de banda de memória é 256 GB/s (bus de 256 bits), ~3× menor que M2 Ultra — velocidades competitivas apesar do dobro de RAM endereçável. Melhor caminho orçamento para 128 GB de memória unificada, ponto.
   - *AMD MI300X ($25K, enterprise)*: 192 GB HBM3, 5,3 TB/s de largura de banda, 80-120 tok/s em 70B. Mencionado para完整性; não é compra de consumidor.

7. **Estratégia de Fluxo de Trabalho: Híbrido Local + Nuvem** — Editagens multi-arquivo pesadas (5+ templates, refatorações grandes de codebase) representam ~20% da carga total de trabalho. Para código não privado: Devstral oferece 262K contexto nativo no tier gratuito da API Mistral; Gemini 2.5 Pro oferece 1 milhão de tokens. A pergunta certa não é "como rodar meus trabalhos mais difíceis localmente?" — é "meus trabalhos mais difíceis devem ser locais?"

8. **A Correção** — Patch de configuração + nova definição de modelo Ollama para desbloquear a janela de contexto 262K completa. Feito ao vivo durante a pesquisa. Custo zero.

### Recursos de Hardware
- [Apple Mac Mini](https://www.apple.com/mac-mini/) - Recomendado para IA local
- [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) - Opção orçamento
- [Ollama](https://ollama.com) - Runtime LLM local

---

### Principais Conclusões

1. **Um rótulo de modelo não é um teto de capacidade.** O nome do modelo Ollama `qwen3-coder:30b-262k` disse a verdade; o rótulo do momento de criação não. Sempre verifique a configuração de janela de contexto contra a especificação real do modelo.
2. **Geração de tokens é limitada por largura de banda de memória, não por computação.** O DGX Spark tem menos largura de banda de memória que um Mac Studio. Largura de banda é o gargalo — sempre verifique GB/s, não apenas GB.
3. **Strix Halo (Ryzen AI Max+ 395) é o caminho mais barato para 128 GB de memória unificada.** Nada mais se接近a sob $3K. A compensação é ~3× menos largura de banda que Apple Silicon.
4. **Diagnostique antes de comprar.** Três camadas de configuração errada (limite de contexto errado + timeout muito curto + limite do modelo excedido) pareceram falha de hardware. Eram totalmente corrigíveis por configuração.
5. **O split híbrido local/nuvem é a alavanca de eficiência real.** Desloque os 20% de tarefas pesadas de contexto não privadas para Devstral ou Gemini 2.5 Pro. Rode os outros 80% localmente onde a privacidade importa.

---

### Recursos e Links

| Item | Detalhes |
|------|----------|
| **Qwen3-Coder 30B** | Ollama: `ollama pull qwen3-coder:30b-262k` |
| **NVIDIA DGX Spark** | $3.000 — nvidia.com/en-us/project-digits |
| **Mac Studio M3 Ultra** | $3.999 (192 GB) / $7.999+ (512 GB) — apple.com |
| **AMD Ryzen AI Max+ 395** | Framework Desktop AMD Edition ~$2.000-$2.500 |
| **ASUS ROG Flow Z13** | $2.499 — Ryzen AI Max+ 395, até 128 GB |
| **AMD MI300X** | $25.000+ enterprise — apenas para referência |
| **Devstral** | 262K contexto, tier gratuito — mistral.ai |
| **Gemini 2.5 Pro** | 1M contexto — aistudio.google.com |
| **llama.cpp** | Backend de inferência CPU — github.com/ggerganov/llama.cpp |
| **Ollama** | Runtime de modelo local — ollama.com |
