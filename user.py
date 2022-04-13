
from flask import redirect, render_template
import psycopg2 
import psycopg2.extras
from datetime import date
import uuid

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


def db_to_login(user_email, user_password):
    
    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("SELECT email, password, id, f_name FROM \"profile\" where email = %s and password = %s", (user_email, user_password))
    records = cursor.fetchall()
    
    if records == []:
        print("Användaren finns ej")
        close_db_omsa(connection)
        return redirect("/login") 
    else:   
        print("Lyckades")
        close_db_omsa(connection) 
        return records

def create_user_in_db(user_name, user_password, user_email, user_f_name, user_l_name, user_adress, user_zip_code, city, user_phone_number):
    '''
    Skapar en post i databasen med användinformationen 
    '''
    psycopg2.extras.register_uuid()
    connection = open_db_omsa()

    user_id = uuid.uuid4()

    cursor = connection.cursor()
    cursor.execute("""
    insert into profile (id, user_name, password, email, f_name, l_name, adress, zip_code, city_id, phone_number)
    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """,(user_id, user_name, user_password, user_email, user_f_name, user_l_name, user_adress, user_zip_code, city, user_phone_number))

    cursor.close()
    connection.commit()
    close_db_omsa(connection)
          
