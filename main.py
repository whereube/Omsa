from flask import Flask, redirect, render_template, request, flash, session, g
from article import *
from user import *
from ima import *
from werkzeug.utils import secure_filename
import os
from datetime import datetime

UPLOAD_FOLDER = 'static/article_images'

app = Flask(__name__, static_url_path='/static')
app.run(debug=True)
app.config['SECRET_KEY'] = 'thisissecret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def start():
    return render_template("index.html")

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
    category = request.form.get("category")
    user_id = session["USER_ID"]

    file = request.files['file']
    if file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    create_article_in_db(title, description, zip_code, tier, city, category, user_id, file.filename)
    return redirect("/")

@app.route("/remove")
def remove_article_form():
    ''' 
    Hämtar in formuläret för att ta bort en artikel och skickar vidare detta för att ta bort en post i databasen
    '''
    user_id = session["USER_ID"]
    articles = get_user_articles(user_id)
    return render_template("remove_article.html", articles = articles)

@app.route("/article_removed", methods=['GET', 'POST'])
def remove_article():
    article = request.form.get("article")
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
                return redirect("/show_profile_page")
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
    if interest == 1:
        save_interest_to_db(transaction_id)
    elif interest == 0:
        remove_interest_from_db(transaction_id)

    return redirect("/show_profile_page")

'''Visar intresse för en produkt och hämtar in wife_article_id beroende på vilken artikel man trycker på, returnar sedan /choose_exchange.html tillsammans med artikel id samt den inloggaes artiklar'''
@app.route("/wife_article_id", methods=['GET', 'POST'])
def get_wife_article_id():

    user_id = session["USER_ID"]
    articles = get_user_articles(user_id)  

    wife_article_id = request.form.get("wife_article_id")
    return render_template("/choose_exchange.html", articles = articles, wife_article_id = wife_article_id)

'''Funktionen för att registrera intresse i databasen'''
@app.route("/show_interest", methods=['GET', 'POST'])
def register_interest():
    wife_article_id = request.form.get("wife_article")    
    husband_article_id = request.form.get("husband_article_id")
    show_interest(wife_article_id, husband_article_id)
    return redirect("/")
