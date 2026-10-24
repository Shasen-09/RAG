from connection import get_connection

db = get_connection()

print("Database connected successfullly")

db.close()
