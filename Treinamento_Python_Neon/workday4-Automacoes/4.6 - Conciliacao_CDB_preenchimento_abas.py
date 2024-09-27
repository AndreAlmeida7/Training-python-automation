import pandas as pd

#DATA DA CONCILIAÇÃO (D-1) (SEMPRE VERIFICAR)#
data_conciliação = '20230612'
#DATA DA CONCILIAÇÃO (D-1) (SEMPRE VERIFICAR)#


#DATA DA PLANILHA CDB(D-2) (SEMPRE VERIFICAR)#
data_CDB_D1 = '20230609'
#DATA DA PLANILHA CDB(D-2) (SEMPRE VERIFICAR)#


#DATA DA PLANILHA VENCIMENTO (SEMPRE VERIFICAR)#
data_vencimento = '20230608'
#DATA DA PLANILHA VENCIMENTO (SEMPRE VERIFICAR)#

#Lendo as planilhas para preencher a aba NEON 
matriz_conciliacao_aba_NEON = pd.read_excel('Matriz Conciliação Novo CDB.xlsx', sheet_name='NEON')
planilha_data_compras = pd.read_excel(f'Planilha_{data_conciliação}.xlsx', sheet_name ='Compras')
planilha_data_vendas = pd.read_excel(f'Planilha_{data_conciliação}.xlsx', sheet_name ='Vendas')

#Lendo as planilhas para preencher a aba Complemento
matriz_conciliacao_aba_COMPLEMENTO = pd.read_excel('Matriz Conciliação Novo CDB.xlsx', sheet_name='Complemento')
planilha_data_complemento = pd.read_excel(f'Planilha_{data_conciliação}.xlsx', sheet_name ='Complementos')

#Lendo as planilhas para preencher a aba CDB DIA D(0)
matriz_conciliacao_aba_CDB_D0 = pd.read_excel('Matriz Conciliação Novo CDB.xlsx', sheet_name='CDB DIA (D0)')
planilha_operacoes_dia_CDB_D0 = pd.read_excel(f'planilha_Operacoes_NEON_CDB_{data_conciliação}.xlsx', sheet_name= 'Sheet1')

#Lendo as planilhas para preencher a aba CDB DIA (D-1)
matriz_conciliacao_aba_CDB_D1 = pd.read_excel('Matriz Conciliação Novo CDB.xlsx', sheet_name='CDB DIA (D-1)')
planilha_operacoes_dia_CDB_D1 = pd.read_excel(f'planilha_Operacoes_NEON_CDB_{data_CDB_D1}.xlsx', sheet_name= 'Sheet1')

#Lendo as planilhas para preencher a aba Vencimento
# matriz_conciliacao_aba_Vencimento = pd.read_excel('Matriz Conciliação Novo CDB.xlsx', sheet_name='Vencimento')
# planilha_posicao_Vencimentos = pd.read_excel(f'POSICAO_VENCIMENTOS_{data_vencimento}.xlsx', sheet_name = f'POSICAO_VENCIMENTOS_{data_vencimento}')

#Lendo as planilhas para preencher a aba BV
matriz_conciliacao_aba_BV = pd.read_excel('Matriz Conciliação Novo CDB.xlsx', sheet_name='BV')
planilha_ExtLiq = pd.read_excel(f'ExtLiqSPRF_NEON_{data_conciliação}000000_{data_conciliação}000000.xlsx', sheet_name= f'ExtLiqSPRF_NEON_{data_conciliação}000000_')

#Criando variável para saber o número de linhas da planilha
num_linhas_cdb = matriz_conciliacao_aba_NEON.shape[0]

#concatena a sheet compras com sheet vendas
planilha_data = pd.concat([planilha_data_compras, planilha_data_vendas], ignore_index = True)

#concatena as informações
matriz_conciliacao_aba_NEON = pd.concat([matriz_conciliacao_aba_NEON,planilha_data])
matriz_conciliacao_aba_COMPLEMENTO = pd.concat([matriz_conciliacao_aba_COMPLEMENTO,planilha_data_complemento])
matriz_conciliacao_aba_CDB_D0 = pd.concat([matriz_conciliacao_aba_CDB_D0,planilha_operacoes_dia_CDB_D0])
matriz_conciliacao_aba_CDB_D1 = pd.concat([matriz_conciliacao_aba_CDB_D1,planilha_operacoes_dia_CDB_D1])
# matriz_conciliacao_aba_Vencimento = pd.concat([matriz_conciliacao_aba_Vencimento,planilha_posicao_Vencimentos])
matriz_conciliacao_aba_BV = pd.concat([matriz_conciliacao_aba_BV,planilha_ExtLiq])

#exclui a 1ª linhas em branco que houver na variável de número de linhas
matriz_conciliacao_aba_NEON = matriz_conciliacao_aba_NEON.iloc[num_linhas_cdb:, :]
matriz_conciliacao_aba_COMPLEMENTO = matriz_conciliacao_aba_COMPLEMENTO.iloc[num_linhas_cdb:, :]
matriz_conciliacao_aba_CDB_D0 = matriz_conciliacao_aba_CDB_D0.iloc[num_linhas_cdb:, :]
matriz_conciliacao_aba_CDB_D1 = matriz_conciliacao_aba_CDB_D1.iloc[num_linhas_cdb:, :]
matriz_conciliacao_aba_BV = matriz_conciliacao_aba_BV.iloc[num_linhas_cdb:, :]


#cria abas com as informações
with pd.ExcelWriter('Matriz Conciliação Novo CDB.xlsx', mode='a') as writer:
    matriz_conciliacao_aba_NEON.to_excel(writer, sheet_name='copiar_para_aba_NEON', index=False)
    matriz_conciliacao_aba_COMPLEMENTO.to_excel(writer, sheet_name='copiar_para_aba_COMPLEMENTO', index=False)
    matriz_conciliacao_aba_CDB_D0.to_excel(writer, sheet_name='copiar_para_aba_CDB DIA (D0)', index=False)
    matriz_conciliacao_aba_CDB_D1.to_excel(writer, sheet_name='copiar_para_aba_CDB DIA (D-1)', index=False)
    # matriz_conciliacao_aba_Vencimento.to_excel(writer, sheet_name='copiar_para_aba_Vencimento', index=False)
    matriz_conciliacao_aba_BV.to_excel(writer, sheet_name='copiar_para_aba_bv', index=False)


   