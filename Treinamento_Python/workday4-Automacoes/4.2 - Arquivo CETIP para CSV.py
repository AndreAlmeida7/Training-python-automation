import os

# Arquivo original ".CETIP21"
file_original = '15064_240516_DRESUMOEMIS-CDB.CETIP21'

# Retirando o prefixo ".CETIP" para ".CSV"
new_file = file_original.replace('.CETIP21', '.csv')

# Renomeando o próprio arquivo
os.rename(file_original, new_file)