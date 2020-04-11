

class QueryBuilder:

    def __init__(self, limit):
        if limit > 0:
            self.query = f'SELECT TOP {limit}'
        else:
            self.query = 'SELECT'
        self.columns = ''
        self.table = ''
        self.joins = ''

    def query_columns(self, columns):
        if self.columns != '':
            self.columns = f' {self.columns},'
        for column in columns:
            self.columns = self.columns + f' [{column}],'
        self.columns = self.columns[0:-1]

    def table_from(self, table):
        self.table = f' FROM [MetaData].[metadata].[{table}]'

