from flask import Flask, render_template
from flask_mysqldb import MySQL
import os

from routes.auth import auth, init_mysql
from routes.menu import menu, init_menu
from routes.cart import cart, init_cart
from routes.order import order, init_order
from routes.admin import admin, init_admin

app = Flask(__name__)


app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
app.config["MYSQL_PORT"] = int(os.getenv("MYSQL_PORT"))


app.config["UPLOAD_FOLDER"] = "static/food_images"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_secret")


mysql = MySQL(app)

init_mysql(mysql)
init_menu(mysql)
init_cart(mysql)
init_order(mysql)
init_admin(mysql)


app.register_blueprint(auth)
app.register_blueprint(menu)
app.register_blueprint(cart)
app.register_blueprint(order)
app.register_blueprint(admin)


@app.route("/")
def home():
    return render_template("home.html")

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

@app.route("/dbinfo")
def dbinfo():
    return {
        "host": app.config["MYSQL_HOST"],
        "db": app.config["MYSQL_DB"],
        "user": app.config["MYSQL_USER"],
        "port": app.config["MYSQL_PORT"]
    }    


@app.route("/check_foods")
def check_foods():
    cur = mysql.connection.cursor()
    cur.execute("SHOW TABLES")
    tables = cur.fetchall()
    return str(tables)    