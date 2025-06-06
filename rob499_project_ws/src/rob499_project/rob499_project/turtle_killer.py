#!/usr/bin/env python3

# turtle_killer.py
#
# Cory Hungate
#
# a node that calles turtlesims /kill command


import rclpy
from rclpy.node import Node
from turtlesim.srv import Kill
from std_msgs.msg import Int64


class ServiceCaller(Node):
	def __init__(self):
		
		super().__init__('turtle_killer')

		self.get_logger().info("killer node started")

		self.client = self.create_client(Kill, '/kill')

		while not self.client.wait_for_service(timeout_sec=1):
			self.get_logger().info('waiting for service to start')

		self.sub = self.create_subscription(Int64, 'keystroke_data', self.keystroke_callback, 10)

		self.get_logger().info("Turtle killer is READY!")

		self.note_used = 48


	def keystroke_callback(self, msg):
		
		self.get_logger().info(f"Note {msg.data} received to killer service")
		if msg.data == self.note_used:
			self.kill_turtle('turtle1')
			self.get_logger().info("sending kill request")
	
	def kill_turtle(self, name):
		request = Kill.Request()
		request.name = name
		future = self.client.call_async(request)
		future.add_done_callback(self.kill_complete)
	
	def kill_complete(self, future):
		try: 
			future.result()
			self.get_logger().info("Turtle killed")
		except:
			self.get_logger().info("Failed to kill turtle")




def main(args=None):

	rclpy.init(args=args)

	print("kill node is just beginning")

	service = ServiceCaller()

	rclpy.spin(service)

	#adding this so that it removes everything once the turtle is dead.
	service.destroy_node()

	rclpy.shutdown()
	

if __name__ == '__main__':
	main()