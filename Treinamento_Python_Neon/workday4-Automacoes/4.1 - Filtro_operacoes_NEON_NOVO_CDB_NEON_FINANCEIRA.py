import pandas as pd
import shutil

#SEMPRE ALTERAR A DATA DA CONCILIAÇÃO
data = '20230730'
nome_arquivo = f'Planilha_Operacoes_NEON_NOVO_CDB_NEON_FINANCEIRA_{data}.xlsx'

#LEITURA DAS PLANILHAS DE OPERAÇÕES DO DIA (ALTERAR TODOS OS DIAS)
df = pd.read_excel(r"\\sgnfiles.neon.local\Compartilhado\Financeiro-Produtos\SGN\2023\07.JULHO\20230730\[SGN]Relatorio_Operacoes_Dia_20230730_20230731_07330158_Parte-1.xlsx") 
df_1 = pd.read_excel(r"\\sgnfiles.neon.local\Compartilhado\Financeiro-Produtos\SGN\2023\07.JULHO\20230730\[SGN]Relatorio_Operacoes_Dia_20230730_20230731_07340129_Parte-2.xlsx")
df_2 = pd.read_excel(r"\\sgnfiles.neon.local\Compartilhado\Financeiro-Produtos\SGN\2023\07.JULHO\20230730\[SGN]Relatorio_Operacoes_Dia_20230730_20230731_07345899_Parte-3.xlsx")
# df_3 = pd.read_excel(r"\\sgnfiles.neon.local\Compartilhado\Financeiro-Produtos\SGN\2023\07.JULHO\20230730\[SGN]Relatorio_Operacoes_Dia_20230730_20230801_07364393_Parte-4.xlsx")
# df_4 = pd.read_excel(r"\\sgnfiles.neon.local\Compartilhado\Financeiro-Produtos\SGN\2023\07.JULHO\20230722\[SGN]Relatorio_Operacoes_Dia_20230714_20230714_07452369_Parte-5.xlsx")

#FILTRO DOS BROKERS
broker_00 = df[df.BrokerId.isin([663, 274, 666, 664, 273, 275, 276, 277, 563, 665, 667, 282, 673])]
broker_01 = df_1[df_1.BrokerId.isin([663, 274, 666, 664, 273, 275, 276, 277, 563, 665, 667, 282, 673])]
broker_02 = df_2[df_2.BrokerId.isin([663, 274, 666, 664, 273, 275, 276, 277, 563, 665, 667, 282, 673])]
# broker_03 = df_3[df_3.BrokerId.isin([663, 274, 666, 664, 273, 275, 276, 277, 563, 665, 667, 282, 673])]
# broker_04 = df_4[df_4.BrokerId.isin([663, 274, 666, 664, 273, 275, 276, 277, 563, 665, 667, 282, 673])]

#CONCATENA AS INFORMAÇÕES FILTRADAS
super_planilha = pd.concat([broker_00,broker_01,broker_02])

#CRIAR UMA PLANILHA COM AS INFORMAÇÕES
super_planilha.to_excel(nome_arquivo, index=False)

#MOVE OS ARQUIVOS DO CAMINHO_1 PARA CAMINHO_2 (ALTERAR SEMPRE O CAMINHO 1)
caminho_1 = r"C:\Users\U003659\Desktop"

caminho_2 = r"G:\Drives compartilhados\arquitetura\Documentos\Arquitetura Operacional\BACKOFFICE FINANCEIRO\CONCILIAÇÃO PRODUTOS\CDB\CDB NEON FINANCEIRA\Arquivo_Operações_CDB"

shutil.move(f"{caminho_1}\\{nome_arquivo}", f"{caminho_2}\\{nome_arquivo}")


