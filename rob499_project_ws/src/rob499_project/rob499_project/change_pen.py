#!/usr/bin/env python3

# change_pen.py
#
# Cory Hungate
#
# a node that monitors knobs 6-8 and uses them to change RGB values of the pen, then 
# changes the background color on a service call

import rclpy
from rclpy.node import Node
from turtlesim.srv import SetPen
from std_msgs.msg import Int64MultiArray, Int64
import numpy as np

def remap_data(value):
	new_value = np.interp(value, [0,100], [0, 255])
	return int(new_value)

class PenServiceCaller(Node):
	def __init__(self):
		
		super().__init__('set_pen_service')

		self.knob_sub = self.create_subscription(Int64MultiArray, 'knob_data', self.modify_rgb, 10)
		self.keystroke_sub = self.create_subscription(Int64, 'keystroke_data', self.keystroke_callback, 10)
		self.rgb_pub = self.create_publisher(Int64, 'rgb_data', 10)

		self.client = self.create_client(SetPen, '/turtle1/set_pen')

		while not self.client.wait_for_service(timeout_sec=1):
			self.get_logger().info('set_pen service not yet available...')


		self.get_logger().info("color change node is live!")

		self.note_used = 60

		self.red_value = 255
		self.green_value = 0
		self.blue_value = 0


	def modify_rgb(self, msg):
		new_msg = Int64()
		knob_num = msg.data[0]
		og_value = msg.data[1]
		
		if knob_num == 6:
			self.red_value = remap_data(og_value)
			new_msg.data = 1000 + self.red_value
			self.rgb_pub.publish(new_msg)
		
		elif knob_num == 7:
			self.green_value = remap_data(og_value)
			new_msg.data = 2000 + self.green_value
			self.rgb_pub.publish(new_msg)

		elif knob_num == 8:
			self.blue_value = remap_data(og_value)
			new_msg.data = 3000 + self.blue_value
			self.rgb_pub.publish(new_msg)
	
	def keystroke_callback(self, msg):

		self.get_logger().info(f"note {msg.data} received to set pen.")
		
		if msg.data == self.note_used:
			self.set_pen_color()
			self.get_logger().info("sending clear request")
	
	def set_pen_color(self):
		request = SetPen.Request()
		request.r = self.red_value
		request.g = self.green_value
		request.b = self.blue_value
		request.width = 5
		request.off = False
		self.client.call_async(request)
		self.get_logger().info("set pen request sent to turtlesim")
	


def main(args=None):

	rclpy.init(args=args)

	service = PenServiceCaller()

	rclpy.spin(service)

	service.destroy_node()

	rclpy.shutdown()
	

if __name__ == '__main__':
	main()