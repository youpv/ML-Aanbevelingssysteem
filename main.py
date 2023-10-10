from flask import Flask, jsonify
from flask_cors import CORS
from recommendations import get_recommendations

# Zorg meteen voor CORS support
app = Flask(__name__)
CORS(app)

# Beide routes aanmaken zodat je zowel los een product als product met aantal aanbevelingen kan opvragen
@app.route("/api/recommendation/<string:product_handle>", methods=["GET"])
@app.route("/api/recommendation/<string:product_handle>/<int:num_recs>", methods=["GET"])

# Functie om aanbevelingen op te vragen
def get_recommendation(product_handle, num_recs=999999999):
    try:
        recommendations = get_recommendations(product_handle, num_recs=num_recs)
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