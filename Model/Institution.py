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
        if results.size > 0:
            institution = Institution()
            institution.set_institution_id(results[0][0])
            institution.set_name(results[0][1])
            institution.set_desc(results[0][2])
            institution.set_owner(results[0][3])
            query = f"""
                    SELECT
                        [UserId]
                        ,[Role]
                    FROM 
                        [MetaData].[usr].[InstitutionMember]
                    WHERE 
                        [InstitutionID] = '{institution_id}'
                    """
            results = Database.execute_query(query, cursor)
            if results.size > 0:
                members = []
                for row in results:
                    member = User.get_user_info(row[0])
                    member.set_institution_role(row[1])
                    members.append(member)
                institution.set_members(members)
        conn.close()

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
        self.institution['Owner']

    def set_members(self, members):
        self.institution['Members'] = members
        return self

    def get_members(self):
        return self.institution['Members']
