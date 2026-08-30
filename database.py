import sqlite3

#cria uma conexão com o sqlite e cria a tabela "biblioteca" caso ela não exista
conn = sqlite3.connect("biblioteca.db")

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
