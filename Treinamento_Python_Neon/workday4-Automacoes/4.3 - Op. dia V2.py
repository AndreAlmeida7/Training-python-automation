#Bibliotecas
import pandas as pd
import shutil
import datetime as dt
import os
from datetime import timedelta

# worksheet_consolidated_total

#Função: Filtrar os relatórios Operação dia pela lista de brokers
def filter_brokers(df, broker_ids): 
    return df[df['BrokerId'].isin(broker_ids)]

#Função: Mover os arquivos da pasta de trabalho para Drive BackOffice
def save_and_move_data(final_worksheet, file_name, origin_path, destination_path, 
    directory_drive_consolidated, directory_drive_consolidated_deivi, worksheet_consolidated_total, file_name_consolidated):
    
    final_worksheet.to_excel(file_name, index=False)
    worksheet_consolidated_total.to_excel(file_name_consolidated, index=False)

    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    
    shutil.move(f"{origin_path}\\{file_name}", f"{destination_path}\\{file_name}")
    shutil.copy(f"{origin_path}\\{file_name_consolidated}", f"{directory_drive_consolidated_deivi}\\{file_name_consolidated}")
    shutil.move(f"{origin_path}\\{file_name_consolidated}", f"{directory_drive_consolidated}\\{file_name_consolidated}")



#Função principal
def main():
    
    current_date = dt.date.today()
    number_of_week_day = dt.date.today().isoweekday() #RETORNA UM NÚMERO DO DIA DA SEMANA (SEGUNDA = 1, ... , DOMINGO = 7)

    # SEGUNDA FEIRA
    if number_of_week_day == 1: 
        file_date = current_date - timedelta(1) #DATA D-1
    # DE TERÇA ATÉ SEXTA
    elif number_of_week_day == 2 or number_of_week_day == 3 or number_of_week_day == 4 or number_of_week_day == 5: 
        file_date = current_date - timedelta(1) #DATA D-1
    # SÁBADO
    elif number_of_week_day == 6:
        file_date = current_date - timedelta(1) #DATA D-1
    # DOMINGO
    elif number_of_week_day == 7:
        file_date = current_date - timedelta(1) #DATA D-1

    

    file_date = file_date.strftime('%Y%m%d')
    path_origin = r"C:\Users\U003659\Desktop"
    directory_drive = r"G:\Drives compartilhados\arquitetura\Documentos\Arquitetura Operacional\BACKOFFICE FINANCEIRO\CONCILIAÇÃO PRODUTOS\ARQUIVOS_OPERAÇÃO_DIA"
    directory_drive_consolidated = r"G:\Drives compartilhados\Contas transitorias\Extrato Transitória\Consolidação_por_broker_CCN"
    directory_drive_consolidated_deivi = r"G:\Drives compartilhados\arquitetura\Documentos\Arquitetura Operacional\BACKOFFICE FINANCEIRO\DASHBOARD\DASH_OPERACIONAL\Automatização\Operação_dia"
    path_destination = os.path.join(directory_drive, file_date)

            
    broker_filters = {
        'CDB_NEON_FINANCEIRA': [663, 274, 666, 664, 273, 275, 276, 277, 563, 665, 667, 282, 673],
        'CDB_FAMILHAO': [308, 309, 310, 311],
        'IS2B': [9, 18, 301, 302, 694, 695],
        'BOLETOS_CASHOUT_ITAU': [250, 251, 640, 641],
        'TRANSF.INTERNA': [2],
        'CDB_BV': [69, 72, 617, 71, 74],
        'CONTA_RELATO': [188, 223, 579],
        'BLOQUEIO_JUDICIAL': [17],
        'PGTO_EMPRESTIMO_MEI': [243],
        'PROTEÇÃO_BENS_DINHEIRO': [225, 135],
        'ABBC_BOLETO_CREDITO': [8],
        'CREDITO_PESSOAL':[54],
        'TRANSF.JUDICIAL': [26],
        'SLC': [28],
        'CASHBACK_CLIENTES': [63],
        'CASHBACK_NEON': [236],
        'PREJUIZO': [30],
        'MARKETING': [39],
        'REFERRAL': [38],
        'TED_SPB': [241, 242, 245, 246, 614, 632, 633, 635, 636, 639, 672],
        'VIRA_CREDITO': [228, 667, 617], 
        'PIX_CRÉDITO': [670, 279],
        'FITBANK': [36],
        'PGTO_PARCELA_EP_PF': [283],
        'PERDAS_OPERACIONAIS_CHARGEBACK': [592, 589, 661],
        'REPATRIAÇÕES': [25],
        'BLOQUEIO_CAUTELAR': [289, 681],
        'BROKERS_VAZIOS' : ["", " ", 0, False, None]
        }

    directory_SGN = r"\\sgnfiles\Compartilhado\Financeiro-Produtos\SGN"
    year_actually = "2024"
    month_actually = "05.MAIO"
    directory_op_day = os.path.join(directory_SGN, year_actually, month_actually, file_date)


    dfs = []

    part_file_name = f'part-'
    #arquivos = os.listdir(directory_op_day)
    for name_file in os.listdir(directory_op_day):
        if name_file.startswith("SGN_RELATORIO_OPERACOES_DIA_") and part_file_name in name_file and name_file.endswith('.csv'):
            df_part = pd.read_csv(os.path.join(directory_op_day, name_file), sep=";")
            dfs.append(df_part)

    if dfs:

        df_concatenated = pd.concat(dfs, ignore_index=True)

        def identificar_positivo_negativo(Valor):
            if Valor > 0:
                return 'Positivo'
            elif Valor < 0:
                return 'Negativo'
            elif Valor == 0:
                return 'zerado'

        df_concatenated['Classificacao'] = df_concatenated['Valor'].apply(identificar_positivo_negativo)
        worksheet_consolidated_total = df_concatenated.groupby(['RegisterDate','Classificacao','BrokerId','BrokersDescription'])['Valor'].agg(['sum', 'count']).reset_index()

        for broker_name, broker_ids in broker_filters.items():
            
            df_filtered = filter_brokers(df_concatenated, broker_ids) 
            file_name = f'Planilha_operação_dia_{broker_name}_{file_date}.xlsx' 
            file_name_consolidated = f'Planilha_consolidada_por_broker_{file_date}.xlsx'          
            save_and_move_data(df_filtered, file_name, path_origin, path_destination, directory_drive_consolidated, directory_drive_consolidated_deivi, worksheet_consolidated_total, file_name_consolidated)

    else:
        print('Nenhum arquivo encontrado para processar')

        
if __name__ == "__main__":
    
    main()