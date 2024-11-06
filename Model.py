#File for AI model 

#Download these libraries if you don't have them install already
import cv2
import torch
import mediapipe as mp

import datetime
import pytz

model_path = "JuniorAcademy-AI-Surveillance\pose_landmarker_full.task"

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO)

with PoseLandmarker.create_from_options(options) as landmarker:

#Shubh
#Get objects of the shelves that are subjected to shoplifting using YOLO. 
def get_Obj(frame): 
    # define objects ex. soda cans, box of cereals
  results = model(frame)
  detections = results.xyxy[0]

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
    
  return frame;


    
#Stephen
#Returns the points of a person's body using OpenPose
def get_Pose_Points(frame):

#Alan
#Takes in the body points and location of items in the store and
#detects for shoplifting if items are too close to certain body parts
def detect_Anomaly(objects, pose_points):
    # check if object is in hand of person
    
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

