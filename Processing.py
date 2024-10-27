#File for video processing and filtering

#Blur people faces if anomaly isn't detected
def blurFaces():

#Send a video to one of two server (local servers used for testing). If anomaly is detected, send to central
#if no anomaly is detected, save temporarily in local server. 
def send_Video():

#Deletes all footage if no anomaly is detected in 5 minutes
def delete():

#Main function for parsing a video, dividing it into smaller clips, and running the Ai model to
#see if there's an anomaly in each clip 
def process_Video(video_path):
