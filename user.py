
from flask import redirect, render_template
import psycopg2 
import psycopg2.extras
from datetime import date
import uuid

current_date = date.today()

def open_db_online_store():
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

def close_db_online_store(connection):
    connection.close()

def db_to_login(user_email, user_password):
    
    connection = open_db_online_store()

    cursor = connection.cursor()
    cursor.execute("SELECT email, password, id, f_name FROM \"profile\" where email = %s and password = %s", (user_email, user_password))
    records = cursor.fetchall()
    
    
    if records == []:
        print("Användaren finns ej")
        close_db_online_store(connection)
        return render_template("login.html")
    else:   
        print("Lyckades")
        return records
        
    close_db_online_store(connection) 
    