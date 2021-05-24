#from picamera import PiCamera
import os
from time import sleep
import ftplib


file1_path = r'D:\sec_yearly_fold\Unipharm\raspberry\1_6_vid.mp4'
file2_path = r'D:\sec_yearly_fold\Unipharm\raspberry\7_12_vid.mp4'
forklift_id = '1'
side = 'left'
server_url, username, password = "192.168.0.4:21", "user", "12345"
#camera = PiCamera()
session = ftplib.FTP()
session.connect("192.168.0.4", 21)
session.login(username, password)
#h264_file_name = '/home/pi/Desktop/video.h264'
#mp4_file_name = '/home/pi/Desktop/video.mp4'
video_length = 5


def m():
    for x in range(1):
        # camera.start_preview()
        #    camera.start_recording(h264_file_name)
        # sleep(video_length)
        # camera.stop_recording()
        # camera.stop_preview()
        # os.system(
        # f'MP4Box -add {h264_file_name} {mp4_file_name}')
        # file = open(mp4_file_name, 'rb')   # file to send
        file = open(file1_path, 'rb')
        session.storbinary(f'STOR vid_{forklift_id}_{side}_1.mp4',
                           file)     # send the file
    # session.storbinary(f'STOR {mp4_file_name}',
        #                   file)     # send the file
        file.close()
        # os.remove(h264_file_name)
        # os.remove(mp4_file_name)
        sleep(5)
        file = open(file2_path, 'rb')
        session.storbinary(f'STOR vid_{forklift_id}_{side}_2.mp4',
                           file)
        file.close()


if __name__ == "__main__":
    m()
