import json
import mysql.connector

conexao = mysql.connector.connect(host="localhost", user="root", password="1125", database="db1")

if conexao.is_connected("db1"):
    db_info=conexao.get_server_info()
    print("Conectado ao banco com sucesso!")

print(db_info)