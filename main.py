from dotenv import load_dotenv
load_dotenv() 
import psycopg2
from flask import Flask, jsonify, g
from flask_cors import CORS
from recommendations import get_recommendations, get_dataframe_from_products
import os


# Zorg meteen voor CORS support
app = Flask(__name__)
CORS(app)
print(os.getenv("DATABASE_URL"))

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(os.getenv("DATABASE_URL"))
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    # close the database connection if it exists
    db = g.pop('db', None)
    if db is not None:
        db.close()

def fetch_all_products():
    # fetch all products from the database
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    cur.close()
    return rows

with app.app_context():
    all_products = fetch_all_products()


# Beide routes aanmaken zodat je zowel los een product als product met aantal aanbevelingen kan opvragen
@app.route("/api/recommendation/<string:product_handle>", methods=["GET"])
@app.route("/api/recommendation/<string:product_handle>/<int:num_recs>", methods=["GET"])
# Functie om aanbevelingen op te vragen
def get_recommendation(product_handle, num_recs=999999999):
    try:
        # Krijg aanbevelingen
        recommendations = get_recommendations(product_handle, products=all_products, num_recs=num_recs)
        # return aanbevelingen als JSON
        return jsonify({
            'active_product': product_handle,
            'recommendations': recommendations
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5137)