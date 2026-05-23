import mysql.connector

def get_database_connection():

    connection = mysql.connector.connect(
        host="sql12.freesqldatabase.com",
        user="sql12828003",
        password="5LYVAU99sm",
        database="sql12828003",
        port=3306
    )

    return connection