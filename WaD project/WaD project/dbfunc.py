# Student ID - 2400965 , Student name - Harry Masters 
import mysql.connector
from mysql.connector import errorcode

hostname = "localhost"
username = "root"
passwd = "003150"
db = "travel"

def getConnection():    
    try:
        conn = mysql.connector.connect(
            host=hostname,
            user=username,
            password=passwd,
            database=db
        )
        return conn  # Moved this line up to avoid reaching the end without a return
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('User name or Password is not working')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist')
        else:
            print(err)
