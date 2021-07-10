from DB_Queries import DatabaseQueries
import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from flask import *
import json
import sys
sys.path.append('../algo')
from BarcodesCoupling import *


db = DatabaseQueries()

# Initialize Flask app
app = Flask(__name__)
port_num = 8080
ip = '0.0.0.0'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET'])
def show_form():
    # Display the form responsible for parameter tuning
    try:
        return render_template("tune_params_form.html", sample_rate="7")
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/', methods=['POST'])
def update_params():
    try:
        # Load json file containing the tuning parameters
        with open("barcode_params.json", "r") as jsonFile:
            data = json.load(jsonFile)
        # Get the new values that the user submitted
        data["sample_rate"] = request.form['sample_rate']
        data["crop"] = request.form['crop']
        # Update json with the new values
        with open("barcode_params.json", "w") as jsonFile:
            json.dump(data, jsonFile)
        return render_template("tune_params_form.html", sample_rate="7")
    except Exception as e:
        return f"An Error Occured: {e}"

class FTP_Server:
    def __init__(self):
        self.authorizer = DummyAuthorizer()
        self.authorizer.add_anonymous(os.getcwd())

        self.handler = FTP_Server.FileReceiverHandler
        self.handler.authorizer = self.authorizer
        self.authorizer.add_user('user', '12345', '.', perm='elradfmwMT')
        self.handler.permit_foreign_addresses = True
        
        self.address = (ip, 21)
        server = FTPServer(self.address, self.handler)
        server.serve_forever()


    class FileReceiverHandler(FTPHandler):
        def __init__(self, conn, server, ioloop):
            super().__init__(conn, server, ioloop=ioloop)
            self.db = db

        def on_file_received(self, file):
            """ When a file (video) received we should:
                read the barcodes,
                compare the results with the data stored in Unipharm's DB,
                emit any mismatches to a log file,
                and delete the video file from server's storage """
            actual_data = couple_barcodes(file)
            self.__compare_and_log(actual_data)
            os.remove(file)

        def __compare_and_log(self, data: BarcodesTrios):
            for trio in data:
                self.db.check_box_status(trio.location.data, trio.material.data, trio.raft.data)

port = int(os.environ.get('PORT', port_num))
if __name__ == '__main__':
    app.run(threaded=True, host=ip, port=port, debug=True)
    FTP_Server()
