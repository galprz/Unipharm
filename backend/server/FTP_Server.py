from DB_Queries import DatabaseQueries
import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def analyze(x):
    yield [("5,96,60", "material 882"),("5,82,0", "material 872"),("-65,103,0", "material 463"),("-95,96,0", "material 820"),("5,131,60", "material 879"),("-115,89,30", "material 158"),("-105,117,60", "material 237"),("-105,131,0", "material 236"),("-25,110,30", "material 707"),("-25,12,0", "material 666")]
    yield [("-35,68,30", "material 629"),("-5,40,30", "material 797"),("-65,26,0", "material 626"),("-85,54,0", "material 767"),("-95,138,30", "material 299"),("-95,19,0", "material 247"),("5,75,0", "material 871"),("5,68,30", "material 868"),("-95,103,0", "material 283"),("-15,61,0", "material 745")]
    while(True):
        yield [("-35,68,30", "material 629"),("-5,40,30", "material 797"),("-65,26,0", "material 626"),("-85,54,0", "material 767"),("-95,138,30", "material 299"),("-95,19,0", "material 247"),("5,75,0", "material 871"),("5,68,30", "material 868"),("-95,103,0", "material 283"),("-15,61,0", "material 745")]


db = DatabaseQueries()
a = analyze(1)
y = 1

class FTP_Server:
    def __init__(self):
        self.authorizer = DummyAuthorizer()
        self.authorizer.add_anonymous(os.getcwd())

        self.handler = FTP_Server.FileReceiverHandler
        self.handler.authorizer = self.authorizer
        self.authorizer.add_user('user', '12345', '.', perm='elradfmwMT')
        self.handler.permit_foreign_addresses = True
        # Listen on 0.0.0.0:21 (TODO: change it?)
        self.address = ('192.168.0.4', 21)
        server = FTPServer(self.address, self.handler)
        server.serve_forever()


    class FileReceiverHandler(FTPHandler):
        def __init__(self, conn, server, ioloop):
            super().__init__(conn, server, ioloop=ioloop)
            self.db = db

        def on_file_received(self, file):
            """ When a file (video) received we should:
                read the barcodes,
                compare the results with the data stored in Unipharm's DB
                and emit any mismatches to a log file """
            actual_data = next(a)  # analyze gets a video and returns a list of tuples (location, material)
            self.__compare_and_log(actual_data)

        def __compare_and_log(self, data):
            for loc, material in data:
                self.db.check_box_status(loc, material)


if __name__ == '__main__':
    FTP_Server()
