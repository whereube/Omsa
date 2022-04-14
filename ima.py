import psycopg2
import psycopg2.extras
from datetime import date, datetime
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


def trade_proposals (user_id):
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
    where (transaction.wife_complete is null or transaction.wife_complete = FALSE)
    and (transaction.denied is null or transaction.denied = FALSE)
    and (wife.id = %s or husband.id = %s or husband_handshake.id = %s)
    """, (user_id, user_id, user_id,)) 
    records = cursor.fetchall()
    cursor.close()
    close_db_omsa(connection)
    return records
