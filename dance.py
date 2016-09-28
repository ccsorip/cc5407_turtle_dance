#!/usr/bin/env python
# license removed for brevity
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState

data = None

def mover_linea_recta(pasos, rate, pub):
	global data
	tw = Twist()

	#setear posicion inicial para este paso
	posicion_inicial = data

	#caminar hacia el frente hasta que se avance N pasos
	while not (data[0] - posicion_inicial[0]  >= pasos and data[1] - posicion_inicial[1]  >= pasos):
		tw.linear.x = 0.5
		rospy.loginfo("diff: " + str(data[0] - posicion_inicial[0]))
		pub.publish(tw)
		rate.sleep()

	#detente turtlebot
	pub.publish()

def girar_grados(pasos, rate, pub, vel_ang):
	global data
	tw = Twist()
	#setear posicion inicial para este paso
	posicion_inicial = data

	#girar hasta que la rueda avance N pasos
	while not (abs(data[0] - posicion_inicial[0])  >= pasos and abs(data[1] - posicion_inicial[1]) >= pasos):
		tw.angular.z = vel_ang
		rospy.loginfo("diff: " + str(abs(data[0] - posicion_inicial[0])))
		pub.publish(tw)
		rate.sleep()

	#detente turtlebot
	pub.publish()

def callback(data_cb):
	global data
	data = [data_cb.position[0], data_cb.position[1]]

def talker():
	global data
	pub = rospy.Publisher('/cmd_vel_mux/input/teleop', Twist, queue_size=10)
	rospy.init_node('dancer', anonymous=True)
	rospy.Subscriber("/joint_states", JointState, callback)
	rate = rospy.Rate(10) # 10hz
	#espera hasta que haya data del callback
	while not data:
		rate.sleep()

	while not rospy.is_shutdown():
		mover_linea_recta(40, rate, pub)
		girar_grados(10.5, rate, pub, 0.5) #180 grados
		mover_linea_recta(40, rate, pub)

		mover_linea_recta(40, rate, pub)
		girar_grados(10.5, rate, pub, 0.5) #180 grados
		mover_linea_recta(40, rate, pub)

		girar_grados(2.625, rate, pub, 0.5) #45 grados
		mover_linea_recta(40, rate, pub)
		girar_grados(5.25, rate, pub, -0.5) #-90 grados
		mover_linea_recta(40, rate, pub)
		girar_grados(5.25, rate, pub, -0.5) #-90 grados
		mover_linea_recta(40, rate, pub)
		girar_grados(5.25, rate, pub, -0.5) #-90 grados
		mover_linea_recta(40, rate, pub)
		girar_grados(2.625 + 5.25, rate, pub, -0.5) #-135 grados

if __name__ == '__main__':
	try:
		#inicio
		talker()
	except rospy.ROSInterruptException:
		pass
