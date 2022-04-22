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

def create_article_in_db(title, description, zip_code, tier, city, category, user_id, filename):
    '''
    Skapar en post i databasen med artikelinformationen
    '''
    psycopg2.extras.register_uuid()
    connection = open_db_omsa()

    article_id = uuid.uuid4()

    cursor = connection.cursor()
    cursor.execute("""
    insert into article (id, title, description, zip_code, create_date, tier_id, city_id, user_id)
    values(%s, %s, %s, %s, %s, %s, %s, %s)
    """,(article_id,title, description, zip_code, datetime.now(), tier, city, user_id,))

    cursor.close()
    connection.commit()
    close_db_omsa(connection)

    create_article_category_in_db(article_id, category)
    if filename != '':
        create_file_path_in_db(article_id, filename)

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
    delete from transaction
    where (wife_article_id = %s or husband_article_id = %s)
    """,(article, article))

    cursor.execute("""
    delete from article 
    where id = %s
    """,(article,))

    cursor.close()
    connection.commit()
    close_db_omsa(connection)

def create_file_path_in_db(article_id, filename):
    '''
    Skapar en post i databasen med artikelinformationen
    '''
    psycopg2.extras.register_uuid()
    connection = open_db_omsa()

    id = uuid.uuid4()

    cursor = connection.cursor()
    cursor.execute("""
    insert into article_image (id, article_id, file_name)
    values(%s, %s, %s)
    """,(id, article_id, filename,))

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

def get_sub_category_1():
    '''
    Hämtar alla kategorier
    '''
    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    select * from category
    where level = '2'
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

def get_article_images():
    '''
    Hämtar alla artikel bilder
    '''
    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    select * from article_image
    """)
    records = cursor.fetchall()
    cursor.close()
    close_db_omsa(connection)
    return records

def get_user_articles(user_id):
    '''
    Hämtar alla artiklar som har användarens user_id
    args:
        user_id: Användarens id
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
    where article.user_id = %s
    """, (user_id,))
    records = cursor.fetchall()
    cursor.close()
    close_db_omsa(connection)
    return records

def get_article_by_id(article_id):
    '''
    Hämtar artikel med specifikt id
    args:
        article_id: artikelns id
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
    where article.id = %s
    """, (article_id,))
    records = cursor.fetchall()
    cursor.close()
    close_db_omsa(connection)
    return records


def get_article_by_title(search_term):
    '''
    Hämtar alla artiklar vars titel innehåller en term
    args:
        search_term: Artiklar som visas innehåller termen
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
    where (title like %s)
    """, (search_term,))
    records = cursor.fetchall()
    cursor.close()
    close_db_omsa(connection)
    return records