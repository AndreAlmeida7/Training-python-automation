# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

#Criação o aplicativo da biblioteca Dash (site)
app = Dash(__name__) 

#Leitura do meu excel
df = pd.read_excel(r'C:\Users\U003659\Desktop\WorkshopPython\workday4\Vendas.xlsx') 

#Criando o gráfico (definindo os eixos do meu gráfico)
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")

#Criando uma lista de opções para ter no botão
opcoes = list(df["ID Loja"].unique())
opcoes.append("Todas as lojas")


#Criando caracteríticas do meu site local ( HTML -> elementos visuais que não tem relação com o dashboard .
#DCC -> Componentes do dashboard)

app.layout = html.Div(children=[
    html.H1(children='Faturamento da loja'),
    html.H2(children='Gráfico com o faturamento de todos os produtos separados por loja'),

    html.Div(children='''
        OBS: Esse gráfico mostra a quantidade de produtos vendidos, não o faturamento.
    '''),
    #botão com as lojas
    dcc.Dropdown(opcoes, value="Todas as lojas", id="Lista Lojas"),

    dcc.Graph(
        id='Gráfico_Quantidade_vendas',
        figure=fig
    )
])

#Quando você seleciona uma loja no botão, retorna no gráfico a loja em questão
@app.callback(
    Output('Gráfico_Quantidade_vendas', 'figure'),
    Input('Lista Lojas', 'value')
)
def update_output(value):
    if value == "Todas as lojas":
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    else:
        tabela_filtrada = df.loc[df["ID Loja"]==value,:]
        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    return fig


#Criação do link:
if __name__ == '__main__':
    app.run_server(debug=True)

