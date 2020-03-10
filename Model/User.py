from Utils.Database import Database


class User:

    def __init__(self):
        self.user_id = None
        self.user = {}

    @staticmethod
    def user_login(email, password):
        query = """
                [usr].[UserLogin] ?, ?
                """
        params = (email, password)
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_sproc(query, params, cursor)
        conn.commit()
        conn.close()
        return results[0][0]

    def user_register(self):
        query = """
                [usr].[CreateUser] ?, ?, ?, ?
                """
        params = (self.get_email(), self.get_password(), self.get_first_name(), self.get_last_name())
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_sproc(query, params, cursor)
        if results[0][0] is not 500:
            response = results[0][0]
            conn.commit()
        else:
            response = results[0][0]
        conn.close()
        return response

    @staticmethod
    def create_user_obj(user_obj):
        user = User()
        user.set_email(user_obj['Email'])
        user.set_password(user_obj['Password'])
        user.set_first_name(user_obj['FirstName'])
        user.set_last_name(user_obj['LastName'])
        return user

    @staticmethod
    def get_user_from_session(session_id):
        query = """
                [usr].[GetUserIDFromSession] ?
                """
        params = session_id
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_sproc(query, params, cursor)
        conn.close()
        return results[0][0]

    def set_user_id(self, user_id):
        self.user_id = user_id
        return self

    def get_user_id(self):
        return self.user_id

    def set_email(self, email):
        self.user['email'] = email
        return self

    def get_email(self):
        return self.user['email']

    def set_password(self, password):
        self.user['password'] = password
        return self

    def get_password(self):
        return self.user['password']

    def set_first_name(self, first_name):
        self.user['first_name'] = first_name
        return self

    def get_first_name(self):
        return self.user['first_name']

    def set_last_name(self, last_name):
        self.user['last_name'] = last_name
        return self

    def get_last_name(self):
        return self.user['last_name']
