# Python program to save a
# video using OpenCV


import cv2
import numpy as np


# Create an object to read
# from camera
video = cv2.VideoCapture(0,cv2.CAP_DSHOW)

# We need to check if camera
# is opened previously or not
if (video.isOpened() == False):
	print("Error reading video file")

# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(video.get(3))
frame_height = int(video.get(4))

size = (1280, 480)

# Below VideoWriter object will create
# a frame of above defined The output
# is stored in 'filename.avi' file.
result = cv2.VideoWriter('filename.avi',
						cv2.VideoWriter_fourcc(*'MJPG'),
						10, size)
img=cv2.imread('images/cat.jpg')
img=cv2.resize(img, (640,480))

while(True):
    ret, frame = video.read()
    if(ret == True):
        print(frame.shape)
        img1=np.hstack((frame,img))
        result.write(img1)
        cv2.imshow('img', img1)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
    else:
        break

# When everything done, release
# the video capture and video
# write objects
video.release()
result.release()
	
# Closes all the frames
cv2.destroyAllWindows()

print("The video was successfully saved")
