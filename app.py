from flask import Flask, render_template
from flask_mysqldb import MySQL
import os

from routes.auth import auth, init_mysql
from routes.menu import menu, init_menu
from routes.cart import cart, init_cart
from routes.order import order, init_order
from routes.admin import admin, init_admin

app = Flask(__name__)


app.config["MYSQL_HOST"] = os.getenv("mysql-26a6c399-ai-food-hub.c.aivencloud.com")
app.config["MYSQL_USER"] = os.getenv("avnadmin")
app.config["MYSQL_PASSWORD"] = os.getenv("AVNS_7X6uVu6p2o3vqSlM4s6")
app.config["MYSQL_DB"] = os.getenv("defaultdb")
app.config["MYSQL_PORT"] = int(os.getenv("21835"))

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