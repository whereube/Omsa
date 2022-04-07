
import psycopg2 
from datetime import date

def open_db_omsa():
    try:
        connection = psycopg2.connect(
            user = 'am6110',
            password = 'y4dpegsc', 
            host = 'pgserver.mau.se',
            port = '5432',
            database = 'am6110'
            )
        return connection
    except: 
        print("Databasen finns inte!")

def close_db_omsa(connection):
    connection.close()

def login(user_email, user_password):
    
    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("SELECT email, password FROM \"profile\" where email = %s and password = %s", (user_email, user_password))
    records = cursor.fetchall()
    

    if records == []:
        print(records)
        print(user_email)
        print(user_password)
    else:    
        return 1

    close_db_omsa(connection)
                
                
