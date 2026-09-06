from datetime import datetime, timedelta
import sqlite3

def criar_tabelas():
    '''Cria tabelas e o banco de dados no SQLite.
    
    Returns: 
        str: Mensagem de confirmação de tabela e banco de dados criados.
    '''
    
    #Cria uma conexão com o sqlite e cria a tabela "biblioteca" caso ela não exista
    conn = sqlite3.connect('biblioteca.db')

    #Ativa as chaves estrangeiras (são desativadas por padrão) antes de abrir o banco de dados
    conn.execute('PRAGMA foreign_keys = ON')

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
    '''Realiza o cadastro do usuário e salva na tabela usuarios.

        Args:
            nome (str): Nome completo do usuário a ser cadastrado.
            email (str): Email do usuário a ser cadastrado.
        
        Returns:
            str: Mensagem de confirmação de cadastro de usuário.

        Examples:
            >>> cadastrar_usuario("John McCallen", "johnmc@gmail.com")
            'Usuário cadastrado com sucesso!'
    '''

    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()

    cursor.execute('SELECT email FROM usuarios WHERE email = ?', (email,)
    )
    usuario_cadastrado = cursor.fetchone()
    if usuario_cadastrado:
        conn.close()
        return 'O usuário com esse email já existe!'

    cursor.execute('INSERT INTO usuarios(nome, email) VALUES (?, ?)', (nome, email)
    )
    conn.commit()
    conn.close()
    return 'Usuário cadastrado com sucesso!'

def verificar_multa(id_usuario):
    '''Faz a verificação de multas pendentes do usuário na coluna 'multa' da tabela emprestimo.
    
        Args:
            id_usuario (int): ID do usuário cadastrado.

        Returns:
            float: valor da multa do usuário.
        
        Examples:
            >>> verificar_multa(1)
            1.5
    '''

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
    '''Faz o empréstimo do livro para o usuário.

        Caso o usuário tenha multas pendentes, o empréstimo será negado, após isso,
        é feita a verificação do usuário já ter o mesmo livro emprestado no seu nome 
        e por fim, faz a verificação do livro estar disponível no estoque e atualiza a quantidade disponível do livro para 0.

        Args:
            id_usuario (int): ID do usuário cadastrado.
            id_livro (int): ID do livro cadastrado.
        
        Returns:
            str: Mensagem de confirmação que o livro foi emprestado.
        
        Examples:
            >>> emprestar_livro(1,1)
            'Não foi possivel realizar o empréstimo, o usuário possui multa de 3.00 reais.'

            >>> emprestar_livro(2,4)
            'O livro já está emprestado no seu nome!'

            >>> emprestar livro(3,5)
            'Livro emprestado com sucesso!'
    '''

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
    '''Função para devolver o livro de volta para o sistema e 'retirar' o livro do usuário.

        Args:
            id_usuario (int): ID do usuário cadastrado.
            id_livro (int): ID do livro cadastrado.
        
        Returns:
            str: Mensagem de confirmação de devolução do livro.

        Examples:
            >>> devolver_livro(3,5)
            'Livro devolvido com sucesso!'
    '''

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
    '''Cadastra o livro na tabela livros.

        Args:
            titulo_livro (str): Título do livro que deseja cadastrar
            autor (str): Autor do livro que deseja cadastrar

        Returns:
            str: Mensagem de confirmação do cadastro do livro.
        
        Examples:
            >>> cadastrar_livro('A república', 'Platão')
            'Livro cadastrado com sucesso!'
    '''

    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO livros(titulo_livro, autor) VALUES (?, ?)', (titulo_livro, autor)
    )
    conn.commit()
    conn.close()
    return 'Livro cadastrado com sucesso!'  

def visualizar_livro():
    '''Lista os livros disponíveis no banco de dados.

        Returns:
            list[dict]: Lista de dicionários '[{ }]' com os dados (id_livro, autor, titulo_livro, quantidade_disponivel). 

        Examples:
            >>> visualizar_livro()
            [{'id_livro' : 5, 'autor' : 'Platão', 'titulo_livro' : 'A república', 'quantidade_disponivel' : 0}]
    '''

    conn = sqlite3.connect('biblioteca.db')

    #Acessa os dados pelo nome das colunas
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id_livro, autor, titulo_livro, quantidade_disponivel FROM livros
    ''')
    leitura = cursor.fetchall()
    conn.close()

    #Transforma os valores da tabela [( )] em dicionario { }
    return [dict(leituras) for leituras in leitura]

def visualizar_emprestimo():
    '''Visualiza os empréstimos (ativos ou não) no banco de dados.

        Returns:
            list[dict]: Lista de dicionários '[{ }]' com os dados (id_emprestimo, id_usuario, id_livro, data_entrega, multa, disponibilidade).
        
        Examples:
            >>> visualizar_emprestimo()
            [{'id_emprestimo' : 1, 'id_usuario' : 3, 'id_livro' : 5, 'data_entrega' : '12-09-2026', 'multa' : 0.0, 'disponibilidade' : 1}]
    '''

    conn = sqlite3.connect('biblioteca.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id_emprestimo, id_usuario, id_livro, data_entrega, multa, disponibilidade FROM emprestimo
    ''')
    visualizacao = cursor.fetchall()
    conn.close()
    return [dict(visualizacoes) for visualizacoes in visualizacao]

def visualizar_usuario():
    '''Visualiza os usuários cadastrados no banco de dados.

        Returns:
            list[dict]: Lista de dicionários '[{ }]' com os dados (id_usuario, nome, email).

        Examples: 
            >>> visualizar_usuario()
            [{'id_usuario' : 1, 'nome' : 'John McCallen', 'email' : 'johnmc@gmail.com'}] 
    '''

    conn = sqlite3.connect('biblioteca.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id_usuario, nome, email FROM usuarios
    ''')
    ver_usuarios = cursor.fetchall()
    cursor.close()
    return [dict(visualizar) for visualizar in ver_usuarios]

def visualizar_livros_emprestados(id_usuario):
    '''Visualiza os livros emprestados do usuário

        Args: id_usuario (int) = ID do usuário que deseja consultar os livros emprestados

        Returns:
            list[dict]: Lista de dicionários '[{ }]' com os dados (id_livro, titulo_livro, data_entrega)
        
        Examples:
            >>> visualizar_livros_emprestados(3)
            [{'id_livro' : 5, 'titulo_livro' : 'A república', 'data_entrega' : '12-09-2026'}]   
    '''

    conn = sqlite3.connect("biblioteca.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('''
        SELECT livros.id_livro, livros.titulo_livro, emprestimo.data_entrega
        FROM emprestimo
        JOIN livros ON emprestimo.id_livro = livro.id_livro
        WHERE emprestimo.id_usuario = ? AND emprestimo.disponibilidade = 1
    ''', (id_usuario,))

    ver_emprestimos = cursor.fetchall()
    conn.close()
    return [dict(ver) for ver in ver_emprestimos]