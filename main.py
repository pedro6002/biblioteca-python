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

    while True:
        inicio()
        opcao = input('Escolha uma opção: ')
        match opcao:
            case 1:
                nome = input('Nome completo: ')
                email = input('Email: ')
                novo_usuario = Usuario(nome=nome, email=email)
                print(database.cadastrar_usuario(novo_usuario.nome, novo_usuario.email))

            case 2:
                usuarios = database.visualizar_usuario()
                for i in usuarios:
                    print(f'ID: {i['id_usuario']} | Nome: {i['nome']} | Email: {i['email']}')

            case 3:
                nome_livro = input('Nome do livro: ')
                autor = input('Autor(a): ')
                novo_livro = Livro(nome_livro = nome_livro, autor = autor)
                print(database.cadastrar_livro(novo_livro.nome_livro, novo_livro.autor))

            case 4:
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
                    print(f'ID: {livro.id} | Título: {livro.titulo_livro} | Autor: {livro.autor} | Qtd: {livro.quantidade_disponivel}')
            case 5:
                id_usuario = int(input('Digite o ID do usuário: '))
                id_livro_emprestar = int(input('Digite o ID do livro que deseja emprestar:'))
                print(database.emprestar_livro(id_usuario, id_livro_emprestar))

            case 6:
                id_usuario = int(input('Digite o ID do usuário: '))
                livros_emprestados = database.visualizar_livros_emprestados(id_usuario)

                if not livros_emprestados:
                    print('Usuário não tem livros emprestados no momento.')
                else:
                    print('\n--Livros emprestados--')
                    for livro in livros_emprestados:
                        print(f'ID Livro: {livro[id_livro]} | Titulo: {[titulo_livro]} | Data de entrega: {[data_entrega]}')

            case 7: 
                emprestimos = database.visualizar_emprestimo()
                for ver in emprestimos:
                    print(ver)

            case 8:
                print('Até a próxima!')
                break

            case _:
                print('Opção inválida! Tente novamente.')

if __name__ == '__main__':
    menu(inicio)