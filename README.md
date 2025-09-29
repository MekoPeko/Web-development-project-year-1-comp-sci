# Student ID - 2400965 , Student name - Harry Masters 
# Horizen Travels Web Application

**Student ID:** 2400965  
**Student Name:** Harry Masters

---

## Database Information

- **Database Name:** `travil`
- **Database Username:** `root`
- **Database Password:** `003150`

### Tables

| Table Name      | Description                                 |
|-----------------|---------------------------------------------|
| `accounts`      | Stores user account information             |
| `flight_info`   | Stores all flight details                   |
| `booking_table` | Stores booked flights                       |
| `payments_table`| Stores payment and card information         |

### Accounts

| Account Type | Name   | Email             | Password |
|--------------|--------|-------------------|----------|
| Admin        | Harry  | Harry@gmail.com   | 112233   |
| Customer     | Ollie  | ben@gmail.com     | 12345    |

---

## Overview

Horizen Travels is a web-based flight booking system built with **Python (Flask)**, **MySQL**, and **HTML/CSS/JS**.  
It allows users to register, book flights, manage bookings, make payments, and request refunds.  
**Admin users** can manage flights, bookings, accounts, and view sales analytics.

---

## Features

- **User Registration & Login**
- **Flight Search & Booking**
- **Dynamic Discounts for Early Bookings**
- **Booking Management (View, Delete, Refund)**
- **Secure Payment Processing**
- **PDF Receipt Generation**
- **Admin Dashboard**
  - Manage Users, Flights, Bookings
  - View Sales Reports & Analytics
- **Responsive Design**

---

## Setup Instructions

### 1. Requirements

- Python 3.x
- MySQL Server
- pip (Python package manager)

### 2. Install Python Dependencies

```bash
pip install flask mysql-connector-python
```

### 3. Database Setup

1. Create a MySQL database named `travel`.
2. Import the required tables (`accounts`, `flight_info`, `booking_table`, `payments_table`, etc.).
3. Update the MySQL connection credentials in `index.py` if needed.

### 4. Running the Application

```bash
python index.py
```

- The app will run on [http://127.0.0.1:5000/](http://127.0.0.1:5000/) by default.

---

## Project Structure

```
project/
│
├── index.py                # Main Flask application
├── dbfunc.py               # (Optional) Database helper functions
├── templates/              # HTML templates (Jinja2)
│   ├── *.html
├── static/                 # Static files (CSS, JS, images)
│   ├── *.css
│   ├── *.js
├── README.md               # This file
```

---

## Usage

- Visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.
- Register a new account or log in.
- Book flights, manage your bookings, and make payments.
- Admin users can access `/admin` for management features.

---

## Admin Access

- To access admin features, set the `account_type` of a user to `Admin` in the `accounts` table.

---

## Security Notes

- **Passwords are stored in plaintext for demonstration. Do not use in production.**
- Card numbers are not stored in full; only the last 4 digits are kept for receipts.
- Session timeout is set to 5 minutes of inactivity.

---

## Credits

Developed by **Harry Masters (2400965)** for UWE Bristol WaD project.

