import pymysql
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='shopeasy'
)

print("Database Connected Successfully")