# 📜 Gerenciador de Notas Fiscais  

🚀 **Um sistema para organizar, armazenar e consultar notas fiscais de forma eficiente, desenvolvido com Django e Docker.**  

## 🛠 Tecnologias Utilizadas  

- **Backend:** Django + Django REST Framework  
- **Banco de Dados:** PostgreSQL  
- **Conteinerização:** Docker + Docker Compose  
- **Autenticação:** Django Authentication  
- **Outras Bibliotecas:** Pandas (para manipulação de dados), Celery (para tarefas assíncronas)  

---

## 📌 Funcionalidades  

✅ Cadastro e armazenamento de notas fiscais  
✅ Consulta e filtragem por CNPJ, data e valor  
✅ Upload e extração automática de dados de XMLs de NF-e  
✅ Exportação de relatórios em CSV e PDF  
✅ API REST para integração com outros sistemas  
✅ Integração com mensageria para processamento assíncrono (opcional)  

---

## 🚀 Como Rodar o Projeto  

### 📦 1. Clonar o Repositório  
```bash
git clone https://github.com/seu-usuario/gerenciador-notas-fiscais.git
cd gerenciador-notas-fiscais
🐳 2. Subir os Containers com Docker
bash
Copiar
Editar
docker-compose up --build
Isso iniciará o backend e o banco de dados PostgreSQL.

🎯 3. Criar o Superusuário para o Admin Django
bash
Copiar
Editar
docker exec -it gerenciador-notas-fiscais-backend python manage.py createsuperuser
🔥 4. Acessar a Aplicação
API REST: http://localhost:8000/api/
Admin Django: http://localhost:8000/admin/
📂 Estrutura do Projeto
bash
Copiar
Editar
📁 gerenciador-notas-fiscais
├── 📂 app
│   ├── 📂 core             # Configuração principal do Django
│   ├── 📂 notas_fiscais    # App principal para gerenciar notas
│   ├── 📂 usuarios         # Gestão de usuários e autenticação
│   ├── 📂 templates        # Templates para exibição no Django Admin
│   ├── manage.py
│   ├── requirements.txt
├── 📜 Dockerfile
├── 📜 docker-compose.yml
├── 📜 README.md
📌 Endpoints Principais
Método	Endpoint	Descrição
GET	/api/notas/	Lista todas as notas fiscais
POST	/api/notas/	Adiciona uma nova nota fiscal
GET	/api/notas/{id}/	Obtém detalhes de uma nota fiscal
PUT	/api/notas/{id}/	Atualiza uma nota fiscal
DELETE	/api/notas/{id}/	Remove uma nota fiscal
POST	/api/upload/	Faz upload de um arquivo XML de NF-e
🛠 Como Contribuir
Fork o repositório
Crie uma branch: git checkout -b minha-feature
Faça as alterações e commit: git commit -m "Nova funcionalidade"
Envie para o repositório: git push origin minha-feature
Abra um Pull Request 🚀
📄 Licença
Este projeto está sob a licença MIT. Sinta-se à vontade para usá-lo e melhorá-lo!

💡 Dúvidas ou sugestões? Me chame no LinkedIn ou abra uma issue! 🚀
