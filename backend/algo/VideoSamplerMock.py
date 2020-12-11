import cv2
import os


def sample(self: VideoSampler, path: str, length: int, fps: int, rate: int) -> list:
     os.chdir("D:\\Unifarm\\U\\Unipharm\\backend\\algo\\data")
    img = cv2.imread('uni4.png')
    return [img]
