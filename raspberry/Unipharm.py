#!/usr/bin/python3
import sys
import json
from time import sleep
import ftplib
from picamera import PiCamera

#  Load data from configuration file.
with open("/home/pi/Desktop/Unipharm_config.json") as config_file:
    data = json.load(config_file)

#  Following function tries to take a video of the predefined length and store it on the given path.
#  Returns True if successful or False if something is wrong with the camera.


def get_video(output_path):
    success = False
    with PiCamera() as camera:
        camera.framerate = data["framerate"]
        camera.start_recording(output_path)
        sleep(data["video_length"])
        camera.stop_recording()
        success = True

    return success


def connect_to_server():
    success = False

    try:
        session = ftplib.FTP()
        session.connect(data["server_url"], data["port"])
        session.login(data["username"], data["password"])
        success = True
    except Exception:
        session = False
    return session, success


def routine():
    session, success = connect_to_server()
    while not success:
        #  retry until successful in connecting to the server
        sleep(5)
        session, success = connect_to_server()
    while True:
        if get_video(
                f'/home/pi/Desktop/vid_{data["identifier"]}_{data["side"]}_1'):
            # Send video to the servetr using FTP
            with open(f'/home/pi/Desktop/vid_{data["identifier"]}_{data["side"]}_1', 'rb') as file:
                session.storbinary(
                    f'STOR vid_{data["identifier"]}_{data["side"]}_1.mp4', file)
        # wait either for the video to be sent or just wait to try again because there was a problem with the camera.
        sleep(3)


if __name__ == "__main__":
    print("hello world!")
    print(sys.version)
    print("Starting")
    routine()
    print("Done")
