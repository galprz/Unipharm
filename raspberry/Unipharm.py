from picamera import PiCamera
import os
from time import sleep
import ftplib
server_url, username, password = "", "", ""
camera = PiCamera()
session = ftplib.FTP(server_url, username, password)
while(True):
    camera.start_preview()
    camera.start_recording('/home/pi/Desktop/video.h264')
    sleep(5)
    camera.stop_recording()
    camera.stop_preview()
    os.system(
        "MP4Box -add /home/pi/Desktop/video.h264.h264 /home/pi/Desktop/video.h264.mp4")
    file = open('/home/pi/Desktop/video.h264.mp4', 'rb')   # file to send
    session.storbinary('STOR /home/pi/Desktop/video.h264.mp4',
                       file)     # send the file
    file.close()
    os.remove("/home/pi/Desktop/video.h264")
    os.remove("/home/pi/Desktop/video.mp4")
