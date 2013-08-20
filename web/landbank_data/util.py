# Utilities for various web project tasks

# Turns a sql query resultset into a python dict
def sqltodict(query,param):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute(query,param)
    fieldnames = [name[0] for name in cursor.description]
    result = []
    for row in cursor.fetchall():
        rowset = []
        for field in zip(fieldnames, row):
            rowset.append(field)
        result.append(dict(rowset))
    return result

