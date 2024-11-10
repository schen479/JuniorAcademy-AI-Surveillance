#File for AI model 

#Download these libraries if you don't have them install already
import cv2
import torch
import mediapipe as mp

import datetime
import pytz

model_path = "JuniorAcademy-AI-Surveillance\pose_landmarker_full.task"


#Shubh
#Get objects of the shelves that are subjected to shoplifting using YOLO. 
def get_Obj(frame): 
    # define objects ex. soda cans, box of cereals
  results = model(frame)
  detections = results.xyxy[0]
  objs = {}

  for *box, conf, cls in detections:
    x1, y1, x2, y2 = map(int, box)
    label = model.names[int(cls)]
    objs.append({
      'label' = label,
      'confidence' = float(conf),
      'box' = [x1, y1, x2, y2]
    })
    
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
  return frame, objs;


    
#Stephen
#Returns the points of a person's body using OpenPose
def get_Pose_Points(frame):
  BaseOptions = mp.tasks.BaseOptions
  PoseLandmarker = mp.tasks.vision.PoseLandmarker
  PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
  VisionRunningMode = mp.tasks.vision.RunningMode

  options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO)

  with PoseLandmarker.create_from_options(options) as landmarker: 
    mp_frame = mp.Image(image_format = mp.ImageFormat.SRGB, data = frame)
    pose_result = landmarker.detect(mp_frame)

    if pose_result.pose_landmarks:
      for landmark in pose_result.pose_landmarks.landmark:
        x, y = int(landmark.x * fran.) 

  return pose_result

#Alan
#Takes in the body points and location of items in the store and
#detects for shoplifting if items are too close to certain body parts
    # check if object is in hand of person
def detect_Anomaly(pose_result, detected_objects, frame_count, threshold=10, disappearance_frames=5):
  # check if object is in hand of person
  is_suspicious = False
  object_tracker = {}

  left_hand = pose_result[16]
  right_hand = pose_result[15]
  left_hip = pose_result[23] 
  right_hip = pose_result[24]
  
  for obj in detected_objects:
    if is_near(obj, left_hand, right_hand, threshold):
      obj_id = f"{obj['name']}"
      if obj_id not in object_tracker:
        object_tracker[obj_id] = {
          "last_seen": frame_count,
          "near_pocket": is_near(obj, left_hip, right_hip, threshold)
        }
      else:
          object_tracker[obj_id]["last_seen"] = frame_count
          object_tracker[obj_id]["near_pocket"] = is_near(obj, left_hip, right_hip, threshold)

  for obj_id, obj_data in list(object_tracker.items()):
      if obj_data["status"] == "near_pocket" and (frame_count - obj_data["last_seen"]) > disappearance_frames:
          is_suspicious = True
          del object_tracker[obj_id]
          break

  for obj_id in list(object_tracker.keys()):
      if (frame_count - object_tracker[obj_id]["last_seen"]) > disappearance_frames * 2:
          del object_tracker[obj_id]

  return is_suspicious

def is_near(obj, left_hand, right_hand, threshold=0.05):
    obj_center = ((obj['box'][0] + obj['box'][2]) / 2, (obj['box'][1] + obj['box'][3]) / 2)
    return (
        (abs(left_hand.x - obj_center[0]) < threshold and abs(left_hand.y - obj_center[1]) < threshold) or
        (abs(right_hand.x - obj_center[0]) < threshold and abs(right_hand.y - obj_center[1]) < threshold)
    )  
    # 

# Kevin
#Alert owner of shoplifting event to their messenges
'''
Parameters:
    reason - string - possible reasons of found in ['stealing', 'violating products']
    suspectDesc - dictionary describing suspect's details
        'race', 'hairColor', 'isWearingGlasses', 'shirtColor', 'leggingColor', 'height'
'''
def alertOwner(reason, suspectDesc):

    # send text
    current_time = datetime.datetime.now(tz=pytz.UTC)
    message = "Shoplifting Detected at: " + str(current_time) + "\n Subject is possibly " + reason
    suspectDescText = "Subject is "

    print(current_time)
    print(message)
    pri
    # send video frame of event

