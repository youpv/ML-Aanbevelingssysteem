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
    
# @app.route("/api/products", methods=["POST"])
# def process_products():
#     try:
#         # Extract products from request data
#         products = request.json.get('products', {}).get('edges', [])
#         data.global_products = products
#         print("Products updated")
#         print(data.global_products)
        
#         # Trim down to 4 products
#         trimmed_products = products[:4]
        
#         # Extract product IDs
#         product_ids = [product['node']['id'] for product in trimmed_products]
        
#         return jsonify({
#             'recommendedIds': product_ids
#         })
#     except Exception as e:
#         import traceback
#         traceback.print_exc()  # This will print the detailed error to the console
#         return jsonify({
#             'error': str(e)
#         }), 500







# from flask import Flask, jsonify, request
# from flask_cors import CORS
# from recommendations import get_recommendations

# app = Flask(__name__)
# CORS(app)

# @app.route("/api/recommendation/<string:product_handle>", methods=["GET", "POST"])
# @app.route("/api/recommendation/<string:product_handle>/<int:num_recs>", methods=["GET", "POST"])
# def get_recommendation(product_handle, num_recs=999999999):
#     products = None
#     # If it's a POST request, extract the products
#     if request.method == "POST":
#         try:
#             products = request.json.get('products', {}).get('edges', [])
#         except Exception as e:
#             import traceback
#             traceback.print_exc()  # This will print the detailed error to the console
#             return jsonify({
#                 'error': str(e)
#             }), 500

#     # Process the recommendation request
#     try:
#         recommendations = get_recommendations(product_handle, products, num_recs=num_recs)
#         return jsonify({
#             'active_product': product_handle,
#             'recommendations': recommendations
#         })
#     except Exception as e:
#         return jsonify({
#             'error': str(e)
#         }), 500

# if __name__ == '__main__':
#     app.run(debug=True, port=5137)




# JA NU MOET JE NOG EVEN ZORGEN DAT JE IN DE NEXTJS APP NOG EVEN DIE POST COMBINEERT MET DE ANDERE SHIT.







# from flask import Flask, jsonify
# import requests

# app = Flask(__name__)

# @app.route('/fetch-hello-world')
# def fetch_hello_world():
#     # Define the URL of the Next.js API endpoint
#     url = "https://6eca-94-247-4-243.ngrok-free.app/api/helloWorld"

#     # Define the headers with the authentication token
#     headers = {
#         "X-Auth-Token": "WatIsDitKutZeg"  # Replace with your static token
#     }

#     # Fetch the endpoint with the headers
#     response = requests.get(url, headers=headers)

#     # Check if the request was successful
#     if response.status_code == 200:
#         data = response.json()
#         print(data['message'])  # Print the "Hello World" message
#         return jsonify(data)
#     else:
#         return "Failed to fetch the endpoint", 500


# @app.route('/get-all-products')
# def get_all_products():
#     try:
#         # Use the products data to fetch the products from the Shopify API
#         url = "https://youpteststore1.myshopify.com/products.json?limit=10"
#         response = requests.get(url)
#         print(response.content)
#         # Return the products data as JSON
#         return response.json()
#     except Exception as e:
#         return jsonify({
#             'error': str(e)
#         }), 500


# if __name__ == '__main__':
#     app.run(debug=True)
