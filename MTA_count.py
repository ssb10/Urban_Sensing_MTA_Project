import cv2
import numpy as np
import math
import matplotlib.pyplot as pl
pl.ion()

count = 0 # number of people per frame
print("Reading Video...")
cap = cv2.VideoCapture('C:/Users/shrey/Videos/video_1.MP4')

subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=True) # Create Background subtractor

kernelOp = np.ones((3,3),np.uint8)
kernelCl = np.ones((11,11),np.uint8)

# Getting frame width and height to calculate frame area
width = cap.get(3)
height = cap.get(4)
frame_area = width * height

# area threshold
areaTH = frame_area/250

# Defining area of interest

pt_5 = [width/2,0]
pt_6 = [width/2, height]
pt_7 = [0,height/2]
pt_8 = [width, height/2]

pts_start = np.array([pt_5,pt_6], np.int32)
pts_start = pts_start.reshape((-1,1,2))
pts_end = np.array([pt_7,pt_8], np.int32)
pts_end = pts_end.reshape((-1,1,2))

print("Subtracted Background...")
while cap.isOpened():
    ret, frame = cap.read() # read a frame
    
    subtracted_frame = subtractor.apply(frame)
    
    try:
        ret, binary_image = cv2.threshold(subtracted_frame,200,255,cv2.THRESH_BINARY) # converting to binary image
        image_mask = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernelOp) # remove noise
        image_mask = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernelCl) #to join white regions
        
    except:
        print("File ended ")
        #print("Count: {}".format(count))
        break
    
    _, contours0, hierarchy = cv2.findContours(image_mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # finding contours
    
    for cnt in contours0:
        #cv2.drawContours(frame, cnt, -1, (0,255,0), 3, 8)
        area = cv2.contourArea(cnt)
        #print (area)
        if area > areaTH:           
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)            
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.circle(frame,(x,y), 5,(255,0,0), -1)
            cv2.circle(frame, (x+w,y+h),5, (255,0,0), -1)
            #Check if the rectangle lies within area of interest
            if (x*1.0<width*0.7) & (y*1.0>height*0.7) & ((x+w)*1.0<width*0.7) & ((y+h)*1.0>height*0.7):
                count += 1
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        print("EOF")
        break
    
    frame = cv2.polylines(frame, [pts_start], False, (255,255,255), thickness=2)
    frame = cv2.polylines(frame,[pts_end], False, (255,255,255), thickness=2)
    #cv2.putText(frame, "Out: {}".format(str(count/60)), (10, 70),
                #cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("Frame",frame)
print("Counting done!")
print(count)
count = count/60 #Video is captured at 60FPS

print("Final Count: {}".format(math.floor(count)))
cap.release()
cv2.destroyAllWindows()