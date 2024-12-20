#Download these libraries if you don't have them install already
import cv2
import torch
import mediapipe as mp
import warnings
import os
import time
import shutil


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


object_tracker = {}
global is_suspicious


# #Send a video to one of two server (local servers used for testing). If anomaly is detected, send to central
# #if no anomaly is detected, save temporarily in local server.
def send_Video(path):
  global is_suspicious
  server_path = "Main" if is_suspicious else "Side"
  shutil.move(path, server_path)
 
# #Deletes all footage if no anomaly is detected in 5 minutes
def delete_Footage():
  shutil.rmtree("Side")
  os.makedirs("Side")


#Get objects of the shelves that are subjected to shoplifting using YOLO.
def get_Obj(frame):
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
   
  return objs
   
#Returns the points of a person's body using OpenPose
def get_Pose_Points(frame, timestamp):
  with PoseLandmarker.create_from_options(options) as landmarker:
    mp_frame = mp.Image(image_format = mp.ImageFormat.SRGB, data = frame)
    pose_result = landmarker.detect_for_video(mp_frame, timestamp)


    if pose_result.pose_landmarks:
      return pose_result.pose_landmarks[0]
    return None


#Takes in the body points and location of items in the store and
#detects for shoplifting if items are too close to certain body parts
def detect_Anomaly(pose_result, detected_objects, frame_count, x_scale, y_scale, threshold=50, disappearance_frames=3):
    global is_suspicious


    left_hand = pose_result[16]
    right_hand = pose_result[15]
    left_hip = pose_result[23]
    right_hip = pose_result[24]
   
    for obj in detected_objects:
      if is_near(obj, left_hand, right_hand, x_scale, y_scale, threshold):
        obj_id = f"{obj['label']}"
        if obj_id not in object_tracker:
          object_tracker[obj_id] = {
            "last_seen": frame_count,
            "near_pocket": True if is_near(obj, left_hip, right_hip, x_scale, y_scale, threshold) else False,
          }
        else:
            object_tracker[obj_id]["last_seen"] = frame_count
            object_tracker[obj_id]["near_pocket"] = True if is_near(obj, left_hip, right_hip, x_scale, y_scale, threshold) else False


    for obj_id, obj_data in list(object_tracker.items()):
        if obj_data["near_pocket"] == True and obj_id != "person" and (frame_count - obj_data["last_seen"]) > disappearance_frames:
            is_suspicious = True
            del object_tracker[obj_id]
            break


    for obj_id in list(object_tracker.keys()):
        if (frame_count - object_tracker[obj_id]["last_seen"]) > disappearance_frames * 3:
            del object_tracker[obj_id]


def is_near(obj, left, right, x_scale, y_scale, threshold=0.05):
    obj_center = ((obj['box'][0] + obj['box'][2]) / 2, (obj['box'][1] + obj['box'][3]) / 2)
    return (
        (abs(left.x * x_scale - obj_center[0]) < threshold and abs(left.y * x_scale - obj_center[1]) < threshold) or
        (abs(right.x * y_scale - obj_center[0]) < threshold and abs(right.y * y_scale - obj_center[1]) < threshold)
    )  


#Main function for parsing a video, dividing it into smaller clips, and running the Ai model to
#see if there's an anomaly in each clip
def process_Video(video_path):
    cap = cv2.VideoCapture(video_path)


    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_duration = 1 / fps  
    frame_count = 0




    global is_suspicious
    is_suspicious = False
   
    while cap.isOpened():
        ret, frame = cap.read()


        if not ret:
            break


        timestamp = frame_count * frame_duration
        timestamp = int(timestamp * 1e6)
        frame_count += 1


        detected_objects = get_Obj(frame)  
        pose_landmarks = get_Pose_Points(frame, timestamp)


        # if frame is not None and ret:
        #     cv2.imshow("Shoplifting Detector", frame)
       
        if pose_landmarks is not None and detected_objects is not None:
          x_scale = frame.shape[0]
          y_scale = frame.shape[1]
          detect_Anomaly(pose_landmarks, detected_objects, frame_count, x_scale, y_scale)
          if is_suspicious:
            break


    cap.release()
    cv2.destroyAllWindows()


directory_path = "Video"
for filename in os.listdir(directory_path):
  file_path = os.path.join(directory_path, filename)
  process_Video(file_path)
  send_Video(file_path)