def menu_principal():
    print("\n===== SISTEMA DE MERCADO =====")
    print("1 - Produtos")
    print("2 - Estoque")
    print("3 - Vendas")
    print("0 - Sair")
    return input("Escolha: ")

def menu_produtos():
    print("\n--- MENU PRODUTOS ---")
    print("1 - Cadastrar produto")
    print("2 - Listar produtos")
    print("0 - Voltar")
    return input("Escolha: ")

def menu_estoque():
    print("\n--- MENU ESTOQUE ---")
    print("1 - Ver estoque")
    print("2 - Entrada de produto no estoque")
    print("0 - Voltar")
    return input("Escolha: ")

def menu_vendas():
    print("\n--- MENU VENDAS ---")
    print("1 - Realizar venda")
    print("2 - Relatório de vendas")
    print("0 - Voltar")
    return input("Escolha: ")
