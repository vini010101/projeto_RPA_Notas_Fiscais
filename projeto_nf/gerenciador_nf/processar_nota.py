import pandas as pd
from datetime import datetime
from .models import NotaFiscal, Usuarios
import re
from django.contrib.auth.models import User

def processar_nota_fiscal(upload_file, usuario_id):
    """
    Função para processar a planilha enviada e salvar os dados no banco de dados.
    
    :param upload_file: arquivo Excel ou CSV enviado pelo usuário.
    :param usuario_id: ID do usuário responsável pelo upload.
    """
    try:
        # Carregar a planilha em um DataFrame
        if upload_file.name.endswith('.xlsx') or upload_file.name.endswith('.xls'):
            df = pd.read_excel(upload_file)
        elif upload_file.name.endswith('.csv'):
            df = pd.read_csv(upload_file)
        else:
            raise ValueError("Formato de arquivo não suportado. Use .xlsx, .xls ou .csv")
    except Exception as e:
        raise ValueError(f"Erro ao processar a planilha: {e}")

    # Buscar o usuário responsável pelo upload
    try:
        usuario = Usuarios.objects.get(id=usuario_id)
    except Usuarios.DoesNotExist:
        raise ValueError("Usuário não encontrado.")

    user = usuario.user  # Obtém a instância do User associada ao Usuario

    # Processar os dados e salvar no banco
    for _, row in df.iterrows():
        cpf_cnpj = None
        data_nota = None
        valor_nota = None
        descricao_produto = None

        # Itera sobre as colunas para mapear os campos
        for coluna in row.index:
            valor_coluna = str(row[coluna])

            # CPF/CNPJ
            if not cpf_cnpj:
                cpf_cnpj_regex = r'(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})'
                cpf_cnpj_match = re.search(cpf_cnpj_regex, valor_coluna)
                cpf_cnpj = cpf_cnpj_match.group(0) if cpf_cnpj_match else None

            # Data da Nota (ajustado para o formato yyyy-mm-dd)
            if not data_nota:
                data_regex = r"\d{4}-\d{2}-\d{2}"  # regex ajustado para o formato yyyy-mm-dd
                data_match = re.search(data_regex, valor_coluna)
                if data_match:
                    data_nota = datetime.strptime(data_match.group(0), "%Y-%m-%d")
                else:
                    # Tentar converter diretamente se o formato for outro
                    try:
                        data_nota = pd.to_datetime(valor_coluna, errors='coerce')
                    except:
                        pass

            # Valor da Nota (ajustado para permitir valores como 150.75)
            if not valor_nota:
                valor_regex = r'\d+(\.\d{1,2})?'  # regex ajustado para aceitar valores como 150.75
                valor_match = re.search(valor_regex, valor_coluna)
                if valor_match:
                    valor_nota = valor_match.group(0)

            # Descrição do Produto
            if not descricao_produto:
                descricao_produto = valor_coluna.strip()  # Simplesmente pega o valor da coluna como descrição

            if not cpf_cnpj or not data_nota or not descricao_produto or not valor_nota:
                raise ValueError(f'Dados incompletos para a nota fiscal: {row}')

        # Criar instância do modelo e salvar no banco
        try:
            nota_fiscal = NotaFiscal(
                cpf_cnpj=cpf_cnpj,
                data_nota=data_nota,
                valor_nota=float(valor_nota) if valor_nota else 0.0,
                descricao_produto=descricao_produto,
                usuario=user  # Atribuindo o User ao invés do Usuario
            )
            nota_fiscal.save()
        except Exception as e:
            print(f"Erro ao salvar a nota fiscal: {e}")  # Debug: imprima o erro de salvar
