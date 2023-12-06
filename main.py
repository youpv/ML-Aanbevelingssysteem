from dotenv import load_dotenv
load_dotenv()
import os
import psycopg2
from flask import Flask, jsonify, g
from flask_cors import CORS
from recommendations import get_recommendations
from recommendationEngine import get_recommendations_please

# Initialize Flask application with CORS support
app = Flask(__name__)
CORS(app)

def get_db():
    """Establish a database connection."""
    if 'db' not in g:
        g.db = psycopg2.connect(os.getenv("DATABASE_URL"))
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    """Close the database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def fetch_all_products():
    """Fetch all products from the database."""
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM products")
        return cur.fetchall()
    
def fetch_all_orders():
    """Fetch all orders from the database."""
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM orders")
        return cur.fetchall()

# Fetch all products and orders at the start
with app.app_context():
    all_products = fetch_all_products()
    all_orders = fetch_all_orders()

@app.route("/api/recommendation/<string:product_handle>", methods=["GET"])
@app.route("/api/recommendation/<string:product_handle>/<int:num_recs>", methods=["GET"])
@app.route("/api/recommendation/<string:product_handle>/<int:num_recs>/<string:customer_id>", methods=["GET"])
# voeg hier dadelijk na het eten ook een optie toe om de gebruiker ID mee te geven.
def get_recommendation(product_handle, num_recs=99999, customer_id=None):
    """API endpoint to get product recommendations."""
    try:
        # recommendations = get_recommendations(product_handle, products=all_products, num_recs=num_recs)
        recommendations = get_recommendations_please(product_handle, products=all_products, orders=all_orders, customer_id=customer_id, num_recs=num_recs)
        return jsonify({'active_product': product_handle, 'recommendations': recommendations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5137)