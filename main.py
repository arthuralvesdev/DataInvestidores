# Em: main.py

import os
from src import data_handler, analysis, visualization

# --- Configurações do Projeto ---
# Arquivos de Entrada
DATA_MERCADO_FILE = 'data/dados_mercado.csv'
PERFIL_FILE = 'data/InvestidoresTesouroDireto2024.csv' # SEU ARQUIVO DE PERFIL

# Diretório de Saída
OUTPUT_DIR = 'output'

# Arquivos de Saída
DASHBOARD_MERCADO_FILE = os.path.join(OUTPUT_DIR, 'dashboard_mercado_financeiro.png')
REPORT_MERCADO_FILE = os.path.join(OUTPUT_DIR, 'relatorio_mercado_financeiro.csv')
# --- NOVA SAÍDA PARA O DASHBOARD DE PERFIL ---
DASHBOARD_PERFIL_FILE = os.path.join(OUTPUT_DIR, 'dashboard_perfil_investidores.png')


def main():
    print("INICIANDO ANÁLISE DE INVESTIDORES NO BRASIL")
    print("="*60)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- FLUXO 1: ANÁLISE DETALHADA DO MERCADO FINANCEIRO (EXISTENTE) ---
    print("\n[FLUXO 1] Executando análise do arquivo de mercado...")
    # dados_mercado = data_handler.carregar_dados_mercado(DATA_MERCADO_FILE)
    
    # if dados_mercado is not None:
    #     estatisticas = analysis.analisar_crescimento(dados_mercado)
    #     visualization.criar_dashboard_completo(dados_mercado, estatisticas, salvar_arquivo=DASHBOARD_MERCADO_FILE)
    #     data_handler.exportar_relatorio_completo(dados_mercado, nome_arquivo=REPORT_MERCADO_FILE)
    #     analise_texto = analysis.criar_analise_textual(estatisticas, dados_mercado)
    #     print("\n" + "="*60)
    #     print(analise_texto)
    #     print("="*60)
    # else:
    #     print("Não foi possível carregar os dados de mercado. Fluxo 1 ignorado.")

    # --- FLUXO 2: GERAÇÃO DO DASHBOARD DE PERFIL (NOVO) ---
    print("\n[FLUXO 2] Executando análise do arquivo de perfil do investidor...")
    dados_perfil = data_handler.carregar_dados_perfil(PERFIL_FILE)
    
    # A nova função de visualização de perfil é chamada aqui
    visualization.criar_dashboard_perfil_investidor_refatorado(dados_perfil, salvar_arquivo=DASHBOARD_PERFIL_FILE)
    
    print("\n✅ PROCESSO FINALIZADO COM SUCESSO!")
    print("Verifique os arquivos gerados na pasta 'output':")
    print(f"📊 Dashboard Mercado: {DASHBOARD_MERCADO_FILE}")
    print(f"📈 Relatório Mercado: {REPORT_MERCADO_FILE}")
    print(f"📊 Dashboard Perfil: {DASHBOARD_PERFIL_FILE}")


if __name__ == "__main__":
    main()