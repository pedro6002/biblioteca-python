class Livro:
    def __init__(self, id_livro, titulo_livro, autor, quantidade_disponivel):
        self.id = id_livro
        self.titulo_livro = titulo_livro
        self.autor = autor
        self.quantidade_disponivel = quantidade_disponivel

class Usuario:
    def __init__(self, id_usuario, nome, email):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email

class Emprestimo:
    def __init__(self, id_livro, id_usuario, data_entrega, id_emprestimo = None, multa = 0.0, disponibilidade = 1):
        self.id_emprestimo = id_emprestimo
        self.data_entrega = data_entrega
        self.multa = multa
        self.disponibilidade = disponibilidade
        self.id_usuario = id_usuario
        self.id_livro = id_livro
