# USAGE
# python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel
#Code provided from https://www.pyimagesearch.com/2017/09/18/real-time-object-detection-with-deep-learning-and-opencv/

#To run
#activate tensorflow
#python real_time_object_detection.py --prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import sensor_msgs.msg
import numpy as np
import argparse
import RPi.GPIO as GPIO
import imutils
from geometry_msgs.msg import PoseStamped

import std_msgs.msg
import time

import cv2
import rospy

from tf import TransformListener
import math
import tf
#import servoNeutral
import sys
#from std_msgs.msg import String
distanceToObject=10000
def callback(data):
    global distanceToObject
    distanceToObject=data.range
def listener():
    rospy.Subscriber("ultrasonic/middle",sensor_msgs.msg.Range,callback)

#Set up ROS publishing
pub=rospy.Publisher('goal_position',PoseStamped, queue_size=1000)
rospy.init_node('demo_pub_node')
r=rospy.Rate(1)
#I apparently can't just call the set servo as a function as when the function ends it kills the servo... So I have to do it right here
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)
pwmClose=GPIO.PWM(3,50)
pwmClose.start(12.5)
GPIO.setup(15,GPIO.OUT)
pwmFar=GPIO.PWM(15,50)
pwmFar.start(2.5)
#For far 12.5 is close 2.5 is open
#For close 12.5 us up and 2.5 is down
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument( "--prototxt", required=True,
   help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
   help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
   help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
   "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
   "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
   "sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()
rate = rospy.Rate(1)
frameSize=400
degreesToRadians=math.pi/180
angleConversion=31.1/(frameSize/2)#31.1 degrees from center to left/right 
#servoNeutral.setGripOpen()#Have the servo be open and straight at start
#sys.exit()
transform=TransformListener()
while not rospy.is_shutdown():
	# loop over the frames from the video stream
	while True:
	   # grab the frame from the threaded video stream and resize it
	   # to have a maximum width of 400 pixels
	   frame = vs.read()
	   frame = imutils.resize(frame, width=frameSize)

	   # grab the frame dimensions and convert it to a blob
	   (h, w) = frame.shape[:2]
	   blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
	      0.007843, (300, 300), 127.5)

	   # pass the blob through the network and obtain the detections and
	   # predictions
	   net.setInput(blob)
	   detections = net.forward()

	   # loop over the detections
	   for i in np.arange(0, detections.shape[2]):
	      # extract the confidence (i.e., probability) associated with
	      # the prediction
	      confidence = detections[0, 0, i, 2]

	      # filter out weak detections by ensuring the `confidence` is
	      # greater than the minimum confidence
	      if confidence > args["confidence"]:
		 # extract the index of the class label from the
		 # `detections`, then compute the (x, y)-coordinates of
		 # the bounding box for the object
		 idx = int(detections[0, 0, i, 1])
		 box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		 (startX, startY, endX, endY) = box.astype("int")

		 # draw the prediction on the frame
		 label = "{}: {:.2f}%".format(CLASSES[idx],
		    confidence * 100)
		 cv2.rectangle(frame, (startX, startY), (endX, endY),
		    COLORS[idx], 2)
		 y = startY - 15 if startY - 15 > 15 else startY + 15
		 cv2.putText(frame, label, (startX, y),
		    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
		
		 if(label.split(':',1)[0]=='bottle'):
		    average=(startX+endX)/2
		    degreesToTurn=((average-frameSize/2)*angleConversion)
		    radToTurn=degreesToTurn*degreesToRadians
		    listener()
                    rospy.loginfo(distanceToObject)
		    rospy.loginfo(degreesToTurn)
		    rospy.loginfo('_____________')
		   # t=transform.getLatestCommonTime("base_link","odom")
		    
                    if(abs(degreesToTurn)>3):
			    if(average>frameSize/2):#If it is to the RIGHT
			       q=tf.transformations.quaternion_from_euler(0,0,radToTurn)
		      
		               p=PoseStamped()

		            
		               p.header.stamp=rospy.get_rostime()
		               p.header.frame_id='base_link'
		               p.pose.position.x=0
			       p.pose.position.y=0
		               p.pose.position.z=0
		               p.pose.orientation.x=q[0]
		               p.pose.orientation.y=q[1]
		               p.pose.orientation.z=q[2]
		               p.pose.orientation.w=q[3]
			       rospy.loginfo("RIGHT TURN")
			       t=transform.getLatestCommonTime("base_link","odom")
			       position,quaternion=transform.lookupTransform("base_link","odom",t)             
			       mapP=PoseStamped()
			       mapP.header.stamp=rospy.get_rostime()
			       mapP.header.frame_id="odom"
			       mapP.pose.position.x=position[0]
			       mapP.pose.position.y=position[1]
                               mapP.pose.position.z=position[2]
                               mapP.pose.orientation.x=quaternion[0]
                               mapP.pose.orientation.y=quaternion[1]
                               mapP.pose.orientation.z=quaternion[2]
                               mapP.pose.orientation.w=quaternion[3]
                              
			      # print(position)
			      # print(quaternion)
			       pNew=transform.transformPose("odom",p)
			       print(pNew)
			       pub.publish(p) 
		               rospy.loginfo(p)
			       sys.exit()
		               rate.sleep()
	  		    else:#If it is to the left or equal
		               degreesToTurn=degreesToTurn*-1#The negative 1 is so it will turn to the left
			       q=tf.transformations.quaternion_from_euler(0,0,radToTurn)
		               p=PoseStamped()

		            
		               p.header.stamp=rospy.get_rostime()
		               p.header.frame_id='base_link'
		               p.pose.position.x=0
			       p.pose.position.y=0
		               p.pose.position.z=0
		               p.pose.orientation.x=q[0]
		               p.pose.orientation.y=q[1]
		               p.pose.orientation.z=q[2]
		               p.pose.orientation.w=q[3]
			       pub.publish(p) 
                               rospy.loginfo("LEFT TURN")
		               rospy.loginfo(p)
		               rate.sleep()
			# pub.publish(label)
		    elif(distanceToObject>.1):
			if(distanceToObject>100):#HANDLE THE INITIAL
			    distanceToObject=0
		       
			p=PoseStamped()

	                rospy.loginfo(distanceToObject)
	                p.header.stamp=rospy.get_rostime()
	                p.header.frame_id='base_link'
	                p.pose.position.x=distanceToObject-.1#We need to leave the room for the arm
		        p.pose.position.y=0
	                p.pose.position.z=0
	                p.pose.orientation.x=0
	                p.pose.orientation.y=0
	                p.pose.orientation.z=0
	                p.pose.orientation.w=0
		        pub.publish(p) 
	                rospy.loginfo(p)
			rospy.loginfo("MOVE FORWARD")
	                rate.sleep()
		    elif(distanceToObject<.1 and abs(degreesToTurn)<=3):
			pwmClose.ChangeDutyCycle(7.5)
			pwmFar.ChangeDutyCycle(12.5)
			rospy.loginfo("ATTEMPT GRIP")
			
		 
		 print('sending data...')
		 r.sleep()

	   # show the output frame
         #THIS IS THE PIECE OF CODE YOU HAVE TO UNCOMMENT TO SEE A FRAME
	 #  cv2.imshow("Frame", frame)
	   key = cv2.waitKey(1) & 0xFF

	   # if the `q` key was pressed, break from the loop
	   if key == ord("q"):
	      break

	   # update the FPS counter
	   fps.update()

# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()

