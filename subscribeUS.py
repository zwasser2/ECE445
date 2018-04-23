import rospy
import geometry_msgs.msg
import sensor_msgs.msg
def callback(data):
   # rospy.loginfo("i Heard %s",data)
    rospy.loginfo(data.range)
    rospy.loginfo("HI")
def listener():
    rospy.init_node('demo_sub_node')
    rospy.Subscriber("ultrasonic/middle",sensor_msgs.msg.Range,callback)
    rospy.spin()
listener()
