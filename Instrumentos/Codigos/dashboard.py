import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
import plotly.offline as pyo

# Carregar o DataFrame
df = pd.read_csv('responses_up_votes.csv')

# Definir as três colunas
colunas = ['up_votes', 'comment_count', 'answer_count', 'score']

# Criar um subplot para cada coluna
fig = sp.make_subplots(rows=len(colunas),
                       row_titles=colunas,
                       column_widths=[200, 50, 50, 50, 200],
                       cols=5,
                       specs=[[
                           {
                               'type': 'xy'
                           },
                           {
                               'type': 'indicator'
                           },
                           {
                               'type': 'indicator'
                           },
                           {
                               'type': 'indicator'
                           },
                           {
                               'type': 'xy'
                           },
                       ] for i in colunas])

# Iterar pelas colunas
for i, coluna in enumerate(colunas):
    # Histograma
    fig.add_trace(
        go.Histogram(x=df[coluna], name='Histograma'),
        row=i + 1,
        col=1,
    )

    # Boxplot
    fig.add_trace(
        go.Box(y=df[coluna], name='Boxplot'),
        row=i + 1,
        col=5,
    )

    # Média
    media = df[coluna].mean()
    fig.add_trace(
        go.Indicator(
            mode='number',
            value=media,
            title='Média',
        ),
        row=i + 1,
        col=2,
    )

    # Mediana
    mediana = df[coluna].median()
    fig.add_trace(
        go.Indicator(
            mode='number',
            value=mediana,
            title='Mediana',
        ),
        row=i + 1,
        col=3,
    )

    # Soma
    soma = df[coluna].sum()
    fig.add_trace(
        go.Indicator(
            mode='number',
            value=soma,
            title='Soma',
        ),
        row=i + 1,
        col=4,
    )

# Atualizar o layout do subplot
fig.update_layout(
    showlegend=False,
    height=2000,
    title='Caracterização do dataset',
    yaxis=dict(title_standoff=30),
)
pyo.plot(fig, filename='dashboard.html', auto_open=True)
