import mysql.connector

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1125",
    database="db1",
    auth_plugin='mysql_native_password'
)



if conexao.is_connected():
    db_info = conexao.get_server_info()
    print("Conectado ao banco com sucesso!")
    print("Versão do servidor:", db_info)

cursor = conexao.cursor()
cursor.execute("SHOW TABLES")

for tabela in cursor:
    print(tabela)

cursor.close()
conexao.close()
