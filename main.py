from dotenv import load_dotenv
load_dotenv()
import os
import psycopg2
from flask import Flask, jsonify, g
from flask_cors import CORS
from recommendations import get_recommendations

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

# Fetch all products at the start
with app.app_context():
    all_products = fetch_all_products()

@app.route("/api/recommendation/<string:product_handle>", methods=["GET"])
@app.route("/api/recommendation/<string:product_handle>/<int:num_recs>", methods=["GET"])
def get_recommendation(product_handle, num_recs=99999):
    """API endpoint to get product recommendations."""
    try:
        recommendations = get_recommendations(product_handle, products=all_products, num_recs=num_recs)
        return jsonify({'active_product': product_handle, 'recommendations': recommendations})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5137)