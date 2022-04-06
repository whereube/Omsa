from tempfile import tempdir
from flask import Flask, render_template, request
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
    return render_template("index.html")

@app.route("/")
def start():
    return render_template("index.html")