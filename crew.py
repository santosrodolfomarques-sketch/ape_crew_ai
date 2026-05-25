from crewai import Crew, Process
import os

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

from tasks import (
    task_interpretacao_demanda,
    task_debate_governo,
    task_debate_privado,
    task_debate_sociedade,
    task_consolidacao_debate,
    task_extracao_evidencias,
    task_normalizacao,
    task_mapeamento_sementes,
    task_agrupamento_eventos,
    task_classificacao_elementos,
    task_analise_estrutural,
    task_proposta_condicionantes,
    task_geracao_cenarios,
    task_consistencia_cenarios,
    task_recomendacoes_estrategicas,
    task_relatorio_final,
    task_brainstorming_disruptivo,
    task_consolidacao_criativa
)

DEMANDA_INICIAL_GLOBAL = ""
OUTPUT_DIR_GLOBAL = "."


# --- DEFINE CALLBACKS PARA OS GATES ASÍNCRONOS EM MARKDOWN ---

def save_gate_elementos_callback(output):
    """Callback executado ao fim da classificação de elementos para gerar gate_elementos.md"""
    try:
        content = "# GATE 1: VALIDAÇÃO DE ELEMENTOS DE FUTURO - PMV\n\n"
        content += f"**Status**: Salvo para Auditoria Assíncrona\n\n"
        content += f"## Saída Bruta da LLM:\n\n{output.raw}\n\n"
        if output.pydantic:
            pyd = output.pydantic
            content += "## Eventos no Horizonte Consolidados:\n\n"
            for ev in pyd.eventos:
                content += f"### Evento: {ev.titulo} (ID: {ev.id})\n"
                content += f"- **Descrição**: {ev.descricao}\n"
                content += f"- **Horizonte Temporal**: {ev.horizonte_temporal}\n"
                content += f"- **Impacto Estimado**: {ev.impacto_estimado}\n\n"
            
            content += "## Elementos de Futuro Classificados:\n\n"
            for el in pyd.elementos:
                content += f"### Elemento: {el.titulo} (ID: {el.id})\n"
                content += f"- **Categoria**: {el.categoria}\n"
                content += f"- **Descrição**: {el.descricao}\n"
                content += f"- **Evento de Origem ID**: {el.evento_origem_id}\n"
                content += f"- **Justificativa**: {el.justificativa}\n"
                content += f"- **Confiança**: {el.confianca}\n\n"
            
            if pyd.pendencias_validacao:
                content += "## Pendências de Validação Humana:\n\n"
                for pend in pyd.pendencias_validacao:
                    content += f"- {pend}\n"
        
        path = os.path.join(OUTPUT_DIR_GLOBAL, "gate_elementos.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("\n" + "="*50 + "\n[PMV] GATE 1: Arquivo 'gate_elementos.md' gerado e salvo com sucesso.\n" + "="*50 + "\n")
    except Exception as e:
        print(f"[PMV Error] Falha ao salvar gate_elementos.md: {e}")

def save_gate_condicionantes_callback(output):
    """Callback executado ao fim da análise estrutural para gerar gate_condicionantes.md"""
    try:
        content = "# GATE 2: VALIDAÇÃO DE CONDICIONANTES DE FUTURO - PMV\n\n"
        content += f"**Status**: Salvo para Auditoria Assíncrona pós Análise Estrutural\n\n"
        content += f"## Saída Bruta da LLM:\n\n{output.raw}\n\n"
        if output.pydantic:
            pyd = output.pydantic
            content += "## Matrizes de Análise Estrutural:\n\n"
            content += "### 1. Quadrante Impacto x Incerteza\n\n"
            for item in pyd.analise_estrutural.matriz_impacto_incerteza:
                content += f"- **Elemento ID**: {item.elemento_id} | **Título**: {item.titulo} | **Impacto**: {item.impacto:.2f} | **Incerteza**: {item.incerteza:.2f} | **Quadrante**: {item.posicionamento}\n"
            
            content += "\n### 2. Espaço Motricidade x Dependência\n\n"
            for item in pyd.analise_estrutural.matriz_motricidade_dependencia:
                content += f"- **Elemento ID**: {item.elemento_id} | **Título**: {item.titulo} | **Motricidade**: {item.motricidade:.2f} | **Dependência**: {item.dependencia:.2f} | **Posição**: {item.posicionamento}\n"
            
            content += "\n### 3. Matriz de Impacto Cruzado (Influência Direta)\n\n"
            mic = pyd.analise_estrutural.matriz_impacto_cruzado
            content += f"IDs dos Elementos de Referência: `{' | '.join(mic.elementos_ids)}`\n\n"
            content += "| Elemento | " + " | ".join(mic.elementos_ids) + " |\n"
            content += "| --- | " + " | ".join(["---"] * len(mic.elementos_ids)) + " |\n"
            for i, row in enumerate(mic.matriz):
                row_str = " | ".join(map(str, row))
                content += f"| **{mic.elementos_ids[i]}** | {row_str} |\n"
            
            content += "\n## Condicionantes de Futuro Candidatos (Derivados das Matrizes):\n\n"
            for cond in pyd.candidatos_condicionantes:
                content += f"### Condicionante: {cond.titulo} (ID: {cond.id})\n"
                content += f"- **Descrição**: {cond.descricao}\n"
                content += f"- **Elemento de Origem ID**: {cond.elemento_origem_id}\n"
                content += f"- **Motivo de Derivação (Análise Estrutural)**: {cond.motivo_derivacao}\n"
                content += f"- **Estados Plausíveis (Bifurcações)**: {', '.join(cond.estados_plausiveis)}\n\n"
        
        path = os.path.join(OUTPUT_DIR_GLOBAL, "gate_condicionantes.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("\n" + "="*50 + "\n[PMV] GATE 2: Arquivo 'gate_condicionantes.md' gerado e salvo com sucesso.\n" + "="*50 + "\n")
    except Exception as e:
        print(f"[PMV Error] Falha ao salvar gate_condicionantes.md: {e}")

def save_gate_consistencia_callback(output):
    """Callback executado ao fim da auditoria de consistência para gerar gate_consistencia.md"""
    try:
        content = "# GATE 3: ANÁLISE DE CONSISTÊNCIA LOGICA DOS CENÁRIOS - PMV\n\n"
        content += f"**Status**: Salvo para Auditoria Assíncrona HITL\n\n"
        content += f"## Saída Bruta da LLM:\n\n{output.raw}\n\n"
        if output.pydantic:
            pyd = output.pydantic
            content += f"## Veredicto de Consistência Interna: **{'APROVADO E COERENTE' if pyd.aprovado_consistente else 'REPROVADO/PENDENTE'}**\n\n"
            
            content += "### Análise de Coerência e Pontos Fortes:\n"
            for achado in pyd.achados:
                content += f"- **Área**: {achado.get('tema', 'Geral')} | **Detalhamento**: {achado.get('detalhe', '')}\n"
            
            content += "\n### Contradições Identificadas nas Narrativas:\n"
            for cont in pyd.contradicoes:
                content += f"- {cont}\n"
            
            content += "\n### Lacunas Estruturais Identificadas:\n"
            for lac in pyd.lacunas:
                content += f"- {lac}\n"
        
        path = os.path.join(OUTPUT_DIR_GLOBAL, "gate_consistencia.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("\n" + "="*50 + "\n[PMV] GATE 3: Arquivo 'gate_consistencia.md' gerado e salvo com sucesso.\n" + "="*50 + "\n")
    except Exception as e:
        print(f"[PMV Error] Falha ao salvar gate_consistencia.md: {e}")


# --- CALLBACKS DE RELATÓRIOS EM PDF ---

def save_fase0_pdf_callback(output):
    """Gera o PDF consolidado da Fase 0 - Ideação Criativa."""
    try:
        from pdf_generator import gerar_pdf_fase0
        ideias_dados = []
        eixos = []
        provocacoes = []
        if output.pydantic:
            pyd = output.pydantic
            eixos = getattr(pyd, "eixos_ruptura", [])
            provocacoes = getattr(pyd, "provocacoes_atores", [])
            for ideia in getattr(pyd, "ideias", []):
                ideias_dados.append({
                    "id": getattr(ideia, "id", ""),
                    "titulo": getattr(ideia, "titulo", ""),
                    "descricao": getattr(ideia, "descricao", ""),
                    "autor_origem": getattr(ideia, "autor_origem", ""),
                    "plausibilidade": getattr(ideia, "plausibilidade", 0.0)
                })
        dados_fase0 = {
            "demanda_inicial": DEMANDA_INICIAL_GLOBAL or "Tema não especificado",
            "eixos_ruptura": eixos,
            "provocacoes_atores": provocacoes,
            "ideias": ideias_dados
        }
        path = os.path.join(OUTPUT_DIR_GLOBAL, "relatorio_fase0_criativa.pdf")
        gerar_pdf_fase0(dados_fase0, path)
        print("\n" + "="*50 + "\n[PMV] FASE 0: Relatório PDF 'relatorio_fase0_criativa.pdf' gerado com sucesso.\n" + "="*50 + "\n")
    except Exception as e:
        print(f"[PMV Error] Falha ao gerar PDF da Fase 0: {e}")

def save_fase1_diagnostico_pdf_callback(output):
    """Gera o PDF consolidado da Fase 1 - Diagnóstico, Workshop de Atores e Incertezas (GATE 1)."""
    try:
        save_gate_elementos_callback(output)
    except Exception as e:
        print(f"[PMV Error] Falha ao salvar gate markdown 1: {e}")
    try:
        from pdf_generator import gerar_pdf_fase1_diagnostico
        
        # 1. Dados do Workshop de Atores
        opinioes_dados = []
        for name, task_obj in [
            ("Governo", task_debate_governo),
            ("Setor Privado", task_debate_privado),
            ("Sociedade Civil", task_debate_sociedade)
        ]:
            if task_obj.output and task_obj.output.pydantic:
                pyd = task_obj.output.pydantic
                opinioes_dados.append({
                    "ator_nome": name,
                    "postura_debate": getattr(pyd, "postura_debate", ""),
                    "argumento_chave": getattr(pyd, "argumento_chave", ""),
                    "preocupacao_risco": getattr(pyd, "preocupacao_risco", ""),
                    "oportunidade_vista": getattr(pyd, "oportunidade_vista", "")
                })
        
        consol_dados = {}
        if task_consolidacao_debate.output and task_consolidacao_debate.output.pydantic:
            pyd = task_consolidacao_debate.output.pydantic
            consol_dados = {
                "pontos_consenso": getattr(pyd, "pontos_consenso", []),
                "pontos_divergencia": getattr(pyd, "pontos_divergencia", []),
                "insights_sintetizados": getattr(pyd, "insights_sintetizados", [])
            }
            
        # 2. Dados do Mapeamento de Sinais e Classificação
        sementes_dados = []
        if task_mapeamento_sementes.output and task_mapeamento_sementes.output.pydantic:
            for sem in task_mapeamento_sementes.output.pydantic.sementes:
                sementes_dados.append({
                    "id": getattr(sem, "id", ""),
                    "descricao": getattr(sem, "descricao", ""),
                    "origem_debate": getattr(sem, "origem_debate", ""),
                    "confianca": getattr(sem, "confianca", 0.0),
                    "alertas": getattr(sem, "alertas", [])
                })
        
        eventos_dados = []
        elementos_dados = []
        pendencias = []
        if output.pydantic:
            pyd = output.pydantic
            for ev in getattr(pyd, "eventos", []):
                eventos_dados.append({
                    "id": getattr(ev, "id", ""),
                    "titulo": getattr(ev, "titulo", ""),
                    "descricao": getattr(ev, "descricao", ""),
                    "sementes_vinculadas": getattr(ev, "sementes_vinculadas", []),
                    "horizonte_temporal": getattr(ev, "horizonte_temporal", ""),
                    "impacto_estimado": getattr(ev, "impacto_estimado", 0.0)
                })
            for el in getattr(pyd, "elementos", []):
                elementos_dados.append({
                    "id": getattr(el, "id", ""),
                    "titulo": getattr(el, "titulo", ""),
                    "categoria": getattr(el, "categoria", ""),
                    "descricao": getattr(el, "descricao", ""),
                    "justificativa": getattr(el, "justificativa", ""),
                    "confianca": getattr(el, "confianca", 0.0)
                })
            pendencias = getattr(pyd, "pendencias_validacao", [])
            
        demanda = DEMANDA_INICIAL_GLOBAL or "Como a transição demográfica acelerada no Brasil impactará a previdência social?"
        
        dados_diagnostico = {
            "demanda_inicial": demanda,
            "diretrizes_coordenador": task_interpretacao_demanda.output.raw if task_interpretacao_demanda.output else "",
            "opinioes": opinioes_dados,
            "consolidacao": consol_dados,
            "sementes": sementes_dados,
            "eventos": eventos_dados,
            "elementos": elementos_dados,
            "pendencias_validacao": pendencias
        }
        
        path = os.path.join(OUTPUT_DIR_GLOBAL, "relatorio_fase1_diagnostico_e_incertezas.pdf")
        gerar_pdf_fase1_diagnostico(dados_diagnostico, path)
        print("\n" + "="*50 + "\n[PMV] FASE 1: Relatório PDF 'relatorio_fase1_diagnostico_e_incertezas.pdf' gerado com sucesso.\n" + "="*50 + "\n")
    except Exception as e:
        print(f"[PMV Error] Falha ao gerar PDF de Diagnóstico da Fase 1: {e}")

def save_fase3_pdf_callback(output):
    """Gera o PDF consolidado da Fase 1 - Matrizes e Análise Estrutural (Gate 2)."""
    try:
        save_gate_condicionantes_callback(output)
    except Exception as e:
        print(f"[PMV Error] Falha ao salvar gate markdown 2: {e}")
    try:
        from pdf_generator import gerar_pdf_fase3
        matriz_ii = []
        matriz_md = []
        matriz_ic = {}
        condicionantes_dados = []
        
        if output.pydantic:
            pyd = output.pydantic
            # Impacto-Incerteza
            for item in getattr(pyd.analise_estrutural, "matriz_impacto_incerteza", []):
                matriz_ii.append({
                    "elemento_id": getattr(item, "elemento_id", ""),
                    "titulo": getattr(item, "titulo", ""),
                    "impacto": getattr(item, "impacto", 0.0),
                    "incerteza": getattr(item, "incerteza", 0.0),
                    "posicionamento": getattr(item, "posicionamento", "")
                })
            # Motricidade-Dependência
            for item in getattr(pyd.analise_estrutural, "matriz_motricidade_dependencia", []):
                matriz_md.append({
                    "elemento_id": getattr(item, "elemento_id", ""),
                    "titulo": getattr(item, "titulo", ""),
                    "motricidade": getattr(item, "motricidade", 0.0),
                    "dependencia": getattr(item, "dependencia", 0.0),
                    "posicionamento": getattr(item, "posicionamento", "")
                })
            # Impacto Cruzado
            mic = getattr(pyd.analise_estrutural, "matriz_impacto_cruzado", None)
            if mic:
                matriz_ic = {
                    "elementos_ids": getattr(mic, "elementos_ids", []),
                    "matriz": getattr(mic, "matriz", [])
                }
            # Condicionantes candidatos
            for cond in getattr(pyd, "candidatos_condicionantes", []):
                condicionantes_dados.append({
                    "id": getattr(cond, "id", ""),
                    "titulo": getattr(cond, "titulo", ""),
                    "descricao": getattr(cond, "descricao", ""),
                    "elemento_origem_id": getattr(cond, "elemento_origem_id", ""),
                    "motivo_derivacao": getattr(cond, "motivo_derivacao", ""),
                    "estados_plausiveis": getattr(cond, "estados_plausiveis", [])
                })
        
        dados_estruturais = {
            "matriz_impacto_incerteza": matriz_ii,
            "matriz_motricidade_dependencia": matriz_md,
            "matriz_impacto_cruzado": matriz_ic,
            "condicionantes": condicionantes_dados
        }
        path = os.path.join(OUTPUT_DIR_GLOBAL, "relatorio_fase1_matrizes_estruturais.pdf")
        gerar_pdf_fase3(dados_estruturais, path)
        print("\n" + "="*50 + "\n[PMV] FASE 1 - MATRIZES: Relatório PDF 'relatorio_fase1_matrizes_estruturais.pdf' gerado com sucesso.\n" + "="*50 + "\n")
    except Exception as e:
        print(f"[PMV Error] Falha ao gerar PDF de Matrizes da Fase 1: {e}")

def save_fase2_cenarios_pdf_callback(output):
    """Gera o PDF consolidado da Fase 2 - Cenários e Recomendações (Gate 3)."""
    try:
        from pdf_generator import gerar_pdf_fase2_cenarios
        metodologia = ""
        justificativa = ""
        cenarios_dados = []
        if task_geracao_cenarios.output and task_geracao_cenarios.output.pydantic:
            pyd_cen = task_geracao_cenarios.output.pydantic
            metodologia = getattr(pyd_cen, "metodologia_sugerida", "")
            justificativa = getattr(pyd_cen, "justificativa_metodologica", "")
            for cen in getattr(pyd_cen, "cenarios", []):
                cenarios_dados.append({
                    "id": getattr(cen, "id", ""),
                    "titulo": getattr(cen, "titulo", ""),
                    "tipo": getattr(cen, "tipo", ""),
                    "descricao": getattr(cen, "descricao", ""),
                    "condicionantes_chaves": getattr(cen, "condicionantes_chaves", []),
                    "atores_envolvidos": getattr(cen, "atores_envolvidos", []),
                    "plausibilidade": getattr(cen, "plausibilidade", 0.0)
                })
        
        consistencia_dados = {}
        if task_consistencia_cenarios.output and task_consistencia_cenarios.output.pydantic:
            pyd_con = task_consistencia_cenarios.output.pydantic
            consistencia_dados = {
                "achados": getattr(pyd_con, "achados", []),
                "contradicoes": getattr(pyd_con, "contradicoes", []),
                "lacunas": getattr(pyd_con, "lacunas", []),
                "aprovado_consistente": getattr(pyd_con, "aprovado_consistente", False)
            }
        
        recom_dados = []
        conclusao = "Estudo prospectivo PMV finalizado."
        if output.pydantic:
            pyd_rec = output.pydantic
            conclusao = getattr(pyd_rec, "conclusao_PMV", "")
            for rec in getattr(pyd_rec, "recomendacoes", []):
                bridges = []
                for br in getattr(rec, "pontes_decisao", []):
                    bridges.append({
                        "oportunidade_ou_risco": getattr(br, "oportunidade_ou_risco", ""),
                        "cenario_id": getattr(br, "cenario_id", ""),
                        "descricao": getattr(br, "descricao", ""),
                        "gatilho": getattr(br, "gatilho", ""),
                        "acao_imediata": getattr(br, "acao_imediata", "")
                    })
                recom_dados.append({
                    "id": getattr(rec, "id", ""),
                    "titulo": getattr(rec, "titulo", ""),
                    "descricao": getattr(rec, "descricao", ""),
                    "prioridade": getattr(rec, "prioridade", ""),
                    "rastreabilidade_condicionante_id": getattr(rec, "rastreabilidade_condicionante_id", ""),
                    "pontes_decisao": bridges
                })
        
        dados_cenarios = {
            "metodologia_sugerida": metodologia,
            "justificativa_metodologica": justificativa,
            "cenarios": cenarios_dados,
            "consistencia": consistencia_dados,
            "recomendacoes": recom_dados,
            "conclusao_pmv": conclusao
        }
        path = os.path.join(OUTPUT_DIR_GLOBAL, "relatorio_fase2_elaboracao_cenarios.pdf")
        gerar_pdf_fase2_cenarios(dados_cenarios, path)
        print("\n" + "="*50 + "\n[PMV] FASE 2: Relatório PDF 'relatorio_fase2_elaboracao_cenarios.pdf' gerado com sucesso.\n" + "="*50 + "\n")
    except Exception as e:
        print(f"[PMV Error] Falha ao gerar PDF de Cenários da Fase 2: {e}")

def save_relatorio_final_pdf_callback(output):
    """Gera o PDF consolidado do Relatório Final Master de até 10 páginas."""
    try:
        from pdf_generator import gerar_pdf_relatorio_final
        dados_w = {}
        if task_consolidacao_debate.output and task_consolidacao_debate.output.pydantic:
            pyd = task_consolidacao_debate.output.pydantic
            dados_w = {
                "pontos_consenso": getattr(pyd, "pontos_consenso", []),
                "pontos_divergencia": getattr(pyd, "pontos_divergencia", [])
            }
        
        dados_m = {}
        if task_classificacao_elementos.output and task_classificacao_elementos.output.pydantic:
            pyd = task_classificacao_elementos.output.pydantic
            elementos = []
            for el in getattr(pyd, "elementos", []):
                elementos.append({
                    "id": getattr(el, "id", ""),
                    "titulo": getattr(el, "titulo", ""),
                    "categoria": getattr(el, "categoria", ""),
                    "descricao": getattr(el, "descricao", "")
                })
            dados_m = {"elementos": elementos}
        
        dados_e = {}
        if task_analise_estrutural.output and task_analise_estrutural.output.pydantic:
            pyd = task_analise_estrutural.output.pydantic
            condicionantes = []
            for cond in getattr(pyd, "candidatos_condicionantes", []):
                condicionantes.append({
                    "id": getattr(cond, "id", ""),
                    "titulo": getattr(cond, "titulo", ""),
                    "descricao": getattr(cond, "descricao", ""),
                    "estados_plausiveis": getattr(cond, "estados_plausiveis", [])
                })
            dados_e = {"condicionantes": condicionantes}
        
        dados_c = {}
        if task_recomendacoes_estrategicas.output and task_recomendacoes_estrategicas.output.pydantic:
            pyd = task_recomendacoes_estrategicas.output.pydantic
            recoms = []
            for rec in getattr(pyd, "recomendacoes", []):
                bridges = []
                for br in getattr(rec, "pontes_decisao", []):
                    bridges.append({
                        "gatilho": getattr(br, "gatilho", ""),
                        "acao_imediata": getattr(br, "acao_imediata", "")
                    })
                recoms.append({
                    "id": getattr(rec, "id", ""),
                    "titulo": getattr(rec, "titulo", ""),
                    "descricao": getattr(rec, "descricao", ""),
                    "prioridade": getattr(rec, "prioridade", ""),
                    "pontes_decisao": bridges
                })
            
            cenarios = []
            if task_geracao_cenarios.output and task_geracao_cenarios.output.pydantic:
                for cen in getattr(task_geracao_cenarios.output.pydantic, "cenarios", []):
                    cenarios.append({
                        "titulo": getattr(cen, "titulo", ""),
                        "tipo": getattr(cen, "tipo", ""),
                        "descricao": getattr(cen, "descricao", ""),
                        "plausibilidade": getattr(cen, "plausibilidade", 0.0)
                    })
            
            dados_c = {
                "cenarios": cenarios,
                "recomendacoes": recoms,
                "conclusao_pmv": getattr(pyd, "conclusao_PMV", "Estudo Estratégico Concluído.")
            }
        
        resumo = ""
        transversal = ""
        conclusao_final = "Estudo prospectivo modular do PMV concluído com sucesso."
        raw_out = output.raw
        
        if "Resumo Executivo" in raw_out or "RESUMO EXECUTIVO" in raw_out:
            parts = raw_out.split("1. Fase 1" if "1. Fase 1" in raw_out else "1.")
            if len(parts) > 1:
                resumo = parts[0].replace("Resumo Executivo", "").replace("RESUMO EXECUTIVO", "").strip()
                transversal = parts[1].strip()
            else:
                transversal = raw_out
        else:
            transversal = raw_out
        
        # --- CÁLCULO DINÂMICO DE METRICAS ---
        total_flash_input = 0
        total_flash_output = 0
        total_pro_input = 0
        total_pro_output = 0
        
        all_agents = [
            coordenador_metodologia,
            futurologista_fronteira,
            ficcionista_cenarios,
            voz_juventude,
            sintetizador_criativo,
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
            agente_redator_relatorios
        ]
        
        for agent in all_agents:
            try:
                usage = agent.llm.get_token_usage_summary()
                model = agent.llm.model
                if "flash" in model.lower():
                    total_flash_input += usage.prompt_tokens
                    total_flash_output += usage.completion_tokens
                elif "pro" in model.lower():
                    total_pro_input += usage.prompt_tokens
                    total_pro_output += usage.completion_tokens
            except Exception:
                pass
                
        cost_flash = (total_flash_input / 1_000_000) * 0.075 + (total_flash_output / 1_000_000) * 0.30
        cost_pro = (total_pro_input / 1_000_000) * 1.25 + (total_pro_output / 1_000_000) * 5.00
        total_usd = cost_flash + cost_pro
        total_brl = total_usd * 5.20
        
        metrics_summary = {
            "flash_input": total_flash_input,
            "flash_output": total_flash_output,
            "flash_total": total_flash_input + total_flash_output,
            "flash_cost_usd": cost_flash,
            
            "pro_input": total_pro_input,
            "pro_output": total_pro_output,
            "pro_total": total_pro_input + total_pro_output,
            "pro_cost_usd": cost_pro,
            
            "total_input": total_flash_input + total_pro_input,
            "total_output": total_flash_output + total_pro_output,
            "total_tokens": total_flash_input + total_pro_input + total_flash_output + total_pro_output,
            "total_cost_usd": total_usd,
            "total_cost_brl": total_brl
        }
        
        demanda = DEMANDA_INICIAL_GLOBAL or "Como a transição demográfica acelerada no Brasil impactará a previdência social?"
        dados_compilados = {
            "demanda_inicial": demanda,
            "resumo_executivo": resumo,
            "analise_transversal": transversal,
            "conclusao_PMV": conclusao_final,
            "workshop": dados_w,
            "mapeamento": dados_m,
            "estruturais": dados_e,
            "cenarios": dados_c,
            "metrics": metrics_summary
        }
        path = os.path.join(OUTPUT_DIR_GLOBAL, "relatorio_final_prospectiva_pmv.pdf")
        gerar_pdf_relatorio_final(dados_compilados, path)
        print("\n" + "="*50 + "\n[PMV] RELATÓRIO FINAL: PDF 'relatorio_final_prospectiva_pmv.pdf' gerado com sucesso.\n" + "="*50 + "\n")
    except Exception as e:
        print(f"[PMV Error] Falha ao gerar PDF do Relatório Final: {e}")


import csv
import ast

def process_task_tuples(task_name, raw_output):
    """
    Verifica se a saída da tarefa contém ou é uma lista de tuplas/listas.
    Se sim, exibe como uma tabela limpa no console e salva em um arquivo .csv.
    """
    parsed_data = None
    
    # 1. Tenta identificar se o objeto é diretamente uma lista de tuplas/listas
    if isinstance(raw_output, list) and all(isinstance(item, (tuple, list)) for item in raw_output):
        parsed_data = raw_output
    # 2. Se for uma string, tenta avaliar se representa uma lista de tuplas
    elif isinstance(raw_output, str):
        cleaned = raw_output.strip()
        if (cleaned.startswith("[") and cleaned.endswith("]")) or (cleaned.startswith("(") and cleaned.endswith(")")):
            try:
                evaluated = ast.literal_eval(cleaned)
                if isinstance(evaluated, list) and all(isinstance(item, (tuple, list)) for item in evaluated):
                    parsed_data = evaluated
            except Exception:
                pass
                
    if parsed_data:
        # Temos uma lista de tuplas!
        print(f"\n[PMV] Detectada saída em formato de lista de tuplas na tarefa '{task_name}'!")
        
        if not parsed_data:
            return
            
        # Determina o número máximo de colunas
        num_cols = max(len(item) for item in parsed_data)
        headers = [f"Coluna {i+1}" for i in range(num_cols)]
        
        # Calcula largura das colunas
        col_widths = [len(h) for h in headers]
        for row in parsed_data:
            for i, val in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(val)))
                    
        # Linha de separação
        sep = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
        
        # Cabeçalho da tabela
        header_row = "|" + "|".join(f" {headers[i].ljust(col_widths[i])} " for i in range(num_cols)) + "|"
        
        # Imprime a tabela no console (será capturada no log .md!)
        print(sep)
        print(header_row)
        print(sep)
        for row in parsed_data:
            row_str = "|"
            for i in range(num_cols):
                val = row[i] if i < len(row) else ""
                row_str += f" {str(val).ljust(col_widths[i])} |"
            print(row_str)
        print(sep)
        
        # Salva em arquivo .csv
        csv_filename = os.path.join(OUTPUT_DIR_GLOBAL, f"saida_{task_name.lower().replace(' ', '_')}.csv")
        try:
            with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                for row in parsed_data:
                    writer.writerow(list(row))
            print(f"[PMV] Dados da lista de tuplas salvos com sucesso no arquivo CSV: '{csv_filename}'")
        except Exception as e:
            print(f"[PMV Erro] Falha ao salvar arquivo CSV '{csv_filename}': {e}")


def make_general_callback(task_name, original_callback=None):
    def callback_wrapper(output):
        # 1. Executa o callback original se houver
        if original_callback:
            try:
                original_callback(output)
            except Exception as e:
                print(f"[PMV Error] Falha no callback original da tarefa '{task_name}': {e}")
        
        # 2. Processa possíveis listas de tuplas na saída bruta
        try:
            process_task_tuples(task_name, output.raw)
        except Exception as e:
            pass
            
    return callback_wrapper


# --- ATRIBUIÇÃO DOS CALLBACKS UNIVERSAIS ÀS TAREFAS ---
task_interpretacao_demanda.callback = make_general_callback("Interpretacao Demanda")
task_brainstorming_disruptivo.callback = make_general_callback("Brainstorming Disruptivo")
task_consolidacao_criativa.callback = make_general_callback("Consolidacao Criativa", save_fase0_pdf_callback)
task_debate_governo.callback = make_general_callback("Debate Governo")
task_debate_privado.callback = make_general_callback("Debate Privado")
task_debate_sociedade.callback = make_general_callback("Debate Sociedade")
task_consolidacao_debate.callback = make_general_callback("Consolidacao Debate")
task_extracao_evidencias.callback = make_general_callback("Extracao Evidencias")
task_normalizacao.callback = make_general_callback("Normalizacao")
task_mapeamento_sementes.callback = make_general_callback("Mapeamento Sementes")
task_agrupamento_eventos.callback = make_general_callback("Agrupamento Eventos")

# Estas tarefas possuem callbacks específicos de Gates, preservados e encapsulados:
task_classificacao_elementos.callback = make_general_callback("Classificacao Elementos", save_fase1_diagnostico_pdf_callback)
task_analise_estrutural.callback = make_general_callback("Analise Estrutural", save_fase3_pdf_callback)
task_proposta_condicionantes.callback = make_general_callback("Proposta Condicionantes")
task_geracao_cenarios.callback = make_general_callback("Geracao Cenarios")
task_consistencia_cenarios.callback = make_general_callback("Consistencia Cenarios", save_gate_consistencia_callback)
task_recomendacoes_estrategicas.callback = make_general_callback("Recomendacoes Estrategicas", save_fase2_cenarios_pdf_callback)
task_relatorio_final.callback = make_general_callback("Relatorio Final", save_relatorio_final_pdf_callback)




# --- CLASSE DE ORQUESTRAÇÃO DA CREW ---

class AnaliseProspectivaCrew:
    """Orquestração multiagente sequencial e por debates para o PMV."""
    
    def __init__(self, demanda_inicial: str):
        self.demanda_inicial = demanda_inicial

    def kickoff(self) -> str:
        # Configura fallbacks de demanda inicial para os callbacks
        global DEMANDA_INICIAL_GLOBAL
        DEMANDA_INICIAL_GLOBAL = self.demanda_inicial
        
        # Configura os contextos de tarefas encadeadas da Fase 1 e Relatório Final
        task_debate_governo.context = [task_consolidacao_criativa]
        task_debate_privado.context = [task_consolidacao_criativa]
        task_debate_sociedade.context = [task_consolidacao_criativa]
        
        task_relatorio_final.context = [
            task_interpretacao_demanda,
            task_consolidacao_criativa,
            task_consolidacao_debate,
            task_classificacao_elementos,
            task_proposta_condicionantes,
            task_geracao_cenarios,
            task_consistencia_cenarios,
            task_recomendacoes_estrategicas
        ]

        # Instancia a Crew com os 19 agentes e 18 tarefas mapeados
        crew = Crew(
            agents=[
                coordenador_metodologia,
                futurologista_fronteira,
                ficcionista_cenarios,
                voz_juventude,
                sintetizador_criativo,
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
                agente_redator_relatorios
            ],
            tasks=[
                task_interpretacao_demanda,
                task_brainstorming_disruptivo,
                task_consolidacao_criativa,
                task_debate_governo,
                task_debate_privado,
                task_debate_sociedade,
                task_consolidacao_debate,
                task_extracao_evidencias,
                task_normalizacao,
                task_mapeamento_sementes,
                task_agrupamento_eventos,
                task_classificacao_elementos,
                task_analise_estrutural,
                task_proposta_condicionantes,
                task_geracao_cenarios,
                task_consistencia_cenarios,
                task_recomendacoes_estrategicas,
                task_relatorio_final
            ],
            process=Process.sequential,
            verbose=True
        )
        
        # Executa a orquestração do funil prospectivo
        print(f"[PMV] Inicializando a execução do Crew de Análise Prospectiva...")
        result = crew.kickoff(inputs={"demanda_inicial": self.demanda_inicial})
        print(f"[PMV] Execução finalizada com sucesso.")
        
        # --- CÁLCULO E EXIBIÇÃO DO MONITOR DE TOKENS E CUSTOS ---
        try:
            total_flash_input = 0
            total_flash_output = 0
            total_pro_input = 0
            total_pro_output = 0
            
            for agent in crew.agents:
                try:
                    usage = agent.llm.get_token_usage_summary()
                    model = agent.llm.model
                    if "flash" in model.lower():
                        total_flash_input += usage.prompt_tokens
                        total_flash_output += usage.completion_tokens
                    elif "pro" in model.lower():
                        total_pro_input += usage.prompt_tokens
                        total_pro_output += usage.completion_tokens
                except Exception:
                    pass
            
            flash_in_cost = (total_flash_input / 1_000_000) * 0.075
            flash_out_cost = (total_flash_output / 1_000_000) * 0.30
            flash_cost_usd = flash_in_cost + flash_out_cost
            
            pro_in_cost = (total_pro_input / 1_000_000) * 1.25
            pro_out_cost = (total_pro_output / 1_000_000) * 5.00
            pro_cost_usd = pro_in_cost + pro_out_cost
            
            total_cost_usd = flash_cost_usd + pro_cost_usd
            total_cost_brl = total_cost_usd * 5.20
            
            print("\n" + "="*80)
            print("                     MONITOR DE CONSUMO E CUSTOS DA ANÁLISE")
            print("="*80)
            print("  * Câmbio estático referencial: 1 USD = 5.20 BRL")
            print("-"*80)
            print("  MODELO GEMINI 3.5 FLASH (Econômico):")
            print(f"    - Tokens de Entrada : {total_flash_input:,} (${flash_in_cost:.4f} USD / R$ {flash_in_cost*5.20:.4f} BRL)")
            print(f"    - Tokens de Saída   : {total_flash_output:,} (${flash_out_cost:.4f} USD / R$ {flash_out_cost*5.20:.4f} BRL)")
            print(f"    - Subtotal          : {total_flash_input + total_flash_output:,} tokens (${flash_cost_usd:.4f} USD / R$ {flash_cost_usd*5.20:.2f} BRL)")
            print("")
            print("  MODELO GEMINI 2.5 PRO (Alta Capacidade):")
            print(f"    - Tokens de Entrada : {total_pro_input:,} (${pro_in_cost:.4f} USD / R$ {pro_in_cost*5.20:.4f} BRL)")
            print(f"    - Tokens de Saída   : {total_pro_output:,} (${pro_out_cost:.4f} USD / R$ {pro_out_cost*5.20:.4f} BRL)")
            print(f"    - Subtotal          : {total_pro_input + total_pro_output:,} tokens (${pro_cost_usd:.4f} USD / R$ {pro_cost_usd*5.20:.2f} BRL)")
            print("-"*80)
            print("  ACUMULADO TOTAL DO ESTUDO MODULAR:")
            print(f"    - Total de Tokens   : {total_flash_input + total_flash_output + total_pro_input + total_pro_output:,} tokens")
            print(f"    - Custo Total USD   : ${total_cost_usd:.4f} USD")
            print(f"    - Custo Total BRL   : R$ {total_cost_brl:.2f} BRL")
            print("="*80 + "\n")
            
            # Acrescenta painel de faturamento no arquivo de log do console markdown
            log_metrics_md = (
                "\n\n## Painel de Auditoria de Consumos e Custos LLM\n\n"
                f"- **Câmbio estático referencial**: 1 USD = 5.20 BRL\n\n"
                "| Categoria | Tokens de Entrada | Tokens de Saída | Total de Tokens | Custo (USD) | Custo (BRL) |\n"
                "| --- | --- | --- | --- | --- | --- |\n"
                f"| **Gemini 3.5 Flash** | {total_flash_input:,} | {total_flash_output:,} | {total_flash_input + total_flash_output:,} | ${flash_cost_usd:.4f} | R$ {flash_cost_usd*5.20:.2f} |\n"
                f"| **Gemini 2.5 Pro** | {total_pro_input:,} | {total_pro_output:,} | {total_pro_input + total_pro_output:,} | ${pro_cost_usd:.4f} | R$ {pro_cost_usd*5.20:.2f} |\n"
                f"| **TOTAL ACUMULADO** | {total_flash_input + total_pro_input:,} | {total_flash_output + total_pro_output:,} | {total_flash_input + total_flash_output + total_pro_input + total_pro_output:,} | **${total_cost_usd:.4f}** | **R$ {total_cost_brl:.2f}** |\n"
            )
            # Tenta salvar no fim de log_execucao_pmv.md
            try:
                log_md_path = os.path.join(OUTPUT_DIR_GLOBAL, "log_execucao_pmv.md")
                if os.path.exists(log_md_path):
                    with open(log_md_path, "a", encoding="utf-8") as f_log:
                        f_log.write(log_metrics_md)
            except Exception:
                pass
        except Exception as ex_metrics:
            print(f"[PMV Error] Erro ao processar monitor de consumo: {ex_metrics}")
            
        return result

