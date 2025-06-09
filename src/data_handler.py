import pandas as pd

def carregar_dados_mercado(caminho_arquivo: str) -> pd.DataFrame:

    print(f"Carregando dados de: {caminho_arquivo}")
    df = pd.read_csv(caminho_arquivo)

    # Calcular métricas derivadas de investidores
    df['total_investidores_milhoes'] = (
        df['cpfs_b3_milhoes'] + 
        df['cotistas_milhoes'] * 0.3  
    )

    df['crescimento_investidores'] = (
        df['total_investidores_milhoes'].pct_change() * 100
    )

    df['patrimonio_total_trilhoes'] = (
        df['volume_negociado_trilhoes'] * 0.2 + 
        df['patrimonio_fundos_trilhoes']
    )

    print(f"Dados carregados: {len(df)} anos de histórico")
    return df

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
    Carrega os dados de perfil do investidor
    """
    print(f"\n[DIAGNÓSTICO] Tentando carregar dados de perfil de: {caminho_arquivo}")
    try:
        df = pd.read_csv(caminho_arquivo, sep=';', on_bad_lines='warn')

        if df.empty:
            print("ERRO CRÍTICO: O arquivo foi lido, mas o DataFrame está vazio. Verifique o conteúdo do CSV.")
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
        print(f"ERRO CRÍTICO: Arquivo de perfil '{caminho_arquivo}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"ERRO CRÍTICO ao carregar o arquivo de perfil: {e}")
        return None

# def exportar_relatorio_completo(df: pd.DataFrame, nome_arquivo: str):

#     """
#     Exporta o DataFrame completo para um arquivo CSV.
#     """
#     colunas_portugues = {
#         'ano': 'Ano', 'cpfs_b3_milhoes': 'CPFs_B3_Milhões', 'volume_negociado_trilhoes': 'Volume_Negociado_Trilhões_R$',
#         'empresas_listadas': 'Empresas_Listadas_B3', 'patrimonio_fundos_trilhoes': 'Patrimônio_Fundos_Trilhões_R$',
#         'numero_fundos': 'Número_Fundos_Disponíveis', 'cotistas_milhoes': 'Cotistas_Fundos_Milhões',
#         'total_investidores_milhoes': 'Total_Investidores_Milhões', 'crescimento_investidores': 'Crescimento_Anual_%',
#         'patrimonio_total_trilhoes': 'Patrimônio_Total_Trilhões_R$', 'pib_trilhoes': 'PIB_Trilhões_R$',
#         'selic_media': 'Taxa_SELIC_Média_%', 'inflacao_ipca': 'Inflação_IPCA_%', 'desemprego': 'Taxa_Desemprego_%'
#     }

#     relatorio_final = df.rename(columns=colunas_portugues).round(2)
#     relatorio_final.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')
#     print(f"Relatório completo exportado para: {nome_arquivo}")