 Módulo de Importação de Ocorrências

### 📌 Objetivo

Este módulo tem como objetivo importar automaticamente dados de Boletins de Ocorrência de planilhas Excel (.xlsx), filtrar apenas os tipos de violência doméstica permitidos e salvar os dados no banco de dados local para posterior integração com outros módulos, como o de Medidas Protetivas.

---

### ⚙️ Tecnologias utilizadas

* **Linguagem:** Python 3.11+
* **Framework:** Django 4.x
* **Leitura de planilhas:** Pandas
* **Banco de dados:** MySQL
* **Frontend:** HTML + Bootstrap (formulário simples)
* **Admin:** Django Admin

---

### 📦 Requisitos para rodar o projeto

#### 1. Sistema operacional:

* Windows 10/11
* Linux (Ubuntu 20.04+ ou compatível)

#### 2. Dependências:

* Python 3.11+
* MySQL Server
* `pip`, `venv`, `virtualenv`
* Pacotes Python: `django`, `mysqlclient`, `pandas`, `openpyxl`, `django-environ`

---

### 🧪 Passo a passo para testar o projeto

#### 💻 Windows / Linux

##### 1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/projetoBPM.git
cd projetoBPM
```

##### 2. Crie o ambiente virtual:

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

##### 3. Instale as dependências:

```bash
pip install -r requirements.txt
```

##### 4. Crie o arquivo `.env`:

```env
DEBUG=True
SECRET_KEY=sua-chave-secreta
DB_NAME=ocorrencias
DB_USER=lucas
DB_PASSWORD=lucasx123
DB_HOST=localhost
DB_PORT=3306
```

##### 5. Realize as migrações:

```bash
python manage.py makemigrations
python manage.py migrate
```

##### 6. Crie o superusuário:

```bash
python manage.py createsuperuser
```

##### 7. Rode o servidor:

```bash
python manage.py runserver
```

---

### 📥 Como usar o sistema

1. Acesse o endereço: [http://127.0.0.1:8000/importar/](http://127.0.0.1:8000/importar/)
2. Faça upload de uma planilha com os seguintes campos obrigatórios:

```
nome_assistida, rua_assistida, numero_assistida, bairro_assistida, cidade_assistida, municipio_assistida,
nome_agressor, rua_agressor, numero_agressor, bairro_agressor, cidade_agressor, municipio_agressor,
local_ocorrencia, tipo, relacao_vitima_autor, data
```

3. Após o envio, o sistema:

   * Filtra apenas os tipos válidos (ex: Ameaça, Lesão corporal);
   * Valida datas e colunas obrigatórias;
   * Insere os dados no banco.

4. Acesse [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) para visualizar os dados inseridos.

---

### 🗃️ Estrutura do projeto

```
projetoBPM/
│
├── registro/
│   ├── models.py       # Modelos: Assistida, Agressor, Endereco, Ocorrencia
│   ├── views.py        # Função de importação via planilha
│   ├── templates/
│   │   ├── importar.html
│   │   └── sucesso.html
│   ├── admin.py        # Registro dos modelos no Admin
│
├── projetoBPM/
│   └── settings.py     # Configurações de banco, apps, etc.
│
├── requirements.txt    # Dependências do projeto
├── manage.py
└── .env                # Variáveis de ambiente (criar manualmente)
```

---

### 🛠️ Observações

* O banco de dados deve estar criado previamente com o nome `ocorrencias`.
* A filtragem ignora automaticamente registros com:

  * Tipos de violência não reconhecidos;
  * Datas inválidas;
  * Campos obrigatórios vazios.
* O sistema é compatível com extensões `.xlsx`.
* A estrutura dos dados importados é reutilizável por outros módulos do sistema.

---
Status -> Em desenvolvimento 