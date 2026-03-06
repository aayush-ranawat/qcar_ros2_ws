#!/usr/bin/env python3
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : File Description and Imports

import rclpy
import numpy as np
from rclpy.node import Node
from pal.utilities.gamepad import LogitechF710
from geometry_msgs.msg import Vector3Stamped
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : QCar Command Node

class CommandNode(Node):

	def __init__(self):
		super().__init__('command_node',
			allow_undeclared_parameters=True,
			automatically_declare_parameters_from_overrides=True
		)
		self.config = {"command_publish_frequency": 100}
		self.gpad = LogitechF710()

		gamepadPublishRate = int(self.config["command_publish_frequency"]) # Hz

		# Configure gamepad publisher
		self.gpadPublisher = self.create_publisher(Vector3Stamped,
												'/qcar/user_command', 10)

		self.timer 		   = self.create_timer(1/gamepadPublishRate,
												self.timer_callback)

		# save joystick commands
		self.userCommand     = [0,0]
		self.throttleCommand = 0
		self.steeringCommand = 0
		print("command_node started")


	def timer_callback(self):
		# check if there is new data from the logitech gamepad
		new = self.gpad.read()

		# Define user commands based on new signals
		if new and self.gpad.buttonLeft == 1:
			# print("command recieved")

			# Command to be +/- 0.3 radian
			self.steeringCommand = self.gpad.rightJoystickX*0.3
		

			# configure throttle to be from 0 to + 30% PWM command
			self.throttleCommand = (self.gpad.leftJoystickY)*0.2

			if self.gpad.buttonA == 1:
				self.throttleCommand = self.throttleCommand*-1


		self.userCommand  = [self.throttleCommand, self.steeringCommand]
		
		self.process_command(new)
		# # Print out the gamepad IO read
		# print("Left Laterial:\t\t{0:.2f}\nLeft Longitudonal:\t{1:.2f}\nTrigger:\t\t{2:.2f}\nRight Lateral:\t\t{3:.2f}\nRight Longitudonal:\t{4:.2f}"
		# 	.format(self.gpad.leftJoystickX, self.gpad.leftJoystickY, self.gpad.trigger, self.gpad.rightJoystickX, self.gpad.rightJoystickY))
		# print("Button A:\t\t{0:.0f}\nButton B:\t\t{1:.0f}\nButton X:\t\t{2:.0f}\nButton Y:\t\t{3:.0f}\nButton LB:\t\t{4:.0f}\nButton RB:\t\t{5:.0f}"
		# 	.format(self.gpad.buttonA, self.gpad.buttonB, self.gpad.buttonX, self.gpad.buttonY, self.gpad.buttonLeft, self.gpad.buttonRight))
		# print("Up:\t\t\t{0:.0f}\nRight:\t\t\t{1:.0f}\nDown:\t\t\t{2:.0f}\nLeft:\t\t\t{3:.0f}"
		# 	.format(self.gpad.up, self.gpad.right, self.gpad.down, self.gpad.left))
	def process_command(self, new):

		if new:
			commandPublisher = Vector3Stamped()
			commandPublisher.header.stamp = self.get_clock().now().to_msg()
			commandPublisher.header.frame_id = 'command_input'
			commandPublisher.vector.x = float(self.userCommand[0])
			commandPublisher.vector.y = float(self.userCommand[1])
			self.gpadPublisher.publish(commandPublisher)
		else:
			commandPublisher = Vector3Stamped()
			commandPublisher.header.stamp = self.get_clock().now().to_msg()
			commandPublisher.header.frame_id = 'command_input'
			commandPublisher.vector.x = float(self.userCommand[0])
			commandPublisher.vector.y = float(self.userCommand[1])
			
			self.gpadPublisher.publish(commandPublisher)

	def stop_gampad(self):
		self.gpad.terminate()
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Main

def main(args=None):
	rclpy.init(args=args)
	r = CommandNode()
	while rclpy.ok():
		try:
			rclpy.spin_once(r)
		except KeyboardInterrupt:
			r.stop_gampad()
			break

	rclpy.shutdown()
	print("Gamepad has been stopped....")
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Run

if __name__ == '__main__':
	main()
#endregion
