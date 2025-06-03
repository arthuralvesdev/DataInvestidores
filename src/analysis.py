import pandas as pd

def analisar_crescimento(df: pd.DataFrame) -> dict:

    print("\n" + "="*60)
    print("ANÁLISE DO CRESCIMENTO DE INVESTIDORES NO BRASIL")
    print("="*60)
    
    primeiro_ano = df['ano'].iloc[0]
    ultimo_ano = df['ano'].iloc[-1]
    
    # Crescimento total
    investidores_inicial = df['total_investidores_milhoes'].iloc[0]
    investidores_final = df['total_investidores_milhoes'].iloc[-1]
    crescimento_total = ((investidores_final / investidores_inicial) - 1) * 100
    
    # CPFs na B3
    cpfs_inicial = df['cpfs_b3_milhoes'].iloc[0]
    cpfs_final = df['cpfs_b3_milhoes'].iloc[-1]
    crescimento_b3 = ((cpfs_final / cpfs_inicial) - 1) * 100
    
    # Patrimônio em fundos
    patrimonio_inicial = df['patrimonio_fundos_trilhoes'].iloc[0]
    patrimonio_final = df['patrimonio_fundos_trilhoes'].iloc[-1]
    crescimento_patrimonio = ((patrimonio_final / patrimonio_inicial) - 1) * 100
    
    # Imprimir resultados
    print(f"Período analisado: {primeiro_ano} - {ultimo_ano}")
    print(f"Investidores em {ultimo_ano}: {investidores_final:.1f} milhões (Crescimento de {crescimento_total:.1f}%)")
    print(f"CPFs na B3 em {ultimo_ano}: {cpfs_final:.1f} milhões (Crescimento de {crescimento_b3:.0f}%)")
    print(f"Patrimônio em Fundos em {ultimo_ano}: R$ {patrimonio_final:.1f} trilhões (Crescimento de {crescimento_patrimonio:.1f}%)")
    
    return {
        'crescimento_total': crescimento_total,
        'crescimento_b3': crescimento_b3,
        'crescimento_patrimonio': crescimento_patrimonio
    }

def criar_analise_textual(stats: dict, df: pd.DataFrame) -> str:
    """
    Texto que aparece no terminal, uma pequena análise
    """
    analise = f"""
ANÁLISE DETALHADA: REVOLUÇÃO DOS INVESTIDORES NO BRASIL

O Brasil vive uma verdadeira revolução no mercado de investimentos. Os dados de {df['ano'].min()} a {df['ano'].max()} mostram um crescimento extraordinário.

PRINCIPAIS DESCOBERTAS:

1. EXPLOSÃO DE INVESTIDORES NA BOLSA
   - Os CPFs cadastrados na B3 saltaram de {df['cpfs_b3_milhoes'].iloc[0]:.1f} milhão para {df['cpfs_b3_milhoes'].iloc[-1]:.1f} milhões.
   - Crescimento de mais de {stats['crescimento_b3']:.0f}% em apenas {df['ano'].nunique()} anos.

2. CRESCIMENTO DO PATRIMÔNIO EM FUNDOS
   - Patrimônio em fundos cresceu de R$ {df['patrimonio_fundos_trilhoes'].iloc[0]:.1f} trilhões para R$ {df['patrimonio_fundos_trilhoes'].iloc[-1]:.1f} trilhões.
   - Aumento de {stats['crescimento_patrimonio']:.1f}% no período, superando o crescimento do PIB.
    """
    return analise