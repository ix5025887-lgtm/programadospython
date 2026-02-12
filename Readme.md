# Sistema de Gerenciamento de Cantina

O seguinte projeto trata-se de um sistema de gerenciamento de cantina escolar, desenvolvido em Python. Inclui controle de estoque, vendas, cadastros e relatórios.

O sistema também conta com implementação utilizando **Django** para gerenciamento via interface web e API.

## Funcionalidades

### Controle de produtos

* Cadastrar produto
* Editar produto
* Excluir produto
* Inativar produtos
* Consultar produtos
* Avaliação do produto

### Controle de estoque

* Controle de entrada/saída
* Relatórios
* Organização por categoria

### Controle de vendas

* Quantidade de vendas

### Relatórios

* Gerar relatórios

## Tecnologias utilizadas

* Python 3.10+
* Django 4.0+
* MySQL 8.0+
* MySQL Connector/Python
* pip

## Instalação

### MySQL

1. Abra o navegador e acesse: [https://dev.mysql.com/downloads/mysql/](https://dev.mysql.com/downloads/mysql/)
2. Role a página até a lista de downloads disponíveis. Clique no botão "Download" ao lado do download desejado.

   * Windows 64 bits - Windows (x86, 64 bits), MSI
   * Windows 32 bits - Windows (x86, 32 bits), MSI

Se você não tiver certeza, considere que está usando um computador de 64 bits.

---

### Django

Instale o Django via pip:

```
pip install django
```

Caso utilize Django REST Framework:

```
pip install djangorestframework
```

---

### MySQL connector/Python

A API clássica pode ser instalada via pip:

```
pip install mysql-connector-python
```

## Execução (Django)

Após configurar o banco de dados:

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Acesse no navegador:

```
http://127.0.0.1:8000/
```

## Autores

* [Arthur Silva](https://github.com/ArthurAlder)
* [Icaro Pacheco](https://github.com/ix5025887-lgtm)
