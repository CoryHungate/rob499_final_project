#!/usr/bin/env python3

# turtle_movement.py
#
# Cory Hungate
#
# Simple Node that controls the velocity of of the turtle in turtlesim using a midi controller


import rclpy
from rclpy.node import Node

from std_msgs.msg import Int64
from geometry_msgs.msg import Twist

import numpy as np


class MovementPublisher(Node):
	def __init__(self):

		super().__init__('knob1_sub_pub')

		self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
		self.sub = self.create_subscription(Int64, 'knob1', self.callback_1, 10)
		self.sub = self.create_subscription(Int64, 'knob2', self.callback_2, 10)

		#10 hz publishing seems like more than enough
		self.timer = self.create_timer(.1, self.timer_callback)

		#initializing the speed variable with a value of 0. 
		self.linear_vel = 0.0
		self.angular_vel = 0.0


	#changing the linear_vel value when a new one arrives
	def callback_1(self, msg):
		remapped_val = np.interp(float(msg.data), [0.0, 100], [-2.0, 2.0])
		self.linear_vel = remapped_val

	#changing the angular_vel value when a new one arrives
	def callback_2(self, msg):
		remapped_val = np.interp(float(msg.data), [0.0, 100], [-2.0 * np.pi, 2.0 * np.pi])
		self.angular_vel = remapped_val

	#because turtlesim expects continuous publishing, I'm publishing to cmd_vel inside of a timer. 
	def timer_callback(self):
		new_msg = Twist()
		new_msg.linear.x = self.linear_vel
		new_msg.angular.z = self.angular_vel

		self.pub.publish(new_msg)



def main(args=None):

	rclpy.init(args=args)

	publisher = MovementPublisher()

	rclpy.spin(publisher)

	rclpy.shutdown()
	

if __name__ == '__main__':
	main()