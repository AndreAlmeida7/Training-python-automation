from trino.dbapi import connect
from trino.auth import BasicAuthentication
import csv
import os
from datetime import datetime, timedelta

usuario = input('Favor colocar seu usuário: ')
senha = input('Favor colocar sua senha: ')

# Configurações de conexão ao Trino
trino_config = {
    'host': 'trino.de.in.devneon.com.br',  # Endereço do servidor Trino
    'port': 443,                           # Porta padrão para HTTPS
    'user': 'u003659',                        # Seu usuário no Trino
    'catalog': 'hive',                     # Nome do catálogo
    'http_scheme': 'https',                # Protocolo HTTP (use 'http' se não estiver usando HTTPS)
    'auth': BasicAuthentication(f'{usuario}', f'{senha}'), # ALTERAR SENHA E USUÁRIO
}

# Defina a pasta de saída
saida_do_arquivo = r'G:\Drives compartilhados\BackOffice - Cadastro\CONTROLES (TESTES EFETIVIDADE)\BASES\CONTA ENCERRADAS - RELATÓRIO BACEN (SEMESTRAL)\Bases_2024'

# Certifique-se de que a pasta de saída existe
os.makedirs(saida_do_arquivo, exist_ok=True)

# Obter o ano e o mês atual
ano_atual = datetime.now().year
mes_atual = datetime.now().month

# Determinar o semestre atual
semestre_atual = "1º" if mes_atual <= 6 else "2º"

# query para obter contas encerradas no segundo semestre do ano atual
queries_base = [
    {"query": 
     "select distinct c.id as clientid, cc.name, cc.cpf_cnpj, case when a.balance_event_vl is null then 0 else a.balance_event_vl end as Saldo, a.reference_dt as Data_Base, a.cancellation_dt as Data_Cancelamento, a.account_st as Status, case when rc.Description is null then 'Outros' else rc.Description end as MotivoCancelamento, d.bankaccountnumber as Numero_Conta, d.bankaccountdigit as Digito_Conta from refined.core_entity.checking_account a inner join hive.neonpottencial.dbo_person_uuid b on a.person_uuid = b.person_uuid inner join hive.neonpottencial.dbo_client c on b.identifier_nu= c.cpf inner join hive.aml.neondw_bi_dimension_client cc on c.id = cc.clientid inner join hive.neonpottencial.dbo_bankaccount d on c.id = d.clientid left join neonpottencial.dbo_reasoncancellation rc on rc.Id = c.ReasonCancellationId where a.account_st = 'Cancelado' and a.cancellation_dt between date_add('day', -180, current_date) AND date_add('day', 0, current_date)", 
     "output_file": f"Contas_Encerradas_{semestre_atual}_semestre_{ano_atual}.xlsx"}]

try:
    # Criar uma conexão com Trino
    conn = connect(
        host=trino_config['host'],
        port=trino_config['port'],
        user=trino_config['user'],
        catalog=trino_config['catalog'],
        http_scheme=trino_config['http_scheme'],
        auth=trino_config['auth'],)

    # Criar um cursor para executar as consultas
    cursor = conn.cursor()

    # Obter intervalos de datas para as queries
    for query_info in queries_base:
        query = query_info["query"]
        output_file = query_info["output_file"]
        output_path = os.path.join(saida_do_arquivo, output_file)

        # Executar a query
        cursor.execute(query)

        # Pegar os resultados
        records = cursor.fetchall()

        # Pegar os nomes das colunas
        column_names = [desc[0] for desc in cursor.description]

        # Escrever os resultados em um arquivo CSV
        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Escrever os cabeçalhos das colunas
            writer.writerow(column_names)
            # Escrever as linhas de dados
            writer.writerows(records)
        print(f"Os resultados da consulta '{query}' foram exportados para {output_path}")
except Exception as error:
    print(f"Erro ao conectar ao Trino ou executar a consulta: {error}")
finally:
    if conn:
        cursor.close()
        conn.close()
        print("Conexão ao Trino fechada.")
