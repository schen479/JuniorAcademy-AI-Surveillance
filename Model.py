#File for AI model 

#Download these libraries if you don't have them install already
import cv2
import torch
import openpose

objs = []

#Get objects of the shelves that are subjected to shoplifting using YOLO. 
def get_Obj(frame): 
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

#Returns the points of a person's body using OpenPose
def get_Pose_Points(frame):

#Takes in the body points and location of items in the store and
#detects for shoplifting if items are too close to certain body parts
def detect_Anomaly(objects, pose_points):

