import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import mannwhitneyu, wilcoxon


def add_quartis(q1_gpt, median_gpt, q3_gpt, q1_stack, median_stack, q3_stack):
    plt.text(0.05, q1_gpt, f'{q1_gpt:.2f}', horizontalalignment='left')
    plt.text(1.05, q1_stack, f'{q1_stack:.2f}', horizontalalignment='left')
    plt.text(0.05, median_gpt, f'{median_gpt:.2f}')
    plt.text(1.05, median_stack, f'{median_stack:.2f}')
    plt.text(0.05, q3_gpt, f'{q3_gpt:.2f}', horizontalalignment='left')
    plt.text(1.05, q3_stack, f'{q3_stack:.2f}', horizontalalignment='left')


def boxplot(df, i, ax=None, fliers=True):
    sns.boxplot(data=df,
                x=["ChatGPT"] * len(df[i[0]]) +
                ["Stackoverflow"] * len(df[i[1]]),
                y=pd.concat([df[i[0]], df[i[1]]]),
                width=0.1,
                boxprops={'zorder': 2},
                showfliers=fliers,
                ax=ax)


def salva(title):
    plt.savefig('figs/' + title)
    plt.show()


df = pd.read_csv('../OutrosInstrumentos/responses_final.csv',
                 index_col='index')

duplas = [
    ['loc_gpt', 'loc_stackoverflow', 'LOC'],
    ['comments_gpt', 'comments_stackoverflow', '# Comentários'],
    [
        'comments_density_gpt', 'comments_density_stackoverflow',
        'Densidade de comentários'
    ],
    ['cc_gpt', 'cc_stackoverflow', 'Complexidade Ciclomática'],
    ['npath_gpt', 'npath_stackoverflow', 'Complexidade de Caminhos'],
    ['cognitive_gpt', 'cognitive_stackoverflow', 'Complexidade Cognitiva'],
    [
        'var_names_gpt', 'var_names_stackoverflow',
        'Tamanho médio identificadores'
    ],
    ['mi_gpt', 'mi_stackoverflow', 'Indice de Manutenibilidade'],
]

for i in duplas:
    # calcula o maximo, o minimo e quartis
    min = df[i[:2]].min()
    max = df[i[:2]].max()
    quartis = df[i[:2]].quantile([0.25, 0.5, 0.75])
    sum = df[i[:2]].sum()
    print(
        f'\tmin:\n{min}\n\tmax:\n{max}\n\tquartis:\n{quartis}\n\tsoma:\n{sum}')

    statistic, pvalue = wilcoxon(df[i[0]], df[i[1]])
    print(f'\tR-test:\nstatistic: {statistic:.2f}\np-value: {pvalue:.10f}')

    # calcula os quartis
    q1_gpt, median_gpt, q3_gpt = df[i[0]].quantile([0.25, 0.5, 0.75])
    q1_stack, median_stack, q3_stack = df[i[1]].quantile([0.25, 0.5, 0.75])

    #graficos de distribuição
    sns.set_style('whitegrid')
    sns.histplot(data=df, x=i[1], label='StackOverflow', kde=True)
    sns.histplot(data=df, x=i[0], label='ChatGPT', kde=True)
    plt.legend()
    plt.xlabel(i[2])
    plt.ylabel('Contagem')
    salva(f'distribuição {i[2]}')

    sns.set_style('white')

    # gera os boxplotes
    plt.figure(figsize=(10, 6))
    ax = sns.violinplot(
        data=df,
        x=["ChatGPT"] * len(df[i[0]]) + ["Stackoverflow"] * len(df[i[1]]),
        y=pd.concat([df[i[0]], df[i[1]]]),
    )
    for patch in ax.collections:
        patch.set_alpha(0.5)
    boxplot(df=df, i=i, ax=ax)
    add_quartis(q1_gpt, median_gpt, q3_gpt, q1_stack, median_stack, q3_stack)

    # definindo os rótulos dos eixos
    stop = max[i[0]] if max[i[0]] > max[i[1]] else max[i[1]]
    start = min[i[0]] if min[i[0]] < min[i[1]] else min[i[1]]
    plt.xlabel('Ferramenta')
    plt.ylabel(i[2])
    plt.yticks(np.linspace((start), (stop), 20))

    # exibindo o gráfico
    salva(f'boxplot {i[2]}.png')

    # sem outliers
    boxplot(df=df, i=i, fliers=False)
    add_quartis(q1_gpt, median_gpt, q3_gpt, q1_stack, median_stack, q3_stack)
    # definindo os rótulos dos eixos
    plt.xlabel('Ferramenta')
    plt.ylabel(i[2])

    # exibindo o gráfico
    salva(f'boxplot {i[2]} sem outlier.png')

    # Gera o ECDF
    sns.set_style('whitegrid')
    sns.ecdfplot(data=df, x=i[0], label='ChatGPT')
    sns.ecdfplot(data=df, x=i[1], label='StackOverflow')
    plt.legend()
    plt.xlabel(i[2])
    plt.ylabel('Proporção')

    # Exibir o gráfico
    salva(f'ecdf {i[2]}.png')

    # calcula a proporção
    count_gpt = count_stack = count_igual = 0
    for j, row in df.iterrows():
        if row[i[0]] > row[i[1]]:
            count_gpt += 1
        elif row[i[0]] == row[i[1]]:
            count_igual += 1
        else:
            count_stack += 1
    print()
    print(
        f'GPT maior: {count_gpt}, Stack maior: {count_stack}, Iguais: {count_igual}'
    )
    diff = (df[i[0]] - df[i[1]]).sum()
    print(f'Diferença GPT - Stack: {diff}')
    print('--------------------------------------------')
    print()
