import psycopg
from pgvector.psycopg import register_vector


def get_connection():
    con = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="Multi-modal RAG",
        user="postgres",
        password="shasen"
    )

    register_vector(con)

    return con
