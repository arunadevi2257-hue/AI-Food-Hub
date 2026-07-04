from flask import Blueprint, render_template, request, redirect, flash, session

menu = Blueprint("menu", __name__)

mysql = None

def init_menu(mysql_instance):
    global mysql
    mysql = mysql_instance


# =========================
# MENU PAGE
# =========================
@menu.route("/menu")
def menu_page():
    try:
        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT id, food_name, description, price, image
            FROM foods
        """)

        foods = cur.fetchall()
        cur.close()

        return render_template("menu.html", foods=foods)

    except Exception as e:
        return f"Menu Error: {e}"


# =========================
# ADD REVIEW
# =========================
@menu.route("/review/<int:food_id>", methods=["POST"])
def add_review(food_id):

    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect("/login")

    rating = request.form.get("rating")
    review = request.form.get("review")

    try:
        cur = mysql.connection.cursor()

        cur.execute("""
            INSERT INTO reviews (user_id, food_id, rating, review)
            VALUES (%s, %s, %s, %s)
        """, (session["user_id"], food_id, rating, review))

        mysql.connection.commit()
        cur.close()

        flash("Review Added Successfully", "success")

    except Exception as e:
        flash(f"Error: {e}", "danger")

    return redirect("/menu")


# =========================
# RECOMMENDATIONS
# =========================
@menu.route("/recommendations")
def recommendations():

    if "user_id" not in session:
        return redirect("/login")

    try:
        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT
                foods.food_name,
                foods.price,
                foods.image,
                COUNT(cart.food_id) AS total_orders
            FROM cart
            JOIN foods ON cart.food_id = foods.id
            GROUP BY foods.id
            ORDER BY total_orders DESC
            LIMIT 6
        """)

        foods = cur.fetchall()
        cur.close()

        return render_template("recommendations.html", foods=foods)

    except Exception as e:
            return f"Recommendation Error: {e}

@menu.route("/menu")
def menu_page():
    try:
        cur = mysql.connection.cursor()

        cur.execute("SELECT DATABASE()")
        db = cur.fetchone()

        cur.execute("SHOW TABLES")
        tables = cur.fetchall()

        return f"Database: {db}<br>Tables: {tables}"

    except Exception as e:
        return f"Menu Error: {e}"