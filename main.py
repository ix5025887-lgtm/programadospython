from conexao import ConexaoSingleton
from screen import (
    menu_principal, menu_produtos,
    menu_estoque, menu_vendas
)
from services import ServiceFactory

def main():
    conexao = ConexaoSingleton(
        "localhost", "root", "1125", "db1", "mysql_native_password"
    ).get_conexao()

    produto_service = ServiceFactory.criar_servico("produto", conexao)
    estoque_service = ServiceFactory.criar_servico("estoque", conexao)
    venda_service = ServiceFactory.criar_servico("venda", conexao)

    while True:
        opcao = menu_principal()

        # ===== PRODUTOS =====
        if opcao == "1":
            while True:
                op = menu_produtos()

                if op == "1":
                    codigo = int(input("Código: "))
                    nome = input("Produto: ")
                    preco = float(input("Preço: "))
                    produto_service.cadastrar(codigo, nome, preco)
                    print("Produto cadastrado com sucesso!")

                elif op == "2":
                    produtos = produto_service.listar()
                    if not produtos:
                        print("Nenhum produto cadastrado.")
                    else:
                        for p in produtos:
                            print(p)

                elif op == "0":
                    break

        # ===== ESTOQUE =====
        elif opcao == "2":
            while True:
                op = menu_estoque()

                if op == "1":
                    estoque = estoque_service.listar()
                    if not estoque:
                        print("Estoque vazio.")
                    else:
                        for e in estoque:
                            print(e)

                elif op == "2":
                    codigo = int(input("Código do produto: "))
                    quantidade = int(input("Quantidade de entrada: "))
                    estoque_service.entrada_produto(codigo, quantidade)

                elif op == "0":
                    break

        # ===== VENDAS =====
        elif opcao == "3":
            while True:
                op = menu_vendas()

                if op == "1":
                    codigo = int(input("Código do produto: "))
                    quantidade = int(input("Quantidade: "))
                    venda_service.registrar_venda(codigo, quantidade)
                
                    print("Venda realizada!")

                elif op == "2":
                    venda_service.cursor.execute("SELECT * FROM vendas")
                    vendas = venda_service.cursor.fetchall()
                    if not vendas:
                        print("Nenhuma venda realizada.")
                    else:
                        for v in vendas:
                            print(v)

                elif op == "0":
                    break

        elif opcao == "0":
            print("Encerrando sistema...")
            break

        else:
            print("Opção inválida.")

    conexao.close()

if __name__ == "__main__":
    main()
