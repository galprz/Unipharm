from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime


class DatabaseQueries:
    def __init__(self):
        cred = credentials.Certificate('key.json')
        initialize_app(cred)
        self.db = firestore.client()

    def get_material_by_location(self, location_id):
        try:
            location = self.db.collection('actual_locations').document(
                location_id).get().to_dict()
            material_saved = location['material']
        except Exception as e:
            print(f"An Error Occurred: {e}")
            return None
        return material_saved

    def check_box_status(self, location_id, material_expected):
        """
            box_status() : Returns true if the material that was passed is the material recorded in firebase under the location passed,
            otherwise false.
            Ensure you pass a location id and material as part of json body in post request,
            e.g. json={'location_id': '-105,103,30', 'material': 'material 224'}
        """
        material_found = self.get_material_by_location(location_id)
        if material_expected == material_found:
            return True
        elif material_found:
            with open('log.txt', 'a') as outfile:
                outfile.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " " +
                              location_id + " " + material_expected + " " + material_found + "\n")
            return False
