# a launch file that opens the rest of the nodes made for my ROB499 project
# these are all the nodes that wouldn't open in the first launch file but would open
# when moved into their own launch file
#
# This file should be opened AFTER turtle_launch.py
#
# turtle_launch2.py
#
# Cory Hungate

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
	return LaunchDescription([
		Node(
			package = 'rob499_project',
			executable= 'serial_data',
			name = 'serial_data',
		),
		Node(
			package = 'rob499_project',
			executable= 'kill_turtle',
			name = 'kill_turtle',
			output = 'screen',
		),
		Node(
			package = 'rob499_project',
			executable= 'clear',
			name = 'clear_path',
			output = 'screen',
		),
		Node(
			package = 'rob499_project',
			executable= 'change_pen',
			name = 'change_pen',
			output = 'screen',
		),

		
	])