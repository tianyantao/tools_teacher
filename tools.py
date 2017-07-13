import pymssql


def db_connect(host = 233, database = 'ETeacher'):
    if host == 233:
        if database == 'ETeacher':
            conn = pymssql.connect(host='sqlserver.233.mistong.com', user='ETeacher', password='ETeacher', database='ETeacher')
            cur = conn.cursor()
            return cur
        else:
            conn = pymssql.connect(host='sqlserver.233.mistong.com', user='CeShi', password='28c5be9426611a12', database=database)
            cur = conn.cursor()
            return cur
    if host == 64:
        conn = pymssql.connect(host='10.0.0.64', user='ewt360', password='ewt360@123',
                               database=database)
        cur = conn.cursor()
        return cur
        


