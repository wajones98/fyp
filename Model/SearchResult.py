import boto3
from Utils.Database import Database
import json


class Search:

    def __init__(self, request, search_type):
        if search_type is None:
            view = 'Search'
        else:
            view = 'SearchPrivate'

        self.query = f"""
                SELECT
                    s.[FileId]
                    ,s.[Filename]
                    ,s.[DatasetName]
                    ,s.[ProjectName]
                    ,s.[SignalType]
                    ,s.[Species]
                    ,s.[Gender]
                    ,s.[Age]
                    ,s.[Target]
                    ,s.[Action]
                    ,s.[ChannelCount]
                    ,s.[Device]
                    ,s.[Change]
                    ,s.[Filepath]
                    ,s.[DatasetId]
                    ,s.[Previous]
                    ,s.[PreviousChange]
                FROM
                    [metadata].[{view}] s
                """
        self.where_clause = 'WHERE '
        if 'Parameters' in request:
            for key in request['Parameters'].keys():
                val = request['Parameters'].get(key)
                if not isinstance(val, str):
                    self.where_clause = \
                        f"{self.where_clause} s.[{key}] IN ("
                    for item in val:
                        self.where_clause = \
                            f"{self.where_clause}'{item}',"
                    self.where_clause = f"{self.where_clause[0:-1]}) AND "
                else:
                    self.where_clause = \
                        f"{self.where_clause} s.[{key}] = '{val}' AND "
                self.where_clause = self.where_clause[0:-4]
        if 'Tags' in request:
            self.query = f"{self.query} INNER JOIN [metadata].[Tag] t ON s.[DatasetId] = t.[DatasetId] "
            val = request['Tags']
            for key in val.keys():
                self.query_tags(key, val)

    def query_tags(self, key, request):
        if self.where_clause == 'WHERE ':
            self.where_clause = f"{self.where_clause} t.[{key}] IN ("
        else:
            self.where_clause = f"{self.where_clause} AND t.[{key}] IN ("
        for item in request.get(key):
            self.where_clause = f"{self.where_clause}'{item}', "
        self.where_clause = f"{self.where_clause[0:-2]})"

    def execute_search(self):

        if self.where_clause != 'WHERE ':
            self.query = self.query + self.where_clause
        conn = Database.connect()
        cursor = conn.cursor()
        results = Database.execute_query(self.query, cursor)
        all_data = []
        for row in results:
            dataset_id = row[14]
            tag_query = f"""
                    SELECT
                        [TagKey]
                        ,[TagValue]
                    FROM
                        [metadata].[Tag]
                    WHERE
                        [DatasetId] = '{dataset_id}'
                    """
            conn = Database.connect()
            cursor = conn.cursor()
            results = Database.execute_query(tag_query, cursor)
            tags = {}
            for tag in results:
                tags[tag[0]] = tag[1]
            projects = {}
            projects_query = f"""
                                SELECT 
                                    s.[ProjectID]
                                    ,s.[ProjectName]
                                    ,p.[Creator]
                                    ,p.[Desc]
                                    ,p.[StartDate]
                                    ,p.[EndDate]
                                FROM 
                                    [MetaData].[metadata].[Search] s
                                    INNER JOIN
                                    [MetaData].[prj].[Project] p
                                ON
                                    s.[ProjectID] = p.[ProjectId]
                                WHERE
                                    s.[ProjectID] IS NOT NULL
                                    AND
                                    s.[Change] = 'project source'
                                    AND
                                    s.[DatasetID] = '{dataset_id}'
                                    AND
                                    p.[Public] = 1
                                GROUP BY
                                    s.[DatasetId], s.[ProjectId], s.[ProjectName], p.[Creator], p.[Desc], p.[StartDate], p.[EndDate] 
                             """
            conn = Database.connect()
            cursor = conn.cursor()
            results = Database.execute_query(projects_query, cursor)
            for project in results:
                projects[project[0]] = {
                    'Name': project[1],
                    'Creator': project[2],
                    'Desc': project[3],
                    'StartDate': str(project[4]),
                    'EndDate': str(project[5])
                }
            conn.close()
            data = {'FileId': row[0]
                ,'Filename': row[1]
                , 'DatasetName': row[2]
                , 'Projects': projects
                , 'SignalType': row[4]
                , 'Species': row[5]
                , 'Gender': row[6]
                , 'Age': row[7]
                , 'Target': row[8]
                , 'Action': row[9]
                , 'ChannelCount': row[10]
                , 'Device': row[11]
                , 'Change': row[12]
                , 'Filepath': row[13]
                , 'DatasetId': row[14]
                , 'Previous': row[15]
                , 'PreviousChange': row[16]
                ,  'Tags': tags}
            all_data.append(data)
        response = {"Results": all_data}
        return json.dumps(response)

