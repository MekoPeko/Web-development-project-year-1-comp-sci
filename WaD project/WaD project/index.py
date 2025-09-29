# Student ID - 2400965 , Student name - Harry Masters 
from flask import Flask, render_template, request, redirect, flash, session, url_for, abort
import dbfunc  # Import the database connection module
import mysql.connector
from functools import wraps
from datetime import datetime, timedelta  # Import datetime and timedelta modules

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management

# --- SESSION TIMEOUT FEATURE START ---
SESSION_TIMEOUT_MINUTES = 5

@app.before_request
def session_timeout_check():
    if 'username' in session:
        now = datetime.utcnow()
        last_activity = session.get('last_activity')
        if last_activity:
            try:
                last_activity_dt = datetime.strptime(last_activity, "%Y-%m-%d %H:%M:%S")
                if now - last_activity_dt > timedelta(minutes=SESSION_TIMEOUT_MINUTES):
                    session.pop('username', None)
                    session.pop('last_activity', None)
                    flash("You have been logged out due to inactivity.")
                    return redirect(url_for('login'))
            except Exception:
                # If parsing fails, reset last_activity
                session['last_activity'] = now.strftime("%Y-%m-%d %H:%M:%S")
        # Update last activity time
        session['last_activity'] = now.strftime("%Y-%m-%d %H:%M:%S")
# --- SESSION TIMEOUT FEATURE END ---

# Update the root route to show the welcome page instead of registration
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

# Add a separate route for the registration page
@app.route("/register_page", methods=["GET"])
def register_page():
    # Change to use RegsterPG1.html instead of home.html
    return render_template("RegsterPG1.html")

# **Login Route**
@app.route("/log", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["Email"]
        password = request.form["psw"]

        # Create the database connection
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="003150",
            database="travel"
        )
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute("SELECT * FROM accounts WHERE name = %s AND email = %s AND password = %s", (name, email, password))
        account = cursor.fetchone()

        # Ensure all results are read
        cursor.fetchall()

        if account:
            # Store the username in the session
            session['username'] = name
            return redirect("/Main")
        else:
            flash("Please check if you have entered name, email, or password correctly.")
            return redirect("/log")

    return render_template("loginPG2.html")  # Show login page

# Decorator to check if the user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("You need to be registered to view this page.")
            return redirect(url_for('The_First_PG'))
        return f(*args, **kwargs)
    return decorated_function

# **Register Route**
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]


    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor()

    # Check if the username or email already exists
    cursor.execute("SELECT * FROM accounts WHERE name = %s OR email = %s", (username, email))
    account = cursor.fetchone()

    if account:
        flash("Name or Email already in use. Please enter a different email or sign in.")
        return redirect("/")

    # Insert the data into the accounts table
    cursor.execute("INSERT INTO accounts (name, email, password) VALUES (%s, %s, %s)", (username, email, password))
    conn.commit()
    cursor.close()
    conn.close()

    # Store the username in the session
    session['username'] = username

    # Redirect to the main page
    return redirect("/Main")

# **Main Page (After Login)**
@app.route("/Main")
@login_required
def MainPG():
    # Retrieve the username from the session
    username = session.get('username', 'Guest')
    
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Fetch account type
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (username,))
    account_type_result = cursor.fetchone()
    account_type = account_type_result['account_type'] if account_type_result else 'Custmer'
    
    # Set is_admin flag
    is_admin = (account_type == 'Admin')
    
    cursor.close()
    conn.close()
    
    return render_template("MainPG.html", name=username, is_admin=is_admin)

# **Other Pages**
@app.route("/info")
@login_required
def The_info_pg():
    # Retrieve the username from the session
    username = session.get('username')
    
    if not username:
        flash("You need to be logged in to view this page.")
        return redirect("/log")
    
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Fetch the account information
    cursor.execute("SELECT name, email, password, account_type FROM accounts WHERE name = %s", (username,))
    account = cursor.fetchone()

    # Ensure all results are read
    cursor.fetchall()

    is_admin = account.get('account_type', 'Custmer') == 'Admin' if account else False

    cursor.close()
    conn.close()

    if not account:
        flash("Account not found.")
        return redirect("/log")

    return render_template("Info.html", account=account, is_admin=is_admin)

@app.route("/Book")
@login_required
def Bookingflight():
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Fetch flight information
    cursor.execute("SELECT idAir_jorneys, Depart, Arrive, Time_depart, Time_arrive, Seat_cost FROM flight_info")
    flight_data = cursor.fetchall()

    # Extract unique departure locations
    unique_departures = list(set(flight['Depart'] for flight in flight_data))

    # Retrieve the username from the session
    username = session.get('username', 'Guest')

    # Fetch account type
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (username,))
    account_type_result = cursor.fetchone()
    is_admin = account_type_result and account_type_result['account_type'] == 'Admin'

    cursor.close()
    conn.close()

    return render_template("booking.html", flight_data=flight_data, unique_departures=unique_departures, name=username, is_admin=is_admin)

@app.route("/select_flight", methods=["POST"])
@login_required
def select_flight():
    username = session.get('username')
    seats = request.form['seats']
    travel_date = request.form['travel_date']
    selected_flight = request.form['selected_flight']
    seat_type = request.form['seat_type']  # New seat type

    # Debugging: Print received form data
    print(f"Received form data: seats={seats}, travel_date={travel_date}, selected_flight={selected_flight}, seat_type={seat_type}")

    # Validate input data
    if not selected_flight.isdigit():
        flash("Invalid flight selection.")
        return redirect("/Book")

    if not seats.isdigit() or int(seats) <= 0:
        flash("Invalid number of seats.")
        return redirect("/Book")

    # Calculate days in advance
    try:
        travel_date_obj = datetime.strptime(travel_date, "%Y-%m-%d")
        booking_date = travel_date_obj  # Store the selected travel date as booking_date
        booking_time = datetime.now()   # Store the current datetime for booking_time (MySQL DATETIME)
        days_in_advance = (travel_date_obj - datetime.now()).days
    except Exception as e:
        flash("Invalid travel date format.")
        return redirect("/Book")

    # Discount logic (updated)
    discount = 0.0
    if 80 <= days_in_advance <= 90:
        discount = 0.25  # 25% discount
    elif 60 <= days_in_advance <= 79:
        discount = 0.15  # 15% discount
    elif 45 <= days_in_advance <= 59:
        discount = 0.10  # 10% discount
    # else: discount remains 0.0 for under 45 days

    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor()

    # Fetch the user ID
    cursor.execute("SELECT ID FROM accounts WHERE name = %s", (username,))
    user_id = cursor.fetchone()[0]

    # Fetch the seat cost for the selected flight
    cursor.execute("SELECT Seat_cost FROM flight_info WHERE idAir_jorneys = %s", (selected_flight,))
    seat_cost = cursor.fetchone()[0]
    seat_cost = float(seat_cost)  # Ensure seat_cost is a float

    # --- BUSINESS CLASS MULTIPLIER ---
    if seat_type.lower() == "business class":
        seat_cost *= 2

    # Calculate the total cost with discount
    total_cost = int(seats) * seat_cost
    discount_amount = total_cost * discount
    total_cost_after_discount = total_cost - discount_amount

    # Debugging: Print total cost and discount
    print(f"Total cost: {total_cost}, Discount: {discount*100}%, Final: {total_cost_after_discount}")

    # Insert the booking data into the booking_table
    try:
        cursor.execute("""
            INSERT INTO booking_table (user_id, flight_id, seats_booked, booking_date, booking_time, booking_status, seat_type, Booking_cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, int(selected_flight), int(seats), booking_date, booking_time, 'pending', seat_type, total_cost_after_discount))
        conn.commit()
        # Debugging: Print success message
        print("Booking data inserted successfully.")
    except mysql.connector.Error as err:
        # Debugging: Print error message
        print(f"Error: {err}")
        flash("An error occurred while processing your booking. Please try again.")
        return redirect("/Book")

    cursor.close()
    conn.close()

    return redirect("/sbooking")

@app.route("/sbooking", methods=["GET", "POST"])
@login_required
def sbooking():
    username = session.get('username')

    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Fetch account type
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (username,))
    account_type_result = cursor.fetchone()
    account_type = account_type_result['account_type'] if account_type_result else 'Custmer'
    
    # Set is_admin flag
    is_admin = (account_type == 'Admin')

    # Fetch booking information based on account type
    if account_type == 'Admin':
        cursor.execute("""
            SELECT 
                b.booking_id, 
                a.name as user_name, 
                a.email as user_email, 
                f.Depart as flight_depart, 
                f.Time_depart as depart_time,
                f.Arrive as flight_arrive,
                f.Time_arrive as arrive_time,
                b.booking_date,
                b.booking_status,
                b.seat_type,
                b.seats_booked,
                b.Booking_cost,
                f.Seat_cost,
                b.booking_date + INTERVAL 1 DAY as date_booked_for -- Include travel date
            FROM booking_table b
            JOIN accounts a ON b.user_id = a.ID
            JOIN flight_info f ON b.flight_id = f.idAir_jorneys
        """)
    else:
        cursor.execute("""
            SELECT 
                b.booking_id, 
                a.name as user_name, 
                a.email as user_email, 
                f.Depart as flight_depart, 
                f.Time_depart as depart_time,
                f.Arrive as flight_arrive,
                f.Time_arrive as arrive_time,
                b.booking_date,
                b.booking_status,
                b.seat_type,
                b.seats_booked,
                b.Booking_cost,
                f.Seat_cost,
                b.booking_date + INTERVAL 1 DAY as date_booked_for -- Include travel date
            FROM booking_table b
            JOIN accounts a ON b.user_id = a.ID
            JOIN flight_info f ON b.flight_id = f.idAir_jorneys
            WHERE a.name = %s
        """, (username,))
    
    bookings = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("sbooking.html", bookings=bookings, name=username, is_admin=is_admin)

@app.route("/delete_booking", methods=["POST"])
@login_required
def delete_booking():
    booking_id = request.form["booking_id"]
    
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    
    try:
        # Start a transaction
        conn.start_transaction()
        cursor = conn.cursor()
        
        # First, fetch the flight_id for this booking
        cursor.execute("SELECT flight_id FROM booking_table WHERE booking_id = %s", (booking_id,))
        result = cursor.fetchone()
        
        if result:
            flight_id = result[0]
            
            # Check if there are any payment records associated with this booking's flight_id
            cursor.execute("SELECT payment_id FROM payments_table WHERE booking_id = %s", (flight_id,))
            payment_records = cursor.fetchall()
            
            # If payment records exist, delete them first
            if payment_records:
                cursor.execute("DELETE FROM payments_table WHERE booking_id = %s", (flight_id,))
                
            # Now delete the booking
            cursor.execute("DELETE FROM booking_table WHERE booking_id = %s", (booking_id,))
            
            # Commit the transaction
            conn.commit()
            flash("Booking deleted successfully.")
        else:
            flash("Booking not found.")
    
    except mysql.connector.Error as err:
        # Rollback in case of error
        conn.rollback()
        flash(f"Error deleting booking: {err}")
        print(f"Database error: {err}")
    
    finally:
        # Close cursor and connection
        if 'cursor' in locals():
            cursor.close()
        conn.close()
    
    return redirect("/sbooking")

@app.route("/change_password", methods=["POST"])
@login_required
def change_password():
    current_password = request.form["current_password"]
    new_password = request.form["new_password"]
    username = session.get('username')


    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor()

    # Verify the current password
    cursor.execute("SELECT * FROM accounts WHERE name = %s AND password = %s", (username, current_password))
    account = cursor.fetchone()

    if not account:
        flash("Current password is incorrect.")
        return redirect("/info")

    # Update the password
    cursor.execute("UPDATE accounts SET password = %s WHERE name = %s", (new_password, username))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Password changed successfully.")
    return redirect("/info")

@app.route("/logout")
@login_required
def logout():
    session.pop('username', None)
    return redirect("/")

@app.route("/check", methods=["POST"])
@login_required
def checkout_page():
    booking_id = request.form["booking_id"]

    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Fetch booking details
    cursor.execute("""
        SELECT 
            b.booking_id,
            a.name as booking_name,
            a.email as booking_email,
            f.Depart as depart,
            f.Time_depart as depart_time,
            f.Arrive as arrive,
            f.Time_arrive as arrive_time,
            b.booking_date,
            b.seats_booked,
            b.Booking_cost,
            b.booking_date + INTERVAL 1 DAY as date_booked_for
        FROM booking_table b
        JOIN accounts a ON b.user_id = a.ID
        JOIN flight_info f ON b.flight_id = f.idAir_jorneys
        WHERE b.booking_id = %s
    """, (booking_id,))
    booking_details = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("checkout_pg.html", booking=booking_details)

@app.route("/payment_page", methods=["GET"])
@login_required
def payment_page():
    booking_id = request.args.get("booking_id")  # Get booking_id from query parameters

    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Fetch booking details
    cursor.execute("""
        SELECT 
            b.booking_id,
            a.name as booking_name,
            a.email as booking_email,
            f.Depart as depart,
            f.Time_depart as depart_time,
            f.Arrive as arrive,
            f.Time_arrive as arrive_time,
            b.booking_date,
            b.seats_booked,
            b.Booking_cost
        FROM booking_table b
        JOIN accounts a ON b.user_id = a.ID
        JOIN flight_info f ON b.flight_id = f.idAir_jorneys
        WHERE b.booking_id = %s
    """, (booking_id,))
    booking = cursor.fetchone()

    # Fetch account type
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (session.get('username'),))
    account_type_result = cursor.fetchone()
    is_admin = account_type_result and account_type_result['account_type'] == 'Admin'

    cursor.close()
    conn.close()

    if not booking:
        flash("Booking not found.")
        return redirect("/sbooking")

    return render_template("payment_details.html", booking=booking, is_admin=is_admin)

@app.route("/process_payment", methods=["POST"])
@login_required
def process_payment():
    username = session.get('username')
    booking_id = request.form["booking_id"]
    card_name = request.form["card_name"]
    card_number = request.form["card_number"]
    
    # Clean the card number - remove any non-digit characters
    card_number = ''.join(filter(str.isdigit, card_number))
    
    # Validate card number length
    if len(card_number) != 16:
        flash("Credit card number must be 16 digits.")
        return redirect(f"/payment_page?booking_id={booking_id}")
    
    # Store only the last 4 digits for security
    stored_card_number = card_number[-4:].zfill(4)  # Store just the last 4 digits, padded if needed
    
    expiry_date = request.form["expiry_date"]
    cvv = request.form["cvv"]
    payment_date = datetime.now()

    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor()

    # Fetch the user ID
    cursor.execute("SELECT ID FROM accounts WHERE name = %s", (username,))
    user_id = cursor.fetchone()[0]

    # Fetch the total price from the booking table
    cursor.execute("SELECT Booking_cost, flight_id FROM booking_table WHERE booking_id = %s", (booking_id,))
    result = cursor.fetchone()
    if not result:
        flash("Booking not found.")
        return redirect("/sbooking")
    
    total_price, flight_id = result
    
    # Insert payment details into the payments_table using flight_id instead of booking_id
    try:
        cursor.execute("""
            INSERT INTO payments_table(
                user_id, booking_id, total_price, payment_date, 
                payments_cardholder_name, payments_cardNum, 
                payments_Expiry_date, payments_CVV
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, flight_id, total_price, payment_date, card_name, stored_card_number, expiry_date, cvv))
        
        # Get the payment ID for the receipt
        payment_id = cursor.lastrowid
        
        # Update booking status to confirmed
        cursor.execute("UPDATE booking_table SET booking_status = 'confirmed' WHERE booking_id = %s", (booking_id,))
        
        conn.commit()
        
        # Redirect to receipt page with payment ID
        return redirect(f"/receipt/{payment_id}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        flash(f"Payment error: {err}")  # Show more detailed error to user
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return redirect("/sbooking")

@app.route("/receipt/<int:payment_id>")
@login_required
def receipt(payment_id):
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Fetch payment details with related information - explicitly select total_price
    cursor.execute("""
        SELECT 
            p.payment_id,
            p.user_id,
            p.booking_id,
            p.total_price, 
            p.payment_date,
            p.payments_cardholder_name,
            p.payments_cardNum,
            p.payments_Expiry_date,
            p.payments_CVV,
            a.name as booking_name,
            a.email as booking_email,
            f.Depart as depart,
            f.Time_depart as depart_time,
            f.Arrive as arrive,
            f.Time_arrive as arrive_time,
            b.seats_booked,
            b.booking_date,
            b.seat_type,
            b.booking_date + INTERVAL 1 DAY as date_booked_for -- Add this field
        FROM payments_table p
        JOIN accounts a ON p.user_id = a.ID
        JOIN booking_table b ON p.booking_id = b.flight_id
        JOIN flight_info f ON b.flight_id = f.idAir_jorneys
        WHERE p.payment_id = %s
    """, (payment_id,))
    payment = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if not payment:
        flash("Receipt not found.")
        return redirect("/sbooking")
    
    # Debug output to console
    print("Payment data retrieved:", payment)
    
    # Convert card number to string to allow slicing
    payment['payments_cardNum'] = str(payment['payments_cardNum'])
    
    # Ensure total_price is properly formatted
    if 'total_price' in payment and payment['total_price'] is not None:
        # Convert to float if needed
        try:
            payment['total_price'] = float(payment['total_price'])
        except (ValueError, TypeError):
            payment['total_price'] = 0.0
    else:
        payment['total_price'] = 0.0
    
    return render_template("receipt.html", payment=payment)

@app.route("/view_receipt/<int:booking_id>")
@login_required
def view_receipt(booking_id):
    username = session.get('username')
    
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)
    
    # First, check if the user has access to this booking
    cursor.execute("""
        SELECT b.booking_id, a.name 
        FROM booking_table b
        JOIN accounts a ON b.user_id = a.ID
        WHERE b.booking_id = %s
    """, (booking_id,))
    booking_owner = cursor.fetchone()
    
    # Fetch account type to check if admin
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (username,))
    account_type_result = cursor.fetchone()
    is_admin = account_type_result and account_type_result['account_type'] == 'Admin'
    
    # Ensure the user owns this booking or is an admin
    if booking_owner and (booking_owner['name'] == username or is_admin):
        # Fetch the payment associated with this booking
        cursor.execute("""
            SELECT 
                p.payment_id
            FROM payments_table p
            WHERE p.booking_id = (
                SELECT flight_id 
                FROM booking_table 
                WHERE booking_id = %s
            )
        """, (booking_id,))
        payment_result = cursor.fetchone()
        
        if payment_result:
            payment_id = payment_result['payment_id']
            cursor.close()
            conn.close()
            # Redirect to the existing receipt page
            return redirect(f"/receipt/{payment_id}")
        else:
            flash("No payment record found for this booking.")
            cursor.close()
            conn.close()
            return redirect("/sbooking")
    else:
        flash("You don't have permission to view this receipt.")
        cursor.close()
        conn.close()
        return redirect("/sbooking")

# Admin page route
@app.route("/admin")
@login_required
def admin_page():
    # Retrieve the username from the session
    username = session.get('username')
    
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Check if user is admin
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (username,))
    account_type_result = cursor.fetchone()
    is_admin = account_type_result and account_type_result['account_type'] == 'Admin'
    
    if not is_admin:
        flash("You don't have permission to access the admin page.")
        return redirect("/Main")
    
    # Fetch all users
    cursor.execute("SELECT ID, name, email, account_type FROM accounts")
    users = cursor.fetchall()
    
    # Fetch all bookings
    cursor.execute("""
        SELECT 
            b.booking_id, 
            a.name as user_name, 
            a.email as user_email, 
            f.Depart as flight_depart, 
            f.Time_depart as depart_time,
            f.Arrive as flight_arrive,
            f.Time_arrive as arrive_time,
            b.booking_date,
            b.booking_status,
            b.seat_type,
            b.seats_booked,
            b.Booking_cost
        FROM booking_table b
        JOIN accounts a ON b.user_id = a.ID
        JOIN flight_info f ON b.flight_id = f.idAir_jorneys
    """)
    bookings = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template("admin.html", name=username, users=users, bookings=bookings)

@app.route("/admin/accounts")
@login_required
def admin_accounts():
    # Retrieve the username from the session
    username = session.get('username')
    
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Check if user is admin
    cursor.execute("SELECT account_type, ID FROM accounts WHERE name = %s", (username,))
    account_result = cursor.fetchone()
    is_admin = account_result and account_result['account_type'] == 'Admin'
    current_user_id = account_result['ID'] if account_result else None
    
    if not is_admin:
        flash("You don't have permission to access the admin page.")
        return redirect("/Main")
    
    # Fetch all users with complete information including password
    cursor.execute("""
        SELECT 
            a.ID, 
            a.name, 
            a.email, 
            a.password, 
            a.account_type,
            COUNT(DISTINCT b.booking_id) as booking_count,
            IFNULL(SUM(p.total_price), 0) as total_spent
        FROM 
            accounts a
        LEFT JOIN 
            booking_table b ON a.ID = b.user_id
        LEFT JOIN 
            payments_table p ON b.flight_id = p.booking_id
        GROUP BY 
            a.ID, a.name, a.email, a.password, a.account_type
        ORDER BY 
            a.ID
    """)
    users = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template("admin_accounts.html", name=username, users=users, current_user_id=current_user_id)

@app.route("/admin/flights")
@login_required
def admin_flights():
    # Retrieve the username from the session
    username = session.get('username')
    
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Check if user is admin
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (username,))
    account_type_result = cursor.fetchone()
    is_admin = account_type_result and account_type_result['account_type'] == 'Admin'
    
    if not is_admin:
        flash("You don't have permission to access the admin page.")
        return redirect("/Main")
    
    # Fetch all flights
    cursor.execute("SELECT * FROM flight_info")
    flights = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template("admin_flights.html", name=username, flights=flights)

@app.route("/admin/bookings")
@login_required
def admin_bookings():
    # Retrieve the username from the session
    username = session.get('username')
    
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Check if user is admin
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (username,))
    account_type_result = cursor.fetchone()
    is_admin = account_type_result and account_type_result['account_type'] == 'Admin'
    
    if not is_admin:
        flash("You don't have permission to access the admin page.")
        return redirect("/Main")
    
    # Fetch all bookings with related data
    cursor.execute("""
        SELECT 
            b.booking_id, 
            a.name as user_name, 
            a.email as user_email, 
            f.Depart as flight_depart, 
            f.Arrive as flight_arrive,
            f.Time_depart as depart_time,
            f.Time_arrive as arrive_time,
            b.booking_date,
            b.booking_status,
            b.seat_type,
            b.seats_booked,
            b.Booking_cost
        FROM booking_table b
        JOIN accounts a ON b.user_id = a.ID
        JOIN flight_info f ON b.flight_id = f.idAir_jorneys
    """)
    bookings = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template("booking_management.html", name=username, bookings=bookings)

# Add a route to approve bookings
@app.route("/admin/approve_booking", methods=["POST"])
@login_required
def admin_approve_booking():
    booking_id = request.form["booking_id"]
    username = session.get('username')
    
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Check if user is admin
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (username,))
    account_type_result = cursor.fetchone()
    is_admin = account_type_result and account_type_result['account_type'] == 'Admin'
    
    if not is_admin:
        flash("You don't have permission to perform this action.")
        return redirect("/Main")
    
    # Update booking status to confirmed
    cursor.execute("UPDATE booking_table SET booking_status = 'confirmed' WHERE booking_id = %s", (booking_id,))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    flash("Booking has been approved successfully.")
    return redirect("/admin/bookings")

# Add a route to delete bookings from admin panel
@app.route("/admin/delete_booking", methods=["POST"])
@login_required
def admin_delete_booking():
    booking_id = request.form["booking_id"]
    username = session.get('username')
    
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Check if user is admin
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (username,))
    account_type_result = cursor.fetchone()
    is_admin = account_type_result and account_type_result['account_type'] == 'Admin'
    
    if not is_admin:
        flash("You don't have permission to perform this action.")
        return redirect("/Main")
    
    # Delete the booking
    cursor.execute("DELETE FROM booking_table WHERE booking_id = %s", (booking_id,))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    flash("Booking has been deleted successfully.")
    return redirect("/admin/bookings")

@app.route("/admin/sales")
@login_required
def admin_sales():
    # Retrieve the username from the session
    username = session.get('username')
    
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Check if user is admin
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (username,))
    account_type_result = cursor.fetchone()
    is_admin = account_type_result and account_type_result['account_type'] == 'Admin'
    
    if not is_admin:
        flash("You don't have permission to access the admin page.")
        return redirect("/Main")
    
    # Get current year for reports
    current_year = datetime.now().year
    
    # ========== OVERALL STATISTICS ==========
    # Total revenue
    cursor.execute("SELECT IFNULL(SUM(total_price), 0) as total_revenue FROM payments_table")
    total_revenue = float(cursor.fetchone()['total_revenue'])  # Convert to float
    
    # Total bookings
    cursor.execute("SELECT COUNT(*) as total_bookings FROM booking_table")
    total_bookings = cursor.fetchone()['total_bookings']
    
    # Unique customers who have made payments
    cursor.execute("""
        SELECT COUNT(DISTINCT user_id) as unique_customers 
        FROM payments_table
    """)
    unique_customers = cursor.fetchone()['unique_customers']
    
    # Average booking value
    avg_booking_value = total_revenue / total_bookings if total_bookings > 0 else 0
    
    # ========== MONTHLY REVENUE DATA ==========
    # Monthly sales for the current year
    cursor.execute("""
        SELECT 
            MONTH(payment_date) as month, 
            IFNULL(SUM(total_price), 0) as monthly_revenue
        FROM payments_table
        WHERE YEAR(payment_date) = %s
        GROUP BY MONTH(payment_date)
        ORDER BY month
    """, (current_year,))
    monthly_revenue_data = cursor.fetchall()
    
    # Create a list of 12 elements (one for each month) with 0 as default value
    monthly_data = [0] * 12
    
    # Fill in the actual values from database
    for item in monthly_revenue_data:
        # Adjust for 0-indexing (month from database is 1-12, array is 0-11)
        monthly_data[item['month']-1] = float(item['monthly_revenue'])
    
    # Find best performing month
    if monthly_revenue_data:
        best_month_data = max(monthly_revenue_data, key=lambda x: x['monthly_revenue'])
        month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
        best_month = {
            'name': month_names[best_month_data['month']-1],
            'revenue': best_month_data['monthly_revenue']
        }
    else:
        best_month = {'name': 'N/A', 'revenue': 0}
    
    # ========== ROUTE PERFORMANCE ==========
    # Get revenue, cost, and profit by route
    cursor.execute("""
        SELECT 
            CONCAT(f.Depart, ' to ', f.Arrive) as route_name,
            IFNULL(SUM(p.total_price), 0) as revenue,
            COUNT(b.booking_id) as bookings,
            f.Seat_cost as base_cost
        FROM flight_info f
        LEFT JOIN booking_table b ON f.idAir_jorneys = b.flight_id
        LEFT JOIN payments_table p ON b.flight_id = p.booking_id
        GROUP BY f.idAir_jorneys, route_name, base_cost
        ORDER BY revenue DESC
    """)
    route_data = cursor.fetchall()
    
    # Calculate profit and determine routes
    profitable_routes = []
    best_route = {'route_name': 'N/A', 'revenue': 0, 'profit': 0}
    
    for route in route_data:
        # Convert Decimal values to float before calculations
        revenue = float(route['revenue'])
        base_cost = float(route['base_cost'])
        bookings = route['bookings']
        
        # Simplified cost calculation (base cost * number of bookings * 0.6)
        # The 0.6 factor represents that 60% of the ticket price is cost
        estimated_cost = base_cost * bookings * 0.6 if bookings > 0 else 0
        profit = revenue - estimated_cost
        profit_margin = (profit / revenue * 100) if revenue > 0 else 0
        
        route_with_profit = {
            'route_name': route['route_name'],
            'revenue': revenue,
            'cost': estimated_cost,
            'profit': profit,
            'margin': profit_margin,
            'bookings': bookings
        }
        
        # Check if this is the best route by revenue
        if revenue > best_route['revenue']:
            best_route = route_with_profit
        
        # Add all routes to the profitable routes list (we're not separating loss routes anymore)
        profitable_routes.append(route_with_profit)
    
    # Sort routes by profit margin (descending)
    profitable_routes.sort(key=lambda x: x['profit'], reverse=True)
    
    # ========== TOP CUSTOMERS ==========
    cursor.execute("""
        SELECT 
            a.name,
            a.email,
            IFNULL(SUM(p.total_price), 0) as total_spent,
            COUNT(DISTINCT b.booking_id) as booking_count,
            MAX(b.booking_date) as last_booking
        FROM accounts a
        JOIN booking_table b ON a.ID = b.user_id
        JOIN payments_table p ON b.flight_id = p.booking_id
        GROUP BY a.ID, a.name, a.email
        ORDER BY total_spent DESC
        LIMIT 10
    """)
    top_customers = cursor.fetchall()
    
    # Calculate average booking value for each customer
    for customer in top_customers:
        # Convert Decimal values to float before calculations
        customer['total_spent'] = float(customer['total_spent'])
        customer['avg_booking'] = customer['total_spent'] / customer['booking_count'] if customer['booking_count'] > 0 else 0
        # Format the last booking date to be more readable
        customer['last_booking'] = customer['last_booking'].strftime('%Y-%m-%d')
    
    # ========== SALES BY JOURNEY ==========
    cursor.execute("""
        SELECT 
            f.Depart as depart,
            f.Arrive as arrive,
            IFNULL(SUM(p.total_price), 0) as total_sales,
            COUNT(b.booking_id) as bookings,
            GROUP_CONCAT(DISTINCT b.seat_type ORDER BY b.seat_type) as seat_types
        FROM flight_info f
        LEFT JOIN booking_table b ON f.idAir_jorneys = b.flight_id
        LEFT JOIN payments_table p ON b.flight_id = p.booking_id
        GROUP BY f.idAir_jorneys, f.Depart, f.Arrive
        ORDER BY total_sales DESC
    """)
    journey_sales = cursor.fetchall()
    
    # Calculate average price per seat
    for journey in journey_sales:
        # Convert Decimal values to float before calculations
        journey['total_sales'] = float(journey['total_sales'])
        journey['avg_price'] = journey['total_sales'] / journey['bookings'] if journey['bookings'] > 0 else 0
    
    # Prepare data for pie chart - ensure all values are float
    journey_labels = [f"{journey['depart']} to {journey['arrive']}" for journey in journey_sales[:7]]  # Top 7 routes
    journey_values = [journey['total_sales'] for journey in journey_sales[:7]]  # Already converted to float above
    
    # ========== MOST POPULAR SEAT TYPE ==========
    cursor.execute("""
        SELECT 
            seat_type as type,
            COUNT(*) as count
        FROM booking_table
        GROUP BY seat_type
        ORDER BY count DESC
        LIMIT 1
    """)
    popular_seat_result = cursor.fetchone()
    popular_seat = popular_seat_result if popular_seat_result else {'type': 'N/A', 'count': 0}
    
    cursor.close()
    conn.close()
    
    return render_template(
        "admin_sales.html", 
        name=username,
        current_year=current_year,
        total_revenue=total_revenue,
        total_bookings=total_bookings,
        unique_customers=unique_customers,
        avg_booking_value=avg_booking_value,
        monthly_data=monthly_data,
        profitable_routes=profitable_routes,
        top_customers=top_customers,
        journey_sales=journey_sales,
        journey_labels=journey_labels,
        journey_values=journey_values,
        best_route=best_route,
        best_month=best_month,
        popular_seat=popular_seat
    )

@app.route("/admin/reviews")
@login_required
def admin_reviews():
    # Retrieve the username from the session
    username = session.get('username')
    
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Check if user is admin
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (username,))
    account_type_result = cursor.fetchone()
    is_admin = account_type_result and account_type_result['account_type'] == 'Admin'
    
    if not is_admin:
        flash("You don't have permission to access the admin page.")
        return redirect("/Main")
    
    # Redirect to admin dashboard with a message since reviews feature isn't implemented
    flash("Review management feature is coming soon!")
    
    cursor.close()
    conn.close()
    
    return redirect("/admin")

@app.route("/contacts")
@login_required
def contacts():
    # Retrieve the username from the session
    username = session.get('username', 'Guest')
    
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Fetch account type
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (username,))
    account_type_result = cursor.fetchone()
    account_type = account_type_result['account_type'] if account_type_result else 'Custmer'
    
    # Set is_admin flag
    is_admin = (account_type == 'Admin')
    
    cursor.close()
    conn.close()
    
    return render_template("contacts.html", name=username, is_admin=is_admin)

@app.route("/send_message", methods=["POST"])
@login_required
def send_message():
    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")
    
    # In a real application, you would:
    # 1. Store this in a database
    # 2. Send an email notification
    # 3. Implement anti-spam measures
    
    # For now, we'll just simulate success
    flash("Thank you for your message! We'll get back to you shortly.")
    return redirect("/contacts")

@app.route("/admin/add_flight", methods=["POST"])
@login_required
def add_flight():
    # Retrieve the username from the session
    username = session.get('username')
    
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Check if user is admin
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (username,))
    account_type_result = cursor.fetchone()
    is_admin = account_type_result and account_type_result['account_type'] == 'Admin'
    
    if not is_admin:
        flash("You don't have permission to perform this action.")
        return redirect("/Main")
    
    # Get form data
    depart = request.form.get('depart')
    arrive = request.form.get('arrive')
    depart_time = request.form.get('depart_time')
    arrive_time = request.form.get('arrive_time')
    seat_cost = request.form.get('seat_cost')
    
    # Validate input
    if not all([depart, arrive, depart_time, arrive_time, seat_cost]):
        flash("All fields are required to add a new flight.")
        return redirect("/admin/flights")
    
    try:
        # Parse seat cost to ensure it's a valid float
        seat_cost = float(seat_cost)
        
        # Insert new flight
        cursor.execute("""
            INSERT INTO flight_info (Depart, Arrive, Time_depart, Time_arrive, Seat_cost)
            VALUES (%s, %s, %s, %s, %s)
        """, (depart, arrive, depart_time, arrive_time, seat_cost))
        
        conn.commit()
        flash(f"Flight from {depart} to {arrive} added successfully!")
    except mysql.connector.Error as err:
        flash(f"Database error: {err}")
    except ValueError:
        flash("Invalid seat cost. Please enter a valid number.")
    finally:
        cursor.close()
        conn.close()
    
    return redirect("/admin/flights")

@app.route("/admin/delete_flight", methods=["POST"])
@login_required
def delete_flight():
    # Retrieve the username from the session
    username = session.get('username')
    
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)

    # Check if user is admin
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (username,))
    account_type_result = cursor.fetchone()
    is_admin = account_type_result and account_type_result['account_type'] == 'Admin'
    
    if not is_admin:
        flash("You don't have permission to perform this action.")
        return redirect("/Main")
    
    # Get form data
    flight_id = request.form.get('flight_id')
    confirmation = request.form.get('confirmation')
    
    # Validate confirmation text
    if confirmation != 'DELETE':
        flash("Deletion confirmation failed. Flight was not deleted.")
        return redirect("/admin/flights")
    
    try:
        # First, check if the flight has any associated bookings
        cursor.execute("SELECT COUNT(*) as booking_count FROM booking_table WHERE flight_id = %s", (flight_id,))
        result = cursor.fetchone()
        booking_count = result['booking_count'] if result else 0
        
        if booking_count > 0:
            # Get flight details for the flash message
            cursor.execute("SELECT Depart, Arrive FROM flight_info WHERE idAir_jorneys = %s", (flight_id,))
            flight = cursor.fetchone()
            route = f"{flight['Depart']} to {flight['Arrive']}" if flight else f"ID: {flight_id}"
            
            # Warn about associated bookings and delete them first
            cursor.execute("DELETE FROM booking_table WHERE flight_id = %s", (flight_id,))
            flash(f"Warning: {booking_count} bookings were removed because they were associated with this flight ({route}).")
        
        # Now delete the flight
        cursor.execute("DELETE FROM flight_info WHERE idAir_jorneys = %s", (flight_id,))
        conn.commit()
        
        flash("Flight deleted successfully.")
    except mysql.connector.Error as err:
        conn.rollback()
        flash(f"Error deleting flight: {err}")
    finally:
        cursor.close()
        conn.close()
    
    return redirect("/admin/flights")

@app.route("/request_refund", methods=["POST"])
@login_required
def request_refund():
    booking_id = request.form["booking_id"]
    username = session.get('username')
    
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)
    
    # Fetch booking details and check if the user owns this booking
    cursor.execute("""
        SELECT 
            b.booking_id, 
            a.name as user_name, 
            a.email as user_email, 
            f.Depart as flight_depart, 
            f.Time_depart as depart_time,
            f.Arrive as flight_arrive,
            f.Time_arrive as arrive_time,
            b.booking_date,
            b.booking_status,
            b.seat_type,
            b.seats_booked,
            b.Booking_cost
        FROM booking_table b
        JOIN accounts a ON b.user_id = a.ID
        JOIN flight_info f ON b.flight_id = f.idAir_jorneys
        WHERE b.booking_id = %s AND a.name = %s AND b.booking_status = 'confirmed'
    """, (booking_id, username))
    
    booking = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if not booking:
        flash("Booking not found or cannot be refunded.")
        return redirect("/sbooking")
    
    return render_template("refund_request.html", booking=booking)

@app.route("/submit_refund", methods=["POST"])
@login_required
def submit_refund():
    booking_id = request.form["booking_id"]
    refund_reason = request.form["refund_reason"]
    refund_details = request.form["refund_details"]
    refund_method = request.form["refund_method"]
    username = session.get('username')
    
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Verify booking exists and belongs to user
        cursor.execute("""
            SELECT b.booking_id, a.ID as user_id, b.flight_id 
            FROM booking_table b
            JOIN accounts a ON b.user_id = a.ID
            WHERE b.booking_id = %s AND a.name = %s
        """, (booking_id, username))
        
        booking_info = cursor.fetchone()
        
        if not booking_info:
            flash("Booking not found or does not belong to you.")
            return redirect("/sbooking")
        
        # Change booking status to 'refund-pending'
        cursor.execute("""
            UPDATE booking_table 
            SET booking_status = 'refund-pending' 
            WHERE booking_id = %s
        """, (booking_id,))
        
        # Insert into a refund_requests table (you would need to create this table)
        # For now, we'll just update the status and could implement this fully later
        
        conn.commit()
        flash("Your refund request has been submitted successfully. We'll process it within 7-10 business days.")
        
    except mysql.connector.Error as err:
        conn.rollback()
        flash(f"Error processing refund request: {err}")
        print(f"Database error: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        conn.close()
    
    return redirect("/sbooking")

@app.route("/admin/edit_user/<int:user_id>", methods=["GET"])
@login_required
def admin_edit_user(user_id):
    username = session.get('username')
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)
    # Check if user is admin
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (username,))
    account_type_result = cursor.fetchone()
    is_admin = account_type_result and account_type_result['account_type'] == 'Admin'
    if not is_admin:
        flash("You don't have permission to access this page.")
        cursor.close()
        conn.close()
        return redirect("/Main")
    # Fetch user info
    cursor.execute("SELECT * FROM accounts WHERE ID = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if not user:
        flash("User not found.")
        return redirect("/admin/accounts")
    return render_template("admin_edit_user.html", user=user)

@app.route("/admin/update_user", methods=["POST"])
@login_required
def admin_update_user():
    username = session.get('username')
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)
    # Check if user is admin
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (username,))
    account_type_result = cursor.fetchone()
    is_admin = account_type_result and account_type_result['account_type'] == 'Admin'
    if not is_admin:
        flash("You don't have permission to perform this action.")
        cursor.close()
        conn.close()
        return redirect("/Main")
    # Get form data
    user_id = request.form.get("user_id")
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    account_type = request.form.get("account_type")
    # Update user info
    try:
        cursor.execute("""
            UPDATE accounts
            SET name = %s, email = %s, password = %s, account_type = %s
            WHERE ID = %s
        """, (name, email, password, account_type, user_id))
        conn.commit()
        flash("User details updated successfully.")
    except mysql.connector.Error as err:
        conn.rollback()
        flash(f"Error updating user: {err}")
    finally:
        cursor.close()
        conn.close()
    return redirect("/admin/accounts")

@app.route("/admin/edit_flight", methods=["POST"])
@login_required
def admin_edit_flight():
    username = session.get('username')
    # Create the database connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="003150",
        database="travel"
    )
    cursor = conn.cursor(dictionary=True)
    # Check if user is admin
    cursor.execute("SELECT account_type FROM accounts WHERE name = %s", (username,))
    account_type_result = cursor.fetchone()
    is_admin = account_type_result and account_type_result['account_type'] == 'Admin'
    if not is_admin:
        flash("You don't have permission to perform this action.")
        cursor.close()
        conn.close()
        return redirect("/Main")
    # Get form data
    flight_id = request.form.get("flight_id")
    depart = request.form.get("depart")
    arrive = request.form.get("arrive")
    depart_time = request.form.get("depart_time")
    arrive_time = request.form.get("arrive_time")
    seat_cost = request.form.get("seat_cost")
    # Validate input
    if not all([flight_id, depart, arrive, depart_time, arrive_time, seat_cost]):
        flash("All fields are required to edit the flight.")
        cursor.close()
        conn.close()
        return redirect("/admin/flights")
    try:
        seat_cost = float(seat_cost)
        cursor.execute("""
            UPDATE flight_info
            SET Depart = %s, Arrive = %s, Time_depart = %s, Time_arrive = %s, Seat_cost = %s
            WHERE idAir_jorneys = %s
        """, (depart, arrive, depart_time, arrive_time, seat_cost, flight_id))
        conn.commit()
        flash("Flight updated successfully.")
    except mysql.connector.Error as err:
        conn.rollback()
        flash(f"Error updating flight: {err}")
    except ValueError:
        flash("Invalid seat cost. Please enter a valid number.")
    finally:
        cursor.close()
        conn.close()
    return redirect("/admin/flights")

if __name__ == "__main__":
    app.run(debug=True)
