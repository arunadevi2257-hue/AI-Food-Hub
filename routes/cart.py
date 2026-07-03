from flask import Blueprint, render_template, redirect, session, flash

cart = Blueprint("cart", __name__)

mysql = None

def init_cart(mysql_instance):
    global mysql
    mysql = mysql_instance


@cart.route("/add_to_cart/<int:food_id>")
def add_to_cart(food_id):

    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect("/login")

    user_id = session["user_id"]

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT id, quantity FROM cart WHERE user_id=%s AND food_id=%s",
        (user_id, food_id)
    )

    item = cur.fetchone()

    if item:
        cur.execute(
            "UPDATE cart SET quantity=quantity+1 WHERE id=%s",
            (item[0],)
        )
    else:
        cur.execute(
            "INSERT INTO cart(user_id, food_id, quantity) VALUES(%s,%s,%s)",
            (user_id, food_id, 1)
        )

    mysql.connection.commit()
    cur.close()

    flash("Food added to cart!", "success")
    return redirect("/menu")

@cart.route("/increase/<int:cart_id>")
def increase(cart_id):

    if "user_id" not in session:
        return redirect("/login")

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE cart
        SET quantity = quantity + 1
        WHERE id = %s
    """, (cart_id,))

    mysql.connection.commit()
    cur.close()

    return redirect("/cart")

from flask import render_template

@cart.route("/cart")
def view_cart():

    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect("/login")

    user_id = session["user_id"]

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            cart.id,
            foods.food_name,
            foods.price,
            foods.image,
            cart.quantity
        FROM cart
        JOIN foods
            ON cart.food_id = foods.id
        WHERE cart.user_id=%s
    """, (user_id,))

    cart_items = cur.fetchall()

    total = 0

    for item in cart_items:
        total += item[2] * item[4]

    cur.close()

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )
    
@cart.route("/decrease/<int:cart_id>")
def decrease(cart_id):

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT quantity FROM cart WHERE id = %s",
        (cart_id,)
    )

    item = cur.fetchone()

    if item and item[0] > 1:
        cur.execute(
            "UPDATE cart SET quantity = quantity - 1 WHERE id = %s",
            (cart_id,)
        )
    else:
        cur.execute(
            "DELETE FROM cart WHERE id = %s",
            (cart_id,)
        )

    mysql.connection.commit()
    cur.close()

    return redirect("/cart")

@cart.route("/remove/<int:cart_id>")
def remove(cart_id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM cart WHERE id = %s",
        (cart_id,)
    )

    mysql.connection.commit()
    cur.close()

    return redirect("/cart")from flask import Blueprint, render_template, redirect, session, flash

cart = Blueprint("cart", __name__)

mysql = None

def init_cart(mysql_instance):
    global mysql
    mysql = mysql_instance


@cart.route("/add_to_cart/<int:food_id>")
def add_to_cart(food_id):

    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect("/login")

    user_id = session["user_id"]

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT id, quantity FROM cart WHERE user_id=%s AND food_id=%s",
        (user_id, food_id)
    )

    item = cur.fetchone()

    if item:
        cur.execute(
            "UPDATE cart SET quantity=quantity+1 WHERE id=%s",
            (item[0],)
        )
    else:
        cur.execute(
            "INSERT INTO cart(user_id, food_id, quantity) VALUES(%s,%s,%s)",
            (user_id, food_id, 1)
        )

    mysql.connection.commit()
    cur.close()

    flash("Food added to cart!", "success")
    return redirect("/menu")

@cart.route("/increase/<int:cart_id>")
def increase(cart_id):

    if "user_id" not in session:
        return redirect("/login")

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE cart
        SET quantity = quantity + 1
        WHERE id = %s
    """, (cart_id,))

    mysql.connection.commit()
    cur.close()

    return redirect("/cart")

from flask import render_template

@cart.route("/cart")
def view_cart():

    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect("/login")

    user_id = session["user_id"]

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            cart.id,
            foods.food_name,
            foods.price,
            foods.image,
            cart.quantity
        FROM cart
        JOIN foods
            ON cart.food_id = foods.id
        WHERE cart.user_id=%s
    """, (user_id,))

    cart_items = cur.fetchall()

    total = 0

    for item in cart_items:
        total += item[2] * item[4]

    cur.close()

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )
    
@cart.route("/decrease/<int:cart_id>")
def decrease(cart_id):

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT quantity FROM cart WHERE id = %s",
        (cart_id,)
    )

    item = cur.fetchone()

    if item and item[0] > 1:
        cur.execute(
            "UPDATE cart SET quantity = quantity - 1 WHERE id = %s",
            (cart_id,)
        )
    else:
        cur.execute(
            "DELETE FROM cart WHERE id = %s",
            (cart_id,)
        )

    mysql.connection.commit()
    cur.close()

    return redirect("/cart")

@cart.route("/remove/<int:cart_id>")
def remove(cart_id):

    cur = mysql.connection.cursor()

    cur.execute(
        "DELETE FROM cart WHERE id = %s",
        (cart_id,)
    )

    mysql.connection.commit()
    cur.close()

    return redirect("/cart")