#!/usr/bin/env python
# license removed for brevity

import roslib
roslib.load_manifest('turtle_dance')
import rospy
import actionlib

from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
from turtle_dance.msg import *

if __name__ == '__main__':
	rospy.init_node('do_dance_client')
	client = actionlib.SimpleActionClient('do_dance', DoDanceAction)
	client.wait_for_server()

	goal = DoDanceGoal()
	while not rospy.is_shutdown():
		goal.step_name = 'walk'
		# Fill in the goal here
		client.send_goal(goal)
		client.wait_for_result(rospy.Duration.from_sec(5.0))


		goal.step_name = 'turn'
		client.send_goal(goal)
		client.wait_for_result(rospy.Duration.from_sec(5.0))