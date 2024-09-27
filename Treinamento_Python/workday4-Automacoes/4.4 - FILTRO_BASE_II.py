#FILter_base_II

#Bibliotecas
import pandas as pd
import shutil
import datetime as dt
import os
from datetime import timedelta


#Função: Mover o arquivo consolidado BASEII da pasta de trabalho para Drive BackOffice
def save_and_move_data_baseII(consolidated_base_II, file_name_base_II, path_origin, path_destination, file_name_base_II_internacional, consolidated_base_II_internacional):
    consolidated_base_II.to_excel(file_name_base_II, index=False)
    consolidated_base_II_internacional.to_excel(file_name_base_II_internacional, index=False)
    shutil.move(f"{path_origin}\\{file_name_base_II}", f"{path_destination}\\{file_name_base_II}")
    shutil.move(f"{path_origin}\\{file_name_base_II_internacional}", f"{path_destination}\\{file_name_base_II_internacional}")


#Função principal
def main():
    
    current_date = dt.date.today()
    number_of_week_day = dt.date.today().isoweekday() #RETORNA UM NÚMERO DO DIA DA SEMANA (SEGUNDA = 1, ... , DOMINGO = 7)

    # SEGUNDA FEIRA UTILIZARÁ AS LINHAS ABAIXO
    if number_of_week_day == 1: 
        file_date = current_date - timedelta(3) #DATA D-3 (SE DESEJA PEGAR ARQUIVO DE SEXTA-FEIRA)
        #file_date = current_date - timedelta(2) #DATA D-2 (SE DESEJA PEGAR ARQUIVO DE SÁBADO)
        # file_date = current_date - timedelta(1) #DATA D-1 (SE DESEJA PEGAR ARQUIVO DE DOMINGO)

     # DE TERÇA ATÉ SEXTA UTILIZARÁ A LINHA ABAIXO
    elif number_of_week_day == 2 or number_of_week_day == 3 or number_of_week_day == 4 or number_of_week_day == 5: 
        file_date = current_date - timedelta(1) #DATA D-1
        
       

    file_date = file_date.strftime('%Y%m%d')
    path_origin = r"C:\Users\U003659\Desktop"
    directory_drive = r"G:\Drives compartilhados\arquitetura\Documentos\Arquitetura Operacional\BACKOFFICE FINANCEIRO\CONCILIAÇÃO PRODUTOS\ARQUIVOS_OPERAÇÃO_DIA"
    path_destination = directory_drive + f'\{file_date}'
  

    file_template_base_II = 'Planilha_Base_II_Domestico_{}.xlsx'
    file_template_base_II_internacional = 'Planilha_Base_II_Internacional_{}.xlsx'
        
    
    directory_SGN = r"\\sgnfiles.neon.local\Compartilhado\Financeiro-Produtos\SGN"
    year_actually = "2024"
    month_actually = "06.JUNHO"
    directory_op_day = os.path.join(directory_SGN, year_actually, month_actually, file_date)

   
    for name_file_base_II in os.listdir(directory_op_day):
        if name_file_base_II.startswith("BASE_II_FUNDO_DOMESTICO") and "part-00000" in name_file_base_II:
            table_1 =(os.path.join(directory_op_day, name_file_base_II))
        elif name_file_base_II.startswith("BASE_II_FUNDO_DOMESTICO") and "part-00001" in name_file_base_II:
            table_2 =(os.path.join(directory_op_day, name_file_base_II))

    for name_file_base_II_internacional in os.listdir(directory_op_day):
        if name_file_base_II_internacional.startswith("BASE_II_FUNDO_INTERNATIONAL") and "part-00000" in name_file_base_II_internacional:
            table_3 =(os.path.join(directory_op_day, name_file_base_II_internacional))
        
    
    df1 = pd.read_csv(table_1, sep=';', nrows=1048576)
    df2 = pd.read_csv(table_2, sep=';', nrows=1048576)
    df3 = pd.read_csv(table_3, sep=';', nrows=1048576)

    table_concatenated = pd.concat([df1, df2])

    filter_base_II = table_concatenated.loc[table_concatenated['DS_FUNDO'].isin(['BIORC_PF','BIORC_PJ'])]

    filter_base_II_internacional = df3.loc[df3['DS_FUNDO'].isin(['BIORC_PF','BIORC_PJ'])]


    filter_base_II['valor'] = filter_base_II['valor'].str.replace(',', '.', regex=True)
    filter_base_II['valor'] = pd.to_numeric(filter_base_II['valor'], errors='coerce')
    filter_base_II['intercambio'] = filter_base_II['intercambio'].str.replace(',', '.', regex=True)
    filter_base_II['intercambio'] = pd.to_numeric(filter_base_II['intercambio'], errors='coerce')

    filter_base_II_internacional['valor'] = filter_base_II_internacional['valor'].str.replace(',', '.', regex=True)
    filter_base_II_internacional['valor'] = pd.to_numeric(filter_base_II_internacional['valor'], errors='coerce')
    filter_base_II_internacional['intercambio'] = filter_base_II_internacional['intercambio'].str.replace(',', '.', regex=True)
    filter_base_II_internacional['intercambio'] = pd.to_numeric(filter_base_II_internacional['intercambio'], errors='coerce')   


    consolidated_base_II = filter_base_II.groupby(['data_ingestao_transacao', 'BIN', 'categoria']).agg({'valor': 'sum', 'intercambio': 'sum'}).round(2).reset_index()
    consolidated_base_II_internacional = filter_base_II_internacional.groupby(['data_ingestao_transacao', 'BIN', 'categoria']).agg({'valor': 'sum', 'intercambio': 'sum'}).round(2).reset_index()

    file_name_base_II = file_template_base_II.format(file_date)  
    file_name_base_II_internacional = file_template_base_II_internacional.format(file_date)

    save_and_move_data_baseII(consolidated_base_II, file_name_base_II, path_origin, path_destination, file_name_base_II_internacional, consolidated_base_II_internacional)        

    

if __name__ == "__main__":
    
    main()