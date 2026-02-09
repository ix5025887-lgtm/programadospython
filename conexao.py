import mysql.connector

class ConexaoSingleton:
    _instancia = None

    def __new__(cls, servidor, usuario, senha, banco, auth):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.conexao = mysql.connector.connect(
                host=servidor,
                user=usuario,
                password=senha,
                database=banco,
                auth_plugin=auth,
                autocommit=True
            )
        return cls._instancia

    def get_conexao(self):
        return self.conexao
