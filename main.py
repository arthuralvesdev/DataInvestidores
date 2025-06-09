import os
from src import data_handler, analysis, visualization

# --- Configurações do Projeto ---

DATA_MERCADO_FILE = 'data/dados_mercado.csv'
PERFIL_FILE = 'data/InvestidoresTesouroDireto2024.csv' 


OUTPUT_DIR = 'output'

DASHBOARD_MERCADO_FILE = os.path.join(OUTPUT_DIR, 'dashboardMercadoFinanceiro.png')
DASHBOARD_TESOURO_FILE = os.path.join(OUTPUT_DIR, 'dashboardTesouroDireto.png')


def main():
    print("INICIANDO ANÁLISE DE INVESTIDORES NO BRASIL")
    print("="*60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- FLUXO 1: ANÁLISE DETALHADA DO MERCADO FINANCEIRO ---
    print("\n[FLUXO 1] Executando análise do arquivo de mercado...")
    dados_mercado = data_handler.carregar_dados_mercado(DATA_MERCADO_FILE)
    
    if dados_mercado is not None:
        estatisticas = analysis.analisar_crescimento(dados_mercado)
        visualization.criar_dashboard_completo(dados_mercado, estatisticas, salvar_arquivo=DASHBOARD_MERCADO_FILE)
        analise_texto = analysis.criar_analise_textual(estatisticas, dados_mercado)
        print("\n" + "="*60)
        print(analise_texto)
        print("="*60)
    else:
        print("Não foi possível carregar os dados de mercado. Fluxo 1 ignorado.")

    # --- FLUXO 2: GERAÇÃO DO DASHBOARD DE PERFIL ---
    print("\n[FLUXO 2] Executando análise do arquivo de perfil do investidor...")
    dados_perfil = data_handler.carregar_dados_perfil(PERFIL_FILE)
    
    visualization.dashboardTesouroDireto(dados_perfil, salvar_arquivo=DASHBOARD_TESOURO_FILE)
    
    print("\nPROCESSO FINALIZADO COM SUCESSO!")
    print("Verifique os arquivos gerados na pasta 'output':")
    print(f"Dashboard Mercado: {DASHBOARD_MERCADO_FILE}")
    print(f"Dashboard Perfil: {DASHBOARD_TESOURO_FILE}")


if __name__ == "__main__":
    main()