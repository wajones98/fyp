from Utils.Database import Database
from Model.User import User
import boto3

import json


class Project:

    @staticmethod
    def add_dataset_to_project(user_id, info):
        query = f"""
            SELECT
                fh.[FileID],
                fh.[Filepath]
            FROM 
                [MetaData].[metadata].[FileHistory] fh
                INNER JOIN 
                [MetaData].[metadata].[File] f
            ON
                fh.[FileID] = f.[FileID]
            WHERE
                f.[DataSet] = '{info['DatasetId']}'
                AND
                fh.[Change] = 'source'
                AND
                fh.[ProjectID] is NULL
                """
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_query(query, cursor)
        print('------Found files------------')
        bucket = 'fyp-data-repo'
        client = boto3.client('s3')
        for row in results:
            print(f'FileID: {row[0]} - FilePath: {row[1]}')
            file_id = row[0]
            file_path = row[1]
            for project in info['Projects']:
                new_path = f'{project}/project_source/{file_path}'
                response = client.copy_object(
                    Bucket=bucket,
                    CopySource=f'/{bucket}/{file_path}',
                    Key=new_path
                )
                print(response)
                print(f'File {file_id} copied to {new_path} for project {project}')
                query = f"""
                            INSERT INTO 
                                [metadata].[FileHistory]
                                ([FileID]
                                ,[UserID]
                                ,[ProjectID]
                                ,[Change]
                                ,[Filepath]
                                ,[Active]
                                ,[StartDate]
                                ,[EndDate])
                            VALUES
                                ('{file_id}','{user_id}','{project}','project source','{new_path}',1,GETDATE(),NULL)
                        """
                Database.execute_non_query(query, cursor)
                cursor.commit()
                print(f"Slowly changing dimension insertion: ('{file_id}','{user_id}','{project}','project source','{new_path}',1,GETDATE(),NULL)")
        conn.close()
        return {'Status': 200, 'Message': 'Dataset added to projects'}

    @staticmethod
    def get_users_invitations(user_id):
        query = f"""
            SELECT
                p.[ProjectID]
                ,p.[Name]
                ,u.[Email]
            FROM 
                [MetaData].[prj].[Project] p
                INNER JOIN
                [MetaData].[usr].[User] u
            ON
                p.[Creator] = u.[UserID]
                LEFT JOIN
                [MetaData].[prj].[ProjectMember] pm
            ON
                p.[ProjectID] = pm.[ProjectID]
            WHERE
                pm.[Pending] = 1
                AND
                pm.[UserID] = '{user_id}'
                """
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_query(query, cursor)
        projects = []
        for row in results:
            project = Project()
            project.set_project_id(row[0])
            project.set_name(row[1])
            project.set_creator(row[2])
            projects.append(project.project)
        conn.close()
        response = {'Projects': projects}
        return json.dumps(response)

    @staticmethod
    def get_users_projects(user_id):
        query = f"""
            SELECT
                p.[ProjectID]
                ,p.[Name]
                ,p.[Desc]
                ,u.[Email]
                ,p.[StartDate]
                ,p.[EndDate]
                ,p.[Public]
            FROM 
                [MetaData].[prj].[Project] p
                INNER JOIN
                [MetaData].[usr].[User] u
            ON
                p.[Creator] = u.[UserID]
                LEFT JOIN
                [MetaData].[prj].[ProjectMember] pm
            ON
                p.[ProjectID] = pm.[ProjectID]
            WHERE
                pm.[Pending] = 0
                AND
                pm.[UserID] = '{user_id}'
                OR
                p.[Creator] = '{user_id}'
            """
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_query(query, cursor)
        projects = []
        for row in results:
            project = Project()
            project.set_project_id(row[0])
            project.set_name(row[1])
            project.set_desc(row[2])
            project.set_creator(row[3])
            project.set_start_date(row[4])
            project.set_end_date(row[5])
            project.set_public(row[6])
            query = f"""
                    SELECT
                        u.[Email],
                        pm.[Pending]
                    FROM
                        [MetaData].[prj].[ProjectMember] pm	
                        INNER JOIN
                        [MetaData].[usr].[User] u
                    ON
                        pm.[UserId] = u.[UserID]
                    WHERE
                        [ProjectID] = '{project.get_project_id()}'
                    """
            cursor = conn.cursor()
            results = Database.execute_query(query, cursor)
            members = []
            for member_row in results:
                user_id = User.get_user_from_email(member_row[0])
                user = User.get_user_info(user_id)
                user.user['pending'] = member_row[1]
                members.append(user.user)
            project.set_project_members(members)
            projects.append(project.project)
        conn.close()
        response = {'Projects': projects}
        return json.dumps(response)

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

        if user_id is not None:
            project_id = project_info['ProjectId']
            params = (user_id, project_id)
            conn = Database.connect()
            cursor = conn.cursor()
            results = Database.execute_sproc(query, params, cursor)
            if results['Status'] == 201:
                cursor.commit()
            conn.close()
        else:
            results = {'Status': 404, 'Message': 'This email does not have a registered account'}
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
        if results['Status'] == 200:
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

    @staticmethod
    def make_public_or_private(project_id, mode):
        query = f"""
                UPDATE
                    [prj].[project]
                SET
                    [public] = {mode}
                WHERE
                    [ProjectId] = '{project_id}'
                """
        conn = Database.connect()
        cursor = conn.cursor()
        Database.execute_non_query(query, cursor)
        cursor.commit()
        conn.close()
        if mode == '1':
            message = 'Project now public'
        else:
            message = 'Project now private'

        return{'Status': 200, 'Message': message}

    def __init__(self):
        self.project = {}

    def set_project_id(self, project_id):
        self.project['ProjectId'] = project_id
        return self

    def get_project_id(self):
        return self.project['ProjectId']

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
        self.project['StartDate'] = str(start_date)
        return self

    def get_start_date(self):
        return self.project['StartDate']

    def set_end_date(self, end_date):
        self.project['EndDate'] = str(end_date)
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
