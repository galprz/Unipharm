import cv2


def load(path: str) -> cv2.VideoCapture:
    """Load video from path.

    Args:
        path (str): The video's path

    Returns:
        cv2.VideoCapture: The VideoCapture of the given video.
    """
    return cv2.VideoCapture(path)


def sample(videoCapture: cv2.VideoCapture, sampleStep=1, startTime=0, length=0) -> list:
    """Samples frames from a given VideoCapture.

    Args:
        videoCapture (cv2.VideoCapture): The VideoCapture of the video from which to sample.
        sampleStep (int, optional): The number of frames to skip between to kept frames. Defaults to 1.
        startTime (int, optional): The time in the video from which to start sampling. Defaults to 0.
        length (int, optional): The sampled interval length. Defaults to 0.

    Returns:
        list: A list of the sampled frames.
    """
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
