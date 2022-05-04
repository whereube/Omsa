import psycopg2
import psycopg2.extras
from datetime import date, datetime
import uuid
from flask import session

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

def create_chat_id(husband_id, wife_id):
    '''
    Skapar ett id i databasen "chat" kopplat till husband och wife.
    '''
    psycopg2.extras.register_uuid()
    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    insert into chat (id, husband_id, wife_id)
    values (%s, %s, %s)
    """,(uuid.uuid4(), husband_id, wife_id))

    cursor.close()
    connection.commit()
    close_db_omsa(connection)

def get_chat_id(user_id):
    user_id = session.get('USER_ID')
    connection = open_db_omsa()
    cursor = connection.cursor()
    cursor.execute("""
    select * from chat 
    left outer join profile as husband on chat.husband_id = husband.id
    left outer join profile as wife on chat.wife_id = wife.id
    where (husband_id = %s or wife_id = %s)  
    """,(user_id, user_id,))

    records = cursor.fetchall()
    cursor.close()
    close_db_omsa(connection)
    return records

def get_chat_messages():
    print("hej")


def send_chat_messages():
    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    insert into (id, husband_id, wife_id)
    values (%s, %s, %s)
    """,())

    cursor.close()
    connection.commit()
    close_db_omsa(connection)