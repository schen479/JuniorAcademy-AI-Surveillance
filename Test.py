import cv2

cap = cv2.VideoCapture("Video/video1.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)