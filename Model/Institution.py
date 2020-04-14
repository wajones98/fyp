from Utils.Database import Database
from Model.User import User


class Institution:

    @staticmethod
    def get_institution(institution_id):
        query = f"""
                SELECT TOP 1
                    [InstitutionID]
                    ,[Name]
                    ,[Desc]
                    ,[Owner]
                FROM 
                    [MetaData].[usr].[Institution]
                WHERE
                    [InstitutionID] = '{institution_id}'
                """
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_query(query, cursor)
        if len(results) > 0:
            institution = Institution()
            institution.set_institution_id(results[0][0])
            institution.set_name(results[0][1])
            institution.set_desc(results[0][2])
            institution.set_owner(results[0][3])
            query = f"""
                    SELECT
                        [UserId]
                        ,[Role]
                        ,[Pending]
                    FROM 
                        [MetaData].[usr].[InstitutionMember]
                    WHERE 
                        [InstitutionID] = '{institution_id}'
                    """
            results = Database.execute_query(query, cursor)
            if len(results) > 0:
                members = []
                for row in results:
                    member = User.get_user_info(row[0])
                    member.set_institution_role(row[1])
                    if row[2] == 0:
                        is_pending = False
                    else:
                        is_pending = True
                    member.set_institution_pending(is_pending)
                    members.append(member)
                institution.set_members(members)
        conn.close()
        return institution

    @staticmethod
    def create_institution(institution_model):
        query = f"""
                [usr].[CreateInstitution] @Name = ?, @Desc = ?, @Owner = ?
                """
        params = (institution_model.get_name(), institution_model.get_desc(), institution_model.get_owner())
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_sproc(query, params, cursor)
        if results['Status'] == 201:
            cursor.commit()
        conn.close()
        return results

    @staticmethod
    def get_all_pending(user_id):
        query = f"""
                SELECT
                    [InstitutionId]
                FROM
                    [usr].[InstitutionMember]
                WHERE
                    [UserId] = '{user_id}'
                    AND
                    [Pending] = 1
                """
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_query(query, cursor)
        conn.close()
        pending_invites = []
        for row in results:
            pending_invites.append(row[0])
        return pending_invites

    @staticmethod
    def accept_pending_invite(user_id, institution_id):
        pending = Institution.get_all_pending(user_id)
        if institution_id in pending:
            query = f"""
                    [usr].[AcceptInstitutionInvite] ?, ?
                    """
            params = (user_id, institution_id)
            conn = Database.connect()
            cursor = conn.cursor()
            results = Database.execute_sproc(query, params, cursor)
            if results['Status'] == 201:
                cursor.commit()
            conn.close()
            return results
        return {'Status': 400, 'Message': 'This institution has not invited this user'}

    @staticmethod
    def invite_member(user_id, invitation_info):
        user = User.get_user_info(user_id)
        if user.get_institution() is not None:
            invited_user_id = User.get_user_from_email(invitation_info['Email'])
            if invited_user_id is not None:
                if user.get_institution() not in Institution.get_all_pending(invited_user_id):
                    query = f"""
                                [usr].[InviteUserToInstitution] ?, ?, ?
                            """
                    params = (invited_user_id, user.get_institution(), invitation_info['Role'])
                    conn = Database.connect()
                    cursor = conn.cursor()
                    results = Database.execute_sproc(query, params, cursor)
                    if results['Status'] == 201:
                        cursor.commit()
                    conn.close()
                    return results
                else:
                    return {'Status': 400, 'Message': 'This account has already been invited'}
            else:
                return {'Status': 400, 'Message': 'There is no account associated with this email'}
        else:
            return {'Status': 400, 'Message': 'User not part of institution'}

    @staticmethod
    def remove_member(user_id, email):
        user = User.get_user_info(user_id)
        if user.get_institution() is not None:
            institution = Institution.get_institution(user.get_institution())
            if institution.get_owner() == user_id:
                remove_user_id = User.get_user_from_email(email)
                if remove_user_id is not None:
                    query = f"""
                            [usr].[RemoveUserFromInstitution] ?, ?
                            """
                    params = (remove_user_id, user.get_institution())
                    conn = Database.connect()
                    cursor = conn.cursor()
                    results = Database.execute_sproc(query, params, cursor)
                    if results['Status'] == 200:
                        cursor.commit()
                    conn.close()
                    return results
                else:
                    return {'Status': 400, 'Message': 'There is no account associated with this email'}
            else:
                return {'Status': 400, 'Message': 'User is not owner of institution'}
        else:
            return {'Status': 400, 'Message': 'User not part of institution'}

    @staticmethod
    def member_leave(user_id):
        user = User.get_user_info(user_id)
        if user.get_institution() is not None:
            query = f"""
                        [usr].[RemoveUserFromInstitution] ?, ?
                    """
            params = (user_id, user.get_institution())
            conn = Database.connect()
            cursor = conn.cursor()
            results = Database.execute_sproc(query, params, cursor)
            if results['Status'] == 200:
                cursor.commit()
            conn.close()
            return results
        else:
            return {'Status': 400, 'Message': 'User not part of institution'}

    def __init__(self):
        self.institution_id = None
        self.institution = {}

    def set_institution_id(self, institution_id):
        self.institution_id = institution_id
        return self

    def get_institution_id(self):
        return self.institution_id

    def set_name(self, name):
        self.institution['Name'] = name
        return self

    def get_name(self):
        return self.institution['Name']

    def set_desc(self, desc):
        self.institution['Desc'] = desc

    def get_desc(self):
        return self.institution['Desc']

    def set_owner(self, owner):
        self.institution['Owner'] = owner

    def get_owner(self):
        return self.institution['Owner']

    def set_members(self, members):
        self.institution['Members'] = members
        return self

    def get_members(self):
        return self.institution['Members']
