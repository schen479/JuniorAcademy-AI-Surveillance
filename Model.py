#File for AI model 

#Download these libraries if you don't have them install already
import cv2
import torch
import openpose

objs = []

#Get objects of the shelves that are subjected to shoplifting using YOLO. 
def get_Obj(frame): 

#Returns the points of a person's body using OpenPose
def get_Pose_Points(frame):

#Takes in the body points and location of items in the store and
#detects for shoplifting if items are too close to certain body parts
def detect_Anomaly(objects, pose_points):

