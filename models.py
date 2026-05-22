from __future__ import annotations
from typing import Any, List, Dict
from pydantic import BaseModel, Field

# --- FASE 1: ATORES E DEBATE (WORKSHOP) ---

class Ator(BaseModel):
    id: str = Field(..., description="Identificador único do ator.")
    nome: str = Field(..., description="Nome do ator ou grupo setorial.")
    papel: str = Field(..., description="Papel institucional ou econômico.")
    interesses: List[str] = Field(default_factory=list, description="Lista de interesses ou objetivos principais no setor.")
    recursos: List[str] = Field(default_factory=list, description="Recursos críticos controlados (financeiro, regulatório, etc.).")
    coalizoes: List[str] = Field(default_factory=list, description="Atores com quem estabelece coalizão ou aliança.")
    capacidade_influencia: float = Field(..., description="Poder de influência estimado no setor (escala de 0.0 a 1.0).")
    postura_inicial: str = Field(..., description="Postura inicial em relação ao tema (favorável, neutro, oposição, etc.).")

class AtorSetorialList(BaseModel):
    atores: List[Ator] = Field(..., description="Lista de atores identificados para o tema.")

class DebateOpinion(BaseModel):
    ator_id: str = Field(..., description="ID do ator que proferiu a opinião.")
    postura_debate: str = Field(..., description="Postura adotada no debate sobre o tema.")
    argumento_chave: str = Field(..., description="Argumento principal defendido pelo ator.")
    preocupacao_risco: str = Field(..., description="Maior preocupação ou risco apontado por este ator.")
    oportunidade_vista: str = Field(..., description="Oportunidade de futuro identificada por este ator.")

class DebateConsolidation(BaseModel):
    tema_debate: str = Field(..., description="Tema central do debate e workshop de atores.")
    participantes: List[str] = Field(..., description="Lista de nomes dos atores participantes.")
    opinioes: List[DebateOpinion] = Field(..., description="Opiniões detalhadas expressas pelos atores.")
    pontos_consenso: List[str] = Field(..., description="Pontos de acordo comum entre os atores.")
    pontos_divergencia: List[str] = Field(..., description="Pontos de atrito ou discordância significativa.")
    insights_sintetizados: List[str] = Field(..., description="Síntese dos principais aprendizados obtidos no workshop.")


# --- FASE 2: SEMENTES E EVENTOS ---

class SementeFuturo(BaseModel):
    id: str = Field(..., description="Identificador único da semente de futuro.")
    descricao: str = Field(..., description="Descrição detalhada do sinal fraco, insight ou indício de mudança.")
    origem_debate: str = Field(..., description="Rastreabilidade da origem (ex: debate do Ator X).")
    sinal_fraco: bool = Field(True, description="Indica se é um sinal fraco (true) ou tendência evidente (false).")
    confianca: float = Field(..., description="Grau de confiança/confiabilidade da informação (escala de 0.0 a 1.0).")
    alertas: List[str] = Field(default_factory=list, description="Alertas ou ressalvas sobre a semente.")

class SementesOutput(BaseModel):
    sementes: List[SementeFuturo] = Field(..., description="Lista de sementes de futuro identificadas.")
    observacoes: List[str] = Field(default_factory=list, description="Observações do analista de sinais.")

class EventoHorizonte(BaseModel):
    id: str = Field(..., description="Identificador único do evento no horizonte.")
    titulo: str = Field(..., description="Título descritivo do evento consolidado.")
    descricao: str = Field(..., description="Descrição compreensiva do evento.")
    sementes_vinculadas: List[str] = Field(..., description="IDs das sementes de futuro agrupadas neste evento.")
    horizonte_temporal: str = Field(..., description="Horizonte estimado de ocorrência (Curto prazo: <5a, Médio: 5-10a, Longo: >10a).")
    impacto_estimado: float = Field(..., description="Impacto estimado do evento (escala de 0.0 a 1.0).")


# --- FASE 3: CLASSIFICAÇÃO EM ELEMENTOS DE FUTURO ---

class ElementoFuturo(BaseModel):
    id: str = Field(..., description="Identificador único do elemento de futuro.")
    titulo: str = Field(..., description="Título formal do elemento.")
    categoria: str = Field(..., description="Categoria analítica (tendência, incerteza, ruptura, driver, megatendência, sinal fraco, fato predeterminado, curinga).")
    descricao: str = Field(..., description="Descrição detalhada das implicações futuras.")
    evento_origem_id: str = Field(..., description="ID do evento no horizonte que originou este elemento.")
    justificativa: str = Field(..., description="Justificativa analítica para a classificação adotada.")
    confianca: float = Field(..., description="Grau de confiança na ocorrência/impacto (escala de 0.0 a 1.0).")

class ClassificacaoOutput(BaseModel):
    eventos: List[EventoHorizonte] = Field(..., description="Lista de eventos no horizonte consolidados.")
    elementos: List[ElementoFuturo] = Field(..., description="Lista de elementos de futuro classificados.")
    pendencias_validacao: List[str] = Field(default_factory=list, description="Casos com baixa confiança para gate de validação humana.")


# --- FASE 4: ANÁLISE ESTRUTURAL E MATRIZES ---

class MatrizImpactoIncertezaItem(BaseModel):
    elemento_id: str = Field(..., description="ID do elemento avaliado.")
    titulo: str = Field(..., description="Título do elemento avaliado.")
    impacto: float = Field(..., description="Pontuação de impacto (escala 0.0 a 1.0).")
    incerteza: float = Field(..., description="Pontuação de incerteza (escala 0.0 a 1.0).")
    posicionamento: str = Field(..., description="Posicionamento no quadrante (ex: Alta Incerteza x Alto Impacto).")

class MatrizMotricidadeDependenciaItem(BaseModel):
    elemento_id: str = Field(..., description="ID do elemento avaliado.")
    titulo: str = Field(..., description="Título do elemento avaliado.")
    motricidade: float = Field(..., description="Grau de influência sobre os outros elementos (soma da linha).")
    dependencia: float = Field(..., description="Grau de dependência dos outros elementos (soma da coluna).")
    posicionamento: str = Field(..., description="Classificação no espaço motricidade/dependência (ex: Motor, Enlace, Dependente, Autônomo).")

class MatrizImpactoCruzado(BaseModel):
    elementos_ids: List[str] = Field(..., description="Lista de IDs ordenados dos elementos para referência de índices.")
    matriz: List[List[float]] = Field(..., description="Grid quadrado (N x N) representando a influência cruzada direta (0=Nula, 1=Fraca, 2=Média, 3=Forte).")

class AnaliseEstrutural(BaseModel):
    matriz_impacto_incerteza: List[MatrizImpactoIncertezaItem] = Field(..., description="Avaliação de Impacto e Incerteza por elemento.")
    matriz_motricidade_dependencia: List[MatrizMotricidadeDependenciaItem] = Field(..., description="Cálculos de Motricidade e Dependência por elemento.")
    matriz_impacto_cruzado: MatrizImpactoCruzado = Field(..., description="Matriz estruturada de impacto cruzado.")
    alertas_metodologicos: List[str] = Field(default_factory=list, description="Indicação de contradições, lacunas ou enlaces de retroalimentação.")

class CondicionanteFuturo(BaseModel):
    id: str = Field(..., description="Identificador único do condicionante de futuro.")
    titulo: str = Field(..., description="Título resumido do condicionante.")
    descricao: str = Field(..., description="Explicação detalhada da incerteza crítica ou fator determinante.")
    elemento_origem_id: str = Field(..., description="ID do elemento de futuro do qual se origina.")
    motivo_derivacao: str = Field(..., description="Justificativa lógica baseada nos resultados das matrizes estruturais.")
    estados_plausiveis: List[str] = Field(..., description="Possíveis bifurcações ou estados que este condicionante pode assumir (ex: Regulação Rígida vs Regulação Flexível).")

class AnaliseEstruturalOutput(BaseModel):
    analise_estrutural: AnaliseEstrutural = Field(..., description="Resultados estruturais completos com as matrizes numéricas.")
    candidatos_condicionantes: List[CondicionanteFuturo] = Field(..., description="Candidatos a condicionantes de futuro identificados a partir dos eixos críticos ou motores.")


# --- FASE 5: CENARIZAÇÃO, CONSISTÊNCIA E RECOMENDAÇÕES ---

class Cenario(BaseModel):
    id: str = Field(..., description="Identificador único do cenário.")
    titulo: str = Field(..., description="Nome atrativo e descritivo do cenário.")
    tipo: str = Field(..., description="Tipo de cenário (otimista, pessimista, tendencial, contrastante/alternativo).")
    descricao: str = Field(..., description="Narrativa detalhada descrevendo o estado futuro do setor.")
    condicionantes_chaves: List[Dict[str, str]] = Field(..., description="Mapeamento dos estados específicos que cada condicionante de futuro assumiu neste cenário.")
    atores_envolvidos: List[Dict[str, str]] = Field(..., description="Papel, postura ou comportamento dos principais atores neste cenário específico.")
    plausibilidade: float = Field(..., description="Probabilidade subjetiva ou nível de plausibilidade estimado (0.0 a 1.0).")

class CenariosOutput(BaseModel):
    metodologia_sugerida: str = Field(..., description="Metodologia prospectiva adotada para cenarização (ex: Matriz de Impacto Cruzado, Eixos de Schwartz).")
    justificativa_metodologica: str = Field(..., description="Explicação técnica para a escolha da metodologia.")
    cenarios: List[Cenario] = Field(..., description="Conjunto de cenários alternativos e plausíveis construídos.")

class ConsistenciaOutput(BaseModel):
    achados: List[Dict[str, Any]] = Field(..., description="Pontos fortes e análises de coerência identificadas nos cenários.")
    contradicoes: List[str] = Field(..., description="Contradições lógicas ou inconsistências encontradas nas narrativas.")
    lacunas: List[str] = Field(..., description="Lacunas de informação ou falta de fundamentação conceitual.")
    aprovado_consistente: bool = Field(..., description="Indica se os cenários passaram na auditoria de consistência lógica interna.")

class PonteDecisao(BaseModel):
    id: str = Field(..., description="ID único do gatilho ou ponte de decisão.")
    oportunidade_ou_risco: str = Field(..., description="Identifica se o foco é capturar 'oportunidade' ou mitigar 'risco'.")
    cenario_id: str = Field(..., description="ID do cenário de referência ao qual esta ponte se acopla.")
    descricao: str = Field(..., description="A situação crítica de bifurcação estratégica.")
    gatilho: str = Field(..., description="Evento ou indicador mensurável que serve de gatilho estratégico (trigger).")
    acao_imediata: str = Field(..., description="Ação imediata a ser tomada quando o gatilho for acionado.")

class Recomendacao(BaseModel):
    id: str = Field(..., description="Identificador único da recomendação.")
    cenario_alvo_id: str = Field(..., description="ID do cenário para o qual esta recomendação é crítica.")
    titulo: str = Field(..., description="Título resumido da recomendação.")
    descricao: str = Field(..., description="Descrição detalhada da ação ou diretriz recomendada.")
    pontes_decisao: List[PonteDecisao] = Field(..., description="Pontes de decisão associadas (gatilhos de riscos/oportunidades).")
    prioridade: str = Field(..., description="Nível de prioridade para a tomada de decisão (Alta, Média, Baixa).")
    rastreabilidade_condicionante_id: str = Field(..., description="Vínculo com o condicionante de futuro mitigado ou aproveitado.")

class RecomendacoesOutput(BaseModel):
    tema: str = Field(..., description="Tema central da análise prospectiva.")
    recomendacoes: List[Recomendacao] = Field(..., description="Lista de recomendações contingentes formuladas.")
    conclusao_PMV: str = Field(..., description="Mensagem final de encerramento do relatório gerencial do PMV.")


# --- FASE 0: IDEAÇÃO CRIATIVA E SINAIS DE FRONTEIRA ---

class IdeiaForaDaCaixa(BaseModel):
    id: str = Field(..., description="ID único do sinal de fronteira ou ideia disruptiva.")
    titulo: str = Field(..., description="Título curto e impactante da ideia.")
    descricao: str = Field(..., description="Descrição compreensiva da ruptura ou sinal de fronteira.")
    autor_origem: str = Field(..., description="Quem propôs a ideia no brainstorming (ex: Futurologista de Fronteira).")
    plausibilidade: float = Field(..., description="Estimativa de plausibilidade de ocorrência no horizonte temporal (escala de 0.0 a 1.0).")

class BrainstormingConsolidation(BaseModel):
    tema: str = Field(..., description="Tema central do debate de ideação.")
    ideias: List[IdeiaForaDaCaixa] = Field(..., description="Lista de ideias fora-da-caixa e sinais disruptivos mapeados.")
    eixos_ruptura: List[str] = Field(..., description="Eixos temáticos de ruptura conceitual identificados.")
    provocacoes_atores: List[str] = Field(..., description="Perguntas provocativas, dilemas éticos ou técnicos direcionados aos atores convencionais da Fase 1.")

