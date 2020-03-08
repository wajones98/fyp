from Utils.Database import Database

class User:

    def __init(self, content):
        self.user_id = content['UserID']

    @staticmethod
    def user_login(email, password):
        query = """
                [usr].[UserLogin] ?, ?
                """
        params = (email, password)
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_sproc(query, params, cursor)
        conn.close()
        if results[0][0] is not 500:
            return results[0][0]
        else:
            return results[0][0]
