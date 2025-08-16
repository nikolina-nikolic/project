import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import jinja2
from helpers import login_required, apology
import re
from datetime import datetime
from flask import jsonify



import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('household.db')
cursor = conn.cursor()


# Create the users table without the CHECK constraint
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        user_type TEXT CHECK(user_type IN ('customer','cleaner')) NOT NULL
    )
""")
# Try adding new columns if they don't exist
try:
    cursor.execute("ALTER TABLE users ADD COLUMN city_input TEXT")
except sqlite3.OperationalError:
    pass  # Column already exists
try:
    cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT")
except sqlite3.OperationalError:
    pass  # Column already exists
try:
    cursor.execute("ALTER TABLE users ADD COLUMN description TEXT")
except sqlite3.OperationalError:
    pass  # Column already exists

# Commit changes and close the connection
conn.commit()
conn.close()

#Database for reviews
conn=sqlite3.connect('household.db')
cursor=conn.cursor()
cursor.execute("""
               CREATE TABLE IF NOT EXISTS reviews(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
               reviewer_id INTEGER NOT NULL,
               cleaner_id INTEGER NOT NULL,
               rating INTEGER CHECK(rating >=1 AND rating <=5) NOT NULL,
               comment TEXT,
               created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (reviewer_id) REFERENCES users(id),
               FOREIGN KEY (cleaner_id) REFERENCES users(id)
              )
               """)
conn.commit()
conn.close()

# Configure application
app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    '''Index page'''
    if 'user_id' not in session: 
        return render_template("index.html")
    
    # Redirect user to home page
    conn=sqlite3.connect("household.db")
    cursor=conn.cursor()
    cursor.execute( "SELECT user_type FROM users WHERE id = ?", (session["user_id"],))
    rows=cursor.fetchall()
    conn.commit()
    conn.close()
    user_type = rows[0][0] if rows else None
    if user_type == 'customer':
        return redirect(url_for("customer_home"))
    elif user_type == 'cleaner':
        return redirect(url_for("cleaner_home"))



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        conn=sqlite3.connect("household.db")
        cursor=conn.cursor()
        cursor.execute( "SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
        rows=cursor.fetchone()
        conn.close()

        # Ensure username exists and password is correct
        if not rows or not check_password_hash(
            rows[5], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]

        # Redirect user to home page
        if rows[6]=='customer':
            return redirect(url_for("customer_home"))
        elif rows[6]=='cleaner':
            return redirect(url_for("cleaner_home"))
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


def is_valid_email(email):
    # Regular expression pattern for a valid email
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    # Use re.match() to see if the email matches the pattern
    if re.match(pattern, email):
        return True
    else:
        return False



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    username=request.form.get("username")
    password=request.form.get("password")
    confirmation=request.form.get("confirmation")
    name=request.form.get("name")
    surname=request.form.get("surname")
    email=request.form.get("email")
    user_type=request.form.get("user_type")
    city_input=request.form.get("city_input")
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        # Ensure username, password and confirmation were submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)
        elif not request.form.get("name"):
            return apology("must provide name", 400)
        elif not request.form.get("surname"):
            return apology("must provide surname", 400)
        elif not request.form.get("email"):
            return apology("must provide email", 400)
        elif not request.form.get("user_type"):
            return apology("must provide user-type", 400)
        elif not request.form.get("city_input"):
            return apology("must provide city_input", 400)
        if not password == confirmation:
            return apology("password and confirmation must match",400)
        if is_valid_email(email) == False:
            return apology("invalid email",400)
        if not city_input in CITIES:
            return apology("invalid city",400)
        #Ensure username is not already taken
        conn=sqlite3.connect("household.db")
        cursor=conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username=?", (username,))
        row=cursor.fetchall()
        conn.commit()
        conn.close()
        if row:
            return apology("must choose new username. this one is already taken.")
        conn=sqlite3.connect("household.db")
        cursor=conn.cursor()
        cursor.execute(
        "INSERT INTO users(username, password, name, surname, email, user_type, city_input) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (username, generate_password_hash(password), name, surname, email, user_type, city_input,)
        )
        conn.commit()
        conn.close()
          
        conn=sqlite3.connect("household.db")
        cursor=conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        user_id =cursor.fetchone()
        conn.commit()
        conn.close()
        if user_id:
            session["user_id"] = user_id[0]
        flash("Successfully registered!")
        # Redirect user to home page
        conn=sqlite3.connect("household.db")
        cursor=conn.cursor()
        cursor.execute( "SELECT user_type FROM users WHERE username = ?", (request.form.get("username"),))
        rows=cursor.fetchone()
        conn.commit()
        conn.close()
        if rows and rows[0]=='customer':
            return redirect(url_for("customer_home"))
        elif rows and rows[0]=='cleaner':
            return redirect(url_for("cleaner_home"))



@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    #CHANGE PASSWORD
    if request.method == "GET":
        return render_template("change_password.html")
    elif request.method == "POST":
        conn=sqlite3.connect("household.db")
        cursor=conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (session["user_id"],))
        rows =cursor.fetchall()
        conn.commit()
        conn.close()
        old_password=request.form.get("old_password").strip()
        password=request.form.get("password").strip()
        confirmation_password=request.form.get("password_confirmation").strip()
        if not old_password:
            return apology("enter old password",400)
        elif not password:
            return apology("enter password",400)
        elif not confirmation_password:
            return apology("enter password confirmation",400)

        # Ensure old password is correct
        if  not check_password_hash(
            rows[0][5], old_password):
            return apology("invalid old password", 400)

        if password != confirmation_password:
            return apology("password and password confirmation doesn't match",400)

        conn=sqlite3.connect("household.db")
        cursor=conn.cursor()
        cursor.execute("UPDATE users SET password=? WHERE id=?", (generate_password_hash(password),session["user_id"]))
        conn.commit()
        conn.close()
        flash("Password changed successfully!")
        return redirect("/")
    
@app.route("/my_profile")
@login_required
def my_profile():
    """View profile"""
    conn=sqlite3.connect("household.db")
    conn.row_factory = sqlite3.Row
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id= ?", (session["user_id"],))
    user=cursor.fetchone()
    conn.close()
    if not user:
        return apology("User not found", 404)
    
    reviews=[]
    avg_rating=0
    review_count=0
    if user["user_type"] == 'cleaner':
        conn=sqlite3.connect("household.db")
        conn.row_factory = sqlite3.Row
        cursor=conn.cursor()
        cursor.execute("""
                       SELECT reviews.*, users.username AS reviewer_username
                       FROM reviews
                       JOIN users ON reviews.reviewer_id=users.id
                       WHERE reviews.cleaner_id=?
                       ORDER BY reviews.created_at DESC
                       """,(user["id"],))
        reviews=cursor.fetchall()

        cursor.execute("SELECT COUNT(*), AVG(rating) FROM reviews WHERE cleaner_id=?",(user["id"],))
        review_count,avg_rating=cursor.fetchone()
        if avg_rating :
            avg_rating=round(avg_rating,2)
        conn.close()
    return render_template("my_profile.html",user=user,reviews=reviews,avg_rating=avg_rating,review_count=review_count)



@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    conn=sqlite3.connect("household.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id= ?", (session["user_id"],))
    user=cursor.fetchone()
    if not user:
        return apology("User not found",404)
    if request.method == "POST":
        username=request.form.get("username").strip()
        name=request.form.get("name").strip()
        surname=request.form.get("surname").strip()
        email=request.form.get("email").strip()
        user_type=request.form.get("user_type")
        city_input=request.form.get("city_input").strip()
        phone=request.form.get("phone").strip() if request.form.get("phone") else None
        description=request.form.get("description").strip() if request.form.get("description") else None
        #Ensure all required fields are filled
        if not username or not name or not surname or not email:
            return apology("Username, name, surname and email are required fields.") 
        #Ensure username is not already taken
        conn=sqlite3.connect("household.db")
        cursor=conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username=? AND id != ?", (username, session["user_id"],))
        row=cursor.fetchall()
        if row:
            return apology("must choose new username. this one is already taken.")
        #Ensure email is valid
        if is_valid_email(email) == False:
            return apology("invalid email",400)
        #Ensure city is valid
        if not city_input in CITIES:
            return apology("invalid city",400)
        #Update user profile
        cursor.execute("""
                UPDATE users 
                SET username=?, name=?, surname=?, email=?, user_type=?, city_input=?, phone=?, description=?
                WHERE id=? 
        """, (username, name, surname, email, user_type, city_input, phone, description, session["user_id"]))
        conn.commit()
        conn.close()
        flash("Profile updated successfully!")
        return redirect(url_for("my_profile"))
    else:
        return render_template("edit_profile.html",user=user)
        
CITIES = [
    "Beograd", "Novi Sad", "Niš", "Kragujevac", "Subotica", "Kraljevo",
    "Novi Pazar", "Zrenjanin", "Čačak", "Šabac", "Smederevo", "Valjevo",
    "Vranje", "Sremska Mitrovica", "Loznica", "Sombor", "Užice", "Požarevac",
    "Jagodina", "Stara Pazova", "Pirot", "Kikinda", "Ruma", "Bačka Palanka",
    "Zaječar", "Paraćin", "Vršac", "Inđija", "Aleksinac", "Smederevska Palanka",
    "Aranđelovac", "Bujanovac", "Bor", "Gornji Milanovac", "Prokuplje", "Vrbas",
    "Trstenik", "Kula", "Velika Plana", "Preševo", "Tutin", "Prijepolje", "Bečej",
    "Negotin", "Kovin", "Šid", "Ivanjica", "Bačka Topola", "Požega", 
    "Petrovac na Mlavi", "Temerin", "Ub", "Vlasotince", "Knjaževac", "Ćuprija",
    "Vrnjačka Banja", "Odžaci", "Bogatić", "Sjenica", "Žabalj", "Bajina Bašta",
    "Priboj", "Apatin", "Aleksandrovac", "Raška", "Kovačica", "Kanjiža", "Svilajnac",
    "Novi Bečej", "Topola", "Pećinci", "Despotovac", "Lebane", "Vladičin Han",
    "Kladovo", "Alibunar", "Arilje", "Surdulica", "Lučani", "Doljevac", "Kuršumlija",
    "Veliko Gradište", "Čajetina", "Majdanpek", "Bela Crkva", "Vladimirci", "Krupanj",
    "Srbobran", "Varvarin", "Titel", "Beočin", "Lajkovac", "Žitorađa", "Brus", 
    "Nova Varoš", "Žitište", "Ada", "Sokobanja", "Ljubovija", "Mionica", "Merošina", 
    "Kučevo", "Knić", "Bački Petrovac", "Bač", "Mali Zvornik", "Koceljeva", "Svrljig", 
    "Ljig", "Sečanj", "Boljevac", "Kosjerić", "Batočina", "Mali Iđoš", "Osečina", 
    "Bela Palanka", "Žagubica", "Blace", "Bojnik", "Irig", "Žabari", "Babušnica", 
    "Malo Crniće", "Plandište", "Novi Kneževac", "Čoka", "Nova Crnja", "Rekovac", 
    "Dimitrovgrad", "Sremski Karlovci", "Ćićevac", "Ražanj", "Golubac", "Lapovo", 
    "Medveđa", "Bosilegrad", "Gadžin Han", "Trgovište", "Crna Trava"
]

@app.route('/customer_home')
@login_required
def customer_home():
    conn=sqlite3.connect("household.db")
    conn.row_factory = sqlite3.Row #Access columns by name
    cursor=conn.cursor()
    cursor.execute("SELECT city_input FROM users WHERE id=? AND user_type='customer'",(session["user_id"],))
    row=cursor.fetchone()
    if not row:
        conn.close()
        return apology("User not found or not customer",404)
    customer_city=row[0]
    cursor.execute("SELECT * FROM users WHERE user_type='cleaner' AND city_input=?",(customer_city,))
    cleaners=cursor.fetchall()
    cleaners_info =[]
    for c in cleaners:
        cursor.execute("SELECT COUNT(*), AVG(rating) FROM reviews WHERE cleaner_id=?", (c["id"],))
        count,avg=cursor.fetchone()
        cursor.execute("""SELECT reviews.*, users.username AS reviewer_username 
        FROM reviews 
        JOIN users ON reviews.reviewer_id = users.id 
        WHERE reviews.cleaner_id=?
        ORDER BY reviews.created_at DESC
        LIMIT 5""", (c["id"],))
        initial_reviews=cursor.fetchall()
        cleaners_info.append({
            "cleaner": c,
            "review_count": count if count is not None else 0,
            "avg_rating": round(avg,2) if avg is not None else 0,
            "initial_reviews": initial_reviews
            })
    conn.close()
    return render_template('customer_home.html', cleaners_info=cleaners_info)



@app.route('/cleaner_home')
@login_required
def cleaner_home():
    conn=sqlite3.connect("household.db")
    conn.row_factory = sqlite3.Row #Access columns by name
    cursor=conn.cursor()
    cursor.execute("SELECT city_input FROM users WHERE id=? AND user_type='cleaner'",(session["user_id"],))
    row=cursor.fetchone()
    if not row:
        conn.close()
        return apology("User not found or not cleaner",404)
    cleaner_city=row["city_input"]
    cursor.execute("SELECT * FROM users WHERE user_type='cleaner' AND city_input=? AND id!=?",(cleaner_city,session["user_id"],))
    cleaners=cursor.fetchall()
    cleaners_info =[]
    for c in cleaners:
        cursor.execute("SELECT COUNT(*), AVG(rating) FROM reviews WHERE cleaner_id=? ", (c["id"],))
        count,avg=cursor.fetchone()
        cursor.execute("""SELECT reviews.*, users.username AS reviewer_username 
        FROM reviews 
        JOIN users ON reviews.reviewer_id = users.id 
        WHERE reviews.cleaner_id=?
        ORDER BY reviews.created_at DESC
        LIMIT 5""", (c["id"],))
        initial_reviews=cursor.fetchall()
        cleaners_info.append({
            "cleaner": c,
            "review_count": count if count is not None else 0,
            "avg_rating": round(avg,2) if avg is not None else 0,
            "initial_reviews": initial_reviews
            })
    conn.close()
    return render_template('cleaner_home.html', cleaners_info=cleaners_info)
    


@app.route("/load_more_comments/<int:cleaner_id>/<int:offset>")
@login_required
def load_more_comments(cleaner_id,offset):
    conn=sqlite3.connect("household.db")
    conn.row_factory = sqlite3.Row
    cursor=conn.cursor()
    cursor.execute(""" SELECT reviews.*, users.username AS reviewer_username
                    FROM reviews
                   JOIN users ON reviews.reviewer_id=users.id
                   WHERE reviews.cleaner_id=?
                   ORDER BY reviews.created_at DESC
                   LIMIT 5 OFFSET ? """,(cleaner_id, offset))
    
    more_comments=cursor.fetchall()
    conn.close()
    return jsonify([dict(comment) for comment in more_comments])

@app.route("/leave_review", methods=["POST"])
@login_required
def leave_review():
   cleaner_id=request.form.get("cleaner_id")
   rating=int(request.form.get("rating"))
   comment=request.form.get("comment")
   reviewer_id=session["user_id"] 
   if int(cleaner_id) == reviewer_id:
        flash("You cannot review yourself.")
        return redirect("/")
   if not cleaner_id or not rating or not comment:
       flash("All fields are required.")
       return redirect("/")
   
   try:
       rating = int(rating)
       if rating<1 or rating>5:
           flash("Rating must be beteween 1 and 5.")
           return redirect("/")
   
   except ValueError:
       flash("Invalid rating.")
       return redirect("/")
   
   conn=sqlite3.connect("household.db")
   cursor=conn.cursor()
   cursor.execute("INSERT INTO reviews(reviewer_id,cleaner_id,rating,comment)"
   "VALUES(?,?,?,?)",(reviewer_id,cleaner_id,rating,comment))
   conn.commit()
   conn.close()
   flash("Review submitted successfully!")
   return redirect (url_for("index"))

   
if __name__ =='__main__':
    app.run(debug=True)