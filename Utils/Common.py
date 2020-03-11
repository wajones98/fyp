from Utils.Database import Database


def generate_unique_identifier():
    query = """
            SELECT NEWID()
            """
    conn = Database.connect()
    cursor = conn.cursor()
    results = Database.execute_query(query, cursor)
    conn.close()
    return results[0][0]