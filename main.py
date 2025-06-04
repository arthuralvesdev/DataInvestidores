import os
from src import data_handler, analysis, visualization

# --- Configurações do Projeto ---
DATA_FILE = 'data/dados_mercado.csv'
TESOURO_FILE = 'data/InvestidoresTesouroDireto2024.csv'
OUTPUT_DIR = 'output'
DASHBOARD_FILE = os.path.join(OUTPUT_DIR, 'investidores_brasil_dashboard.png')
REPORT_FILE = os.path.join(OUTPUT_DIR, 'relatorio_investidores_brasil.csv')


def main():
    """
    Função principal para executar a análise completa.
    """
    print("INICIANDO ANÁLISE DE INVESTIDORES NO BRASIL")
    print("="*60)
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1. Carregar e processar os dados
    dados_completos = data_handler.carregar_dados(DATA_FILE)
    
    # 2. Realizar análise estatística
    estatisticas = analysis.analisar_crescimento(dados_completos)
    
    # 3. Gerar e exibir o dashboard visual
    visualization.criar_dashboard_completo(dados_completos, estatisticas, salvar_arquivo=DASHBOARD_FILE)
    
    # 4. Exportar o relatório completo em CSV
    data_handler.exportar_relatorio_completo(dados_completos, nome_arquivo=REPORT_FILE)
    
    # 5. Gerar e imprimir a análise textual
    analise_texto = analysis.criar_analise_textual(estatisticas, dados_completos)
    print("\n" + "="*60)
    print(analise_texto)
    print("="*60)

    print("\n PROCESSO FINALIZADO COM SUCESSO!")
    print("ARQUIVOS GERADOS NA PASTA 'output':")
    print(f"📊 {DASHBOARD_FILE}")
    print(f"📈 {REPORT_FILE}")


if __name__ == "__main__":
    main()