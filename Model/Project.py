from Utils.Database import Database
from Model.User import User


class Project:

    @staticmethod
    def create_project(user_id, project_info):

        query = """
                [prj].[CreateProject] @Creator = ?, @Name = ?, @Desc = ?, @Public = ?
                """
        params = (user_id, project_info['Name'], project_info['Desc'], project_info['Public'])
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_sproc(query, params, cursor)
        if results['Status'] == 201:
            cursor.commit()
        conn.close()
        return results

    @staticmethod
    def join_project(user_id, project_id):
        query = """
                [prj].[AcceptProjectInvite] @UserId = ?, @ProjectId = ?
                """
        params = (user_id, project_id)
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_sproc(query, params, cursor)
        if results['Status'] == 201:
            cursor.commit()
        conn.close()
        return results

    @staticmethod
    def invite_to_project(project_info):
        query = """
                [prj].[InviteUserToProject] @UserId = ?, @ProjectId = ?
                """
        user_id = User.get_user_from_email(project_info['Email'])
        project_id = project_info['ProjectId']
        params = (user_id, project_id)
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_sproc(query, params, cursor)
        if results['Status'] == 201:
            cursor.commit()
        conn.close()
        return results

    @staticmethod
    def leave_project(user_id, project_id):
        query = """
                [prj].[RemoveProject] @UserId = ?, @ProjectId = ?
                """
        params = (user_id, project_id)
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_sproc(query, params, cursor)
        if results['Status'] == 201:
            cursor.commit()
        conn.close()
        return results

    @staticmethod
    def remove_project(user_id, project_id, email):
        query = f"""
                SELECT 
                    [creator]
                FROM
                    [prj].[project]
                WHERE
                    [ProjectId] = '{project_id}'
                """
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_query(query, cursor)
        conn.close()
        if user_id == results[0][0]:
            remove_member = User.get_user_from_email(email)
            if remove_member is not None:
                query = """
                        [prj].[RemoveProject] @UserId = ?, @ProjectId = ?
                        """
                params = (user_id, project_id)
                conn = Database.connect()
                cursor = conn.cursor()
                results = Database.execute_sproc(query, params, cursor)
                if results['Status'] == 201:
                    cursor.commit()
                conn.close()
                return results
            else:
                return {'Status': 400, 'Message': 'There is no account associated with this email'}
        else:
            return {'Status': 400, 'Message':'This user is not the owner of the project'}

    def __init__(self):
        self.project_id = None
        self.project = {}

    def set_project_id(self, project_id):
        self.project_id = project_id
        return self

    def get_project_id(self):
        return self.project_id

    def set_creator(self, creator):
        self.project['Creator'] = creator
        return self

    def get_creator(self):
        return self.project['Creator']

    def set_name(self, name):
        self.project['Name'] = name
        return self

    def get_name(self):
        return self.project['Name']

    def set_desc(self, desc):
        self.project['Desc'] = desc
        return self

    def get_desc(self):
        return self.project['Desc']

    def set_start_date(self, start_date):
        self.project['StartDate'] = start_date
        return self

    def get_start_date(self):
        return self.project['StartDate']

    def set_end_date(self, end_date):
        self.project['EndDate'] = end_date
        return self

    def get_end_date(self):
        return self.project['EndDate']

    def set_public(self, public):
        self.project['Public'] = public
        return self

    def get_public(self):
        return self.project['Public']

    def set_project_members(self, members):
        self.project['Members'] = members
        return self

    def get_project_members(self):
        return self.project['Members']