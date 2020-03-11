import pyodbc


class Database:

    @staticmethod
    def connect():
        conn = pyodbc.connect(
                'Driver={ODBC Driver 17 for SQL Server};'
                'Server=secretsasquatchsociety.chefvdjywstx.eu-west-2.rds.amazonaws.com,1433;'
                'Database=MetaData;'
                'uid=admin;'
                'pwd=letsusefirebase;')
        return conn

    @staticmethod
    def execute_sproc(sproc, params, cursor):
        query = f"""
            DECLARE @return_value int, @out nvarchar(max);
            EXEC    @return_value = {sproc}, 
                    @responseMessage = @out OUTPUT;
            SELECT @return_value AS return_value, @out AS the_output;         
            """
        cursor.execute(query, params)
        results = cursor.fetchall()
        return {'Status': results[0][0], 'Message': results[0][1]}

    @staticmethod
    def execute_query(query, cursor):
        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def execute_non_query(query, cursor):
        cursor.execute(query)

