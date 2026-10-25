# ConstructionMart — Civil Engineering Materials Purchase Website

Project engineer: Minot Kumar

A starter Django project for browsing construction materials, calculating prices, managing a shopping cart, and submitting sample orders.

## Features
- Product catalogue: cement, steel, bricks, sand and aggregates
- Search and category filters
- Quantity and price calculator on product cards
- Session-based shopping cart
- Demo checkout and order confirmation
- Admin interface for managing products and orders
- Responsive layout

## Run on Windows
1. Install Python 3.10+.
2. Extract the ZIP and open a terminal inside the `ConstructionMart` folder.
3. Create and activate a virtual environment:
   ```bat
   py -m venv venv
   venv\Scripts\activate
   ```
4. Install dependencies:
   ```bat
   pip install -r requirements.txt
   ```
5. Create the database tables:
   ```bat
   python manage.py migrate
   ```
6. Load demo products:
   ```bat
   python manage.py seed_products
   ```
7. Start the development server:
   ```bat
   python manage.py runserver
   ```
8. Open http://127.0.0.1:8000/

## Admin login
Create your own admin user with:
```bat
python manage.py createsuperuser
```
Then open http://127.0.0.1:8000/admin/

## Important
This is a learning/demo project. Checkout does not collect real payments and does not contact real suppliers. Prices and stock are sample values. Before production use, add authentication, payment gateway integration, delivery policies, security review, and verified supplier/material information.
