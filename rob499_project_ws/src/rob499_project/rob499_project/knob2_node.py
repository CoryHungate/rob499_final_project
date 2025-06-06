#!/usr/bin/env python3

# knob2_node.py
#
# Cory Hungate
#
# Very simple node that extracts the data from knob 2 on the midi controller and republishes it


import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64, Int64MultiArray


KNOB_NUM = 2

class KnobSubscriber(Node):
	def __init__(self):

		super().__init__('knob1_sub_pub')

		self.pub = self.create_publisher(Int64, 'knob2', 10)
		self.sub = self.create_subscription(Int64MultiArray, 'knob_data', self.callback, 10)


	def callback(self, msg):
		
		if msg.data[0] == KNOB_NUM:
			new_msg = Int64()
			new_msg.data = msg.data[1]
			self.pub.publish(new_msg)



def main(args=None):

	rclpy.init(args=args)

	pubsub = KnobSubscriber()

	rclpy.spin(pubsub)

	rclpy.shutdown()
	

if __name__ == '__main__':
	main()