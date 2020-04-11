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
        return results

    def user_register(self):
        query = """
                [usr].[CreateUser] ?, ?, ?, ?
                """
        params = (self.get_email(), self.get_password(), self.get_first_name(), self.get_last_name())
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_sproc(query, params, cursor)
        if results['Status'] != 500:
            conn.commit()
        conn.close()
        return results

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
        if results['Status'] == 404:
            cursor.commit()
        conn.close()
        return results

    @staticmethod
    def get_user_info(user_id):
        query = f"""
                SELECT TOP 1
                    [Email]
                    ,[FirstName]
                    ,[LastName]
                    ,[Institution]
                FROM
                    [usr].[User]
                WHERE
                    [UserID] = {user_id}
                """
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_query(query, cursor)
        conn.close()
        user = User()
        for row in results:
            user.set_user_id(user_id)
            user.set_email(row[0])
            user.set_first_name(row[1])
            user.set_last_name(row[2])
            if row[3] is not None:
                user.set_institution(row[3])
        return user

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

    def set_institution(self, institution):
        self.user['institution'] = institution
        return self

    def get_institution(self):
        return self.user['institution']

    def set_institution_role(self, role):
        self.user['role'] = role
        return self

    def get_institution_role(self):
        return self.user['role']
