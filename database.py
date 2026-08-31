import sqlite3

#cria uma conexão com o sqlite e cria a tabela "biblioteca" caso ela não exista
conn = sqlite3.connect("biblioteca.db")
#ativa as chaves estrangeiras (são desativadas por padrão) antes de abrir o banco de dados
conn.execute("PRAGMA foreign_keys = ON;")

#cria um cursor para realizar os comandos no SQL 
cursor = conn.cursor()

#cria a tabela de livros e passa os atributos da tabela
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

def cadastrar_usuario(nome, email):
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO usuarios(
        nome, email
    ) VALUES (?, ?)
''',
(nome, email)
)
    conn.commit()
    conn.close()

def verificar_multa(id_usuario):
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()

    cursor.execute('''
    SELECT SUM(multa) FROM emprestimo
    WHERE id_usuario = ? AND multa > 0
''',
(id_usuario,)
)
    resultado = cursor.fetchone()[0]
    conn.close
    return resultado if resultado else 0.0
