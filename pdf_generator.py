import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# --- CANVAS CUSTOMIZADO PARA NUMERAÇÃO DINÂMICA DE PÁGINAS "X de Y" ---
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        # Salva o estado da página atual para renderização posterior
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        # Segunda passagem: renderiza a numeração de páginas em todas as páginas salvas
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super().showPage()
        super().save()

    def draw_page_elements(self, page_count):
        # Primeira página (geralmente capa) não recebe cabeçalhos ou rodapés
        if self._pageNumber == 1:
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1A365D")) # Navy
        
        # Cabeçalho running
        self.drawString(54, 750, "PMV - SISTEMA MODULAR DE ANÁLISE PROSPECTIVA")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        self.drawRightString(558, 750, "MGI - SUBSECRETARIA DE PLANEJAMENTO ESTRATÉGICO")
        
        # Linha do cabeçalho
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)
        
        # Linha do rodapé
        self.line(54, 55, 558, 55)
        
        # Rodapé
        self.drawString(54, 42, "DOCUMENTO TÉCNICO DE TRABALHO - PMV DE ANÁLISE PROSPECTIVA")
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(558, 42, page_text)
        
        self.restoreState()


# --- CONFIGURAÇÃO DE ESTILOS ---
def get_custom_styles():
    styles = getSampleStyleSheet()
    
    # Customizações
    primary_color = colors.HexColor("#1A365D")  # Navy
    secondary_color = colors.HexColor("#4A5568") # Slate
    body_color = colors.HexColor("#2D3748")      # Charcoal
    
    # Adiciona ou altera estilos
    styles.add(ParagraphStyle(
        name='CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=primary_color,
        alignment=1, # Centered
        spaceAfter=15
    ))
    
    styles.add(ParagraphStyle(
        name='CoverSubtitle',
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        alignment=1, # Centered
        spaceAfter=30
    ))
    
    styles.add(ParagraphStyle(
        name='CoverMeta',
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        textColor=secondary_color,
        alignment=1, # Centered
    ))
    
    styles.add(ParagraphStyle(
        name='CustomTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=15,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='CustomH1',
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=15,
        spaceAfter=8,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='CustomH2',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    ))

    styles.add(ParagraphStyle(
        name='CustomBody',
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=body_color,
        spaceAfter=10
    ))

    styles.add(ParagraphStyle(
        name='CustomBullet',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=body_color,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=6
    ))

    styles.add(ParagraphStyle(
        name='CustomCallout',
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor("#2C5282"),
        backColor=colors.HexColor("#EBF8FF"),
        borderColor=colors.HexColor("#BEE3F8"),
        borderWidth=1,
        borderPadding=8,
        spaceBefore=10,
        spaceAfter=10,
        borderRadius=4
    ))
    
    styles.add(ParagraphStyle(
        name='LogLine',
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1A202C")
    ))

    return styles


# --- GERADORES DE RELATÓRIO PDF ---

def gerar_pdf_log(texto_log, path_saida="log_execucao_pmv.pdf"):
    """Gera um PDF estruturado contendo o log completo de execução do terminal."""
    doc = SimpleDocTemplate(
        path_saida,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = get_custom_styles()
    story = []
    
    # Cabeçalho do Log no PDF
    story.append(Paragraph("REGISTRO DE AUDITORIA DE EXECUÇÃO DO PMV", styles['CustomTitle']))
    story.append(Paragraph("<i>Este log registra todas as operações, pensamentos de agentes e saídas intermediárias de execução.</i>", styles['CustomBody']))
    story.append(Spacer(1, 10))
    
    # Processa linha por linha para manter o layout monoespaçado e quebra de linhas automática
    linhas = texto_log.split("\n")
    log_story = []
    for linha in linhas:
        # Substitui tabulações por espaços e escapa caracteres XML
        linha_limpa = (
            linha.replace("\t", "    ")
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        if not linha_limpa.strip():
            log_story.append(Spacer(1, 4))
        else:
            log_story.append(Paragraph(linha_limpa, styles['LogLine']))
            
    story.extend(log_story)
    
    doc.build(story, canvasmaker=NumberedCanvas)


def gerar_pdf_fase1(dados_workshop, path_saida="relatorio_fase1_workshop.pdf"):
    """Gera o PDF consolidado da Fase 1 - Escopo e Workshop de Atores."""
    doc = SimpleDocTemplate(
        path_saida,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = get_custom_styles()
    story = []
    
    # Capa
    story.append(Spacer(1, 150))
    story.append(Paragraph("RELATÓRIO CONSOLIDADO: FASE 1", styles['CoverTitle']))
    story.append(Paragraph("Workshop de Atores, Escopo e Alinhamento Estrutural do PMV", styles['CoverSubtitle']))
    story.append(Spacer(1, 100))
    story.append(Paragraph("<b>Demanda Analisada:</b><br/>" + dados_workshop.get("demanda_inicial", ""), styles['CustomCallout']))
    story.append(Spacer(1, 100))
    story.append(Paragraph("Sistema Modular de Análise Prospectiva e Cenários com IA<br/>"
                           "MGI - 2026", styles['CoverMeta']))
    story.append(PageBreak())
    
    # Conteúdo - Seção 1: Diretrizes Metodológicas
    story.append(Paragraph("1. Diretrizes Metodológicas e Escopo", styles['CustomH1']))
    story.append(Paragraph(
        "A prospecção iniciou-se com a estruturação dos objetivos macro e do horizonte temporal pela Coordenação. "
        "O tema foi modelado em eixos estratégicos para orientar os debates e a extração posterior de sementes de futuro.",
        styles['CustomBody']
    ))
    
    diretrizes = dados_workshop.get("diretrizes_coordenador", "Diretrizes não registradas.")
    story.append(Paragraph("<b>Diretrizes Metodológicas Propostas:</b>", styles['CustomH2']))
    
    # Processa parágrafos ou marcadores das diretrizes
    for part in diretrizes.split("\n"):
        if part.strip():
            if part.strip().startswith("-") or part.strip().startswith("*"):
                text = part.strip()[1:].strip()
                story.append(Paragraph(f"• {text}", styles['CustomBullet']))
            else:
                story.append(Paragraph(part.strip(), styles['CustomBody']))
                
    story.append(Spacer(1, 15))
    
    # Seção 2: Debate e Opiniões Setoriais
    story.append(Paragraph("2. Workshop de Atores Setoriais", styles['CustomH1']))
    story.append(Paragraph(
        "O workshop virtual reuniu três grandes grupos de atores representados por agentes especializados. "
        "Cada ator trouxe argumentos e preocupações endógenas com base em suas visões setoriais:",
        styles['CustomBody']
    ))
    
    opinioes = dados_workshop.get("opinioes", [])
    for op in opinioes:
        story.append(Paragraph(f"Ator: {op.get('ator_nome', 'Indefinido')}", styles['CustomH2']))
        story.append(Paragraph(f"<b>Postura no Debate:</b> {op.get('postura_debate', '')}", styles['CustomBody']))
        story.append(Paragraph(f"<b>Argumento-Chave:</b> {op.get('argumento_chave', '')}", styles['CustomBody']))
        story.append(Paragraph(f"<b>Risco / Preocupação:</b> {op.get('preocupacao_risco', '')}", styles['CustomBody']))
        story.append(Paragraph(f"<b>Oportunidade Mapeada:</b> {op.get('oportunidade_vista', '')}", styles['CustomBody']))
        story.append(Spacer(1, 10))
        
    story.append(PageBreak())
    
    # Seção 3: Consolidação do Workshop (Consensos e Divergências)
    story.append(Paragraph("3. Síntese, Consensos e Divergências", styles['CustomH1']))
    story.append(Paragraph(
        "O Rapporteur compilou os pontos comuns e as polarizações observadas durante os debates, mapeando a dinâmica de forças:",
        styles['CustomBody']
    ))
    
    consol = dados_workshop.get("consolidacao", {})
    
    story.append(Paragraph("Pontos de Consenso Estabelecidos:", styles['CustomH2']))
    for cons in consol.get("pontos_consenso", []):
        story.append(Paragraph(f"✔ {cons}", styles['CustomBullet']))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Pontos de Divergência e Fricções:", styles['CustomH2']))
    for div in consol.get("pontos_divergencia", []):
        story.append(Paragraph(f"✖ {div}", styles['CustomBullet']))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Insights Sintetizados pelo Moderador:", styles['CustomH2']))
    for ins in consol.get("insights_sintetizados", []):
        story.append(Paragraph(f"💡 {ins}", styles['CustomBullet']))
        
    doc.build(story, canvasmaker=NumberedCanvas)


def gerar_pdf_fase2(dados_mapeamento, path_saida="relatorio_fase2_mapeamento.pdf"):
    """Gera o PDF consolidado da Fase 2 - Sementes, Eventos e Classificação."""
    doc = SimpleDocTemplate(
        path_saida,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = get_custom_styles()
    story = []
    
    # Capa
    story.append(Spacer(1, 150))
    story.append(Paragraph("RELATÓRIO CONSOLIDADO: FASE 2", styles['CoverTitle']))
    story.append(Paragraph("Sementes de Futuro, Eventos no Horizonte e Classificação Metodológica (GATE 1)", styles['CoverSubtitle']))
    story.append(Spacer(1, 100))
    story.append(Paragraph("Sistema Modular de Análise Prospectiva e Cenários com IA<br/>"
                           "MGI - 2026", styles['CoverMeta']))
    story.append(PageBreak())
    
    # Seção 1: Sementes de Futuro
    story.append(Paragraph("1. Inventário de Sementes de Futuro (Sinais Fracos)", styles['CustomH1']))
    story.append(Paragraph(
        "A partir da análise do workshop, foram isoladas sementes de futuro e sinais fracos "
        "com alta relevância conceitual e rastreabilidade para os discursos de base:",
        styles['CustomBody']
    ))
    
    sementes = dados_mapeamento.get("sementes", [])
    for sem in sementes:
        desc = f"<b>ID: {sem.get('id', '')}</b> - {sem.get('descricao', '')}<br/>" \
               f"<i>Rastreabilidade: {sem.get('origem_debate', '')} | Confiança: {sem.get('confianca', 0.0)*100:.0f}%</i>"
        story.append(Paragraph(f"🌱 {desc}", styles['CustomBullet']))
        if sem.get("alertas"):
            story.append(Paragraph(f"⚠️ Alerta: {', '.join(sem.get('alertas', []))}", styles['CustomBullet']))
        story.append(Spacer(1, 5))
        
    story.append(PageBreak())
    
    # Seção 2: Eventos no Horizonte
    story.append(Paragraph("2. Agrupamento em Eventos no Horizonte", styles['CustomH1']))
    story.append(Paragraph(
        "As sementes de futuro correlacionadas foram consolidadas em Eventos no Horizonte, "
        "com a estimativa de prazo de maturação e impacto estratégico sistêmico:",
        styles['CustomBody']
    ))
    
    eventos = dados_mapeamento.get("eventos", [])
    for ev in eventos:
        desc_ev = f"<b>{ev.get('titulo', '')} (ID: {ev.get('id', '')})</b><br/>" \
                  f"Descrição: {ev.get('descricao', '')}<br/>" \
                  f"<i>Horizonte: {ev.get('horizonte_temporal', '')} | Impacto Sistêmico: {ev.get('impacto_estimado', 0.0)*10:.1f}/10</i><br/>" \
                  f"Sementes Vinculadas: {', '.join(ev.get('sementes_vinculadas', []))}"
        story.append(Paragraph(f"📢 {desc_ev}", styles['CustomBullet']))
        story.append(Spacer(1, 10))
        
    story.append(Spacer(1, 15))
    
    # Seção 3: Classificação e Gate 1
    story.append(Paragraph("3. Classificação Prospectiva e Gate 1", styles['CustomH1']))
    story.append(Paragraph(
        "Os eventos no horizonte foram rigorosamente enquadrados nas categorias do funil prospectivo, "
        "justificando analiticamente sua categorização para o posterior crivo estratégico:",
        styles['CustomBody']
    ))
    
    elementos = dados_mapeamento.get("elementos", [])
    for el in elementos:
        desc_el = f"<b>{el.get('titulo', '')} (ID: {el.get('id', '')})</b><br/>" \
                  f"Categoria: <b>{el.get('categoria', '').upper()}</b> | Confiança: {el.get('confianca', 0.0)*100:.0f}%<br/>" \
                  f"Descrição: {el.get('descricao', '')}<br/>" \
                  f"<i>Justificativa: {el.get('justificativa', '')}</i>"
        story.append(Paragraph(f"📌 {desc_el}", styles['CustomBullet']))
        story.append(Spacer(1, 10))
        
    # Pendências do Gate 1
    pendencias = dados_mapeamento.get("pendencias_validacao", [])
    if pendencias:
        story.append(Paragraph("Pendências para Gate Humano de Validação:", styles['CustomH2']))
        for pend in pendencias:
            story.append(Paragraph(f"⏳ {pend}", styles['CustomBullet']))
            
    doc.build(story, canvasmaker=NumberedCanvas)


def gerar_pdf_fase3(dados_estruturais, path_saida="relatorio_fase3_matrizes.pdf"):
    """Gera o PDF consolidado da Fase 3 - Análise Estrutural e Matrizes (GATE 2)."""
    doc = SimpleDocTemplate(
        path_saida,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = get_custom_styles()
    story = []
    
    # Capa
    story.append(Spacer(1, 150))
    story.append(Paragraph("RELATÓRIO CONSOLIDADO: FASE 3", styles['CoverTitle']))
    story.append(Paragraph("Análise Estrutural, Matrizes Numéricas de Impacto Cruzado e Condicionantes (GATE 2)", styles['CoverSubtitle']))
    story.append(Spacer(1, 100))
    story.append(Paragraph("Sistema Modular de Análise Prospectiva e Cenários com IA<br/>"
                           "MGI - 2026", styles['CoverMeta']))
    story.append(PageBreak())
    
    # Seção 1: Matriz Impacto e Incerteza
    story.append(Paragraph("1. Quadrante de Impacto e Incerteza", styles['CustomH1']))
    story.append(Paragraph(
        "A análise quantitativa inicial avalia o posicionamento dos Elementos de Futuro no plano estratégico de Impacto x Incerteza:",
        styles['CustomBody']
    ))
    
    matriz_ii = dados_estruturais.get("matriz_impacto_incerteza", [])
    
    # Cria Tabela para Impacto x Incerteza
    data_ii = [["ID Elemento", "Título", "Impacto", "Incerteza", "Quadrante"]]
    for item in matriz_ii:
        data_ii.append([
            item.get("elemento_id", ""),
            item.get("titulo", ""),
            f"{item.get('impacto', 0.0):.2f}",
            f"{item.get('incerteza', 0.0):.2f}",
            item.get("posicionamento", "")
        ])
        
    t_ii = Table(data_ii, colWidths=[80, 180, 50, 50, 140])
    t_ii.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A365D")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
    ]))
    
    story.append(t_ii)
    story.append(Spacer(1, 20))
    
    # Seção 2: Motricidade e Dependência
    story.append(Paragraph("2. Motricidade e Dependência", styles['CustomH1']))
    story.append(Paragraph(
        "Calculado o grau de influência (Motricidade) de cada elemento sobre os demais, bem como sua sensibilidade de retroalimentação (Dependência):",
        styles['CustomBody']
    ))
    
    matriz_md = dados_estruturais.get("matriz_motricidade_dependencia", [])
    
    # Cria Tabela para Motricidade x Dependência
    data_md = [["ID Elemento", "Título", "Motricidade (Influência)", "Dependência", "Posição Espacial"]]
    for item in matriz_md:
        data_md.append([
            item.get("elemento_id", ""),
            item.get("titulo", ""),
            f"{item.get('motricidade', 0.0):.2f}",
            f"{item.get('dependencia', 0.0):.2f}",
            item.get("posicionamento", "")
        ])
        
    t_md = Table(data_md, colWidths=[80, 180, 80, 80, 80])
    t_md.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4A5568")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
    ]))
    
    story.append(t_md)
    story.append(PageBreak())
    
    # Seção 3: Matriz de Impacto Cruzado
    story.append(Paragraph("3. Matriz de Impacto Cruzado Direto", styles['CustomH1']))
    story.append(Paragraph(
        "Abaixo, a grade numérica cruzada direta de influência direta mapeada entre os elementos (escala de 0=Nulo, 1=Fraco, 2=Médio, 3=Forte):",
        styles['CustomBody']
    ))
    
    mic = dados_estruturais.get("matriz_impacto_cruzado", {})
    elements_ids = mic.get("elementos_ids", [])
    matrix_grid = mic.get("matriz", [])
    
    if elements_ids and matrix_grid:
        header_row = ["Elemento"] + elements_ids
        table_data_mic = [header_row]
        for i, row in enumerate(matrix_grid):
            row_data = [elements_ids[i]] + [str(int(val)) for val in row]
            table_data_mic.append(row_data)
            
        # Determina larguras de colunas automaticamente
        num_cols = len(elements_ids) + 1
        col_w = [70] + [400 / len(elements_ids)] * len(elements_ids)
        
        t_mic = Table(table_data_mic, colWidths=col_w)
        t_mic.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        story.append(t_mic)
        
    story.append(Spacer(1, 20))
    
    # Seção 4: Condicionantes de Futuro Derivados
    story.append(Paragraph("4. Condicionantes de Futuro (Gate 2)", styles['CustomH1']))
    story.append(Paragraph(
        "Derivados diretamente das variáveis motrizes e críticas das matrizes numéricas, "
        "foram consolidados os Condicionantes de Futuro e suas bifurcações plausíveis:",
        styles['CustomBody']
    ))
    
    condicionantes = dados_estruturais.get("condicionantes", [])
    for cond in condicionantes:
        desc_cond = f"<b>{cond.get('titulo', '')} (ID: {cond.get('id', '')})</b><br/>" \
                    f"Descrição: {cond.get('descricao', '')}<br/>" \
                    f"<i>Elemento Origem: {cond.get('elemento_origem_id', '')}</i><br/>" \
                    f"<i>Motivo Derivação: {cond.get('motivo_derivacao', '')}</i><br/>" \
                    f"<b>Bifurcações / Estados Plausíveis:</b> {', '.join(cond.get('estados_plausiveis', []))}"
        story.append(Paragraph(f"⚡ {desc_cond}", styles['CustomBullet']))
        story.append(Spacer(1, 10))
        
    doc.build(story, canvasmaker=NumberedCanvas)


def gerar_pdf_fase4(dados_cenarios, path_saida="relatorio_fase4_cenarios.pdf"):
    """Gera o PDF consolidado da Fase 4 - Cenários, Consistência e Recomendações (GATE 3)."""
    doc = SimpleDocTemplate(
        path_saida,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = get_custom_styles()
    story = []
    
    # Capa
    story.append(Spacer(1, 150))
    story.append(Paragraph("RELATÓRIO CONSOLIDADO: FASE 4", styles['CoverTitle']))
    story.append(Paragraph("Cenários Prospectivos, Auditoria de Consistência e Recomendações Contingentes (GATE 3)", styles['CoverSubtitle']))
    story.append(Spacer(1, 100))
    story.append(Paragraph("Sistema Modular de Análise Prospectiva e Cenários com IA<br/>"
                           "MGI - 2026", styles['CoverMeta']))
    story.append(PageBreak())
    
    # Seção 1: Arcabouço Metodológico e Cenários
    story.append(Paragraph("1. Arcabouço de Cenários Prospectivos", styles['CustomH1']))
    story.append(Paragraph(
        f"<b>Metodologia Utilizada:</b> {dados_cenarios.get('metodologia_sugerida', '')}<br/>"
        f"<b>Justificativa:</b> {dados_cenarios.get('justificativa_metodologica', '')}",
        styles['CustomBody']
    ))
    
    cenarios = dados_cenarios.get("cenarios", [])
    for cen in cenarios:
        story.append(Paragraph(f"Cenário: {cen.get('titulo', '')} (ID: {cen.get('id', '')})", styles['CustomH2']))
        story.append(Paragraph(f"<b>Tipo:</b> {cen.get('tipo', '').upper()} | Plausibilidade: {cen.get('plausibilidade', 0.0)*100:.0f}%", styles['CustomBody']))
        story.append(Paragraph(f"<b>Narrativa Futura:</b><br/>{cen.get('descricao', '')}", styles['CustomBody']))
        
        # Mapeamento de Condicionantes no Cenário
        conds_str = ", ".join(f"<i>{k}</i> = <b>{v}</b>" for cond_dict in cen.get('condicionantes_chaves', []) for k, v in cond_dict.items())
        story.append(Paragraph(f"Estados dos Condicionantes: {conds_str}", styles['CustomBullet']))
        
        # Comportamento dos Atores no Cenário
        atores_str = ", ".join(f"<i>{k}</i> = {v}" for ator_dict in cen.get('atores_envolvidos', []) for k, v in ator_dict.items())
        story.append(Paragraph(f"Atuação dos Atores: {atores_str}", styles['CustomBullet']))
        story.append(Spacer(1, 15))
        
    story.append(PageBreak())
    
    # Seção 2: Auditoria de Consistência
    story.append(Paragraph("2. Laudo de Consistência Lógica Interna", styles['CustomH1']))
    consist = dados_cenarios.get("consistencia", {})
    status_aprovado = "APROVADO E COERENTE" if consist.get("aprovado_consistente", False) else "PENDENTE / REPROVADO"
    story.append(Paragraph(f"<b>Status de Consistência Interna:</b> <font color='#1A365D'><b>{status_aprovado}</b></font>", styles['CustomBody']))
    
    story.append(Paragraph("Achados e Pontos Fortes de Coerência:", styles['CustomH2']))
    for achado in consist.get("achados", []):
        story.append(Paragraph(f"✔ <b>{achado.get('tema', 'Coerência')}:</b> {achado.get('detalhe', '')}", styles['CustomBullet']))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Contradições Logicamente Identificadas:", styles['CustomH2']))
    for cont in consist.get("contradicoes", []):
        story.append(Paragraph(f"✖ {cont}", styles['CustomBullet']))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Lacunas de Fundamentação:", styles['CustomH2']))
    for lac in consist.get("lacunas", []):
        story.append(Paragraph(f"⏳ {lac}", styles['CustomBullet']))
        
    story.append(PageBreak())
    
    # Seção 3: Recomendações Estratégicas
    story.append(Paragraph("3. Recomendações Contingentes e Pontes de Decisão", styles['CustomH1']))
    
    recoms = dados_cenarios.get("recomendacoes", [])
    for rec in recoms:
        story.append(Paragraph(f"Recomendação: {rec.get('titulo', '')} (ID: {rec.get('id', '')})", styles['CustomH2']))
        story.append(Paragraph(f"<b>Prioridade:</b> {rec.get('prioridade', '')} | Rastreabilidade: {rec.get('rastreabilidade_condicionante_id', '')}", styles['CustomBody']))
        story.append(Paragraph(f"Descrição Técnica: {rec.get('descricao', '')}", styles['CustomBody']))
        
        # Pontes de decisão vinculadas
        story.append(Paragraph("Pontes de Decisão (Gatilhos Operacionais):", styles['CustomH2']))
        for bridge in rec.get("pontes_decisao", []):
            story.append(Paragraph(
                f"• <b>Foco:</b> {bridge.get('oportunidade_ou_risco', '').upper()} | "
                f"<b>Cenário Alvo ID:</b> {bridge.get('cenario_id', '')}<br/>"
                f"Bifurcação Estratégica: {bridge.get('descricao', '')}<br/>"
                f"🚨 <b>Gatilho Operacional:</b> {bridge.get('gatilho', '')}<br/>"
                f"⚡ <b>Ação Imediata:</b> {bridge.get('acao_imediata', '')}",
                styles['CustomBullet']
            ))
        story.append(Spacer(1, 10))
        
    story.append(Spacer(1, 15))
    story.append(Paragraph("Conclusão do PMV:", styles['CustomH2']))
    story.append(Paragraph(dados_cenarios.get("conclusao_pmv", "Análise Concluída."), styles['CustomCallout']))
    
    doc.build(story, canvasmaker=NumberedCanvas)


def gerar_pdf_relatorio_final(dados_compilados, path_saida="relatorio_final_prospectiva_pmv.pdf"):
    """
    Gera o Relatório Master Final de Prospecção Estratégica de até 10 páginas.
    Incorpora o sumário de todas as fases precedentes de forma coesa e editorial.
    """
    doc = SimpleDocTemplate(
        path_saida,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = get_custom_styles()
    story = []
    
    # --- CAPA PREMIUM ---
    story.append(Spacer(1, 100))
    story.append(Paragraph("MINISTÉRIO DA GESTÃO E DA INOVAÇÃO DOS SERVIÇOS PÚBLICOS", styles['CoverMeta']))
    story.append(Spacer(1, 15))
    story.append(Paragraph("RELATÓRIO CONSOLIDADO DE PROSPECÇÃO ESTRATÉGICA", styles['CoverTitle']))
    story.append(Paragraph("Estudo Modular Prospectivo e Mapeamento de Cenários de Longo Prazo", styles['CoverSubtitle']))
    story.append(Spacer(1, 30))
    story.append(Paragraph("<b>DEMANDA BRUTA DE ENTRADA:</b><br/>" + dados_compilados.get("demanda_inicial", ""), styles['CustomCallout']))
    story.append(Spacer(1, 120))
    story.append(Paragraph("<b>Organização:</b> Sistema Modular de Análise Prospectiva e Cenários - PMV<br/>"
                           "<b>Modelo de Linguagem:</b> Google Gemini-3.5-flash &amp; Gemini-2.5-pro (Endógeno)<br/>"
                           "<b>Data de Emissão:</b> 2026", styles['CoverMeta']))
    story.append(PageBreak())
    
    # --- SUMÁRIO EXECUTIVO ---
    story.append(Paragraph("Sumário Executivo", styles['CustomTitle']))
    story.append(Paragraph(
        "Este documento apresenta o consolidado dos resultados do estudo prospectivo conduzido através da metodologia "
        "de funil de prospecção modular com inteligência artificial. O fluxo estruturou análises setoriais em 4 fases "
        "independentes e encadeadas lógica e matematicamente, culminando na formulação de estratégias contingentes "
        "e pontes de decisão estratégicas.",
        styles['CustomBody']
    ))
    
    resumo_executivo = dados_compilados.get("resumo_executivo", "")
    if resumo_executivo:
        story.append(Paragraph(resumo_executivo, styles['CustomBody']))
    else:
        story.append(Paragraph(
            "O estudo abrangeu desde a análise crítica da demanda bruta pela Coordenação de Metodologia, "
            "passando por workshops de debate simulando posições antagônicas públicas, corporativas e científicas, "
            "o mapeamento quantitativo de 15+ sinais e agrupamento em vetores de força, a modelagem de matrizes matemáticas "
            "estruturais de motricidade e a redação auditada de cenários alternativos e robustos.",
            styles['CustomBody']
        ))
        
    story.append(Spacer(1, 15))
    
    # --- SEÇÃO 1: DIRETRIZES E WORKSHOP ---
    story.append(Paragraph("1. Fase 1: Escopo e Workshop de Atores", styles['CustomH1']))
    story.append(Paragraph(
        "A Coordenação estabeleceu o horizonte de análise e orientou o debate. No workshop, os atores "
        "Público, Privado e Social apresentaram visões contrastantes, consolidando consensos fundamentais e divergências estruturais:",
        styles['CustomBody']
    ))
    
    dados_w = dados_compilados.get("workshop", {})
    story.append(Paragraph("<b>Consensos Críticos:</b>", styles['CustomH2']))
    for cons in dados_w.get("pontos_consenso", ["Nenhum consenso registrado."]):
        story.append(Paragraph(f"✔ {cons}", styles['CustomBullet']))
        
    story.append(Spacer(1, 5))
    story.append(Paragraph("<b>Divergências Setoriais:</b>", styles['CustomH2']))
    for div in dados_w.get("pontos_divergencia", ["Nenhuma divergência registrada."]):
        story.append(Paragraph(f"✖ {div}", styles['CustomBullet']))
        
    story.append(PageBreak())
    
    # --- SEÇÃO 2: MAPEAMENTO E ELEMENTOS ---
    story.append(Paragraph("2. Fase 2: Sinais e Elementos de Futuro", styles['CustomH1']))
    story.append(Paragraph(
        "A extração rigorosa mapeou as sementes de futuro de base factual e as correlacionou em Eventos no Horizonte. "
        "Estes eventos foram catalogados nas categorias formais de elementos estratégicos (Gate 1):",
        styles['CustomBody']
    ))
    
    dados_m = dados_compilados.get("mapeamento", {})
    story.append(Paragraph("<b>Elementos de Futuro Catalogados:</b>", styles['CustomH2']))
    for el in dados_m.get("elementos", []):
        story.append(Paragraph(f"• <b>{el.get('titulo', '')} (ID: {el.get('id', '')})</b>: Categoria <i>{el.get('categoria', '').upper()}</i>. {el.get('descricao', '')}", styles['CustomBullet']))
        
    story.append(Spacer(1, 15))
    
    # --- SEÇÃO 3: ANÁLISE ESTRUTURAL ---
    story.append(Paragraph("3. Fase 3: Matrizes de Impacto e Condicionantes", styles['CustomH1']))
    story.append(Paragraph(
        "A modelagem matemática calculou as correlações de força através da matriz de impacto cruzado "
        "e da classificação motricidade/dependência. Desta modelagem quantitativa estrita derivaram-se as variáveis "
        "motores e condicionantes de futuro que governam as bifurcações críticas do setor:",
        styles['CustomBody']
    ))
    
    dados_e = dados_compilados.get("estruturais", {})
    story.append(Paragraph("<b>Condicionantes e Estados Plausíveis (Gate 2):</b>", styles['CustomH2']))
    for cond in dados_e.get("condicionantes", []):
        story.append(Paragraph(
            f"⚡ <b>{cond.get('titulo', '')} (ID: {cond.get('id', '')})</b>: "
            f"{cond.get('descricao', '')}<br/>"
            f"<i>Estados Plausíveis: {', '.join(cond.get('estados_plausiveis', []))}</i>",
            styles['CustomBullet']
        ))
        
    story.append(PageBreak())
    
    # --- SEÇÃO 4: CENÁRIOS E RECOMENDAÇÕES ---
    story.append(Paragraph("4. Fase 4: Cenários, Auditoria e Recomendações", styles['CustomH1']))
    story.append(Paragraph(
        "Os cenários prospectivos alternativos foram gerados a partir do cruzamento de estados de condicionantes e "
        "foram rigorosamente submetidos à auditoria de consistência lógica interna (Gate 3) antes do desenvolvimento estratégico final:",
        styles['CustomBody']
    ))
    
    dados_c = dados_compilados.get("cenarios", {})
    for cen in dados_c.get("cenarios", []):
        story.append(Paragraph(f"Cenário: <b>{cen.get('titulo', '')}</b> (Tipo: {cen.get('tipo', '').upper()} | Plausibilidade: {cen.get('plausibilidade', 0.0)*100:.0f}%)", styles['CustomH2']))
        story.append(Paragraph(f"{cen.get('descricao', '')[:300]}...", styles['CustomBody']))
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Recomendações e Pontes de Decisão (Gatilhos Operacionais):</b>", styles['CustomH2']))
    for rec in dados_c.get("recomendacoes", []):
        story.append(Paragraph(f"<b>Recomendação: {rec.get('titulo', '')}</b> (ID: {rec.get('id', '')}) - Prioridade {rec.get('prioridade', '')}<br/>"
                               f"<i>Diretriz: {rec.get('descricao', '')}</i>", styles['CustomBullet']))
        for bridge in rec.get("pontes_decisao", [])[:1]: # Exibe a ponte mais crítica de cada recomendação
            story.append(Paragraph(
                f"🚨 <b>Gatilho:</b> {bridge.get('gatilho', '')} | ⚡ <b>Ação Imediata:</b> {bridge.get('acao_imediata', '')}",
                styles['CustomBullet']
            ))
            
    story.append(PageBreak())
    
    # --- ANÁLISE TRANSVERSAL DO REDATOR E CONEXÕES ESTRATÉGICAS ---
    story.append(Paragraph("5. Análise Transversal e Conclusões Estratégicas", styles['CustomTitle']))
    
    analise_transversal = dados_compilados.get("analise_transversal", "")
    if analise_transversal:
        story.append(Paragraph(analise_transversal, styles['CustomBody']))
    else:
        story.append(Paragraph(
            "Este estudo de prospecção modular com Inteligência Artificial demonstra a viabilidade metodológica "
            "e a robustez do funil prospectivo. A integração entre a análise textual rica e matrizes numéricas "
            "quantitativas mitiga o viés heurístico e a miopia estratégica. As recomendações geradas oferecem ao formulador "
            "de políticas públicas um painel contingente estruturado, pronto para acionar políticas de mitigação "
            "ou captura de valor conforme os gatilhos no horizonte estratégico comecem a sinalizar de forma clara "
            "qual cenário de futuro está emergindo.",
            styles['CustomBody']
        ))
        
    story.append(Spacer(1, 30))
    story.append(Paragraph("Conclusão Final do Estudo Executivo:", styles['CustomH2']))
    story.append(Paragraph(dados_compilados.get("conclusao_PMV", "Estudo estratégico executivo de prospecção concluído com rigor conceitual e integridade analítica."), styles['CustomCallout']))
    
    doc.build(story, canvasmaker=NumberedCanvas)
