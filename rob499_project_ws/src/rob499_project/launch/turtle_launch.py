# a launch file that opens some of the nodes made for my ROB499 project
# as well as an instance of turtlesim 
# 
# This file should be opened BEFORE turtle_launch2.py
#
# turtle_launch.py
#
# Cory Hungate

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
	return LaunchDescription([
		Node(
			package = 'turtlesim',
			executable= 'turtlesim_node',
			name = 'turtlesim',
			output = 'screen',
		),
		Node(
			package = 'rob499_project',
			executable= 'knob1',
			name = 'knob1',
		),
		Node(
			package = 'rob499_project',
			executable= 'knob2',
			name = 'knob2',
		),
		Node(
			package = 'rob499_project',
			executable= 'turtle_movement',
			name = 'turtle_movement',
		),

		
	])