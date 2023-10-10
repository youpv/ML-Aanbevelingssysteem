from flask import Flask, jsonify
from flask_cors import CORS
from recommendations import get_recommendations

app = Flask(__name__)
CORS(app)

@app.route("/api/recommendation/<string:product_handle>", methods=["GET"])
@app.route("/api/recommendation/<string:product_handle>/<int:num_recs>", methods=["GET"])
def get_recommendation(product_handle, num_recs=999999999):
    try:
        recommendations = get_recommendations(product_handle, num_recs=num_recs)
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