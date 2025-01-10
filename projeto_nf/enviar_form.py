import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os
import uuid

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def enviar_email(nome, fone, fone2, email, mensagem, tempo, custo_estimado, fotos=[]):
    # Configurações do servidor SMTP
    server_smtp = "smtp.gmail.com"
    port = 587
    sender_email = os.getenv('EMAIL_REMETENTE')
    password = os.getenv('EMAIL_SENHA_APP')
    recive_email = os.getenv("EMAIL_DESTINATARIO")
    subject = "Novo orçamento"
    
    # Configurando o corpo do e-mail
    body = f"""
    <h1>Orçamento Solicitado</h1>
    <p><strong>Nome:</strong> {nome}</p>
    <p><strong>Telefone 1:</strong> {fone}</p>
    <p><strong>Telefone 2:</strong> {fone2}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Dias:</strong> {tempo}</p>
    <p><strong>Valor:</strong> {custo_estimado}</p>
    <p><strong>Mensagem:</strong> {mensagem}</p>
    """

    # Cria o objeto de mensagem
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recive_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    # Diretório temporário para salvar os arquivos
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)

    # Salvar fotos temporariamente e anexar ao e-mail
    fotos_paths = []
    try:
        for foto in fotos:
            # Cria um nome único para cada arquivo
            foto_nome = f"{uuid.uuid4()}_{foto.name}"
            foto_path = os.path.join(temp_dir, foto_nome)
            fotos_paths.append(foto_path)

            # Salva o arquivo temporariamente
            with open(foto_path, "wb") as destino:
                for chunk in foto.chunks():
                    destino.write(chunk)

            # Anexa o arquivo ao e-mail
            with open(foto_path, "rb") as file:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(file.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={foto_nome}",
                )
                msg.attach(part)

        # Enviar o e-mail
        with smtplib.SMTP(server_smtp, port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, recive_email, msg.as_string())
            print("Formulário enviado com sucesso!")

    except Exception as e:
        print(f"Erro ao enviar o formulário: {e}")
    
    finally:
        # Excluir os arquivos temporários
        for foto_path in fotos_paths:
            try:
                os.remove(foto_path)
            except Exception as e:
                print(f"Erro ao excluir o arquivo {foto_path}: {e}")
