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
                
     
def create_article_in_db(title, description, zip_code, tier, city, category):
    '''
    Skapar en post i databasen med artikelinformationen
    '''
    psycopg2.extras.register_uuid()
    connection = open_db_omsa()

    article_id = uuid.uuid4()

    cursor = connection.cursor()
    cursor.execute("""
    insert into article (id, title, description, zip_code, create_date, tier_id, city_id)
    values(%s, %s, %s, %s, %s, %s, %s)
    """,(article_id,title, description, zip_code, datetime.now(), tier, city,))

    cursor.close()
    connection.commit()
    close_db_omsa(connection)

    create_article_category_in_db(article_id, category)

def create_article_category_in_db(article_id, category):
    '''
    Skapar en post i databasen med artikelkategorin
    '''
    psycopg2.extras.register_uuid()
    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    insert into article_category (id, article_id, category_id)
    values(%s, %s, %s)
    """,(uuid.uuid4(), article_id, category,))

    cursor.close()
    connection.commit()
    close_db_omsa(connection)

def remove_article_from_db(article):
    '''
    Tar bort en artikel från databasen
    '''
    connection = open_db_omsa()
    cursor = connection.cursor()

    cursor.execute("""
    delete from article_category
    where article_id = %s
    """,(article,))

    cursor.execute("""
    delete from article 
    where id = %s
    """,(article,))

    cursor.close()
    connection.commit()
    close_db_omsa(connection)



def get_tier():
    '''
    Hämtar alla tiers
    '''
    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    select * from tier
    """)
    records = cursor.fetchall()
    cursor.close()
    close_db_omsa(connection)
    return records

def get_city():
    '''
    Hämtar alla städer
    '''
    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    select * from city
    """)
    records = cursor.fetchall()
    cursor.close()
    close_db_omsa(connection)
    return records


def get_main_category():
    '''
    Hämtar alla kategorier
    '''
    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    select * from category
    where level = '1'
    """)
    records = cursor.fetchall()
    cursor.close()
    close_db_omsa(connection)
    return records

def get_articles():
    '''
    Hämtar alla artiklar
    '''
    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    select * from article
    left outer join profile on article.user_id = profile.id
    left outer join city on article.city_id = city.id
    left outer join tier on article.tier_id = tier.id
    left outer join article_category on article.id = article_category.article_id
    left outer join category on article_category.category_id = category.id
    """)
    records = cursor.fetchall()
    cursor.close()
    close_db_omsa(connection)
    return records