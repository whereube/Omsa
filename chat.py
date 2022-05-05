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

def get_chat_messages(chat_id):
    connection = open_db_omsa()
    cursor = connection.cursor()
    cursor.execute("""
    select message.id, message.chat_id, message.user_id, message.text, message.time_sent, profile.user_name 
    inner join profile on message.user_id = profile.id
    where chat_id = %s 
    order by time_sent desc
    """,(chat_id,))

    records = cursor.fetchall()
    cursor.close()
    close_db_omsa(connection)
    return records


def chat_message_to_db(user_message):
    psycopg2.extras.register_uuid()
    user_id = session.get('USER_ID')

    get_chat_id_from_db = get_chat_id(user_id)
    for row in get_chat_id_from_db:
        chat_id = row[0]
    time_now = datetime.now()
    message_id = uuid.uuid4()
    connection = open_db_omsa()
    
    cursor = connection.cursor()
    cursor.execute("""
    insert into message (id, chat_id, user_id, text, time_sent)
    values (%s, %s, %s, %s, %s)
    """,(message_id, chat_id, user_id, user_message, time_now))

    cursor.close()
    connection.commit()
    close_db_omsa(connection)