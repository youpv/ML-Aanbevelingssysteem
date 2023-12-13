from dotenv import load_dotenv
load_dotenv()
import os
import psycopg2
from flask import Flask, jsonify, g
from flask_cors import CORS
# from OUD_recommendations import get_recommendations
from recommendationEngine import get_recommendations_please


app = Flask(__name__)
CORS(app)

def get_db():
    """Verbind met de database."""
    if 'db' not in g:
        g.db = psycopg2.connect(os.getenv("DATABASE_URL"))
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    """Sluit de database connectie."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def fetch_all_products():
    """Fetch alle producten van de database."""
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM products")
        return cur.fetchall()
    
def fetch_all_orders():
    """Fetch alle orders van de database."""
    db = get_db()
    with db.cursor() as cur:
        cur.execute("SELECT * FROM orders")
        return cur.fetchall()

with app.app_context():
    """Fetch alle data bij de start van de applicatie."""
    all_products = fetch_all_products()
    all_orders = fetch_all_orders()

@app.route("/api/recommendation/<string:product_handle>", methods=["GET"])
@app.route("/api/recommendation/<string:product_handle>/<int:num_recs>", methods=["GET"])
@app.route("/api/recommendation/<string:product_handle>/<int:num_recs>/<string:customer_id>", methods=["GET"])
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