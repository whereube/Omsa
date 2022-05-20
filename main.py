from cProfile import Profile
import email
import profile
from flask import Flask, redirect, render_template, request, flash, session, g, jsonify
from article import *
from user import *
from ima import *
from chat import *
from werkzeug.utils import secure_filename
import os
from datetime import datetime

UPLOAD_FOLDER = 'static/article_images'

app = Flask(__name__, static_url_path='/static')
app.run(debug=True)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route("/render_chat_list")
def chat_list():
    user_name = session.get('USER_NAME')
    user_id = session.get('USER_ID')
    linked_user = get_chat_id(user_id)

    return render_template("/chat_page.html", linked_user = linked_user, user_name = user_name, user_id = user_id)

@app.route("/message_page/<chat_id>", methods=['GET', 'POST'])
def show_chat_room(chat_id):
    user_id = session.get('USER_ID')
    linked_user = get_chat_id(user_id)
    chat_info = get_chat_messages(chat_id)

    return render_template("/message_page.html", user_id = user_id, chat_id = chat_id, linked_user = linked_user, chat_info = chat_info)

    
@app.route("/send_message", methods=["GET", "POST"])
def handle_messages():
    
    user_message = request.form.get("message")
    chat_id = request.form.get("chat_id")
    chat_message_to_db(user_message, chat_id)

    return redirect(f"/message_page/{chat_id}")




@app.route("/")
def start():
    main_categories = get_main_category()
    images = get_article_images()
    articles = get_articles()
    cities = get_city()
    user_id = session.get('USER_ID')
    return render_template("index.html", main_categories = main_categories, articles = articles, images = images, user_id = user_id, cities = cities)

@app.context_processor
def context_processor():
    current_user_id = session.get('USER_ID')
    return dict(current_user_id = current_user_id)


'''Error pages'''
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

@app.route("/create")
def create_article_form():
    tiers = get_tier()
    citys = get_city()
    categories = get_main_category()
    return render_template("create_article.html", tiers = tiers, citys = citys, categories = categories)

@app.route("/article_created", methods=['GET', 'POST'])
def create_article():
    ''' 
    Hämtar in formuläret för att skapa en artikel och skickar vidare detta för att skapa en post i databasen
    '''
    title = request.form.get("title")
    description = request.form.get("description")
    zip_code = request.form.get("zip_code")
    tier = request.form.get("tier")
    city = request.form.get("city")
    category = request.form.get("main_category")
    sub_category = request.form.get("sub_category")
    user_id = session["USER_ID"]

    file = request.files['file']
    if file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    create_article_in_db(title, description, zip_code, tier, city, category, user_id, file.filename, sub_category)
    return redirect("/")

@app.route("/remove", methods=['GET', 'POST'])
def remove_article_form():
    ''' 
    Hämtar in formuläret för att ta bort en artikel och skickar vidare detta för att ta bort en post i databasen
    '''
    article_id = request.form.get("article_id")
    article_title = request.form.get("article_title")
    return render_template("remove_article.html", article_id = article_id, article_title = article_title)

@app.route("/article_removed", methods=['GET', 'POST'])
def remove_article():
    article = request.form.get("article_id")
    remove_article_from_db(article)
    return redirect("/")

@app.route("/view_articles")
def view_articles():
    '''
    Visar upp alla artiklar
    '''
    articles = get_articles()
    images = get_article_images()
    return render_template("all_articles.html", articles = articles, images = images)

@app.route("/about")
def about_page():
    return render_template("/about.html")

'''Login function'''
@app.route("/login", methods=["GET", "POST"])
def login_template():
    if request.method == 'POST':
        user_email = request.form.get("user_email")
        user_password = request.form.get("user_password")
        current_user = db_to_login(user_email, user_password)
        if current_user == False:
            flash("Felaktigt e-postadress eller lösenord.")
            return render_template("login.html")
        else:
            for item in current_user:
                user_id = item[2]
                user_name = item[3]
                session["USER_ID"] = user_id
                session['USER_NAME'] = user_name
                return redirect("/")
    else:                
        return render_template("login.html")

'''Logout function'''
@app.route("/logout_user")
def logout():
    session.clear()
    return render_template("logged_out.html")

@app.route("/show_profile_page")
def show_user_profile():
    user_name = session.get('USER_NAME')
    user_id = session.get('USER_ID')
    trades = trade_proposals(user_id)
    images = get_article_images()

    return render_template("profile_page.html", user_name = user_name, trades = trades, user_id = user_id, images = images)

'''Create user function'''
@app.route("/create_profile", methods=["GET", "POST"])
def create_profile_form():
    city = get_city()
    return render_template("create_profile.html", city = city)

@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    user_name = request.form.get("user_name")
    user_password = request.form.get("user_password")
    user_email = request.form.get("user_email")
    user_f_name = request.form.get("user_f_name")
    user_l_name = request.form.get("user_l_name")
    user_adress = request.form.get("user_adress")
    user_zip_code = request.form.get("user_zip_code")
    city = request.form.get("city")
    user_phone_number = request.form.get("user_phone_number")
    
    if user_zip_code.isdigit() and user_phone_number.isdigit() == True:
        create_user_in_db(user_name, user_password, user_email, user_f_name, user_l_name, user_adress, user_zip_code, city, user_phone_number)
        return redirect("/")
    else:
        return redirect("/create_profil")

@app.route("/my_profile")
def show_my_profile():
    user_name = session.get("USER_NAME")
    citys = get_city()
    user_info = get_profile_info()
    return render_template("/my_profile.html" ,user_name = user_name, user_info = user_info, citys = citys )

'''Visa eget förråd'''
@app.route("/show_own_storage")
def show_current_user_storage():
    user_id = session.get("USER_ID")
    articles = get_user_articles(user_id)
    images = get_article_images()
    
    return render_template("/user_storage.html", articles = articles, images = images)

'''Anmäl intresse för en produkt'''
@app.route("/submit_interest", methods=["GET", "POST"])
def submit_interest():
    transaction_id = request.form.get("transaction_id")
    interest = int(request.form.get("interest"))
    wife_id = request.form.get("wife_id")
    husband_id = request.form.get("husband_id")
    if interest == 1:
        chat_exists = check_if_chat_exists(husband_id, wife_id)
        print(chat_exists)
        save_interest_to_db(transaction_id)
        if chat_exists == []:
            chat_id = create_chat_id(wife_id, husband_id)
            create_standard_message(chat_id, wife_id, 'Hej, jag är också intresserad av ett byte')
        else:
            for chat in chat_exists:
                create_standard_message(chat, wife_id, 'Hej, jag är också intresserad av ett byte')

    elif interest == 0:
        remove_interest_from_db(transaction_id)

    return redirect("/show_profile_page")

'''Visar intresse för en produkt och hämtar in wife_article_id beroende på vilken artikel man trycker på, returnar sedan /choose_exchange.html tillsammans med artikel id samt den inloggaes artiklar'''
@app.route("/wife_article_id", methods=['GET', 'POST'])
def get_wife_article_id():

    user_id = session.get("USER_ID")
    if user_id == None:
        return redirect("/login")
    elif user_id != None:
        articles = get_user_articles(user_id)  

        wife_article_id = request.form.get("wife_article_id")
        return render_template("/choose_exchange.html", articles = articles, wife_article_id = wife_article_id)


'''Funktionen för att registrera intresse i databasen'''
@app.route("/show_interest", methods=['GET', 'POST'])
def register_interest():
    wife_article_id = request.form.get("wife_article")    
    husband_article_id = request.form.get("husband_article_id")
    if husband_article_id != "Handshake":
        show_interest(wife_article_id, husband_article_id)
    else:
        show_interest_handshake(wife_article_id)
    return redirect("/")

'''Anmäl att ett byte har genomförts eller inte och lägger in det i wife_confirmed'''
@app.route("/wife_confirm_trade", methods=["GET", "POST"])
def wife_confirm_trade():
    transaction_id = request.form.get("transaction_id")
    print(request.form.get("wife_confirm"))
    confirmed = int(request.form.get("wife_confirm"))
    if confirmed == 1:
        save_wife_confirmed_to_db(transaction_id)
    '''Funktion för att hantera ifall en användare vill neka att ett byte genomförts
    elif confirmed == 0:
        remove_interest_from_db(transaction_id)
    '''

    return redirect("/show_profile_page")

'''Anmäl att ett byte har genomförts eller inte och lägger in det i husband_confirmed'''
@app.route("/husband_confirm_trade", methods=["GET", "POST"])
def husband_confirm_trade():
    transaction_id = request.form.get("transaction_id")
    print(request.form.get("husband_confirm"))
    confirmed = int(request.form.get("husband_confirm"))
    if confirmed == 1:
        husband_wife_confirmed_to_db(transaction_id)
    '''Funktion för att hantera ifall en användare vill neka att ett byte genomförts
    elif confirmed == 0:
        remove_interest_from_db(transaction_id)
    '''

    return redirect("/show_profile_page")

@app.route("/article_search", methods=['GET', 'POST'])
def article_search():

    main_categories = get_main_category()
    images = get_article_images()
    search_term = request.form.get("free_text")
    main_category = request.form.get("main_category")
    sub_category_1 = request.form.get("sub_category")
    city = request.form.get("city_id")
    if search_term == '' and main_category != None and main_category != '':
        articles = get_article_by_category(main_category, sub_category_1)
    elif search_term != '' and ( main_category == None or main_category == ''):
        articles = get_article_by_title(search_term)
    elif search_term != '' and main_category != None and main_category != '':
        articles = get_article_by_title_and_cateogry(search_term, main_category, sub_category_1)
    elif search_term == '' and (main_category == None or main_category == ''):
        articles = get_articles()

    return render_template("/search_results.html", articles = articles, images = images, main_categories = main_categories, city = city)
@app.route("/edit_article", methods=["POST"])
def edit_article():
    article_id = request.form.get("article_id") 
    tiers = get_tier()
    citys = get_city()
    images = get_article_images()
    categories = get_main_category()
    article = get_article_by_id(article_id)
    return render_template("/edit_article.html", article = article, citys = citys, tiers = tiers, categories = categories, images = images, article_id = article_id)

@app.route("/edit_complete", methods=["POST"])
def change_artical():
    article_id = request.form.get("article_id")
    title = request.form.get("title")
    description = request.form.get("description")
    city = request.form.get("city")
    zip_code = request.form.get("zip_code")
    tier = request.form.get("tier")
    date_now = datetime.now()
    category_id = request.form.get("category")

    edit_to_article(title, description, zip_code, tier, date_now, city, article_id )
    edit_article_catergory(category_id, article_id)
    return redirect("/")



'''Visa subkategorier'''
@app.route("/get_child_categories",methods=["GET", "POST"])
def get_child_categories():
    if request.method == "POST":
        parent_id = request.form.get('parent_id')
        category_types = get_main_category_type(parent_id)
        for category in category_types:
            category_type = category
        sub_categories = get_sub_category_1_by_main(category_type)
        return jsonify({'htmlresponse': render_template('respons.html', sub_categories = sub_categories)})


@app.route("/transaction_history")
def show_completed_transactions():
    user_id = session.get("USER_ID")
    trades = get_completed_transactions(user_id)
    images = get_article_images()
    return render_template("/transaction_history.html", trades = trades, images = images)

@app.route("/transaction_undo", methods=["GET", "POST"])
def transacation_undo_now():
    transaction = request.form.get("transaction_id") 
    transaction_delete(transaction)
    return render_template("/transaction_undo_done.html")

@app.route("/edit_profile", methods=["POST", "GET"])
def edit_the_profile():
    citys = get_city()
    user_info = get_profile_info()
    return render_template("/edit_profile.html", user_info = user_info, citys = citys)

@app.route("/edit_profile_complete", methods=["POST"])
def change_profile():
    user_name = request.form.get("user_name")
    email = request.form.get("email")
    f_name = request.form.get("f_name")
    l_name = request.form.get("l_name")
    adress = request.form.get("adress")
    zip_code = request.form.get("zip_code")
    city = request.form.get("city")
    phone_number = request.form.get("phone_number")
    update_user_in_db( user_name, email, f_name, l_name, adress, zip_code, city, phone_number)
    return redirect("/my_profile")

@app.route("/edit_password")
def edit_password():
    return render_template("/edit_password.html")

@app.route("/change_password", methods=["POST"])
def change_password_done():
    password = request.form.get("password")
    change_password_done( password )
    return redirect("/my_profile")