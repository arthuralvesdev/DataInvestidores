# Em: src/data_handler.py

import pandas as pd

# ... (a função carregar_dados_mercado continua igual) ...
def carregar_dados_mercado(caminho_arquivo: str) -> pd.DataFrame:
    print(f"Carregando dados de mercado de: {caminho_arquivo}")
    try:
        df = pd.read_csv(caminho_arquivo)
        df['total_investidores_milhoes'] = (df['cpfs_b3_milhoes'] + df['cotistas_milhoes'] * 0.3)
        df['crescimento_investidores'] = (df['total_investidores_milhoes'].pct_change() * 100)
        df['patrimonio_total_trilhoes'] = (df['volume_negociado_trilhoes'] * 0.2 + df['patrimonio_fundos_trilhoes'])
        print(f"Dados de mercado carregados: {len(df)} anos de histórico")
        return df
    except FileNotFoundError:
        print(f"Erro Crítico: Arquivo de mercado '{caminho_arquivo}' não encontrado.")
        return None

def carregar_dados_perfil(caminho_arquivo: str) -> pd.DataFrame:
    """
    Carrega os dados de perfil do investidor e faz uma limpeza e verificação robusta.
    """
    print(f"\n[DIAGNÓSTICO] Tentando carregar dados de perfil de: {caminho_arquivo}")
    try:
        df = pd.read_csv(caminho_arquivo, sep=';', on_bad_lines='warn')
        
        # VERIFICAÇÃO CRÍTICA: O DataFrame está vazio?
        if df.empty:
            print("❌ ERRO CRÍTICO: O arquivo foi lido, mas o DataFrame está vazio. Verifique o conteúdo do CSV.")
            return None

        print("[DIAGNÓSTICO] Nomes das colunas encontradas:", df.columns.tolist())
        
        colunas_texto = ['Estado Civil', 'Genero', 'Profissao', 'UF do Investidor']
        for coluna in colunas_texto:
            if coluna in df.columns:
                df[coluna] = df[coluna].astype(str).str.strip().str.title()
            else:
                print(f"[ALERTA] Coluna esperada '{coluna}' não foi encontrada no arquivo.")
        
        print(f"Dados de perfil carregados e limpos: {len(df)} linhas.")
        return df
    except FileNotFoundError:
        print(f"❌ ERRO CRÍTICO: Arquivo de perfil '{caminho_arquivo}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"❌ ERRO CRÍTICO ao carregar o arquivo de perfil: {e}")
        return None

# ... (a função exportar_relatorio_completo continua igual) ...