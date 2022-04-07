from flask import Flask, redirect, render_template, request
from article import *

app = Flask(__name__)

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
    create_article_in_db(title, description, zip_code, tier, city, category)
    return redirect("/")

@app.route("/remove")
def remove_article_form():
    ''' 
    Hämtar in formuläret för att ta bort en artikel och skickar vidare detta för att ta bort en post i databasen
    '''
    articles = get_articles()
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
    return render_template("all_articles.html", articles = articles)

@app.route("/")
def start():
    return render_template("index.html")

'''Login function'''
@app.route("/login")
def login_template():
    return render_template("login.html")

@app.route("/user_login", methods=["GET", "POST"])
def user_login():
    user_email = request.form.get("user_email")
    user_password = request.form.get("user_password")
    print(user_email)
    print(user_password)
    a = login(user_email, user_password)

    if a == 1:
        redirect("/")
    elif a == 0:
        print("Fuck you")

    return redirect("/")


