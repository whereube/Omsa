from flask import Flask, redirect, render_template, request, flash, session
from article import *
from user import *

app = Flask(__name__)
app.run(debug=True)
app.config['SECRET_KEY'] = 'thisissecret'
#if __name__ == '__main__':
    #app.run(debug=True)

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
    create_article_in_db(title, description, zip_code, tier, city, category, user_id)
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
    return render_template("all_articles.html", articles = articles)

@app.route("/")
def start():
    return render_template("index.html")

    
'''Login function'''
@app.route("/login", methods=["GET", "POST"])
def login_template():

    if request.method == 'POST':
        user_email = request.form.get("user_email")
        user_password = request.form.get("user_password")
        current_user = db_to_login(user_email, user_password)
        if current_user == False:
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
    session.pop("USER_ID")
    session.pop("USER_NAME")
    return render_template("logged_out.html")


@app.route("/show_profile_page")
def show_user_profile():
    user_name = session.get('USER_NAME')
    return render_template("profile_page.html", user_name=user_name)


'''Create user function'''
@app.route("/create_profil", methods=["GET", "POST"])
def create_profil():
    city = get_city()
    return render_template("create_profil.html", city = city)



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
    
    if user_zip_code.isdigit() == True:
        create_user_in_db(user_name, user_password, user_email, user_f_name, user_l_name, user_adress, user_zip_code, city, user_phone_number)
        return redirect("/")
    else:
        return redirect("/create_profil")


'''Visa eget förråd'''
@app.route("/show_own_storage")
def show_current_user_storage():
    user_id = session.get("USER_ID")
    articles = get_user_articles(user_id)
    
    return render_template("/user_storage.html", articles=articles)

'''Visa vald artikel'''
'''
@app.route("/show_article/<article_id>")
def show_selected_article():
    records = get_article_by_id(article_id)
    return render_template("/show_article", article=article)
'''