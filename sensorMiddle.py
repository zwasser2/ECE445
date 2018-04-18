#This may not work as I didn't get a change to test it, msg me if it doesn't
from geometry_msgs.msg import PoseStamped
import std_msgs.msg
import GPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
TRIG=11
ECHO=16
i=0
total=0
timesToRun=20
array=[]
convertSpeedLightToCentiMeters=17000
pub=rospy.Publisher('chatter',PoseStamped, queue_size=1000)
rospy.init_node('demo_pub_node')
r=rospy.Rate(1)

while not rospy.is_shutdown():
        total=0
        array=[]
    for i in range(timesToRun):
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.output(TRIG,0)

        GPIO.setup(ECHO,GPIO.IN)

        time.sleep(0.1)

        GPIO.output(TRIG,1)
        time.sleep(0.01)
        GPIO.output(TRIG,0)

        while GPIO.input(ECHO)==0:
            pass
        start=time.time()

        while GPIO.input(ECHO)==1:
            pass
        stop=time.time()

        total+=((stop-start)*convertSpeedLightToCentimeters
        array.append((stop-start)*convertSpeedLightToCentimeters)

    GPIO.cleanup()
    p=PoseStamped()

                    
        p.header.stamp=rospy.get_rostime()
        p.header.frame_id='/base_link'
        p.pose.position.x=total/timesToRun
        p.pose.position.y=0
        p.pose.position.z=0
        p.pose.orientation.x=0
        p.pose.orientation.y=0
        p.pose.orientation.z=0
        p.pose.orientation.w=0
        pub.publish(p) 
        rospy.loginfo("seq=%d" % p.header.seq)
        r.sleep()