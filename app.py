from flask import Flask, render_template
from flask_mysqldb import MySQL
from config import Config
from routes.auth import auth, init_mysql
from routes.menu import menu, init_menu
from routes.cart import cart, init_cart
from routes.order import order, init_order
from routes.admin import admin, init_admin
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

init_mysql(mysql)

app.register_blueprint(auth)

init_menu(mysql)
app.register_blueprint(menu)

init_cart(mysql)
app.register_blueprint(cart)

init_order(mysql)
app.register_blueprint(order)

init_admin(mysql)
app.register_blueprint(admin)

app.config['UPLOAD_FOLDER'] = 'static/food_images'

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/menu")
def menu():
    return render_template("menu.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/cart")
def cart():
    return render_template("cart.html")


@app.route("/test_db")
def test_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        cur.close()
        return "✅ Database Connected Successfully!"
    except Exception as e:
        return f"❌ Database Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)