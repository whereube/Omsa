import psycopg2
import psycopg2.extras
from datetime import date, datetime
import uuid
psycopg2.extras.register_uuid()

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

def create_article_in_db(title, description, zip_code, tier, city, category, user_id, filename, sub_category):
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
    create_article_category_in_db(article_id, sub_category)
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
    where (category.level = 1 or 
    not exists
        (select * from article_category
        where article_category.article_id = article_id))
    order by article.create_date desc
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
    and (category.level = 1 or
    not exists
    (select * from article_category
    where article_category.article_id = article_id))
    order by article.create_date desc
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
    and (category.level = 1 or
    not exists
    (select * from article_category
    where article_category.article_id = article_id))
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
    search_term_like1 = (search_term + '%')
    search_term_like2 = ('%' + search_term)
    search_term_like3 = ('%' + search_term + '%')
    cursor.execute( '''
    select * from article
    left outer join profile on article.user_id = profile.id
    left outer join city on article.city_id = city.id
    left outer join tier on article.tier_id = tier.id
    left outer join article_category on article.id = article_category.article_id
    left outer join category on article_category.category_id = category.id
    where (LOWER(title) like %s or LOWER(title) like %s or LOWER(title) like %s or LOWER(title) like %s)
    and (category.level = 1 or
    not exists
    (select * from article_category
    where article_category.article_id = article_id))
    order by article.create_date desc
    ''', (search_term.lower(), search_term_like1.lower(), search_term_like2.lower(), search_term_like3.lower(),))
    records = cursor.fetchall()
    cursor.close()
    close_db_omsa(connection)
    return records

def get_article_by_category(main_category_id, sub_category_1_id):
    '''
    Hämtar alla artiklar vars titel innehåller en term
    args:
        main_category_id: Artiklar som visas har kateogori_idt
    '''
    connection = open_db_omsa()
    cursor = connection.cursor()

    if sub_category_1_id == None or sub_category_1_id == '':
        cursor.execute( '''
        select * from article
        left outer join profile on article.user_id = profile.id
        left outer join city on article.city_id = city.id
        left outer join tier on article.tier_id = tier.id
        left outer join article_category on article.id = article_category.article_id
        left outer join category on article_category.category_id = category.id
        where category.id = %s
        and (category.level = 1 or 
        not exists
        (select * from article_category
        where article_category.article_id = article_id))
        order by article.create_date desc
        ''', (main_category_id,))
        records = cursor.fetchall()
        cursor.close()
        close_db_omsa(connection)
        return records
    elif sub_category_1_id != None and sub_category_1_id != '':
        cursor.execute( '''
        select * from article
        left outer join profile on article.user_id = profile.id
        left outer join city on article.city_id = city.id
        left outer join tier on article.tier_id = tier.id
        left outer join article_category on article.id = article_category.article_id
        left outer join category on article_category.category_id = category.id
        where exists 
        (select * from article_category
        where category_id = %s
        and article_category.article_id = article.id)
        and exists 
        (select * from article_category
        where category_id = %s
        and article_category.article_id = article.id)
        and (category.level = 1 or 
        not exists
        (select * from article_category
        where article_category.article_id = article_id))
        order by article.create_date desc
        ''', (main_category_id, sub_category_1_id,))
        records = cursor.fetchall()
        cursor.close()
        close_db_omsa(connection)
        return records



def get_article_by_title_and_cateogry(search_term, category_id, sub_category_1_id):
    '''
    Hämtar alla artiklar vars titel innehåller en term
    args:
        search_term: Artiklar som visas innehåller termen
    '''
    connection = open_db_omsa()
    cursor = connection.cursor()
    search_term_like1 = (search_term + '%')
    search_term_like2 = ('%' + search_term)
    search_term_like3 = ('%' + search_term + '%')

    if sub_category_1_id == None or sub_category_1_id == '':
        cursor.execute( '''
        select * from article
        left outer join profile on article.user_id = profile.id
        left outer join city on article.city_id = city.id
        left outer join tier on article.tier_id = tier.id
        left outer join article_category on article.id = article_category.article_id
        left outer join category on article_category.category_id = category.id
        where (LOWER(title) like %s or LOWER(title) like %s or LOWER(title) like %s or LOWER(title) like %s) and category.id = %s
        and (category.level = 1 or
        not exists
        (select * from article_category
        where article_category.article_id = article_id))
        order by article.create_date desc
        ''', (search_term.lower(), search_term_like1.lower(), search_term_like2.lower(), search_term_like3.lower(), category_id,))
        records = cursor.fetchall()
        cursor.close()
        close_db_omsa(connection)
        return records
    elif sub_category_1_id != None and sub_category_1_id != '':
        cursor.execute( '''
        select * from article
        left outer join profile on article.user_id = profile.id
        left outer join city on article.city_id = city.id
        left outer join tier on article.tier_id = tier.id
        left outer join article_category on article.id = article_category.article_id
        left outer join category on article_category.category_id = category.id
        where (LOWER(title) like %s or LOWER(title) like %s or LOWER(title) like %s or LOWER(title) like %s)
        and exists 
        (select * from article_category
        where category_id = %s
        and article_category.article_id = article.id)
        and exists 
        (select * from article_category
        where category_id = %s
        and article_category.article_id = article.id)
        and (category.level = 1 or
        not exists
        (select * from article_category
        where article_category.article_id = article_id))
        order by article.create_date desc
        ''', (search_term.lower(), search_term_like1.lower(), search_term_like2.lower(), search_term_like3.lower(), category_id, sub_category_1_id,))
        records = cursor.fetchall()
        cursor.close()
        close_db_omsa(connection)
        return records

def get_sub_category_1_by_main(main_category_type):
    '''
    Hämtar alla kategorier
    '''
    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    select * from category
    where level = '2' and category.category_type = %s
    """, (main_category_type,))
    records = cursor.fetchall()
    cursor.close()
    close_db_omsa(connection)
    return records

def get_main_category_type(cateogry_id):
    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    select category_type from category
    where category.id = %s
    """, (cateogry_id,))
    records = cursor.fetchall()
    cursor.close()
    close_db_omsa(connection)
    return records

def edit_to_article(title, description, zip_code, tier, edit, city, article_id):
    connection = open_db_omsa()
    print(city)
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE article 
    set title = %s, description = %s, city_id = %s, tier_id = %s, edit_date = %s, zip_code = %s
    where article.id = %s
    """,(title, description, city, tier, edit, zip_code, article_id,))
    
    cursor.close()
    connection.commit()
    close_db_omsa(connection)

def edit_article_catergory(category_id, article_category_id):
    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    Update article_category
    set category_id = %s
    where id = %s 
    """,(category_id, article_category_id, ))

    cursor.close()
    connection.commit()
    close_db_omsa(connection)

def get_completed_transactions(user_id):
    '''
    Hämtar alla artiklar som har användarens user_id och som är del av en genomförd transaktion
    args:
        user_id: Användarens id
    '''
    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    select * from transaction
    left outer join article as wife_article on transaction.wife_article_id = wife_article.id
    left outer join article as husband_article on transaction.husband_article_id = husband_article.id
    left outer join profile as wife on wife_article.user_id = wife.id
    left outer join profile as husband on husband_article.user_id = husband.id
    left outer join profile as husband_handshake on transaction.husband_id = husband_handshake.id
    where wife_complete = True 
    and husband_complete = true
    and (wife_article.user_id = %s
    or husband_article.user_id = %s
    or husband_id = %s)
    order by transaction.date_completed desc
    """, (user_id, user_id, user_id,))
    records = cursor.fetchall()
    cursor.close()
    close_db_omsa(connection)
    return records

def transaction_delete(transaction_id):
    connection = open_db_omsa()

    cursor = connection.cursor()
    cursor.execute("""
    delete from transaction
    where transaction.id = %s
    """,(transaction_id,))

    cursor.close()
    connection.commit()
    close_db_omsa(connection)
