import sqlite3
import hashlib
import os

# Lista de usuários de exemplo: (nome, email, telefone)
USUARIOS = [
    ("Maria Silva",    "maria@email.com",    "(21) 99999-9999"),
    ("João Souza",     "joao@email.com",     "(21) 98888-8888"),
    ("Ana Lima",       "ana@email.com",      "(21) 97777-7777"),
    ("Carlos Pereira", "carlos@email.com",   "(21) 96666-6666"),
    ("Fernanda Costa", "fernanda@email.com", "(21) 95555-5555"),
    ("Rafael Almeida", "rafael@email.com",   "(21) 94444-4444"),
    ("Juliana Rocha",  "juliana@email.com",  "(21) 93333-3333"),
    ("Pedro Martins",  "pedro@email.com",    "(21) 92222-2222"),
    ("Camila Santos",  "camila@email.com",   "(21) 91111-1111"),
    ("Lucas Ferreira", "lucas@email.com",    "(21) 90000-0000"),
]

SENHA_PADRAO = "123456"


def gerar_hash(senha):
    """Transforma a senha em hash (não guarda a senha pura)."""
    salt = os.urandom(16)
    h = hashlib.pbkdf2_hmac("sha256", senha.encode(), salt, 100_000)
    return salt.hex() + ":" + h.hex()


def main():
    conexao = sqlite3.connect("meu_sistema.db")
    cursor = conexao.cursor()

    # 1. Cria a tabela do zero
    cursor.execute("DROP TABLE IF EXISTS usuarios")
    cursor.execute("""
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            telefone TEXT,
            senha TEXT NOT NULL
        )
    """)

    # 2. Insere os usuários
    for nome, email, telefone in USUARIOS:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, telefone, senha) VALUES (?, ?, ?, ?)",
            (nome, email, telefone, gerar_hash(SENHA_PADRAO)),
        )

    conexao.commit()

    # 3. Confere o resultado
    print("Banco populado! Usuários cadastrados:\n")
    for linha in cursor.execute("SELECT id, nome, email, telefone FROM usuarios"):
        print(linha)

    conexao.close()


if __name__ == "__main__":
    main()
