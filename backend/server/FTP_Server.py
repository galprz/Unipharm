from DB_Queries import DatabaseQueries
import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from BarcodesCoupling import *


db = DatabaseQueries()

class FTP_Server:
    def __init__(self):
        self.authorizer = DummyAuthorizer()
        self.authorizer.add_anonymous(os.getcwd())

        self.handler = FTP_Server.FileReceiverHandler
        self.handler.authorizer = self.authorizer
        self.authorizer.add_user('user', '12345', '.', perm='elradfmwMT')
        self.handler.permit_foreign_addresses = True
        
        self.address = ('192.168.100.66', 21)
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


if __name__ == '__main__':
    FTP_Server()
