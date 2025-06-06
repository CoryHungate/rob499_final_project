#!/usr/bin/env python3

# clear_path.py
#
# Cory Hungate
#
# a node that calles turtlesims /clear service


import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty
from std_msgs.msg import Int64


class ServiceCaller(Node):
	def __init__(self):
		
		super().__init__('clear_path_service')

		self.client = self.create_client(Empty, '/clear')

		while not self.client.wait_for_service(timeout_sec=1):
			self.get_logger().info('clear service not yet available...')

		self.sub = self.create_subscription(Int64, 'keystroke_data', self.keystroke_callback, 10)

		self.get_logger().info("clear path is READY!")

		self.note_used = 72


	def keystroke_callback(self, msg):

		self.get_logger().info(f"note {msg.data} received to clear service.")
		
		if msg.data == self.note_used:
			self.clear_path()
			self.get_logger().info("sending clear request")
	
	def clear_path(self):
		request = Empty.Request()
		future = self.client.call_async(request)
		self.get_logger().info("Clear request sent to turtlesim")
	



def main(args=None):

	rclpy.init(args=args)

	service = ServiceCaller()

	rclpy.spin(service)

	service.destroy_node()

	rclpy.shutdown()
	

if __name__ == '__main__':
	main()