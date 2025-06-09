import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

def configurar_estilo_graficos():
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
    except:
        plt.style.use('seaborn-darkgrid') 
        
    sns.set_palette("Set2")
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9

def criar_dashboard_completo(df: pd.DataFrame, stats: dict, salvar_arquivo: str = None):
    """
    Aqui começa a criação dos Dashboards, dos gráficos.
    """
    configurar_estilo_graficos()
    
    fig = plt.figure(figsize=(22, 16))
    fig.suptitle('CRESCIMENTO DOS INVESTIMENTOS NO BRASIL (2017-2024)\n' + 
                 '', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # --- Gráfico 1: Evolução do número de investidores ---
    ax1 = plt.subplot(3, 4, 1)
    ax1.plot(df['ano'], df['total_investidores_milhoes'], 
             marker='o', linewidth=3, markersize=8, color='#1f77b4')
    ax1.fill_between(df['ano'], df['total_investidores_milhoes'], 
                     alpha=0.3, color='#1f77b4')
    ax1.set_title('Evolução Total de Investidores', fontweight='bold', pad=20)
    ax1.set_xlabel('Ano')
    ax1.set_ylabel('Investidores (milhões)')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, None)
    for i, (ano, valor) in enumerate(zip(df['ano'], df['total_investidores_milhoes'])):
        ax1.annotate(f'{valor:.1f}M', (ano, valor), textcoords="offset points", 
                     xytext=(0,10), ha='center', fontsize=9)
    
    # --- Gráfico 2: CPFs na B3 ---
    ax2 = plt.subplot(3, 4, 2)
    bars = ax2.bar(df['ano'], df['cpfs_b3_milhoes'], 
                   color='#ff7f0e', alpha=0.8, width=0.6)
    ax2.set_title('CPFs Cadastrados na B3', fontweight='bold', pad=20)
    ax2.set_xlabel('Ano')
    ax2.set_ylabel('CPFs (milhões)')
    ax2.grid(True, alpha=0.3, axis='y')
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                 f'{height:.1f}M', ha='center', va='bottom', fontsize=9)
    
    # --- Gráfico 3: Volume negociado na B3 ---
    ax3 = plt.subplot(3, 4, 3)
    ax3.plot(df['ano'], df['volume_negociado_trilhoes'],
             marker='s', linewidth=3, markersize=8, color='#2ca02c')
    ax3.set_title('Volume Negociado na B3', fontweight='bold', pad=20)
    ax3.set_xlabel('Ano')
    ax3.set_ylabel('Volume (R$ trilhões)')
    ax3.grid(True, alpha=0.3)
    
    # --- Gráfico 4: Patrimônio em fundos ---
    ax4 = plt.subplot(3, 4, 4)
    ax4.fill_between(df['ano'], df['patrimonio_fundos_trilhoes'],
                     color='#d62728', alpha=0.7)
    ax4.plot(df['ano'], df['patrimonio_fundos_trilhoes'],
             color='#d62728', linewidth=2, marker='o')
    ax4.set_title('Patrimônio em Fundos de Investimento', fontweight='bold', pad=20)
    ax4.set_xlabel('Ano')
    ax4.set_ylabel('Patrimônio (R$ trilhões)')
    ax4.grid(True, alpha=0.3)
    
    # --- Gráfico 5: Correlação com indicadores econômicos ---
    ax5 = plt.subplot(3, 4, 5)
    ax5_twin = ax5.twinx()
    line1, = ax5.plot(df['ano'], df['selic_media'], 
                     'o-', color='red', linewidth=2, label='SELIC (%)')
    line2, = ax5_twin.plot(df['ano'], df['cpfs_b3_milhoes'],
                          's-', color='blue', linewidth=2, label='CPFs B3 (milhões)')
    ax5.set_title('SELIC vs Investidores na Bolsa', fontweight='bold', pad=20)
    ax5.set_xlabel('Ano')
    ax5.set_ylabel('Taxa SELIC (%)', color='red')
    ax5_twin.set_ylabel('CPFs na B3 (milhões)', color='blue')
    ax5.grid(True, alpha=0.3)
    lines = [line1, line2]
    ax5.legend(lines, [l.get_label() for l in lines], loc='upper left')
    
    # --- Gráfico 6: PIB vs Patrimônio Total ---
    ax6 = plt.subplot(3, 4, 6)
    ax6.scatter(df['pib_trilhoes'], df['patrimonio_total_trilhoes'],
                c=df['ano'], cmap='viridis', s=100, alpha=0.8)
    ax6.set_title('PIB vs Patrimônio de Investimentos', fontweight='bold', pad=20)
    ax6.set_xlabel('PIB (R$ trilhões)')
    ax6.set_ylabel('Patrimônio Total (R$ trilhões)')
    ax6.grid(True, alpha=0.3)
    for i, ano in enumerate(df['ano']):
        ax6.annotate(str(ano), (df['pib_trilhoes'].iloc[i], 
                                df['patrimonio_total_trilhoes'].iloc[i]),
                     xytext=(5, 5), textcoords='offset points', fontsize=8)
    
    # --- Gráfico 7: Crescimento anual de investidores ---
    ax7 = plt.subplot(3, 4, 7)
    crescimento_limpo = df['crescimento_investidores'].dropna()
    anos_crescimento = df['ano'][1:]
    colors = ['green' if x > 0 else 'red' for x in crescimento_limpo]
    ax7.bar(anos_crescimento, crescimento_limpo, color=colors, alpha=0.8)
    ax7.set_title('Taxa de Crescimento Anual', fontweight='bold', pad=20)
    ax7.set_xlabel('Ano')
    ax7.set_ylabel('Crescimento (%)')
    ax7.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    ax7.grid(True, alpha=0.3, axis='y')
    
    # --- Gráfico 8: Número de fundos disponíveis ---
    ax8 = plt.subplot(3, 4, 8)
    ax8.bar(df['ano'], df['numero_fundos']/1000, 
            color='purple', alpha=0.7)
    ax8.set_title('Fundos de Investimento Disponíveis', fontweight='bold', pad=20)
    ax8.set_xlabel('Ano')
    ax8.set_ylabel('Número de Fundos (milhares)')
    ax8.grid(True, alpha=0.3, axis='y')
    
    # --- Gráfico 9: Comparação inflação vs retornos ---
    ax9 = plt.subplot(3, 4, 9)
    width = 0.35
    anos = df['ano']
    x = np.arange(len(anos))
    ax9.bar(x - width/2, df['inflacao_ipca'], width, 
            label='Inflação (IPCA)', color='orange', alpha=0.8)
    ax9.bar(x + width/2, df['selic_media'], width,
            label='SELIC', color='blue', alpha=0.8)
    ax9.set_title('Inflação vs Taxa SELIC', fontweight='bold', pad=20)
    ax9.set_xlabel('Ano')
    ax9.set_ylabel('Taxa (%)')
    ax9.set_xticks(x)
    ax9.set_xticklabels(anos)
    ax9.legend()
    ax9.grid(True, alpha=0.3, axis='y')
    
    ax10 = plt.subplot(3, 4, (10, 11))
    ax10.axis('off')
    beneficios_texto = f"""
INVESTIMENTOS NO BRASIL EM NUMEROS


• Crescimento de {stats['crescimento_total']:.0f}% em investidores
• {df['total_investidores_milhoes'].iloc[-1]:.1f} milhões de brasileiros investindo
• R$ {df['patrimonio_total_trilhoes'].iloc[-1]:.1f} trilhões em patrimônio total
• {df['empresas_listadas'].iloc[-1]} empresas listadas na B3

    """

    
    ax10.text(0.05, 0.95, beneficios_texto, transform=ax10.transAxes, fontsize=11,
              verticalalignment='top', fontfamily='monospace',
              bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.8))
    
    # --- Bloco 12: Resumo ---
    ax12 = plt.subplot(3, 4, 12)
    ax12.axis('off')
    resumo_texto = f"""
RESUMO DOS DADOS

CRESCIMENTO EXPLOSIVO:
CPFs na B3: {stats['crescimento_b3']:.0f}%
Patrimônio: {stats['crescimento_patrimonio']:.0f}%
    """
    ax12.text(0.05, 0.95, resumo_texto, transform=ax12.transAxes, fontsize=10,
              verticalalignment='top', fontfamily='monospace',
              bbox=dict(boxstyle='round,pad=1', facecolor='lightgreen', alpha=0.8))
    

def dashboardTesouroDireto(df: pd.DataFrame, salvar_arquivo: str = None):
    """
    Dashboard de perfil dos investidores do Tesouro Direto
    """
    if df is None or df.empty:
        print("[AVISO] DataFrame de perfil não fornecido ou vazio. Geração de dashboard ignorada.")
        return

    configurar_estilo_graficos()
    
    fig = plt.figure(figsize=(22, 12))
    fig.suptitle('Dashboard de Perfil dos Investidores do Tesouro Direto', 
                 fontsize=20, fontweight='bold', y=0.98)

    # --- 1. Gráfico de Gênero ---
    ax1 = plt.subplot(2, 3, 1)
    genero_counts = df['Genero'].fillna('Não Informado').value_counts()
    ax1.pie(genero_counts, labels=genero_counts.index, autopct='%1.1f%%', 
            startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
    ax1.set_title('Distribuição por Gênero')
    ax1.set_ylabel('') # Remove o rótulo do eixo y que o `pie` adiciona

    # --- 2. Gráfico de Estado Civil ---
    ax2 = plt.subplot(2, 3, 2)
    estado_civil_counts = df['Estado Civil'].fillna('Não Informado').value_counts().nlargest(5).sort_values()
    bars2 = ax2.barh(estado_civil_counts.index, estado_civil_counts.values, color='skyblue')
    ax2.set_title('Top 5 Estados Civis')
    ax2.set_xlabel('Quantidade')
    # Adicionar rótulos de dados
    for bar in bars2:
        ax2.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2, 
                 f'{int(bar.get_width())}', va='center', ha='left', fontsize=9)

    # --- 3. Distribuição de Idade ---
    ax3 = plt.subplot(2, 3, 3)
    idades_validas = pd.to_numeric(df['Idade'], errors='coerce').dropna()
    sns.histplot(idades_validas, kde=True, ax=ax3, color='salmon', bins=20)
    ax3.set_title('Distribuição por Idade')
    ax3.set_xlabel('Idade')
    ax3.set_ylabel('Frequência')
    # Adicionar linha da média
    ax3.axvline(idades_validas.mean(), color='red', linestyle='--', linewidth=2)
    ax3.text(idades_validas.mean() * 1.05, ax3.get_ylim()[1] * 0.9, 
             f'Média: {idades_validas.mean():.1f} anos', color='red')

    # --- 4. Top 10 Profissões ---
    ax4 = plt.subplot(2, 3, 4)
    profissao_counts = df['Profissao'].fillna('Não Informado').value_counts().nlargest(10).sort_values()
    bars4 = ax4.barh(profissao_counts.index, profissao_counts.values, color='mediumseagreen')
    ax4.set_title('Top 10 Profissões')
    ax4.set_xlabel('Quantidade')
    
    # --- 5. Top 10 Estados (UF) ---
    ax5 = plt.subplot(2, 3, 5)
    uf_counts = df['UF do Investidor'].fillna('Não Informado').value_counts().nlargest(10).sort_values()
    bars5 = ax5.barh(uf_counts.index, uf_counts.values, color='darkorchid')
    ax5.set_title('Top 10 UF dos Investidores')
    ax5.set_xlabel('Quantidade')
    # Adicionar rótulos de dados
    for bar in bars5:
        ax5.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2, 
                 f'{int(bar.get_width())}', va='center', ha='left', fontsize=9)

    # --- 6. Bloco de Resumo Executivo ---
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')
    
    # Gerando estatísticas para o resumo
    try:
        idade_media = f"{df['Idade'].mean():.1f} anos"
        genero_dominante = df['Genero'].mode()[0]
        uf_dominante = df['UF do Investidor'].mode()[0]
        total_investidores = len(df)
    except Exception:
        idade_media = "N/D"
        genero_dominante = "N/D"
        uf_dominante = "N/D"
        total_investidores = "N/D"
        
    resumo_texto = f"""
INSIGHTS

• Total de Investidores na Amostra: {total_investidores}
• Idade Média: {idade_media}
• Gênero Dominante: {genero_dominante}
• Estado com Mais Investidores: {uf_dominante}

O perfil predominante é de
investidores de 39,1 anos, de gênero M,
concentrados na região Sudeste.
    """
    
    ax6.text(0.05, 0.95, resumo_texto, transform=ax6.transAxes, fontsize=12,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#f0f0f0', alpha=0.9))
    
    # --- Finalização e salvamento ---
    plt.tight_layout()
    plt.subplots_adjust(top=0.94)
    
    if salvar_arquivo:
        plt.savefig(salvar_arquivo, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"\n[SUCESSO] Dashboard de perfil salvo em: {salvar_arquivo}")
    
    plt.show()

    