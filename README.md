ROB 499 Final Project
Maintainer: Cory Hungate
License: BSD-3-Clause

Note: this information and more can be found under /docs/documentation.pdf

-------------------------------------------------------------------------------
The following hardware was used for this project
    -Arduino Mega2560
    -Oxygen 8 MIDI controller
    -Assorted bits and bobs. See 'circuit_diagrams_etc' folder for the individual circuit diagrams and a complete list of circuit components used in this project

-------------------------------------------------------------------------------
Running the program

ARDUINO:
open the arduino folder and launch 'midi_reader_advanced.ino'. compile and upload to the arduino. 
NOTE: you will probably want to remove the wire to PIN 19 when uploading if the controller is plugged in. Data from the controller can sometimes interfere with the upload.

Oxygen 8 MIDI Controller:
plug in the controller to the MIDI-IN circuit on the breadboard. In order to use the keys as mapped in the nodes you need to select the correct octave on the controller. Select the "octave/presets" buttons until "--0" is displayed. In this octave the middle C key is "pitch 60" (calls the service to change the turtle path color), low C is 48 (call the Kill Turtle service), and high C is 72 (call the clear path service)

ROS2:
launch the two included ROS2 launch files
    ros2 launch rob499_project turtle_launch.py
    ros2 launch rob499_project turtle_launch2.py
NOTE: these files should be launched in this order. For some unknown reason I had to break the launch file into two files. The files contained in launch2 would fail to launch when included in turtle_launch.py

These launch files will launch every node used in this project


A COUPLE OF NOTES
You're going to need to install turtlesim on your machine. instruction for downloading are found here: 
    https://docs.ros.org/en/jazzy/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html

finding the serial port for the arduino:
first, make sure the Arduino is UNPLUGGED. Then, in the terminal run the line 
	ls /dev/tty*
this will give you a list of all the available ports. Now, plug in the Arduino. If using VirtualBox, you must also go to Devices->USB and select the arduino device listed (arduino mega 2560 for this project) to connect the arduino to the VM. run
	ls /dev/tty*
There should be a new port listed that wasn't there before. that is your serial port.
IF THIS PORT IS DIFFERENT THAN THE ONE ASSIGNED IN 'serial_data_publisher.py' THEN YOU NEED TO CHANGE THE ONE IN THE NODE

Will also likely need to give yourself permission in order to access the serial port. run the following in terminal:
	sudo usermod -aG dialout $USER
then log out and log back in or reboot the machine


-------------------------------------------------------------------------------
Project Overview

For this project I am using a MIDI controller as a physical mechanism by which I will controll the turtle in turtlesim. The MIDI contoller is hooked upto an Arduino 2560, which reads the MIDI input then publishes that information to serial. I have written several basic ROS2 nodes that will take in that information and then use that to perform specific functions. There are also two included launch files.

NODE DESCRIPTIONS:

change_pen.py - a node that monitors the 'knob_data' topic, looks for information from knobs 6-8 on the Oxygen 8 MIDI controller, and uses them to change RGB values of the pen (knob6 for red, knob7 for green, knob8 for blue), sets values for the RGB values based on this data, then changes the turtlesim pen color on a service call. This Node also publishes the value of each color change as a 4 digit integer (1---, 2---, and 3--- for RGB respectively) to the topic 'rgb_data'

clear_path.py - a node that monitors the topic 'keystroke_data' for a keystroke on key pitch 70 on the MIDI controller. if the keystroke is detected, the service to clear the turtlesim pen path is called

knob1.py - simple pubsub node that subscribes to the 'knob_data' topic and republishes the data if a change to knob-1 is found on the topic 'knob1_data'.

knob2.py - simple pubsub node that subscribes to the 'knob_data' topic and republishes the data if a change to knob-2 is found on the topic 'knob2_data'.

serial_data_publisher.py - this node is the heart of this project. This node monitors the serial port for incoming MIDI data from the Arduino. 'Note On' data is republished as an Int64 to the topic 'keystroke_data' where the message is just the pitch value of the note and knob data is republished to the topic 'knob_data' as an integer array of size 2 with the 0-index as the knob that was turned and the 1-index as a 0-100 value that represents the new value of the knob. This node also subscribes to the topic 'rgb_data' from change_pen.py and sends that data to the arduino through serial

turtle_killer.py - a node that monitors the topic 'keystroke_data' for a keystroke on key pitch 48 on the MIDI controller. if the keystroke is detected, the turtlesim service 'kill turtle' is called 

turtle_movement.py - this node subscribes to 'knob1_data' and 'knob2_data' and uses those values to control the movment of the turtle in turtlesim. knob1 controlls the x-velocity and knob2 controlls the angular velocity


-------------------------------------------------------------------------------
Collaborators:
For this assigment I made ample use of chat GPT for debugging, the website and youtube channel "Nuts and Volts" for circuit wiring and midi parsing help, microcontrollerslab for LED display wiring diagrams and help with the arduino code (see link below) several different stack overflow pages, and - of course - class example code


https://microcontrollerslab.com/esp32-74hc595-4-digit-7-segment-display/








