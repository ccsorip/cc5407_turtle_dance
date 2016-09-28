#!/usr/bin/env python
# license removed for brevity

import roslib
roslib.load_manifest('turtle_dance')
import rospy
import actionlib

from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState
from turtle_dance.msg import *


class DoDanceServer:

	def callback(self, data_cb):
		self.data = [data_cb.position[0], data_cb.position[1]]


	def __init__(self):
		self.data = None
		rospy.init_node('dancer', anonymous=True)
		self.pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=10)
		rospy.Subscriber("/joint_states", JointState, self.callback)
		self.rate = rospy.Rate(10)

		while not self.data:
			self.rate.sleep()

		self.server = actionlib.SimpleActionServer('do_dance', DoDanceAction, self.execute, False)
		self.server.start()


	def execute(self, goal):
		feedback = turtle_dance.msg.DoDanceFeedback()
		if goal.step_name == 'walk':
			feedback.percent_complete = 0
			self.server.publish_feedback(feedback) #publicando

			self.mover_linea_recta(40)
			self.girar_grados(10.5, 0.5) #180 grados
			self.mover_linea_recta(40)

			feedback.percent_complete = 50
			self.server.publish_feedback(feedback) #publicando

			self.mover_linea_recta(40)
			self.girar_grados(10.5, 0.5) #180 grados
			self.mover_linea_recta(40)

			feedback.percent_complete = 100
			self.server.publish_feedback(feedback) #publicando

		if goal.step_name == 'turn':
			feedback.percent_complete = 0
			self.server.publish_feedback(feedback) #publicando

			self.girar_grados(2.625, 0.5) #45 grados
			self.mover_linea_recta(40)
			self.girar_grados(5.25, -0.5) #-90 grados
			self.mover_linea_recta(40)

			feedback.percent_complete = 50
			self.server.publish_feedback(feedback) #publicando

			self.girar_grados(5.25, -0.5) #-90 grados
			self.mover_linea_recta(40)
			self.girar_grados(5.25, -0.5) #-90 grados
			self.mover_linea_recta(40)
			self.girar_grados(2.625 + 5.25, -0.5) #-135 grados

			feedback.percent_complete = 100
			self.server.publish_feedback(feedback) #publicando

		self.server.set_succeeded()


	def mover_linea_recta(self, pasos):
		tw = Twist()

		#setear posicion inicial para este paso
		posicion_inicial = self.data

		#caminar hacia el frente hasta que se avance N pasos
		while not (self.data[0] - posicion_inicial[0]  >= pasos and self.data[1] - posicion_inicial[1]  >= pasos):
			tw.linear.x = 0.5
			#rospy.loginfo("diff: " + str(self.data[0] - posicion_inicial[0]))
			self.pub.publish(tw)
			self.rate.sleep()

		#detente turtlebot
		self.pub.publish()


	def girar_grados(self, pasos, vel_ang):
		tw = Twist()
		#setear posicion inicial para este paso
		posicion_inicial = self.data

		#girar hasta que la rueda avance N pasos
		while not (abs(self.data[0] - posicion_inicial[0])  >= pasos and abs(self.data[1] - posicion_inicial[1]) >= pasos):
			tw.angular.z = vel_ang
			#rospy.loginfo("diff: " + str(abs(self.data[0] - posicion_inicial[0])))
			self.pub.publish(tw)
			self.rate.sleep()

		#detente turtlebot
		self.pub.publish()

if __name__ == '__main__':
	server = DoDanceServer()
	rospy.spin()