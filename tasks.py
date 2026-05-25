from crewai import Task
from models import (
    DebateOpinion,
    DebateConsolidation,
    SementesOutput,
    ClassificacaoOutput,
    AnaliseEstruturalOutput,
    CenariosOutput,
    ConsistenciaOutput,
    RecomendacoesOutput,
    BrainstormingConsolidation
)
from agents import (
    coordenador_metodologia,
    ator_governo,
    ator_privado,
    ator_sociedade_civil,
    relator_debate,
    agente_extracao,
    agente_normalizacao,
    agente_sinais,
    agente_agrupamento,
    agente_classificador,
    agente_estruturacao,
    agente_cenarios,
    agente_consistencia,
    agente_analise_estrategica,
    agente_redator_relatorios,
    futurologista_fronteira,
    ficcionista_cenarios,
    voz_juventude,
    sintetizador_criativo
)

# --- FASE 0: IDEAÇÃO CRIATIVA E BRAINSTORMING DISRUPTIVO ---

task_brainstorming_disruptivo = Task(
    description=(
        "Como Futurologista de Fronteira, conduza uma sessão de brainstorming altamente disruptiva e fora do senso comum "
        "sobre a demanda inicial: '{demanda_inicial}'. "
        "Trabalhe em estreita simulação mental com as visões do Ficcionista de Cenários (humanização e cotidiano especulativo) "
        "e da Voz da Juventude (equidade intergeracional, resiliência climática e revolta socioecológica). "
        "Identifique e proponha pelo menos 4 ideias de ruptura radical, sinais fracos periféricos, dilemas éticos "
        "e eixos de mudança profunda que desafiem o status quo econômico e institucional convencional."
    ),
    expected_output="Registro de ideias disruptivas, rupturas conceituais e sinais de fronteira sobre o tema.",
    agent=futurologista_fronteira
)

task_consolidacao_criativa = Task(
    description=(
        "Como Sintetizador e Curador de Ideias Fora-da-Caixa, analise a sessão de brainstorming disruptivo. "
        "Filtre as ideias mais promissoras e impactantes. Consolide-as na estrutura formal exigida no PMV: "
        "identifique e detalhe cada ideia (com título, descrição, autor de origem e plausibilidade), "
        "agrupe-as em eixos de ruptura claros, e formule pelo menos 3 provocações críticas, dilemas éticos "
        "ou técnicos direcionados diretamente para forçar os atores setoriais convencionais (Governo, Privado e Sociedade) "
        "a repensarem suas posturas na Fase 1."
    ),
    expected_output="Consolidação estruturada de brainstorming criativo e rupturas com provocações críticas para os atores.",
    agent=sintetizador_criativo,
    output_pydantic=BrainstormingConsolidation
)


# --- FASE 1: DIRETRIZES E ATORES SETORIAIS (WORKSHOP) ---

# 1. Tarefa de Interpretação e Escopo da Demanda
task_interpretacao_demanda = Task(
    description=(
        "Analise de forma holística e crítica a demanda não estruturada de planejamento governamental fornecida pelo usuário: "
        "'{demanda_inicial}'. "
        "Defina e planeje os eixos estratégicos do estudo no PMV, estabelecendo o escopo do projeto, os objetivos macro e "
        "o horizonte temporal de análise. Essa diretriz servirá como orientação metodológica para o debate dos atores setoriais."
    ),
    expected_output="Diretrizes estruturadas de planejamento, escopo, horizontes e objetivos da prospecção para o PMV.",
    agent=coordenador_metodologia
)

# 2. Debate dos Atores (Workshop) - Ator Governo
task_debate_governo = Task(
    description=(
        "Como Representante Governamental, analise a demanda, as diretrizes de escopo elaboradas pelo coordenador, "
        "e as ideias disruptivas e provocações geradas na Fase Criativa 0. "
        "Você é OBRIGADO a abordar e responder diretamente a essas provocações disruptivas sob a ótica estatal! "
        "Defenda o posicionamento do governo no PMV: priorize a regulação setorial, a estabilidade de políticas públicas de longo prazo, "
        "o impacto fiscal e a equidade social. Apresente seus argumentos, preocupações de risco e oportunidades futuras de base estatal "
        "com base exclusivamente em seu conhecimento endógeno (da LLM) sobre transições e em resposta aos dilemas e eixos de ruptura da Fase 0."
    ),
    expected_output="Posicionamento e opinião detalhada do Ator Público sobre a demanda e as provocações no PMV.",
    agent=ator_governo,
    output_pydantic=DebateOpinion
)

# 3. Debate dos Atores (Workshop) - Ator Privado
task_debate_privado = Task(
    description=(
        "Como Líder do Setor Privado, analise a demanda, as diretrizes do coordenador, "
        "e as ideias disruptivas e provocações geradas na Fase Criativa 0. "
        "Você é OBRIGADO a abordar e responder diretamente a essas provocações disruptivas sob a ótica de mercado! "
        "Defenda o posicionamento do empresariado no PMV: exija desburocratização, segurança jurídica para investimentos, "
        "fomento à inovação de mercado e ganhos de produtividade tecnológica. Apresente seus argumentos e visões de riscos e "
        "oportunidades de mercado em resposta aos dilemas e eixos de ruptura da Fase 0."
    ),
    expected_output="Posicionamento e opinião detalhada do Ator Privado sobre a demanda e as provocações no PMV.",
    agent=ator_privado,
    output_pydantic=DebateOpinion
)

# 4. Debate dos Atores (Workshop) - Ator Sociedade Civil
task_debate_sociedade = Task(
    description=(
        "Como Representante da Sociedade Civil e Especialistas, analise a demanda, as diretrizes do coordenador, "
        "e as ideias disruptivas e provocações geradas na Fase Criativa 0. "
        "Você é OBRIGADO a abordar e responder diretamente a essas provocações sob a ótica da sustentabilidade e equidade! "
        "Defenda os direitos humanos, a sustentabilidade ecológica integral, a justiça social e a governança participativa no PMV. "
        "Apresente seus argumentos éticos e científicos sobre riscos sistêmicos e oportunidades socioambientais em resposta aos dilemas e eixos de ruptura da Fase 0."
    ),
    expected_output="Posicionamento e opinião detalhada da Sociedade Civil e Academia sobre a demanda e as provocações no PMV.",
    agent=ator_sociedade_civil,
    output_pydantic=DebateOpinion
)

# 5. Consolidação do Debate
task_consolidacao_debate = Task(
    description=(
        "Como Relator do Debate, acompanhe a discussão e as opiniões registradas pelos três atores setoriais (Governo, Privado, Sociedade Civil). "
        "Sintetize os posicionamentos do workshop de atores do PMV. Destaque de forma neutra os pontos de consenso explícitos "
        "e as áreas de atrito, fricção ou polarização intensa (divergências), além de insights analíticos gerados no debate."
    ),
    expected_output="Relatório gerencial consolidado do workshop de debate dos atores do PMV.",
    agent=relator_debate,
    output_pydantic=DebateConsolidation
)

# 6. Extração de Evidências
task_extracao_evidencias = Task(
    description=(
        "Como Agente de Extração, analise o relatório consolidado do debate de atores. "
        "Extraia e organize de forma crua, sem fazer conjecturas adicionais, todas as evidências factuais, depoimentos chaves, "
        "sinais de mudança e dados implícitos levantados no workshop. Mantenha a rastreabilidade do ator de origem."
    ),
    expected_output="Inventário estruturado de evidências factuais e falas relevantes do debate do PMV.",
    agent=agente_extracao
)

# 7. Normalização Conceitual
task_normalizacao = Task(
    description=(
        "Como Agente de Normalização Conceitual, padronize os termos e conceitos prospectivos extraídos, "
        "garantindo que se diferencie claramente evidência de simulação. Destaque ambiguidades terminológicas no PMV "
        "sem alterar o sentido original dos depoimentos e dos dados base."
    ),
    expected_output="Relatório conceitual normalizado e lista de termos ambíguos saneados para o PMV.",
    agent=agente_normalizacao
)

# 8. Mapeamento de Sementes e Sinais Fracos
task_mapeamento_sementes = Task(
    description=(
        "Como Agente de Sinais, utilize as evidências normalizadas do debate e a especialização da sua LLM para identificar "
        "sementes de futuro (sinais fracos, indícios de rupturas, inovações conceituais). "
        "Atribua a cada semente de futuro uma pontuação quantitativa de Confiança variando de 0.0 a 1.0. "
        "A Confiança representa o nível de robustez científica, social ou empírica que respalda a semente (onde 0.1-0.3 "
        "indica Confiança Baixa: sinal incipiente com fraca evidência; 0.4-0.6 indica Confiança Média: tendências em "
        "formação com evidência empírica parcial; e 0.7-1.0 indica Confiança Alta: megatendências ou fatos consolidados "
        "com forte base teórica e de dados). Rastreie a origem do ator que mencionou/gerou a semente. "
        "Regra: Você não pode gerar condicionantes nesta etapa."
    ),
    expected_output="Inventário estruturado de sementes de futuro com justificativa conceitual do grau de confiança no PMV.",
    agent=agente_sinais,
    output_pydantic=SementesOutput
)

# 9. Agrupamento em Eventos no Horizonte
task_agrupamento_eventos = Task(
    description=(
        "Como Especialista em Agrupamentos, processe o inventário de sementes de futuro. "
        "Correlacione os sinais e os agrupe em Eventos no Horizonte significativos para o tema. "
        "Estime o horizonte temporal provável de maturação (Curto, Médio ou Longo prazo) e o impacto bruto estimado de cada evento no PMV."
    ),
    expected_output="Lista de eventos no horizonte formados pelo agrupamento analítico de sementes.",
    agent=agente_agrupamento
)

# 10. Classificação em Elementos de Futuro (GATE 1)
# O gate humano físico é bypassado nesta execução automatizada, gerando-se o arquivo gate_elementos.md para auditoria.
task_classificacao_elementos = Task(
    description=(
        "Como Classificador Prospectivo, avalie os eventos no horizonte e os categorize em Elementos de Futuro formais "
        "(tendência, incerteza, ruptura, driver, megatendência, sinal fraco, fato predeterminado ou curinga). "
        "Para cada elemento, calcule a Confiança metodológica geral do enquadramento (de 0.0 a 1.0) combinando a "
        "confiança das sementes originais com a robustez lógica de sua evolução temporal. Forneça uma justificativa conceitual "
        "clara e rigorosa, definindo explicitamente o significado do indicador de confiança adotado para dar transparência ao tomador de decisão. "
        "Aponte casos duvidosos como pendências de validação conceitual."
    ),
    expected_output="Classificação sistemática de Elementos de Futuro com justificativas rigorosas e notas explicativas sobre Confiança no PMV.",
    agent=agente_classificador,
    output_pydantic=ClassificacaoOutput
)

# 11. Análise Estrutural e Matrizes (Matriz de Impacto Cruzado e Motricidade)
task_analise_estrutural = Task(
    description=(
        "Como Analista de Matrizes, execute a análise estrutural dos Elementos de Futuro. "
        "1. Calcule a Matriz de Impacto e Incerteza (pontuação e quadrante de cada elemento).\n"
        "2. Monte a Matriz de Impacto Cruzado direta entre os elementos (N x N, mapeando o grau de influência de A sobre B).\n"
        "3. Calcule o grau de Motricidade e Dependência de cada elemento para classificá-los em motores, de enlace, dependentes ou autônomos.\n"
        "Derive os Condicionantes de Futuro críticos exclusivamente das variáveis que se posicionarem como motores ou de alta incerteza/alto impacto."
    ),
    expected_output=(
        "Resultados analíticos detalhados contendo a matriz de impacto cruzado (grid), "
        "avaliação de motricidade/dependência e os condicionantes de futuro candidatos para o PMV."
    ),
    agent=agente_estruturacao,
    output_pydantic=AnaliseEstruturalOutput
)

# 12. Validação de Condicionantes (GATE 2)
# Executada imediatamente pós-análise estrutural. Gera o gate_condicionantes.md para validação humana.
task_proposta_condicionantes = Task(
    description=(
        "Revise analiticamente os condicionantes de futuro candidatos propostos pela análise estrutural. "
        "Descreva os possíveis estados plausíveis (bifurcações) que cada condicionante de futuro pode assumir no horizonte temporal. "
        "Garanta a rastreabilidade metodológica estrita de cada condicionante para as matrizes estruturais de origem."
    ),
    expected_output="Condicionantes de futuro consolidados com estados plausíveis mapeados no PMV.",
    agent=agente_estruturacao
)

# 13. Metodologia de Cenários e Narrativas
task_geracao_cenarios = Task(
    description=(
        "Como Projetista de Cenários, utilize os condicionantes de futuro aprovados e seus estados para construir "
        "um conjunto de Cenários Prospectivos alternativos, plausíveis e contrastantes (ex: Otimista, Pessimista, Contrastante/Ruptura). "
        "Atenção crítica à coerência sistêmica: garanta que as combinações de estados de condicionantes e as trajetórias "
        "de variáveis em cada cenário sejam matematicamente e logicamente plausíveis entre si, eliminando contradições internas "
        "(ex.: um cenário com baixo investimento estatal não pode, ao mesmo tempo, prever uma infraestrutura pública de ponta). "
        "Justifique detalhadamente a escolha metodológica adotada (e.g., Eixos de Schwartz ou Impacto Cruzado). Redija narrativas "
        "ricas, aprofundadas e altamente explicativas sobre o estado futuro, o comportamento estratégico detalhado dos atores "
        "e a plausibilidade de cada cenário no PMV."
    ),
    expected_output="Arcabouço conceitual expandido e narrativas ricas e consistentes dos cenários prospectivos alternativos.",
    agent=agente_cenarios,
    output_pydantic=CenariosOutput
)

# 14. Auditoria de Consistência (GATE 3 - Consistência HITL)
# Audita logicamente e gera gate_consistencia.md antes das recomendações estratégicas.
task_consistencia_cenarios = Task(
    description=(
        "Como Auditor de Consistência, avalie com máximo rigor metodológico as narrativas e dados de todos os cenários gerados. "
        "Audite a coerência lógica interna cruzada (ex: se atores não agem de forma logicamente implausível, "
        "se estados de condicionantes incompatíveis não foram agrupados de forma indevida). Aponte contradições formais, "
        "premissas frágeis, lacunas estruturais de informação e emita o veredicto de consistência lógica do PMV. "
        "Forneça orientações detalhadas e fundamentadas sobre os pontos de fricção lógica analisados."
    ),
    expected_output="Laudo analítico robusto de consistência lógica interna e auditoria detalhada de cenários no PMV.",
    agent=agente_consistencia,
    output_pydantic=ConsistenciaOutput
)

# 15. Recomendações Estratégicas e Pontes de Decisão
task_recomendacoes_estrategicas = Task(
    description=(
        "Como Formulador Estratégico, elabore as recomendações finais contingentes do PMV para o tema proposto. "
        "Desenhe as Recomendações acopladas a cada cenário construído. "
        "Para cada recomendação, mapeie as Pontes de Decisão críticas, definindo gatilhos (triggers) operacionais e "
        "ações imediatas para mitigar riscos ou capturar oportunidades de futuro. "
        "Garanta rastreabilidade absoluta para os condicionantes e dados de origem, e conclua com uma mensagem gerencial de fechamento do PMV."
    ),
    expected_output="Relatório gerencial de recomendações estratégicas e pontes de decisão no PMV.",
    agent=agente_analise_estrategica,
    output_pydantic=RecomendacoesOutput
)

# 16. Redação do Relatório Final de Prospecção Estratégica (Até 10 Páginas)
task_relatorio_final = Task(
    description=(
        "Como Redator Sênior e Consolidador de Relatórios, revise criticamente o andamento de todo o estudo prospectivo "
        "com base nos contextos e saídas acumulados das etapas anteriores:\n"
        "1. A demanda inicial e diretrizes metodológicas do coordenador.\n"
        "2. Os consensos e divergências setoriais extraídos do workshop de atores.\n"
        "3. Os elementos de futuro e sementes de sinais fracos classificados.\n"
        "4. Os condicionantes de futuro críticos derivados das matrizes estruturais.\n"
        "5. As narrativas lógicas dos cenários construídos e sua auditoria de consistência.\n"
        "6. As recomendações contingentes formuladas e pontes de decisão (gatilhos estratégicos).\n\n"
        "Elabore uma redação científica editorial de altíssimo nível em português. Escreva o resumo executivo formal "
        "do PMV, conduza uma análise transversal conectando o percurso analítico desde a demanda inicial às recomendações "
        "finais, e formule as conclusões gerais do estudo estratégico prospectivo."
    ),
    expected_output="Relatório final consolidado contendo resumo executivo, análise transversal e conclusões de alto nível para o PMV.",
    agent=agente_redator_relatorios
)
