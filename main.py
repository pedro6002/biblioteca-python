import database
from classes import Usuario, Emprestimo, Livro

def inicio():
    database.criar_tabelas()

    print('==== BEM-VINDO ====\n' \
    'Opções\n' \
    '1- Cadastrar usuário\n' \
    '2- Verificar usuários\n' \
    '3- Cadastrar livro \n' \
    '4- Verificar livros\n' \
    '5- Emprestar livro\n'
    '6- Devolver livro\n' \
    '7- Visualizar livros emprestados\n' \
    '8- Sair\n')

def menu(inicio):
    '''
    Exibe a interface interativa de linha de comando do sistema da biblioteca.

    Controla o fluxo contínuo de navegação da aplicação através de um loop principal,
    solicitando comandos do usuário e direcionando a execução para as operações
    de cadastro, consulta, empréstimo e devolução correspondentes via match/case.

    Returns:
        None: A função executa até que a opção de saída seja acionada,
        encerrando a execução do loop interativo.
    '''

    while True:
        inicio()
        opcao = input('Escolha uma opção: ').strip()
        match opcao:
            case '1':
                nome = input('Nome completo: ')
                email = input('Email: ')
                novo_usuario = Usuario(nome=nome, email=email)
                print(database.cadastrar_usuario(novo_usuario.nome, novo_usuario.email))

            case '2':
                usuarios = database.visualizar_usuario()
                for usuario in usuarios:
                    print(f'ID do usuário: {usuario['id_usuario']} | Nome: {usuario['nome']} | Email: {usuario['email']}')

            case '3':
                nome_livro = input('Nome do livro: ')
                autor = input('Autor(a): ')
                novo_livro = Livro(nome_livro = nome_livro, autor = autor)
                print(database.cadastrar_livro(novo_livro.nome_livro, novo_livro.autor))

            case '4':
                dados_livros = database.visualizar_livro()
                livros = [
                    Livro(
                        id_livro = dado['id_livro'],
                        titulo_livro = dado['titulo_livro'],
                        autor = dado['autor'],
                        quantidade_disponivel = dado['quantidade_disponivel']
                    ) for dado in dados_livros
                ]
                for livro in livros:
                    print(f'ID do livro: {livro.id} | Título: {livro.titulo_livro} | Autor: {livro.autor} | Qtd: {livro.quantidade_disponivel}')
            case '5':
                id_usuario = int(input('Digite o ID do usuário: '))
                id_livro_emprestar = int(input('Digite o ID do livro que deseja emprestar:'))
                print(database.emprestar_livro(id_usuario, id_livro_emprestar))

            case '6':
                id_usuario = int(input('Digite o ID do usuário: '))
                livros_emprestados = database.visualizar_livros_emprestados(id_usuario)

                if not livros_emprestados:
                    print('Usuário não tem livros emprestados no momento.')
                else:
                    print('\n--Livros emprestados--')
                    for livro in livros_emprestados:
                        print(f'ID Livro: {livro['id_livro']} | Titulo: {livro['titulo_livro']} | Data de entrega: {livro['data_entrega']}')

            case '7': 
                dados_emprestimo = database.visualizar_emprestimo()
                emprestimos = [
                    Emprestimo(
                        id_emprestimo = dado['id_emprestimo'],
                        id_usuario = dado['id_usuario'],
                        id_livro = dado['id_livro'],
                        data_entrega = dado['data_entrega'],
                        multa = dado['multa'],
                        disponibilidade = dado['disponibilidade']
                    ) for dado in dados_emprestimo
                ]
                print("\n--Histórico de empréstimos--")
                for emprestimo in emprestimos:
                    print(
                    f"Empréstimo: {emprestimo.id_emprestimo} | Usuário ID: {emprestimo.id_usuario} | "
                    f"Livro ID: {emprestimo.id_livro} | Data de entrega: {emprestimo.data_entrega} | Status: {emprestimo.status()}"
                    )

            case '8':
                print('Até a próxima!')
                break

            case _:
                print('Opção inválida! Tente novamente.')

if __name__ == '__main__':
    menu(inicio)