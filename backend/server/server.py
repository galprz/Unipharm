# app.py

# Required imports
import os
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

# Initialize Flask app
app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
locations_ref = db.collection('actual_locations')

# Conn Constants
port_num = 8080
ip = '0.0.0.0'

@app.route('/box_status', methods=['GET'])
def box_status():
    """
        box_status() : Returns true if the material that was passed is the material recorded in firebase under the location passed,
        otherwise false.
        Ensure you pass a location id and material as part of json body in post request,
        e.g. json={'location_id': '-105,103,30', 'material': 'material 224'}
    """
    try:
        # Check if ID and material were passed to URL query
        location_id_passed = request.args.get('location_id')
        material_passed = request.args.get('material')
        if location_id_passed and material_passed:
            location = locations_ref.document(location_id_passed).get().to_dict()
            material_saved = location['material'] 
            if material_passed == material_saved:
                return jsonify({"success": True}), 200
            else:
                return jsonify({"success": False}), 200
        else:
            return f"You didn't format the GET request as needed"
    except Exception as e:
        return f"An Error Occured: {e}"

port = int(os.environ.get('PORT', port_num))
if __name__ == '__main__':
    app.run(threaded=True, host=ip, port=port)