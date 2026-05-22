import os
import sys
import re

# Desativa a telemetria do CrewAI para acelerar a inicialização e evitar erros de rede
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_TELEMETRY_OPT_OUT"] = "true"

# Garante suporte a UTF-8 nos consoles do Windows para evitar erros de codificação de emojis e caixas
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr.encoding != 'utf-8':
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Carrega arquivos .env locais se houver
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from crew import AnaliseProspectivaCrew

class Tee(object):
    """Classe para duplicar saídas do console para a tela e para o arquivo de log do PMV."""
    def __init__(self, file_object, original_stream):
        self.file = file_object
        self.stream = original_stream
        # Expressão regular para remover códigos de escape ANSI (cores do console)
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def write(self, data):
        try:
            # Filtra os códigos de cores ANSI para salvar um log limpo no arquivo .md
            clean_data = self.ansi_escape.sub('', data)
            # Evita que crases triplas no console quebrem a formatação do bloco markdown
            clean_data = clean_data.replace("```", "'''")
            self.file.write(clean_data)
            self.file.flush()
        except Exception:
            pass
        self.stream.write(data)
        self.stream.flush()

    def flush(self):
        try:
            self.file.flush()
        except Exception:
            pass
        self.stream.flush()

def print_banner():
    banner = """
================================================================================
     PMV - SISTEMA MODULAR DE ANÁLISE PROSPECTIVA E GERAÇÃO DE CENÁRIOS
================================================================================
    * Framework: CrewAI
    * LLM Base: Google Gemini (gemini-3.5-flash com fallback gemini-2.5-pro)
    * Processo: Funil Prospectivo Metodológico v5 (Revisado)
    * Abordagem: Conhecimento LLM Endógeno (Sem upload de arquivos externos)
================================================================================
    """
    print(banner)

def verify_environment():
    """Verifica se há credenciais da API do Gemini configuradas."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("[AVISO] Nenhuma chave de API da Google foi encontrada nas variáveis de ambiente.")
        print("Por favor, configure GEMINI_API_KEY ou GOOGLE_API_KEY para evitar erros de execução.")
        print("Exemplo no PowerShell:")
        print("  $env:GEMINI_API_KEY='sua_chave_aqui'")
        print("="*80)
    else:
        print("[PMV] Credenciais do Google Gemini detectadas no ambiente.")

def slugify(text):
    """Gera um slug amigável para nomes de diretórios a partir de uma string,
    removendo acentos, caracteres especiais e espaços extras.
    """
    import unicodedata
    # Normaliza para decompor caracteres acentuados (NFD)
    text = unicodedata.normalize('NFKD', text)
    # Remove os acentos (caracteres que pertencem à categoria de marcação Unicode 'Mn')
    text = "".join([c for c in text if not unicodedata.combining(c)])
    # Converte para minúsculas
    text = text.lower()
    # Substitui caracteres não alfanuméricos por hífen ou underline
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    # Substitui múltiplos espaços ou hífens por um único underline para diretório amigável
    text = re.sub(r'[\s-]+', '_', text).strip('_')
    # Limita o tamanho do slug para não ultrapassar limites de nomes de diretórios
    return text[:50]

def main():
    import datetime
    demanda_bruta = ""
    default_demand = (
        "Como a transição demográfica acelerada no Brasil impactará a sustentabilidade da "
        "previdência social e as políticas públicas de saúde e assistência social até 2050?"
    )
    
    # Captura a demanda se fornecida como argumento ou via input interativo
    if len(sys.argv) > 1:
        demanda_bruta = " ".join(sys.argv[1:])
    else:
        print_banner()
        verify_environment()
        print("[PMV] Nenhuma demanda fornecida por argumento de linha de comando.")
        print(f"Demanda padrão sugerida:\n  '{default_demand}'\n")
        print("Pressione ENTER para usar a demanda padrão sugerida ou")
        user_input = input("digite sua própria demanda e pressione ENTER:\n> ").strip()
        if user_input:
            demanda_bruta = user_input
        else:
            demanda_bruta = default_demand

    # Carimbo de data/hora para isolamento e slug do termo da demanda
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    slug = slugify(demanda_bruta) or "analise"
    folder_name = f"analise_{timestamp}_{slug}"
    folder_path = os.path.join("analises", folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    # Configura o diretório global da Crew para isolamento dos relatórios e gates
    import crew
    crew.OUTPUT_DIR_GLOBAL = folder_path
    
    log_filename = os.path.join(folder_path, "log_execucao_pmv.md")
    
    # Inicializa o cabeçalho em Markdown para o log de auditoria do PMV
    with open(log_filename, "w", encoding="utf-8") as f:
        f.write("# REGISTRO DE AUDITORIA DE EXECUÇÃO DO PMV - ANÁLISE PROSPECTIVA\n\n")
        f.write("Este arquivo registra todas as mensagens em tela, pensamentos de agentes e saídas intermediárias do console do PMV.\n\n")
        f.write("```text\n")
        
    log_file = open(log_filename, "a", encoding="utf-8")
    
    original_stdout = sys.stdout
    original_stderr = sys.stderr
    
    # Habilita o Tee para capturar saídas e erros
    sys.stdout = Tee(log_file, original_stdout)
    sys.stderr = Tee(log_file, original_stderr)
    
    try:
        # Se a demanda veio por CLI, ainda não mostramos o banner com Tee ativo, mostramos agora para auditoria
        if len(sys.argv) > 1:
            print_banner()
            verify_environment()
            
        print(f"\n[PMV] Demanda Recebida para Análise:\n  '{demanda_bruta}'\n")
        print(f"[PMV] Pasta de Saída da Rodada isolada criada em: '{folder_path}'")
        print("[PMV] Iniciando orquestração multiagente...")
        
        # Instancia e roda o fluxo do PMV
        prospecção = AnaliseProspectivaCrew(demanda_inicial=demanda_bruta)
        resultado_final = prospecção.kickoff()
        
        print("\n" + "="*80)
        print("                    SUMÁRIO EXECUTIVO DO PMV FINALIZADO                    ")
        print("="*80)
        print(f"\n[PMV] Relatório Gerencial de Recomendações e Pontes de Decisão:\n")
        print(resultado_final)
        print("="*80)
        print("\n[PMV] Relatórios de validação dos Gates gerados assincronamente:")
        print(f"  1. {os.path.join(folder_path, 'gate_elementos.md')}       -> Validação da Classificação dos Elementos")
        print(f"  2. {os.path.join(folder_path, 'gate_condicionantes.md')}  -> Validação dos Condicionantes pós Análise Estrutural")
        print(f"  3. {os.path.join(folder_path, 'gate_consistencia.md')}    -> Laudo de Auditoria de Consistência dos Cenários")
        print("\n[PMV] Estudo de Futuro concluído com êxito metodológico.")
        print("="*80)
        
    except Exception as e:
        print(f"\n[PMV Erro] Ocorreu uma falha crítica durante a execução do fluxo: {e}")
        print("Verifique a chave de API e a conexão com o endpoint de LLM da Google.")
        sys.exit(1)
        
    finally:
        # Restaura os fluxos de console e fecha o arquivo de auditoria
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        
        try:
            log_file.write("\n```\n\n")
            log_file.write("## 🏁 Fim do Registro de Auditoria do PMV\n\n")
            log_file.write("Os seguintes relatórios de Gates de validação foram gerados nesta execução do PMV:\n\n")
            log_file.write("- 📁 **GATE 1 - Classificação dos Elementos**: [gate_elementos.md](gate_elementos.md)\n")
            log_file.write("- 📁 **GATE 2 - Validação de Condicionantes**: [gate_condicionantes.md](gate_condicionantes.md)\n")
            log_file.write("- 📁 **GATE 3 - Auditoria de Consistência dos Cenários**: [gate_consistencia.md](gate_consistencia.md)\n\n")
            log_file.write("---\n\n")
            log_file.write("### 📝 Informações de Execução\n")
            log_file.write(f"- **Demanda Processada**: `{demanda_bruta}`\n")
            log_file.write("- **Status de Auditoria**: Registro Concluído\n")
        except Exception:
            pass
            
        log_file.close()
        print(f"\n[PMV] Log de execução de tela salvo com sucesso em '{log_filename}'.\n")
        
        # Converte o log .md em um PDF monoespaçado premium
        try:
            print("[PMV] Iniciando a conversão do log de execução para PDF...")
            from pdf_generator import gerar_pdf_log
            with open(log_filename, "r", encoding="utf-8") as f_read:
                conteudo_log = f_read.read()
            
            log_pdf_path = os.path.join(folder_path, "log_execucao_pmv.pdf")
            gerar_pdf_log(conteudo_log, log_pdf_path)
            print(f"[PMV] Log de execução convertido em PDF com sucesso: '{log_pdf_path}'.")
        except Exception as e_pdf:
            print(f"[PMV Erro] Falha ao converter log de execução para PDF: {e_pdf}")

if __name__ == "__main__":
    main()

