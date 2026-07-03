from flask import Blueprint, render_template, redirect, session, flash, request, send_file
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
import os

order = Blueprint("order", __name__)

mysql = None

def init_order(mysql_instance):
    global mysql
    mysql = mysql_instance


# =========================
# CHECKOUT
# =========================
@order.route("/checkout", methods=["GET", "POST"])
def checkout():

    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect("/login")

    try:
        user_id = session["user_id"]

        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT
                foods.food_name,
                foods.price,
                cart.quantity,
                cart.food_id
            FROM cart
            JOIN foods ON cart.food_id = foods.id
            WHERE cart.user_id=%s
        """, (user_id,))

        items = cur.fetchall()

        total = 0
        for item in items:
            total += item[1] * item[2]

        # =====================
        # PLACE ORDER
        # =====================
        if request.method == "POST":

            payment = request.form.get("payment")

            cur.execute("""
                INSERT INTO orders (user_id, total_amount, payment_method)
                VALUES (%s, %s, %s)
            """, (user_id, total, payment))

            mysql.connection.commit()
            order_id = cur.lastrowid

            for item in items:
                cur.execute("""
                    INSERT INTO order_items (order_id, food_id, quantity, price)
                    VALUES (%s, %s, %s, %s)
                """, (order_id, item[3], item[2], item[1]))

            cur.execute(
                "DELETE FROM cart WHERE user_id=%s",
                (user_id,)
            )

            mysql.connection.commit()
            cur.close()

            flash("Order Placed Successfully", "success")
            return redirect("/order_history")

        cur.close()

        return render_template("checkout.html", items=items, total=total)

    except Exception as e:
        return f"Checkout Error: {e}"


# =========================
# ORDER HISTORY
# =========================
@order.route("/order_history")
def order_history():

    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect("/login")

    try:
        user_id = session["user_id"]

        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT id, total_amount, payment_method, ordered_at
            FROM orders
            WHERE user_id=%s
            ORDER BY ordered_at DESC
        """, (user_id,))

        orders = cur.fetchall()
        cur.close()

        return render_template("order_history.html", orders=orders)

    except Exception as e:
        return f"Order History Error: {e}"


# =========================
# ORDER DETAILS
# =========================
@order.route("/order_details/<int:order_id>")
def order_details(order_id):

    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect("/login")

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT foods.food_name, order_items.quantity, order_items.price
        FROM order_items
        JOIN foods ON order_items.food_id = foods.id
        WHERE order_items.order_id=%s
    """, (order_id,))

    items = cur.fetchall()
    cur.close()

    return render_template("order_details.html", items=items, order_id=order_id)


# =========================
# INVOICE (PDF DOWNLOAD)
# =========================
@order.route("/invoice/<int:order_id>")
def invoice(order_id):

    if "user_id" not in session:
        return redirect("/login")

    try:
        cur = mysql.connection.cursor()

        cur.execute("""
            SELECT foods.food_name, order_items.quantity, order_items.price
            FROM order_items
            JOIN foods ON order_items.food_id = foods.id
            WHERE order_items.order_id=%s
        """, (order_id,))

        items = cur.fetchall()
        cur.close()

        filename = f"invoice_{order_id}.pdf"

        pdf = SimpleDocTemplate(filename)

        data = [["Food", "Qty", "Price", "Subtotal"]]

        for item in items:
            subtotal = item[1] * item[2]
            data.append([
                item[0],
                item[1],
                f"₹{item[2]}",
                f"₹{subtotal}"
            ])

        table = Table(data)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige)
        ]))

        pdf.build([table])

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"Invoice Error: {e}"