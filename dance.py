#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState

def callback(data):
    rospy.loginfo(str(data.position[0]) + " " + str(data.position[1]))

def talker():
    pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=10)
    rospy.init_node('dancer', anonymous=True)
    rospy.Subscriber("/joint_states", JointState, callback)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
	tw = Twist()
	tw.linear.x = 0.5
	#tw.angular.z = 0.5
        pub.publish(tw)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
