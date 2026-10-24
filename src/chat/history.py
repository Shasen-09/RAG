
def save_messages(conn, conversation_id, role, context):
    with conn.cursor() as cur:
        cur.execute(
            """
      INSERT INTO chat_messages(conversation_id,role,context)
      VALUES(%s,%s,%s)
      """, (
                str(conversation_id), role, context
            )
        )
    conn.commit()


def get_chat_history(conn, conversation_id, limit=10):
    with conn.cursor() as cur:
        cur.execute(
            """ 
      SELECT role, context FROM (
      SELECT id,role,context FROM chat_messages WHERE conversation_id = %s ORDER BY id DESC LIMIT %s) AS recent ORDER BY id ASC
      """, (str(conversation_id), limit)
        )
        return [
            {"role": role, "content": content}
            for role, content in cur.fetchall()
        ]
