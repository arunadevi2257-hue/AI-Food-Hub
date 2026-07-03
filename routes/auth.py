from flask import Blueprint, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

auth = Blueprint("auth", __name__)

mysql = None

def init_mysql(mysql_instance):
    global mysql
    mysql = mysql_instance


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect("/register")

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT id FROM users WHERE email=%s OR mobile=%s",
            (email, mobile)
        )

        user = cur.fetchone()

        if user:
            flash("Email or Mobile already exists", "warning")
            cur.close()
            return redirect("/register")

        hashed_password = generate_password_hash(password)

        cur.execute(
            """
            INSERT INTO users
            (fullname,email,mobile,password)
            VALUES(%s,%s,%s,%s)
            """,
            (
                fullname,
                email,
                mobile,
                hashed_password
            )
        )

        mysql.connection.commit()

        cur.close()

        flash("Registration Successful", "success")

        return redirect("/login")

    return render_template("register.html")

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT id, fullname, password FROM users WHERE email=%s",
            (email,)
        )

        user = cur.fetchone()

        cur.close()

        if user and check_password_hash(user[2], password):

            session["user_id"] = user[0]
            session["user_name"] = user[1]

            flash("Login Successful", "success")

            return redirect("/")

        else:

            flash("Invalid Email or Password", "danger")

            return redirect("/login")

    return render_template("login.html") 

@auth.route("/profile")
def profile():

    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect("/login")

    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            fullname,
            email,
            mobile
        FROM users
        WHERE id=%s
    """, (session["user_id"],))

    user = cur.fetchone()

    cur.close()

    return render_template("profile.html", user=user) 

@auth.route("/edit_profile", methods=["POST"])
def edit_profile():

    if "user_id" not in session:
        return redirect("/login")

    fullname = request.form["fullname"]
    mobile = request.form["mobile"]

    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE users
        SET fullname=%s,
            mobile=%s
        WHERE id=%s
    """, (fullname, mobile, session["user_id"]))

    mysql.connection.commit()

    cur.close()

    flash("Profile Updated Successfully", "success")

    return redirect("/profile")  

@auth.route("/change_password", methods=["POST"])
def change_password():

    if "user_id" not in session:
        flash("Please login first", "warning")
        return redirect("/login")

    current_password = request.form["current_password"]
    new_password = request.form["new_password"]
    confirm_password = request.form["confirm_password"]

    if new_password != confirm_password:
        flash("New passwords do not match", "danger")
        return redirect("/profile")

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT password FROM users WHERE id=%s",
        (session["user_id"],)
    )

    user = cur.fetchone()

    if not user:
        cur.close()
        flash("User not found", "danger")
        return redirect("/profile")

    if not check_password_hash(user[0], current_password):
        cur.close()
        flash("Current password is incorrect", "danger")
        return redirect("/profile")

    hashed_password = generate_password_hash(new_password)

    cur.execute(
        "UPDATE users SET password=%s WHERE id=%s",
        (hashed_password, session["user_id"])
    )

    mysql.connection.commit()
    cur.close()

    flash("Password Changed Successfully", "success")

    return redirect("/profile")

@auth.route("/logout")
def logout():
    session.clear()
    flash("Logged Out Successfully", "success")
    return redirect("/login")