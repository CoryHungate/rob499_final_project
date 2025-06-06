#!/usr/bin/env python3
#
# serial_data_publisher.py
#
# Cory Hungate
#
# pub/sub node that mimics retreiving serial data and republishes it to change a parameter

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int64, Int64MultiArray
import serial

class SerialReaderNode(Node):
	def __init__(self):
		super().__init__('serial_reader')

        #this first publisher is just going to republish the raw data
		self.raw_pub = self.create_publisher(String, 'midi_serial_data', 10)

		#this next publisher is going to be a parameter publisher
		self.note_pub = self.create_publisher(Int64, 'keystroke_data', 10)
		self.knob_pub = self.create_publisher(Int64MultiArray, 'knob_data', 10)

		#also going to create a subscriber to send data from ROS through serial
		self.rgb_sub = self.create_subscription(Int64, 'rgb_data', self.send_serial_data, 10)

		self.get_logger().info(f'MIDI data reader has started')
		
		#if you need to change the serial port you're reading on, this is where you do it
		self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

		self.timer = self.create_timer(.01, self.read_serial)

	def read_serial(self):
		if self.ser.in_waiting > 0:
			line = self.ser.readline().decode('utf-8').strip()
			stripped_line = line.strip()
			if line:
				raw_msg = String()
				raw_msg.data = line
				self.raw_pub.publish(raw_msg)
				self.get_logger().info(f'Published: "{line}"')
		
			if "Note On" in line:
				note_msg = Int64()
				val = int(stripped_line.split()[-1])
				note_msg.data = val
				self.note_pub.publish(note_msg)
				self.get_logger().info(f'note_value: "{val}"')
			
			if "Knob:" in line:
				#extracting the knob number and value from the serial data
				knob_num = int(stripped_line.split()[1])
				val = int(stripped_line.split()[-1])
				
				#I'm publishing the knob data whole. the user can use logic
				knob_msg = Int64MultiArray()
				knob_msg.data = [knob_num, val] 
				self.knob_pub.publish(knob_msg)
				self.get_logger().info(f'Knob {knob_msg.data[0]} published with value {knob_msg.data[1]}')
	
	def send_serial_data(self, msg):
		if self.ser:
			send_string = f"{msg.data}\n"			
			try:
				self.ser.write(send_string.encode())
				self.get_logger().info(f"send message {send_string} to serial")
			except serial.SerialException:
				self.get_logger().info("Failed to send info to arduino")



def main(args=None):
	rclpy.init(args=args)
	node = SerialReaderNode()
	rclpy.spin(node)
	node.destroy_node()
	rclpy.shutdown()