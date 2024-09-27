import pandas as pd

#Lendo as planilhas e os dados necessários:

planilha_BTG = pd.read_excel(r"C:\Users\U003659\Desktop\PROJETOS_PYTHON\LAYOUT TOPAZ\BTG\Emissoes_bancarias - BTG.xlsx")
codigo_CETIP = int('72080694')

produto = planilha_BTG['Produto']
valor = planilha_BTG['Emissão (R$)']
data_vencimento = planilha_BTG['Data Vencimento']
dias_corridos = planilha_BTG['DC']
Indexador = planilha_BTG['Indexador']
taxa_cliente = planilha_BTG['Taxa Cliente']
quantidade = planilha_BTG['Quantidade']
preco_desagio_sem_formatacao = planilha_BTG['PU Desagiado']
preco_desagio = []

for v in preco_desagio_sem_formatacao:
    preco_desagio.append(f'{(v/100000000):.8f}')

taxa_cliente = taxa_cliente.str.replace('%', '', regex=False).str.replace('.', ',', regex=False)

#Criando sequência de números
lista_numeros = []

numero_inicial = 103233
for n in range(numero_inicial, numero_inicial + len(produto)):
    lista_numeros.append(n)

#Criando a planilha de Emissão no layout Topaz:

# Criar as colunas do DataFrame
colunas = ['Integracao', 'Tipo', 'Contraparte', 'Valor Emissao', 'Valor Vencimento',
           'Data Vencimento', 'Prazo Emissao', 'Prazo Carencia', 'Produto', 'Remuneracao',
           'Percentual', 'Taxa', 'Desagio', 'Preco Desagio', 'Quantidade', 'Ativo']

# Criar um DataFrame vazio com as colunas definidas acima
df = pd.DataFrame(columns=colunas)

# Adicionar dados ao DataFrame
for i in range(len(produto)):
    nova_linha = [lista_numeros[i], 'Aplicação', codigo_CETIP, valor[i], " ", 
                data_vencimento[i].strftime('%d/%m/%Y'), " ", " ",
                "CDB ATACADO (CORRETORAS)", 'DI', taxa_cliente[i], " ", " ", float(preco_desagio[i]), " "," "]
    df.loc[len(df)] = nova_linha


df.to_excel('PLANILHA_EMISSÃO_BTG.xlsx', index=False)

