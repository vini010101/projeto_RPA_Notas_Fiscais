import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import re
import tempfile
from datetime import datetime

# Função para processar o arquivo da nota fiscal
def processar_nota_fiscal(upload_file):
    """
    Função para processar o arquivo da nota fiscal utilizando Tesseract OCR
    e extrair informações como CPF/CNPJ, data da nota, valor e descrição.
    """
    # Salvando o arquivo temporariamente
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(upload_file.read())
        tmp_file_path = tmp_file.name

    # Convertendo o PDF em imagem
    imagens = convert_from_path(tmp_file_path)
    imagem = imagens[0]  # Usando a primeira página do PDF
    texto_extraido = pytesseract.image_to_string(imagem)

    # Usando expressões regulares para extrair dados
    cpf_cnpj_regex = r'(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})'
    data_regex = r'\d{2}/\d{2}/\d{4}'
    valor_regex = r'R\$ [\d\.,]+'
    descricao_regex = r'(?:Descrição|Produto).+'

    # Extração das informações usando regex
    cpf_cnpj = re.search(cpf_cnpj_regex, texto_extraido)
    data_nota = re.search(data_regex, texto_extraido)
    valor_nota = re.search(valor_regex, texto_extraido)
    descricao_produto = re.search(descricao_regex, texto_extraido)

    # Retorna um dicionário com os dados extraídos
    return {
        "cpf_cnpj": cpf_cnpj.group(0) if cpf_cnpj else None,
        "data_nota": datetime.strptime(data_nota.group(0), "%d/%m/%Y") if data_nota else None,
        "valor_nota": valor_nota.group(0).replace("R$", "").replace(",", ".") if valor_nota else None,
        "descricao_produto": descricao_produto.group(0) if descricao_produto else None
    }
