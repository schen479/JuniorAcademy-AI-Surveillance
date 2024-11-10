#Download these libraries if you don't have them install already
import cv2
import torch
import mediapipe as mp
import warnings
import os
import datetime


BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


model_path = "pose_landmarker_full.task"
options = PoseLandmarkerOptions(
  base_options=BaseOptions(model_asset_path=model_path),
  running_mode=VisionRunningMode.VIDEO)


model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


#File for video processing and filtering


# #Stephen
# #Send a video to one of two server (local servers used for testing). If anomaly is detected, send to central
# #if no anomaly is detected, save temporarily in local server.
def send_Video(path, suspicion):
  return 0


# #Shubh
# #Deletes all footage if no anomaly is detected in 5 minutes
def delete_Footage():
  return 0


#Shubh
#Get objects of the shelves that are subjected to shoplifting using YOLO.
def get_Obj(frame):
    # define objects ex. soda cans, box of cereals
  results = model(frame)
  detections = results.xyxy[0]

  objs = []

  for *box, conf, cls in detections:
    x1, y1, x2, y2 = map(int, box)
    label = model.names[int(cls)]
    objs.append({
      "label": label,
      "confidence": float(conf),
      "box": [x1, y1, x2, y2]
    })
   
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
   
  return objs
   
#Stephen
#Returns the points of a person's body using OpenPose
def get_Pose_Points(frame, timestamp):
  with PoseLandmarker.create_from_options(options) as landmarker:
    mp_frame = mp.Image(image_format = mp.ImageFormat.SRGB, data = frame)
    pose_result = landmarker.detect_for_video(mp_frame, timestamp)


    if pose_result.pose_landmarks:
      for landmark in pose_result.pose_landmarks:
        x, y = int(landmark.x * frame.shape[0]), int(landmark.y * frame.shape[1])
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)


    if pose_result.pose_landmarks:
        return pose_result.pose_landmarks
    return None

#Alan
#Takes in the body points and location of items in the store and
#detects for shoplifting if items are too close to certain body parts
def detect_Anomaly(objects, pose_points):
    # check if object is in hand of person
    suspicion = False
    shoplifting = False

#Stephen
#Main function for parsing a video, dividing it into smaller clips, and running the Ai model to
#see if there's an anomaly in each clip
def process_Video(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  #figure why is this 0
    frame_duration = 1 / fps  


    frame_count = 0
    while frame_count < 2:
        ret, frame = cap.read()
       
        if not ret:
            break

        print("hello")
        timestamp = frame_count * frame_duration
        timestamp = int(timestamp * 1e6)
        frame_count += 1


        detected_objects = get_Obj(frame)  
        pose_landmarks = get_Pose_Points(frame, timestamp)


        if frame is not None and ret:
            cv2.imshow("Shoplifting Detector", frame)
        is_suspicious = detect_Anomaly(pose_landmarks, detected_objects)
        send_Video(video_path, is_suspicious)
        delete_Footage()
    cap.release()
    cv2.destroyAllWindows()

process_Video("Videos\\video1.mp4")


