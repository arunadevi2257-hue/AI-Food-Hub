from flask import Blueprint, render_template,request,redirect,flash,session

menu = Blueprint("menu", __name__)

mysql = None

def init_menu(mysql_instance):
    global mysql
    mysql = mysql_instance


@menu.route("/menu")
def menu_page():

    cur = mysql.connection.cursor()

    cur.execute("""
SELECT
id,
food_name,
description,
price,
image
FROM foods
""")

    foods = cur.fetchall()

    cur.close()

    return render_template("menu.html", foods=foods)

@menu.route("/review/<int:food_id>", methods=["POST"])
def add_review(food_id):

    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect("/login")

    rating = request.form["rating"]
    review = request.form["review"]

    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO reviews
        (user_id, food_id, rating, review)
        VALUES (%s, %s, %s, %s)
    """, (session["user_id"], food_id, rating, review))

    mysql.connection.commit()
    cur.close()

    flash("Review Added Successfully", "success")

    return redirect("/menu")    

@menu.route("/recommendations")
def recommendations():

    if "user_id" not in session:
        return redirect("/login")

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            foods.food_name,
            foods.price,
            foods.image,
            COUNT(cart.food_id) AS total_orders
        FROM cart
        JOIN foods
            ON cart.food_id = foods.id
        GROUP BY foods.id
        ORDER BY total_orders DESC
        LIMIT 6
    """)

    foods = cur.fetchall()

    cur.close()

    return render_template(
        "recommendations.html",
        foods=foods
    )    