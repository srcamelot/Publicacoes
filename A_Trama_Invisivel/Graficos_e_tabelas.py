# ============================================================================
# Análise da Distribuição de Gênero nos Grupos de Pesquisa do Brasil
# ============================================================================
# – adaptado para o artigo.
# OBJETIVO:
#   Gerar tabelas e gráficos para o artigo científico "A Trama Invisível:
#   Gênero, Tempo e Liderança na Tapeçaria da Ciência Brasileira".
#   O código processa os dados do Diretório dos Grupos de Pesquisa do CNPq
#   (2000-2025) e produz visualizações que evidenciam:
#     - A evolução da distribuição etária e de gênero;
#     - A assimetria na ocupação de lideranças;
#     - A relação entre presença feminina na base e no poder.
#
# DESENVOLVIDO POR:
#   Conselho Nacional de Desenvolvimento Científico e Tecnológico (CNPq).
#   Diretoria de Análise de Resultados e Soluções Digitais (DASD) 
#   Coordenação-Geral de Apoio e de Análise dos Resultados do Fomento (CGARF) 
#   Coordenação de Apoio ao Monitoramento e Análise de Resultados (COMAR)
#   Equipe COMAR.
#   Data: março de 2026.
#
# DADOS UTILIZADOS:
#   Tabelas originais extraídas do Diretório dos Grupos de Pesquisa do CNPq:
#     - "pesquisadores por sexo e faixa etaria.png"
#     - "por liderança e sexo 3.png"
#   Os valores foram digitados manualmente com base nos arquivos fornecidos.
#
# SAÍDAS:
#   - Três tabelas exibidas no console (distribuição etária, evolução da
#     participação feminina, proporção de líderes por sexo);
#   - Dez gráficos salvos como arquivos PNG de alta resolução (300 dpi);
#   - Um arquivo Excel (tabelas_artigo.xlsx) com todas as tabelas.
#
# DEPENDÊNCIAS:
#   Python 3.x com as bibliotecas:
#     - matplotlib
#     - numpy
#     - pandas
#     - openpyxl (para exportar para Excel)
#
# COMO EXECUTAR:
#   $ python Graficos_e_tabelas.py
#   Os gráficos serão salvos no mesmo diretório do script.
#
# ============================================================================
# ============================================================================

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import openpyxl
import openpyxl

# ============================================================================
# 1. DADOS
# ============================================================================

# --- Dados etários ---
anos_idade = [2000, 2002, 2004, 2006, 2008, 2010, 2014, 2016, 2023, 2025]

# Faixas etárias (exclui "Não informado")
faixas_etarias = ['-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65+']

# Percentuais masculinos (apenas faixas etárias)
masc_perc = [
    [0.14, 0.00, 0.01, 0.00, 0.00, 0.00, 0.01, 0.01, 0.01, 0.00],
    [0.20, 0.22, 0.30, 0.30, 0.30, 0.31, 0.30, 0.23, 0.21, 0.20],
    [1.92, 2.04, 2.58, 2.64, 2.70, 3.01, 2.96, 2.69, 1.59, 1.48],
    [6.02, 5.65, 5.94, 6.13, 6.20, 7.05, 7.63, 7.37, 4.66, 4.10],
    [10.13, 9.95, 8.74, 7.86, 7.73, 7.84, 8.58, 9.15, 8.18, 7.52],
    [10.19, 9.92, 9.97, 9.69, 8.80, 7.54, 7.27, 7.32, 9.07, 8.78],
    [9.89, 9.34, 8.38, 8.05, 7.96, 7.97, 6.60, 6.10, 7.07, 7.69],
    [7.91, 8.22, 7.72, 7.06, 6.56, 6.06, 6.04, 6.06, 5.31, 5.53],
    [4.57, 4.89, 5.15, 5.33, 5.34, 4.96, 4.40, 4.38, 4.54, 4.27],
    [2.31, 2.42, 2.62, 2.84, 3.07, 3.15, 3.30, 3.10, 3.29, 3.64],
    [1.43, 1.60, 1.89, 2.07, 2.28, 2.40, 2.94, 3.22, 3.90, 4.27]
]

# Percentuais femininos (apenas faixas etárias)
fem_perc = [
    [0.07, 0.00, 0.00, 0.00, 0.00, 0.01, 0.01, 0.01, 0.01, 0.01],
    [0.27, 0.28, 0.39, 0.39, 0.44, 0.41, 0.44, 0.37, 0.37, 0.36],
    [2.23, 2.50, 2.75, 2.99, 3.15, 3.58, 3.22, 2.98, 2.23, 2.09],
    [5.10, 5.28, 5.96, 6.23, 6.43, 7.27, 7.98, 7.75, 5.46, 4.83],
    [8.38, 8.57, 7.64, 7.52, 7.78, 7.95, 8.54, 9.23, 8.99, 8.34],
    [8.33, 8.57, 9.04, 9.07, 8.39, 7.47, 7.38, 7.54, 9.69, 9.79],
    [8.30, 8.57, 7.98, 7.85, 8.12, 8.20, 6.82, 6.48, 7.66, 8.37],
    [5.67, 6.33, 6.47, 6.66, 6.57, 6.26, 6.40, 6.33, 5.94, 6.25],
    [2.68, 3.43, 3.82, 4.18, 4.50, 4.49, 4.39, 4.47, 4.88, 4.75],
    [1.15, 1.47, 1.72, 1.99, 2.32, 2.49, 2.71, 2.83, 3.42, 3.82],
    [0.64, 0.73, 0.95, 1.13, 1.36, 1.56, 2.08, 2.38, 3.52, 3.90]
]

# Linha "Não informado" para cada sexo (valores extraídos da tabela original)
masc_ni = [1.60, 0.02, 0.01, 0.00, 0.00, 0.01, 0.00, 0.00, 0.00, 0.00]
fem_ni  = [0.86, 0.01, 0.01, 0.00, 0.00, 0.00, 0.02, 0.01, 0.00, 0.00]

# Categorias completas para a tabela
categorias = faixas_etarias + ['Não informado']

# --- Dados de liderança ---
anos_lead = [2000, 2002, 2004, 2006, 2008, 2010, 2014, 2016, 2023, 2025]

lideres_f = [6485, 8569, 11058, 12420, 13891, 16802, 13873, 15092, 17407, 17774]
nao_lideres_f = [17257, 21338, 30670, 37497, 44881, 57188, 76194, 85422, 112243, 123252]

lideres_m = [9971, 12493, 15432, 16289, 17297, 20452, 16281, 17326, 19106, 19127]
nao_lideres_m = [21226, 24022, 33591, 38981, 45004, 56143, 73844, 81688, 99784, 108436]

nao_info_lideres = [12, 0, 35, 21, 9, 15, 1, 1, 7, 0]
nao_info_nao_lideres = [129, 9, 346, 269, 55, 216, 68, 37, 4, 143]

# Totais incluindo Não Informado
total_f = [l + n for l, n in zip(lideres_f, nao_lideres_f)]
total_m = [l + n for l, n in zip(lideres_m, nao_lideres_m)]
total_ni = [l + n for l, n in zip(nao_info_lideres, nao_info_nao_lideres)]
total_geral = [tf + tm + tni for tf, tm, tni in zip(total_f, total_m, total_ni)]
total_lideres = [lf + lm + lni for lf, lm, lni in zip(lideres_f, lideres_m, nao_info_lideres)]

# Proporções úteis
pct_f_total = [tf / tg * 100 for tf, tg in zip(total_f, total_geral)]
pct_f_lider = [lf / tl * 100 for lf, tl in zip(lideres_f, total_lideres)]

# ============================================================================
# 2. TABELAS (impressão no console e exportação para Excel)
# ============================================================================

# --- TABELA 1: Distribuição percentual completa por sexo e faixa etária ---
print("\n" + "="*100)
print("TABELA 1 – Distribuição percentual de pesquisadores por sexo e faixa etária (2000–2025)")
print("="*100)

# Masculino
data_m = {'Categoria': categorias}
for i, ano in enumerate(anos_idade):
    col_m = [round(masc_perc[j][i], 2) for j in range(len(faixas_etarias))]
    col_m.append(round(masc_ni[i], 2))
    data_m[f'{ano}'] = col_m
df_m = pd.DataFrame(data_m)
print("\n--- MASCULINO ---")
print(df_m.to_string(index=False))

# Feminino
data_f = {'Categoria': categorias}
for i, ano in enumerate(anos_idade):
    col_f = [round(fem_perc[j][i], 2) for j in range(len(faixas_etarias))]
    col_f.append(round(fem_ni[i], 2))
    data_f[f'{ano}'] = col_f
df_f = pd.DataFrame(data_f)
print("\n--- FEMININO ---")
print(df_f.to_string(index=False))

# --- TABELA 2: Evolução da participação feminina ---
print("\n" + "="*80)
print("TABELA 2 – Evolução da participação feminina no total de pesquisadores e na liderança (2000–2025)")
print("="*80)

tab2_data = []
for i, ano in enumerate(anos_lead):
    tab2_data.append([ano, total_f[i], total_geral[i], round(pct_f_total[i], 1),
                     lideres_f[i], total_lideres[i], round(pct_f_lider[i], 1),
                     round(pct_f_lider[i] - pct_f_total[i], 1)])
df_tab2 = pd.DataFrame(tab2_data, columns=['Ano', 'Total mulheres', 'Total geral',
                                           '% mulheres no total', 'Líderes mulheres',
                                           'Total líderes', '% mulheres líderes', 'Diferença (pp)'])
print(df_tab2.to_string(index=False))

# --- TABELA 3: Proporção de líderes por sexo ---
print("\n" + "="*80)
print("TABELA 3 – Proporção de líderes por sexo (2000–2025)")
print("="*80)

tab3_data = []
for i, ano in enumerate(anos_lead):
    pct_m = lideres_m[i] / total_m[i] * 100
    pct_f = lideres_f[i] / total_f[i] * 100
    tab3_data.append([ano, round(pct_m,1), round(pct_f,1), round(pct_f - pct_m,1)])
df_tab3 = pd.DataFrame(tab3_data, columns=['Ano', '% Líderes homens', '% Líderes mulheres', 'Diferença (p.p.)'])
print(df_tab3.to_string(index=False))

# --- Exportar todas as tabelas para um arquivo Excel ---
with pd.ExcelWriter('tabelas_artigo.xlsx', engine='openpyxl') as writer:
    df_m.to_excel(writer, sheet_name='Distribuição_Etaria_Masculino', index=False)
    df_f.to_excel(writer, sheet_name='Distribuição_Etaria_Feminino', index=False)
    df_tab2.to_excel(writer, sheet_name='Participacao_Feminina_Lideranca', index=False)
    df_tab3.to_excel(writer, sheet_name='Proporcao_Lideres', index=False)

print("\nTabelas exportadas para 'tabelas_artigo.xlsx'.")

# ============================================================================
# 3. FUNÇÕES PARA GERAR OS GRÁFICOS
# ============================================================================

def plot_curvas_etarias():
    """Gráfico de linhas (curvas etárias) para todos os anos disponíveis (2000–2025)."""
    plt.figure(figsize=(14, 8))
    cmap_m = plt.cm.Blues   # azul para masculino
    cmap_f = plt.cm.Reds    # vermelho para feminino

    for i, ano in enumerate(anos_idade):
        idx = anos_idade.index(ano)
        m_vals = [masc_perc[j][idx] for j in range(len(faixas_etarias))]
        f_vals = [fem_perc[j][idx] for j in range(len(faixas_etarias))]

        # Intensidade da cor cresce com o ano
        color_m = cmap_m(0.3 + i / len(anos_idade) * 0.6)
        color_f = cmap_f(0.3 + i / len(anos_idade) * 0.6)

        plt.plot(faixas_etarias, m_vals, marker='o', linestyle='-',
                 color=color_m, linewidth=1.5, markersize=4,
                 label=f'Masculino {ano}')
        plt.plot(faixas_etarias, f_vals, marker='s', linestyle='-',
                 color=color_f, linewidth=1.5, markersize=4,
                 label=f'Feminino {ano}')

    plt.xlabel('Faixa Etária', fontsize=12)
    plt.ylabel('Percentual de Pesquisadores (%)', fontsize=12)
    plt.title('Distribuição Etária de Pesquisadores por Sexo (2000–2025)', fontsize=14)
    # Legenda colocada à direita para não ocupar espaço do gráfico
    plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=8)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('curvas_etarias.png', dpi=300, bbox_inches='tight')
    plt.close()

def plot_piramide_etaria(ano=2025):
    """Pirâmide populacional para um ano específico."""
    idx = anos_idade.index(ano)
    m_vals = [masc_perc[i][idx] for i in range(len(faixas_etarias))]
    f_vals = [fem_perc[i][idx] for i in range(len(faixas_etarias))]
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(faixas_etarias, [-m for m in m_vals], color='#1f77b4', label='Masculino')
    ax.barh(faixas_etarias, f_vals, color='#d62728', label='Feminino')
    ax.axvline(0, color='black', linewidth=0.8)
    ax.set_xlabel('Percentual de pesquisadores (%)')
    ax.set_title(f'Pirâmide etária dos pesquisadores brasileiros ({ano})')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f'piramide_etaria_{ano}.png', dpi=300)
    plt.close()

def plot_stacked_bars():
    """Gráfico de barras empilhadas para composição etária (anos 2000, 2010, 2025)."""
    anos_plot = [2000, 2010, 2025]
    fig, axes = plt.subplots(1, 3, figsize=(15, 6), sharey=True)
    for ax, ano in zip(axes, anos_plot):
        idx = anos_idade.index(ano)
        m_vals = [masc_perc[i][idx] for i in range(len(faixas_etarias))]
        f_vals = [fem_perc[i][idx] for i in range(len(faixas_etarias))]
        ax.bar(faixas_etarias, m_vals, color='#1f77b4', label='Masculino')
        ax.bar(faixas_etarias, f_vals, bottom=m_vals, color='#d62728', label='Feminino')
        ax.set_title(ano)
        ax.set_ylabel('Percentual (%)')
        ax.legend()
        ax.tick_params(axis='x', rotation=45)
    fig.suptitle('Composição etária por sexo (barras empilhadas)', fontsize=14)
    plt.tight_layout()
    plt.savefig('stacked_bars.png', dpi=300)
    plt.close()

def plot_area_etaria():
    """Gráfico de área empilhada para evolução das faixas etárias (por sexo)."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
    
    # Construir listas de séries: cada série é uma faixa etária com valores ao longo dos anos
    masc_series = [ [masc_perc[i][j] for j in range(len(anos_idade))] for i in range(len(faixas_etarias)) ]
    fem_series  = [ [fem_perc[i][j] for j in range(len(anos_idade))] for i in range(len(faixas_etarias)) ]
    
    # Cores para as áreas
    cores_masc = plt.cm.Blues(np.linspace(0.4, 0.9, len(faixas_etarias)))
    cores_fem  = plt.cm.Reds(np.linspace(0.4, 0.9, len(faixas_etarias)))
    
    axes[0].stackplot(anos_idade, *masc_series, labels=faixas_etarias, alpha=0.7, colors=cores_masc)
    axes[0].set_title('Masculino')
    axes[0].set_ylabel('Percentual de pesquisadores (%)')
    axes[0].legend(loc='upper left', fontsize=8)
    
    axes[1].stackplot(anos_idade, *fem_series, labels=faixas_etarias, alpha=0.7, colors=cores_fem)
    axes[1].set_title('Feminino')
    axes[1].legend(loc='upper left', fontsize=8)
    
    for ax in axes:
        ax.set_xlabel('Ano')
        ax.set_xticks(anos_idade[::2])
        ax.set_xticklabels(anos_idade[::2], rotation=45)
    
    fig.suptitle('Evolução da distribuição etária por sexo (áreas empilhadas)', fontsize=14)
    plt.tight_layout()
    plt.savefig('area_etaria.png', dpi=300)
    plt.close()

def plot_lideranca_dual():
    """Gráfico com duas escalas: número absoluto (barras) e proporção (linhas)."""
    fig, ax1 = plt.subplots(figsize=(10, 5))
    ax1.bar(anos_lead, lideres_m, width=1.5, color='#1f77b4', alpha=0.6, label='Líderes homens')
    ax1.bar(anos_lead, lideres_f, width=1.5, color='#d62728', alpha=0.6, label='Líderes mulheres', bottom=lideres_m)
    ax1.set_xlabel('Ano')
    ax1.set_ylabel('Número de líderes')
    ax1.legend(loc='upper left')
    ax2 = ax1.twinx()
    prop_m = [l/t*100 for l,t in zip(lideres_m, total_m)]
    prop_f = [l/t*100 for l,t in zip(lideres_f, total_f)]
    ax2.plot(anos_lead, prop_m, 's-', color='darkblue', linewidth=2, label='% líderes homens')
    ax2.plot(anos_lead, prop_f, 'o-', color='darkred', linewidth=2, label='% líderes mulheres')
    ax2.set_ylabel('Proporção de líderes (%)')
    ax2.legend(loc='upper right')
    plt.title('Liderança: números absolutos (barras) e proporções (linhas)')
    plt.tight_layout()
    plt.savefig('lideranca_dual.png', dpi=300)
    plt.close()

def plot_lideranca_proporcao():
    """Gráfico de linhas apenas com a proporção de líderes por sexo."""
    plt.figure(figsize=(10, 5))
    prop_m = [l/t*100 for l,t in zip(lideres_m, total_m)]
    prop_f = [l/t*100 for l,t in zip(lideres_f, total_f)]
    plt.plot(anos_lead, prop_m, 's-', color='#1f77b4', label='Masculino')
    plt.plot(anos_lead, prop_f, 'o-', color='#d62728', label='Feminino')
    plt.xlabel('Ano do Censo')
    plt.ylabel('Proporção de líderes (%)')
    plt.title('Proporção de líderes em grupos de pesquisa por sexo')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.xticks(anos_lead, rotation=45)
    plt.tight_layout()
    plt.savefig('lideranca_proporcao.png', dpi=300)
    plt.close()

def plot_lideranca_absoluto():
    """Gráfico de linhas com números absolutos de líderes."""
    plt.figure(figsize=(10, 5))
    plt.plot(anos_lead, lideres_m, 's-', color='#1f77b4', label='Masculino')
    plt.plot(anos_lead, lideres_f, 'o-', color='#d62728', label='Feminino')
    plt.xlabel('Ano do Censo')
    plt.ylabel('Número de líderes')
    plt.title('Número absoluto de líderes em grupos de pesquisa por sexo')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.xticks(anos_lead, rotation=45)
    plt.tight_layout()
    plt.savefig('lideranca_absoluto.png', dpi=300)
    plt.close()

def plot_heatmap():
    """Heatmap da participação feminina por faixa etária e ano."""
    # Matriz: linhas = faixas, colunas = anos
    fem_share = np.zeros((len(faixas_etarias), len(anos_idade)))
    for i, faixa in enumerate(faixas_etarias):
        for j, ano in enumerate(anos_idade):
            total = masc_perc[i][j] + fem_perc[i][j]
            fem_share[i, j] = (fem_perc[i][j] / total * 100) if total > 0 else 0
    fig, ax = plt.subplots(figsize=(12, 8))
    im = ax.imshow(fem_share, cmap='RdBu_r', aspect='auto', vmin=0, vmax=100)
    ax.set_xticks(range(len(anos_idade)))
    ax.set_xticklabels(anos_idade, rotation=45)
    ax.set_yticks(range(len(faixas_etarias)))
    ax.set_yticklabels(faixas_etarias)
    ax.set_xlabel('Ano')
    ax.set_ylabel('Faixa etária')
    ax.set_title('Participação feminina por faixa etária e ano (%)')
    plt.colorbar(im, ax=ax, label='% mulheres')
    plt.tight_layout()
    plt.savefig('heatmap_feminino.png', dpi=300)
    plt.close()

def plot_scatter_presenca_poder():
    """Dispersão: % mulheres no total vs % mulheres líderes."""
    plt.figure(figsize=(8, 8))
    plt.scatter(pct_f_total, pct_f_lider, s=100, c=range(len(anos_lead)), cmap='viridis', alpha=0.8)
    for i, ano in enumerate(anos_lead):
        plt.annotate(str(ano), (pct_f_total[i], pct_f_lider[i]), textcoords="offset points", xytext=(5,5), ha='center')
    # Linha de igualdade
    max_val = max(max(pct_f_total), max(pct_f_lider))
    plt.plot([0, max_val], [0, max_val], 'k--', alpha=0.5, label='Igualdade (líderes = total)')
    plt.xlabel('Participação feminina no total de pesquisadores (%)')
    plt.ylabel('Participação feminina na liderança (%)')
    plt.title('Relação entre presença e poder na ciência brasileira')
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.5)
    plt.tight_layout()
    plt.savefig('scatter_presenca_poder.png', dpi=300)
    plt.close()

def plot_hiato_lideranca():
    """Evolução do hiato (% líderes - % total) para mulheres."""
    hiato = [pct_f_lider[i] - pct_f_total[i] for i in range(len(anos_lead))]
    plt.figure(figsize=(10, 5))
    plt.bar(anos_lead, hiato, color='#d62728', alpha=0.7)
    plt.axhline(0, color='black', linewidth=0.8)
    plt.xlabel('Ano')
    plt.ylabel('Diferença (p.p.)')
    plt.title('Hiato entre participação na liderança e participação total – mulheres')
    plt.grid(axis='y', linestyle=':', alpha=0.5)
    plt.tight_layout()
    plt.savefig('hiato_lideranca.png', dpi=300)
    plt.close()

# ============================================================================
# 4. EXECUTAR TODOS OS GRÁFICOS
# ============================================================================
plot_curvas_etarias()
plot_piramide_etaria(2025)
plot_stacked_bars()
plot_area_etaria()
plot_lideranca_dual()
plot_lideranca_proporcao()
plot_lideranca_absoluto()
plot_heatmap()
plot_scatter_presenca_poder()
plot_hiato_lideranca()

print("\nTodos os gráficos foram gerados e salvos como arquivos PNG.")
