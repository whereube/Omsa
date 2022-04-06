from flask import Flask, render_template
from article import *

app = Flask(__name__)

@app.route("/create")
def create_article():
    return render_template("create_article.html")