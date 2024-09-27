import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Lendo o dataset
df = pd.read_excel('data_set.xslx')

# Filtrando os dados pela coluna 'Receita' com valores maiores ou iguais a 100.000
dados_filtrados = df[df['Receita'] >= 100000]

# Salvando os dados filtrados em um novo CSV
dados_filtrados.to_excel('dados_filtrados.xlsx', index=False)

# Enviando o e-mail
email_de = 'seu_email@gmail.com'
email_para = 'andre.almeida@neon.com.br'
senha = 'sua_senha'

msg = MIMEMultipart()
msg['From'] = email_de
msg['To'] = email_para
msg['Subject'] = 'Dados filtrados'

corpo_email = 'Segue em anexo os dados filtrados.'
msg.attach(MIMEText(corpo_email, 'plain'))

# Anexando o arquivo CSV
nome_arquivo = 'dados_filtrados.xlsx'
attachment = open(nome_arquivo, 'rb')

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % nome_arquivo)

msg.attach(part)

# Conectando-se ao servidor SMTP do Gmail
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(email_de, senha)

# Enviando o e-mail
texto_email = msg.as_string()
server.sendmail(email_de, email_para, texto_email)

# Encerrando a conexão
server.quit()

print("E-mail enviado com sucesso!")