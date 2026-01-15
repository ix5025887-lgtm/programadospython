def clear():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def menu_login():
    print("""
=== GestorStock ===
          
[1] Fazer Login
[2] Cadastra-se
[3] Esqueci a senha

===================
          """)

def menu(nome_cnpj):

    v="====== " + nome_cnpj + " ====="
    tam=len(v)
    print(f"""
====== {nome_cnpj} =====

[]
[]
[]
[]
          
{"="*tam}
""")