from Utils.Database import Database


class Upload:
    def __init__(self, user_id, content, dataset_id):
        self.user_id = user_id
        self.file_id = None
        self.signal_type = content['SignalType']
        self.species = content['Species']
        self.gender = content['Gender']
        self.age = content['Age']
        self.target = content['Target']
        self.action = content['Action']
        self.dataset_id = dataset_id
        self.tags = content['Tags']

    def upload_file_metadata(self):
        query = f"""
                [metadata].[InsertFileMetaData] ?,?,?,?,?,?,?,?
                """
        params = (self.user_id, self.signal_type, self.species, self.gender,
                  self.age, self.target, self.action, self.dataset_id)
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_sproc(query, params, cursor)
        if results[0][0] is not 'Failure':
            self.file_id = results[0][0]
            for key in self.tags.keys():
                Database.execute_non_query(self.upload_tags(key), cursor)
            cursor.commit()
            response = {"Status": 200, "file_id": self.file_id}
        else:
            cursor.rollback()
            response = {"Response": 500}
        conn.close()
        return response

    @staticmethod
    def generate_dataset_id(dataset_name):
        query = f"""
                [metadata].[InsertDataset] ?
                """
        params = dataset_name
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_sproc(query, params, cursor)
        if results[0][0] is not 'Failure':
            cursor.commit()
            response = {"Status": 200, "DatasetID": results[0][0]}
        else:
            response = {"Status": 500, "Error": results[0][0]}
        conn.close()
        return response

    def upload_tags(self, key):
        query = f"""
                INSERT INTO
                    [metadata].[Tag]
                    ([FileID],[TagKey],[TagValue])
                VALUES
                    ('{self.file_id}','{key}','{self.tags[key]}')
                """
        return query

    @staticmethod
    def update_init_file_path(file_id, file_path):
        query = f"""
                UPDATE 
                    [metadata].[FileHistory]
                SET
                    [FilePath] = '{file_path}'
                WHERE
                    [FileID] = '{file_id}'
                """
        conn = Database.connect()
        cursor = conn.cursor()
        Database.execute_non_query(query, cursor)
        cursor.commit()
        conn.close()