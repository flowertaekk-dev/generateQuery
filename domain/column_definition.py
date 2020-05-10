#!/usr/bin/python3

import re
from utils import filters

class Column:

    def __init__(self, line_of_query: str, db: dict):
        self.line_of_query = line_of_query
        self.db = db

    # retrieve data type from query
    def get_data_type(self):
        data_type = ''

        splited_by_space = re.split('[\s]', self.line_of_query)

        filtered_types = list(filter(lambda data_type: data_type == splited_by_space[0], self.db))
        filtered_type = filtered_types[0] if len(filtered_types) > 0 else ''

        if filtered_type:
            data_type = self.db.get(filtered_type)
        else:
            raise ValueError('Unexpected data type : {0}'.format(filtered_type))

        return data_type
    
    # retrieve column name from query
    def get_column_name(self):
        return filters.retrieve_column_name(self.line_of_query)
    
    # retrieve constraint from query
    def get_constraint(self):
        return filters.retrieve_constraint(self.line_of_query)

    # retrieve comment from query
    def get_comment(self):
        return filters.retrieve_comment(self.line_of_query)