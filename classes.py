class Livro:
    def __init__(self, titulo_livro, autor, quantidade_disponivel, id_livro = None):
        self.titulo_livro = titulo_livro
        self.autor = autor
        self.quantidade_disponivel = quantidade_disponivel
        self.id_livro = id_livro

class Usuario:
    def __init__(self, nome, email, id_usuario = None):
        self.nome = nome
        self.email = email
        self.id_usuario = id_usuario

class Emprestimo:
    def __init__(self, id_livro, id_usuario, data_entrega, id_emprestimo = None, multa = 0.0, disponibilidade = 1):
        self.data_entrega = data_entrega
        self.id_emprestimo = id_emprestimo
        self.multa = multa
        self.disponibilidade = disponibilidade
        self.id_usuario = id_usuario
        self.id_livro = id_livro
