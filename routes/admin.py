from flask import Blueprint, render_template, request, redirect, session, flash
import os
from werkzeug.utils import secure_filename

admin = Blueprint("admin", __name__)

mysql = None

def init_admin(mysql_instance):
    global mysql
    mysql = mysql_instance


@admin.route("/admin", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )

        admin_user = cur.fetchone()

        cur.close()

        if admin_user:

            session["admin"] = username

            return redirect("/admin/dashboard")

        flash("Invalid Admin Login", "danger")

    return render_template("admin_login.html")

@admin.route("/admin/dashboard")
def admin_dashboard():

    if "admin" not in session:
        return redirect("/admin")

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM foods")
    total_foods = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM orders")
    total_orders = cur.fetchone()[0]

    cur.execute("SELECT IFNULL(SUM(total_amount),0) FROM orders")
    total_revenue = cur.fetchone()[0]

    cur.close()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_foods=total_foods,
        total_orders=total_orders,
        total_revenue=total_revenue
    )  

@admin.route("/admin/foods", methods=["GET", "POST"])
def manage_foods():

    if "admin" not in session:
        return redirect("/admin")

    cur = mysql.connection.cursor()

    if request.method == "POST":

        category_id = request.form["category_id"]
        food_name = request.form["food_name"]
        description = request.form["description"]
        price = request.form["price"]
        
        image = request.files["image"]

        filename = secure_filename(image.filename)

        image.save(os.path.join("static/food_images", filename))
        
        print("Category ID =",category_id)

        cur.execute("""
            INSERT INTO foods
            (category_id, food_name, description, price, image)
            VALUES (%s,%s,%s,%s,%s)
        """, (category_id, food_name, description, price, filename))

        mysql.connection.commit()

        flash("Food Added Successfully", "success")

    cur.execute("""
        SELECT
            id,
            food_name,
            price,
            image
        FROM foods
    """)

    foods = cur.fetchall()

    cur.close()

    return render_template("manage_foods.html", foods=foods)

@admin.route("/admin/delete_food/<int:food_id>")
def delete_food(food_id):

    if "admin" not in session:
        return redirect("/admin")

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM foods WHERE id=%s",
        (food_id,)
    )

    mysql.connection.commit()

    cur.close()

    flash("Food Deleted Successfully", "success")

    return redirect("/admin/foods")

@admin.route("/admin/edit_food/<int:food_id>", methods=["GET", "POST"])
def edit_food(food_id):

    if "admin" not in session:
        return redirect("/admin")

    cur = mysql.connection.cursor()

    if request.method == "POST":

        food_name = request.form["food_name"]
        description = request.form["description"]
        price = request.form["price"]

        cur.execute("""
            UPDATE foods
            SET food_name=%s,
                description=%s,
                price=%s
            WHERE id=%s
        """, (food_name, description, price, food_id))

        mysql.connection.commit()

        flash("Food Updated Successfully", "success")

        return redirect("/admin/foods")

    cur.execute(
        "SELECT * FROM foods WHERE id=%s",
        (food_id,)
    )

    food = cur.fetchone()

    cur.close()

    return render_template("edit_food.html", food=food)      

@admin.route("/admin/orders")
def admin_orders():

    if "admin" not in session:
        return redirect("/admin")

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            orders.id,
            users.fullname,
            orders.total_amount,
            orders.payment_method,
            orders.ordered_at
        FROM orders
        JOIN users
        ON orders.user_id = users.id
        ORDER BY orders.ordered_at DESC
    """)

    orders = cur.fetchall()

    cur.close()

    return render_template("admin_orders.html", orders=orders)

@admin.route("/admin/users")
def admin_users():

    if "admin" not in session:
        return redirect("/admin")

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            id,
            fullname,
            email,
            mobile
        FROM users
        ORDER BY id DESC
    """)

    users = cur.fetchall()

    cur.close()

    return render_template(
        "admin_users.html",
        users=users
    )

@admin.route("/admin/delete_user/<int:user_id>")
def delete_user(user_id):

    if "admin" not in session:
        return redirect("/admin")

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM users WHERE id=%s",
        (user_id,)
    )

    mysql.connection.commit()

    cur.close()

    flash("User Deleted Successfully", "success")

    return redirect("/admin/users")

@admin.route("/admin/sales_report")
def sales_report():

    if "admin" not in session:
        return redirect("/admin")

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            DATE(ordered_at),
            COUNT(id),
            SUM(total_amount)
        FROM orders
        GROUP BY DATE(ordered_at)
        ORDER BY DATE(ordered_at) DESC
    """)

    reports = cur.fetchall()

    cur.close()

    return render_template(
        "sales_report.html",
        reports=reports
    )    

