# Fluxo de Trabalho do Projeto APE Crew AI

## Visão Geral

O projeto `ape_crew_ai` implementa um fluxo de análise prospectiva multiagente em Python, organizado em fases sucessivas. A execução começa no ponto de entrada `main.py`, que prepara o ambiente, organiza a pasta de saída da rodada e inicia a orquestração principal definida em `crew.py`.

O objetivo do fluxo é transformar uma demanda inicial em um conjunto de entregáveis estruturados:

- log de execução em Markdown e PDF
- arquivos de gate para auditoria metodológica
- relatórios consolidados por fase
- relatório final executivo

## Etapa 1: Entrada Da Demanda

O fluxo começa em `main.py`.

1. O programa recebe a demanda por argumento de linha de comando ou via entrada interativa.
2. É criado um diretório isolado dentro de `analises/`, com timestamp e slug da demanda.
3. O sistema configura a pasta de saída global usada pela orquestração.
4. A execução passa a ser registrada em um log Markdown com duplicação da saída do console.

### Arquivos envolvidos

- `main.py`
- `analises/<rodada>/log_execucao_pmv.md`

## Etapa 2: Inicialização Da Orquestração

Ainda em `main.py`, a classe `AnaliseProspectivaCrew` é instanciada com a demanda inicial.

Em seguida:

1. `crew.py` recebe a demanda.
2. O fluxo configura os contextos entre tarefas dependentes.
3. A `Crew` é criada em modo sequencial.
4. As tarefas são executadas na ordem definida no pipeline.

### Arquivos envolvidos

- `crew.py`
- `tasks.py`
- `agents.py`

## Etapa 3: Fase 0 - Ideação Criativa

A primeira fase do trabalho é a ideação disruptiva.

1. O agente de fronteira realiza brainstorming sobre a demanda inicial.
2. As ideias são consolidadas em uma estrutura formal.
3. O resultado gera insumos para provocar o debate dos atores setoriais.

### Saídas principais

- eixos de ruptura
- ideias fora da caixa
- provocações para os atores
- relatório PDF da Fase 0

### Arquivos envolvidos

- `tasks.py`
- `pdf_generator.py`

## Etapa 4: Fase 1 - Workshop De Atores

Nesta fase, o sistema simula um debate estruturado entre três perspectivas:

- governo
- setor privado
- sociedade civil

O coordenador metodológico define o escopo e orienta o debate. Depois disso:

1. Cada ator produz sua opinião setorial.
2. O relator consolida consensos, divergências e insights.
3. O sistema extrai evidências do debate.
4. As evidências são normalizadas.
5. Sementes de futuro são identificadas.
6. Os sinais são agrupados em eventos no horizonte.
7. Os eventos são classificados em elementos de futuro.

### Saídas principais

- consolidação do debate
- sementes de futuro
- eventos no horizonte
- classificação de elementos
- `gate_elementos.md`
- relatório PDF da Fase 1

## Etapa 5: Fase 3 - Análise Estrutural

Depois da classificação, o fluxo avança para a análise estrutural.

1. Os elementos de futuro entram em matrizes de impacto e incerteza.
2. O sistema calcula motricidade e dependência.
3. É gerada a matriz de impacto cruzado.
4. A partir dessa análise, surgem condicionantes de futuro.

### Saídas principais

- matriz de impacto x incerteza
- matriz de motricidade x dependência
- matriz de impacto cruzado
- condicionantes de futuro
- `gate_condicionantes.md`
- relatório PDF das matrizes estruturais

## Etapa 6: Fase 2 - Cenários

Com os condicionantes definidos, o sistema passa para a construção de cenários prospectivos.

1. Os condicionantes são combinados em narrativas alternativas.
2. A metodologia de cenarização é explicitada.
3. Os cenários são redigidos com coerência interna.
4. Um auditor de consistência verifica contradições, lacunas e premissas frágeis.

### Saídas principais

- cenários alternativos
- auditoria de consistência
- `gate_consistencia.md`
- recomendações estratégicas
- relatório PDF da Fase 2

## Etapa 7: Relatório Final

A última tarefa consolida todo o estudo.

1. O redator sênior recebe o contexto acumulado das fases anteriores.
2. É produzido um resumo executivo.
3. É gerada uma análise transversal conectando a demanda inicial aos resultados.
4. O documento final fecha o ciclo metodológico do projeto.

### Saídas principais

- relatório final prospectivo
- painel de custos e tokens
- PDF consolidado da execução

## Papel Dos Arquivos Principais

### `main.py`

- ponto de entrada da aplicação
- cria a pasta da rodada
- registra log de execução
- inicializa a orquestração
- converte o log em PDF

### `crew.py`

- define a orquestração principal
- conecta agentes e tarefas
- administra callbacks de geração de arquivos
- cria os arquivos de gate e relatórios intermediários

### `tasks.py`

- declara todas as tarefas do pipeline
- organiza as fases do estudo
- define entradas, saídas esperadas e vínculos entre tarefas

### `models.py`

- define os schemas Pydantic
- estrutura a saída esperada de cada fase
- garante padronização dos dados entre agentes

### `pdf_generator.py`

- converte dados consolidados em documentos PDF
- produz relatórios por fase e relatório final
- formata a saída em estilo técnico e executivo

### `agents.py`

- concentra os agentes especializados
- define perfis, papéis e especializações do fluxo multiagente

## Fluxo Resumido

```text
main.py
  -> cria pasta da análise
  -> registra log
  -> instancia AnaliseProspectivaCrew
    -> Fase 0: ideação criativa
    -> Fase 1: workshop de atores
    -> extração e normalização
    -> mapeamento de sementes
    -> classificação de elementos
    -> análise estrutural
    -> construção de cenários
    -> auditoria de consistência
    -> recomendações estratégicas
    -> relatório final
  -> gera PDFs e arquivos Markdown de auditoria
```

## Entregáveis Finais

Ao final da execução, a pasta da análise contém, em geral:

- `log_execucao_pmv.md`
- `log_execucao_pmv.pdf`
- `gate_elementos.md`
- `gate_condicionantes.md`
- `gate_consistencia.md`
- relatórios PDF das fases
- relatório final prospectivo

## Observação Final

O fluxo foi desenhado para ser rastreável, modular e auditável. Cada fase gera saídas intermediárias reutilizáveis, o que facilita revisão humana, geração de relatórios e diagnóstico do processo prospectivo como um todo.
