#FILter_base_II OPERAÇÕES DIA

#Bibliotecas
import pandas as pd
import shutil
import datetime as dt
import os
from datetime import timedelta

#Função: Ler os relatórios Operação dia
def read_data(file_path):
    return pd.read_excel(file_path, engine="openpyxl")

#Função: Filtrar os relatórios Operação dia pela lista de brokers
def filter_brokers(df, broker_ids): 
    return df[df.BrokerId.isin(broker_ids)]

#Função: Mover os arquivos da pasta de trabalho para Drive BackOffice
def save_and_move_data(final_worksheet, file_name, origin_path, destination_path, worksheet_consolidated_total, 
    file_name_consolidated, directory_drive_consolidated, directory_drive_consolidated_deivi):
    
    final_worksheet.to_excel(file_name, index=False)
    worksheet_consolidated_total.to_excel(file_name_consolidated, index=False)
    shutil.move(f"{origin_path}\\{file_name}", f"{destination_path}\\{file_name}")
    shutil.copy(f"{origin_path}\\{file_name_consolidated}", f"{directory_drive_consolidated_deivi}\\{file_name_consolidated}")
    shutil.move(f"{origin_path}\\{file_name_consolidated}", f"{directory_drive_consolidated}\\{file_name_consolidated}")


#Função principal
def main():
    
    current_date = dt.date.today()
    number_of_week_day = dt.date.today().isoweekday() #RETORNA UM NÚMERO DO DIA DA SEMANA (SEGUNDA = 1, ... , DOMINGO = 7)

    # SEGUNDA FEIRA UTILIZARÁ AS LINHAS ABAIXO
    if number_of_week_day == 1: 
        # file_date = current_date - timedelta(3) #DATA D-3 (SE DESEJA PEGAR ARQUIVO DE SEXTA-FEIRA)
        # file_date = current_date - timedelta(2) #DATA D-2 (SE DESEJA PEGAR ARQUIVO DE SÁBADO)
        file_date = current_date - timedelta(1) #DATA D-1 (SE DESEJA PEGAR ARQUIVO DE DOMINGO)

     # DE TERÇA ATÉ SEXTA UTILIZARÁ A LINHA ABAIXO
    elif number_of_week_day == 2 or number_of_week_day == 3 or number_of_week_day == 4 or number_of_week_day == 5: 
        file_date = current_date - timedelta(18) #DATA D-1
    

    file_date = file_date.strftime('%Y%m%d')
    path_origin = r'C:\Users\U003659\Desktop'
    directory_drive = r"G:\Drives compartilhados\arquitetura\Documentos\Arquitetura Operacional\BACKOFFICE FINANCEIRO\CONCILIAÇÃO PRODUTOS\ARQUIVOS_OPERAÇÃO_DIA"
    directory_drive_consolidated = r"G:\Drives compartilhados\Contas transitorias\Extrato Transitória\Consolidação_por_broker_CCN"
    directory_drive_consolidated_deivi = r"G:\Drives compartilhados\arquitetura\Documentos\Arquitetura Operacional\BACKOFFICE FINANCEIRO\DASHBOARD\DASH_OPERACIONAL\Automatização\Operação_dia"
    path_destination = directory_drive + f'\{file_date}'
    os.makedirs(path_destination)

    file_template = 'Planilha_operação_dia_{}_{}.xlsx'
    file_template_consolidated = 'Planilha_consolidada_por_broker_{}.xlsx'
            
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
        'PGTO_PARCELA_EP_PF': [283, 288],
        'PERDAS_OPERACIONAIS_CHARGEBACK': [592, 589, 661],
        'REPATRIAÇÕES': [25],
        'BLOQUEIO_CAUTELAR': [289, 681]
        }

    df = None
    df_1 = None
    df_2 = None
    df_3 = None
    df_4 = None
    df_5 = None

    directory_SGN = r"\\sgnfiles.neon.local\Compartilhado\Financeiro-Produtos\SGN"
    year_actually = "2024"
    month_actually = "05.MAIO"
    directory_op_day = os.path.join(directory_SGN, year_actually, month_actually, file_date)

    for name_file in os.listdir(directory_op_day):
        if name_file.startswith("[SGN]Relatorio_Operacoes_Dia_") and name_file.endswith('Parte-1.xlsx'):
            df = read_data(os.path.join(directory_op_day, name_file))
        elif name_file.startswith("[SGN]Relatorio_Operacoes_Dia_") and name_file.endswith('Parte-2.xlsx'): 
            df_1 = read_data(os.path.join(directory_op_day, name_file))
        elif name_file.startswith("[SGN]Relatorio_Operacoes_Dia_") and name_file.endswith('Parte-3.xlsx'):
            df_2 = read_data(os.path.join(directory_op_day, name_file))
        elif name_file.startswith("[SGN]Relatorio_Operacoes_Dia_") and name_file.endswith('Parte-4.xlsx'):
            df_3 = read_data(os.path.join(directory_op_day, name_file))
        elif name_file.startswith("[SGN]Relatorio_Operacoes_Dia_") and name_file.endswith('Parte-5.xlsx'):
            df_4 = read_data(os.path.join(directory_op_day, name_file))
        elif name_file.startswith("[SGN]Relatorio_Operacoes_Dia_") and name_file.endswith('Parte-6.xlsx'):
            df_5 = read_data(os.path.join(directory_op_day, name_file))

    #Concatena todos os dataframes
    if  df_5 is not None:
        data_frames_op_dia = [df, df_1, df_2, df_3, df_4, df_5]
    elif  df_4 is not None:
        data_frames_op_dia = [df, df_1, df_2, df_3, df_4]
    elif df_3 is not None:
        data_frames_op_dia = [df, df_1, df_2, df_3]
    else:
        data_frames_op_dia = [df, df_1, df_2]


    #consolida todos os data frames
    consolidated_total = pd.concat(data_frames_op_dia, ignore_index=True) 


    def identificar_positivo_negativo(Valor):
        if Valor > 0:
            return 'Positivo'
        elif Valor < 0:
            return 'Negativo'
        elif Valor == 0:
            return 'zerado'


    consolidated_total['Classificacao'] = consolidated_total['Valor'].apply(identificar_positivo_negativo)
    worksheet_consolidated_total = consolidated_total.groupby(['RegisterDate','Classificacao','BrokerId','BrokersDescription'])['Valor'].agg(['sum', 'count']).reset_index()
    

    for broker_name, broker_ids in broker_filters.items():
        if df_5 is not None:
            df_filtered = filter_brokers(df, broker_ids)
            df_1_filtered = filter_brokers(df_1, broker_ids)
            df_2_filtered = filter_brokers(df_2, broker_ids)             
            df_3_filtered = filter_brokers(df_3, broker_ids)
            df_4_filtered = filter_brokers(df_4, broker_ids)
            df_5_filtered = filter_brokers(df_5, broker_ids)
            final_worksheet = pd.concat([df_filtered, df_1_filtered, df_2_filtered,df_3_filtered,df_4_filtered,df_5_filtered])
        elif df_4 is not None:
            df_filtered = filter_brokers(df, broker_ids)
            df_1_filtered = filter_brokers(df_1, broker_ids)
            df_2_filtered = filter_brokers(df_2, broker_ids)             
            df_3_filtered = filter_brokers(df_3, broker_ids)
            df_4_filtered = filter_brokers(df_4, broker_ids)
            final_worksheet = pd.concat([df_filtered, df_1_filtered, df_2_filtered,df_3_filtered,df_4_filtered])
        elif df_3 is not None:
            df_filtered = filter_brokers(df, broker_ids)
            df_1_filtered = filter_brokers(df_1, broker_ids)
            df_2_filtered = filter_brokers(df_2, broker_ids)
            df_3_filtered = filter_brokers(df_3, broker_ids)
            final_worksheet = pd.concat([df_filtered, df_1_filtered, df_2_filtered,df_3_filtered])
        else:
            df_filtered = filter_brokers(df, broker_ids)
            df_1_filtered = filter_brokers(df_1, broker_ids)
            df_2_filtered = filter_brokers(df_2, broker_ids)
            final_worksheet = pd.concat([df_filtered, df_1_filtered, df_2_filtered])

        file_name = file_template.format(broker_name, file_date)
        file_name_consolidated = file_template_consolidated.format(file_date)

        save_and_move_data(final_worksheet, file_name, path_origin, path_destination, 
        worksheet_consolidated_total, file_name_consolidated, directory_drive_consolidated, 
        directory_drive_consolidated_deivi)

        
if __name__ == "__main__":
    
    main()