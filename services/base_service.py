class BaseService:
    def __init__(self, conexao):
        self.con = conexao
        self.cursor = self.con.cursor(buffered=True)
