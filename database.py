from datetime import datetime, timedelta
import sqlite3

def criar_tabelas():
    
    #Cria uma conexão com o sqlite e cria a tabela "biblioteca" caso ela não exista
    conn = sqlite3.connect('biblioteca.db')

    #Ativa as chaves estrangeiras (são desativadas por padrão) antes de abrir o banco de dados
    conn.execute('PRAGMA foreign_keys = ON;')

    #Cria um cursor para realizar os comandos no SQL 
    cursor = conn.cursor()

    #Cria a tabela de livros e passa os atributos da tabela
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
        id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo_livro TEXT NOT NULL,
        autor TEXT NOT NULL,
        quantidade_disponivel INTEGER DEFAULT 1 
        )
    '''
    )

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL
        )
    '''    
    )

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emprestimo (
        id_emprestimo INTEGER PRIMARY KEY,
        id_usuario INTEGER,
        id_livro INTEGER,
        data_entrega TEXT,
        multa REAL,
        disponibilidade INTEGER DEFAULT 1 CHECK (disponibilidade IN (0,1)),
        FOREIGN KEY (id_livro) REFERENCES livros (id_livro),
        FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
        )
    '''
    )

    conn.commit()
    conn.close()
    return 'Banco de dados e tabela criadas com sucesso!'

def cadastrar_usuario(nome, email):

    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    cursor.execute('SELECT email FROM usuariosWHERE email = ?', (email,)
    )
    usuario_cadastrado = cursor.fetchone()
    if usuario_cadastrado:
        conn.close()
        return 'O usuário com esse email já existe!'

    cursor.execute('INSERT INTO usuarios(nome, email) VALUES (?, ?)',(nome, email)
    )
    conn.commit()
    conn.close()
    return 'Usuário cadastrado com sucesso!'

def verificar_multa(id_usuario):

    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT SUM(multa)
    FROM emprestimo
    WHERE id_usuario = ? AND multa > 0
    ''',
    (id_usuario,)
    )
    checagem = cursor.fetchone()[0]
    conn.close
    return checagem if checagem else 0.0

def emprestar_livro(id_usuario, id_livro):

    #Função para colocar data, evitando do usuário colocar data de entrega como parâmetro
    data_entrega = (datetime.now() + timedelta(days=7)).strftime('%d-%m-%Y')

    #Verifica se o usuário tem multa pendente, negando o empréstimo
    multa_pendente = verificar_multa(id_usuario)
    if multa_pendente > 0:
        return f'Não foi possivel realizar o empréstimo, o usuário possui multa de {multa_pendente:.2f} reais.'
    
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT id_emprestimo FROM emprestimo 
    WHERE id_usuario = ? AND id_livro = ? AND disponibilidade = 1
    ''', (id_usuario, id_livro))
    emprestimo_ativo = cursor.fetchone()

    if emprestimo_ativo:
        conn.close()
        return 'O livro já está emprestado no seu nome!'

    cursor.execute('SELECT quantidade_disponivel FROM livros WHERE id_livro = ?', (id_livro,)
    )
    checagem = cursor.fetchone()

    #Checa se o livro existe e se está disponivel
    if not checagem or checagem[0] <= 0:
        conn.close()
        return 'Não foi possivel realizar o empréstimo, livro indisponível no momento.'

    cursor.execute('''
    INSERT INTO emprestimo (
    id_usuario, id_livro, data_entrega, multa, disponibilidade
    ) VALUES (?, ?, ?, 0.0, 1)
    ''', (id_usuario, id_livro, data_entrega)
    )

    #Atualiza a tabela, colocando a quantidade disponivel em 0
    cursor.execute('''
    UPDATE livros SET quantidade_disponivel = quantidade_disponivel - 1 WHERE id_livro = ?
    ''', (id_livro,)
    )
    conn.commit()
    conn.close()
    return 'Livro emprestado com sucesso!'

def devolver_livro(id_usuario, id_livro):

    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    #Atualiza a tabela de livros, aumentando a quantidade do id do livro emprestado
    cursor.execute('''
    UPDATE livros 
    SET quantidade_disponivel = quantidade_disponivel + 1
    WHERE id_livro = ?
    ''', (id_livro,)
    )

    #Atualiza a tabela de emprestimo, retirando o livro do usuario
    cursor.execute('''
    UPDATE emprestimo
    SET disponibilidade = 0
    WHERE id_usuario = ?
    AND id_livro = ?
    AND disponibilidade = 1
    ''' , (id_usuario, id_livro)
    )
    conn.commit()
    conn.close()
    return 'Livro devolvido com sucesso!' 

def cadastrar_livro(titulo_livro, autor):

    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO livros(titulo_livro, autor) VALUES (?, ?)', (titulo_livro, autor)
    )
    conn.commit()
    conn.close()
    return 'Livro cadastrado com sucesso!'  

def visualizar_livro():

    conn = sqlite3.connect('biblioteca.db')

    #Acessa os dados pelo nome das colunas
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id_livro, autor, titulo_livro, quantidade_disponivel FROM livros
    ''')
    leitura = cursor.fetchall()
    cursor.close()

    #Transforma os valores da tabela [( )] em dicionario { }
    return [dict(leituras) for leituras in leitura]

def visualizar_emprestimo():

    conn = sqlite3.connect('biblioteca.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id_emprestimo, id_livro, data_entrega, multa, disponibilidade FROM emprestimo
    ''')
    visualizacao = cursor.fetchall()
    cursor.close()
    return [dict(visualizacoes) for visualizacoes in visualizacao]

def visualizar_usuario():

    conn = sqlite3.connect('biblioteca.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
    SELECT nome, email FROM usuarios
    ''')
    ver_usuarios = cursor.fetchall()
    cursor.close()
    return [dict(visualizar) for visualizar in ver_usuarios]