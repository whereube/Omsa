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

def trade_proposals(user_id):
    '''
    Hämtar alla bytesförslag där användaren där antingen husband eller wife article_id är kopplat till användaren
    '''

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
    left outer join city as wife_city on wife_article.city_id = wife_city.id
    left outer join city as husband_city on husband_article.city_id = husband_city.id
    where (transaction.wife_complete is null or transaction.husband_complete is null)
    and (transaction.denied is null or transaction.denied = FALSE)
    and (wife.id = %s or husband.id = %s or husband_handshake.id = %s)
    order by transaction.date_proposed desc
    """, (user_id, user_id, user_id,)) 
    records = cursor.fetchall()
    cursor.close()
    close_db_omsa(connection)
    return records


def show_interest(wife_article_id, husband_article_id):
    '''
    lägger till wife_article_id, husband_article_id, date_proposed och husband_id i database vid visat intresse
    '''
    psycopg2.extras.register_uuid()
    connection = open_db_omsa()
    cursor = connection.cursor()
    date_proposed = datetime.now()
    husband_id = session.get("USER_ID")

    cursor.execute("""
    insert into transaction (id, wife_article_id, husband_article_id, date_proposed, husband_id)
    values(%s, %s, %s, %s, %s)
    """,(uuid.uuid4(), wife_article_id, husband_article_id, date_proposed, husband_id))

    cursor.close()
    connection.commit()
    close_db_omsa(connection)

def show_interest_handshake(wife_article_id):
    '''
    lägger till wife_article_id date_proposed och husband_id i database vid visat intresse
    '''
    psycopg2.extras.register_uuid()
    connection = open_db_omsa()
    cursor = connection.cursor()
    date_proposed = datetime.now()
    husband_id = session.get("USER_ID")

    cursor.execute("""
    insert into transaction (id, wife_article_id, date_proposed, handshake_proposed, husband_id)
    values(%s, %s, %s, True, %s)
    """,(uuid.uuid4(), wife_article_id, date_proposed, husband_id))
    
    cursor.close()
    connection.commit()
    close_db_omsa(connection)


def save_interest_to_db(transaction_id):
    '''
    Uppdaterar transactions.denied med värdet false
    args:
        transaction_id: ID till transactionsposten
    '''

    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    update transaction
    set denied = False
    where transaction.id = %s
    """,(transaction_id,))

    cursor.close()
    connection.commit()
    close_db_omsa(connection)


def remove_interest_from_db(transaction_id):
    '''
    Tar bort en artikel från databasen
    '''
    connection = open_db_omsa()
    cursor = connection.cursor()

    cursor.execute("""
    delete from transaction
    where transaction.id = %s
    """,(transaction_id,))

    cursor.close()
    connection.commit()
    close_db_omsa(connection)

def save_wife_confirmed_to_db(transaction_id):
    '''
    Uppdaterar transactions.wife_complete med värdet True
    args:
        transaction_id: ID till transactionsposten
    '''

    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    update transaction
    set wife_complete = True
    where transaction.id = %s
    """,(transaction_id,))

    cursor.close()
    connection.commit()
    close_db_omsa(connection)

def husband_wife_confirmed_to_db(transaction_id):
    '''
    Uppdaterar transactions.husband_complete med värdet True
    args:
        transaction_id: ID till transactionsposten
    '''

    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    update transaction
    set husband_complete = True
    where transaction.id = %s
    """,(transaction_id,))

    cursor.close()
    connection.commit()
    close_db_omsa(connection)


def save_date_completed_to_db(transaction_id, date_complete):
    '''
    Uppdaterar transactions.date_completed
    args:
        transaction_id: ID till transactionsposten
        date_complete: Datum nu
    '''

    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    update transaction
    set date_completed = %s
    where transaction.id = %s
    """,(date_complete, transaction_id,))

    cursor.close()
    connection.commit()
    close_db_omsa(connection)