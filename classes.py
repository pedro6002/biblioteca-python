class Livro:
    def __init__(self, id_livro, nome_livro, autor, quantidade_disponivel):
        self.id = id_livro
        self.nome_livro = nome_livro
        self.autor = autor
        self.quantidade_disponivel = quantidade_disponivel

class Usuario:
    def __init__(self, id_usuario, nome, email):
        self.id_usuario = id_usuario
        self.nome = nome
        self.email = email

class Emprestimo:
    def __init__(self, data_entrega, multa, disponibilidade):
        self.data_entrega = data_entrega
        self.multa = multa
        self.disponibilidade = disponibilidade