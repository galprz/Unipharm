import cv2


def load(path):
    return cv2.VideoCapture(path)


def sample(videoCapture, sampleStep=1, startTime=0, length=0):
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    frame_count = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
    success, frame = videoCapture.read()
    duration = frame_count / fps
    count = 0
    resultFrames = []
    while success:
        if count >= startTime * fps and count <= (startTime+duration)*fps and count % sampleStep == 0:
            resultFrames.append(frame)
        count += 1
        success, frame = videoCapture.read()

    return resultFrames
