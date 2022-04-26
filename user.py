
from flask import redirect, render_template, flash
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
        close_db_omsa(connection)
        return False
    else:   
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
          
def show_linked_users(user_id):
    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    select *,
    case
    when transaction.husband_article_id is null and handshake_proposed = TRUE
    then husband_handshake.id
    else null
    end Handshake_husband
    from transaction
    left outer join article as wife_article on transaction.wife_article_id = wife_article.id
    left outer join article as husband_article on transaction.husband_article_id = husband_article.id
    left outer join profile as wife on wife_article.user_id = wife.id
    left outer join profile as husband on husband_article.user_id = husband.id
    left outer join profile as husband_handshake on transaction.husband_id = husband_handshake.id
    left outer join city as husband_city on husband_article.city_id = husband_city.id
    where (transaction.denied = FALSE)
    and (wife.id = %s or husband.id = %s or husband_handshake.id = %s)
    """, (user_id, user_id, user_id,)) 
    records = cursor.fetchall()
    cursor.close()
    for row in records:
        print(row)
    close_db_omsa(connection)
    return records
