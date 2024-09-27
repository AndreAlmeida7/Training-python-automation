import os
import shutil

# Defina o caminho da pasta de rede
caminho_pasta_rede = r"\\sgnfiles\Compartilhado\Financeiro-Produtos\SGN\2024\05.MAIO"

# Defina o caminho da sua área de trabalho
caminho_area_trabalho = os.path.expanduser(r"C:\Users\U003659\Desktop")

# Percorra todas as pastas de datas dentro da pasta de rede
for nome_pasta in os.listdir(caminho_pasta_rede):
    caminho_pasta = os.path.join(caminho_pasta_rede, nome_pasta)
    
    # Realiza uma verificação se o "caminho_pasta" é uma pasta de rede e também se o nome da pasta começa com "202405"
    if os.path.isdir(caminho_pasta) and nome_pasta.startswith("202405"):
        
        # Percorra todos os arquivos na pasta atual e mova a planilha para sua área de trabalho
        for nome_arquivo in os.listdir(caminho_pasta):
            if nome_arquivo.startswith("Saques_Tecban") or "Saques_Tecban" in nome_arquivo:
                caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
                shutil.copy(caminho_arquivo, os.path.join(caminho_area_trabalho,nome_arquivo)) 
                print(f"Arquivo {nome_arquivo} copiado para {caminho_area_trabalho}")


