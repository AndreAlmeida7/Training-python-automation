import xmltodict #Manipulação de arquivos XML
import pandas as pd 

# Criar objeto em texto com base no arquivo XML e depois faz a leitura do arquivo XML
xml = []
with open(r'C:\Users\u003659\Desktop\6004_293556484.xml', 'r') as f:
    xml = f.read()
f.closed    

# Converte o conteúdo do arquivo XML para o dicionário do python
dict_base = xmltodict.parse(xml)

# Cria as colunas do meu arquivo csv com os campos que possuem as informações
lista = dict_base['CCSDOC']['SISARQ']['CCSArqPosCad']['Repet_ACCS004_Pessoa']['Grupo_ACCS004_Pessoa']

# gero o dataframe com a lista de colunas que criei
base = pd.DataFrame(lista)

# Exportar para um arquivo csv
base.to_csv(r'C:\Users\u003659\Desktop\BACEN.csv',sep=";")



