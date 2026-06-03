# PMV - Sistema Modular de Análise Prospectiva e Geração de Cenários com IA

Um ecossistema multiagente baseado em **CrewAI** e **Google Gemini** para conduzir rodadas completas de análise prospectiva, desde o acolhimento de uma demanda desestruturada de planejamento governamental até a geração de relatórios executivos premium em PDF.

## 🚀 Visão Geral

O projeto implementa o **Funil Prospectivo Metodológico v5** orquestrado via **CrewAI Flows**, organizando o pipeline de 18 tarefas em 6 Crews modulares sob um estado centralizado e tipado (`AnaliseState` com Pydantic). O sistema produz automaticamente:
- 💡 **Fase 0 (Ideação Criativa)**: Agentes disruptivos mitigando o viés do "senso comum" com sinais de fronteira e provocações estruturadas.
- 🗣️ **Fase 1 (Workshop de Atores)**: Debate híbrido avançado, rodando a coleta de opiniões dos atores setoriais em paralelo (`asyncio.gather`) e realizando a consolidação sob uma estrutura hierárquica coordenada pelo Relator (`Process.hierarchical`).
- 📊 **Análise Estrutural e Matrizes**: Cálculo de impacto, incerteza, motricidade e dependência.
- 🔮 **Cenários Prospectivos (Loop de Correção)**: Geração de narrativas plausíveis acoplada a um loop de auto-correção iterativo com o Auditor de Consistência. Se detectadas incoerências lógicas, os cenários são regenerados de forma autônoma (limite de 3 tentativas) a partir do feedback estruturado.
- 📑 **Relatórios Premium**: Geração de logs de execução e outputs de fases em documentos PDF elegantes baseados em `ReportLab`.
- 💰 **Monitor de Custos**: Rastreamento em tempo real do consumo de tokens faturado e convertido para BRL na finalização da orquestração.

## ⚙️ Arquitetura e Fluxo de Trabalho

O pipeline segue um fluxo de eventos orquestrado pelo `AnaliseProspectivaFlow`:
1. **`start_ideacao`** -> Inicializa a ideação com o brainstorming disruptivo.
2. **`debate_phase`** -> Executa o debate setorial paralelo e consolida com Crew Hierárquico.
3. **`classification_phase`** -> Saneamento conceitual e classificação de elementos.
4. **`structural_analysis_phase`** -> Construção de matrizes e definição de condicionantes.
5. **`generate_scenarios`** <-> **`audit_consistency`** -> Loop de consistência de cenários mediado por um router de auditoria.
6. **`recommendations_phase`** -> Geração de recomendações e pontes de decisão.
7. **`final_report_phase`** -> Geração do relatório final e monitor de custos.

Para entender a fundo a dinâmica de cada fase da metodologia, bem como o papel de cada agente especializado e das tarefas interconectadas, consulte a documentação detalhada da arquitetura:
👉 **[FLUXO_DE_TRABALHO.md](./FLUXO_DE_TRABALHO.md)**

## 🛠️ Pré-requisitos e Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/santosrodolfomarques-sketch/ape_crew_ai.git
   cd ape_crew_ai
   ```

2. **Crie e ative o ambiente virtual (Recomendado):**
   No Windows (PowerShell):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Instale as dependências:**
   ```powershell
   pip install -r requirements.txt
   ```

## 🔑 Configuração (API Key)

O sistema utiliza os motores do Google Gemini (`gemini-3.5-flash` e `gemini-2.5-pro`). Para interagir adequadamente com a API, você precisa configurar sua credencial:
1. Crie um arquivo com o nome exato **`.env`** na raiz do projeto (fique tranquilo, ele será ignorado pelo git).
2. Adicione sua chave de desenvolvedor no formato abaixo:
   ```env
   GEMINI_API_KEY=sua_chave_real_aqui
   ```

## ▶️ Como Executar a Análise

No terminal, com o ambiente virtual ativado e a chave configurada, chame o arquivo de inicialização:
```powershell
python main.py
```
- O sistema exibirá o banner e perguntará interativamente se você deseja usar a **demanda padrão** ou se prefere fornecer um **problema customizado**.
- Ao aceitar, o PMV gerará isoladamente todas as saídas (Planilhas CSV, Markdown Gates de auditoria, PDFs metodológicos e histórico completo de terminal) em um novo subdiretório `analises/analise_<data_hora>_<slug_da_demanda>/`, mantendo seu ambiente de código perfeitamente limpo.

## 📂 Estrutura Principal de Arquivos

- `main.py`: Ponto de entrada iterativo, construtor de pastas isoladas, verificador de credenciais e gravador do espelho em log (`Tee`).
- `crew.py`: Orquestrador mestre do pipeline da CrewAI, implementando callbacks assíncronos para PDFs e o monitor dinâmico de tokens.
- `agents.py`: Backstories e parametrização dos 19 agentes com identidades e comportamentos lógicos delimitados.
- `tasks.py`: Orquestração sequencial de entradas, saídas via Pydantic e relacionamentos de dependência mútua (contexto) entre as 18 tarefas.
- `models.py`: Schemas Pydantic tipados que forçam a consistência de output matemático e estrutural do LLM.
- `pdf_generator.py`: Motor de design baseado em `ReportLab` garantindo paletas de cores institucionais, "NumberedCanvas" dinâmicos e grid de callouts e tabelas auto-ajustáveis.

---
*Este ecossistema foi construído e documentado com foco em rastreabilidade sistêmica e inovação na análise prospectiva estratégica.*
