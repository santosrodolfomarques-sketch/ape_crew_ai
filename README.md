# PMV - Sistema Modular de Análise Prospectiva e Geração de Cenários com IA

Um ecossistema multiagente baseado em **CrewAI** e **Google Gemini** para conduzir rodadas completas de análise prospectiva, desde o acolhimento de uma demanda desestruturada de planejamento governamental até a geração de relatórios executivos premium em PDF.

## 🚀 Visão Geral

O projeto implementa o **Funil Prospectivo Metodológico v5**, utilizando conhecimento endógeno de LLMs para simular debates entre atores governamentais, privados e da sociedade civil. O sistema produz automaticamente:
- 💡 **Fase 0 (Ideação Criativa)**: Agentes disruptivos mitigando o viés do "senso comum" com sinais de fronteira e provocações estruturadas.
- 📊 **Análise Estrutural e Matrizes**: Cálculo iterativo de impacto, incerteza, motricidade e dependência.
- 🔮 **Cenários Prospectivos**: Narrativas plausíveis, consistentes e homologadas por agentes auditores independentes.
- 📑 **Relatórios Premium**: Conversão automática de logs de execução e outputs de fases em documentos PDF elegantes com paginação, esquemas visuais e design corporativo.
- 💰 **Monitor de Custos**: Rastreamento em tempo real do consumo volumétrico de tokens (Flash vs. Pro) faturado e convertido para BRL na finalização da orquestração.

## ⚙️ Arquitetura e Fluxo de Trabalho

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
