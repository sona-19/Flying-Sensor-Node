#!/usr/bin/env python
from plutodrone.srv import *
from plutodrone.msg import *
from std_msgs.msg import Int16,Float32,Float32MultiArray
import rospy
import queue
import time

dest_x=380.0
dest_y=155.0
dest_z=95.0
count=0
err=[0.0,0.0,0.0]
max_size=5
sum_x=0.0
sum_y=0.0
sum_z=0.0

class send_data():
	"""docstring for request_data"""
	def __init__(self):
		rospy.init_node('hold')
		self.key_value =0
		self.cmd = PlutoMsg()
		self.cmd.rcRoll =1500
		self.cmd.rcPitch = 1500
		self.cmd.rcYaw =1500
		self.cmd.rcThrottle =1000
		self.cmd.rcAUX1 =1500
		self.cmd.rcAUX2 =1500
		self.cmd.rcAUX3 =1500
		self.cmd.rcAUX4 =1500
		#self.diff=Float32MultiArray()
		self.command_pub = rospy.Publisher('/drone_command', PlutoMsg, queue_size=1)
		#self.error=rospy.Publisher('/error',Float32MultiArray,queue_size=1)
		rospy.Subscriber('/input_key', Int16, self.indentify_key )
		rospy.Subscriber('/coord', Float32MultiArray, self.error)
		
	def arm(self):
		self.cmd.rcRoll=1500
		self.cmd.rcYaw=1500
		self.cmd.rcPitch =1500
		self.cmd.rcThrottle =1000
		self.cmd.rcAUX4 =1500
		self.command_pub.publish(self.cmd)
		rospy.sleep(.1)
		
	def land(self):
		self.cmd.rcRoll=1500
		self.cmd.rcYaw=1500
		#sumerr=[0.0,0.0,0.0]
		self.cmd.rcPitch =1500
		self.cmd.rcThrottle =1400
		self.cmd.rcAUX4 =1500
		self.command_pub.publish(self.cmd)
		rospy.sleep(1)
	def disarm(self):
		self.cmd.rcThrottle =1300
		self.cmd.rcAUX4 = 1200
		self.command_pub.publish(self.cmd)
		rospy.sleep(1)
	
	def indentify_key(self, msg):
		self.key_value = msg.data
		print msg.data
	def forward(self):
		self.cmd.rcPitch =1510
		self.command_pub.publish(self.cmd)
	def backward(self):
		self.cmd.rcPitch =1490
		self.command_pub.publish(self.cmd)
	def left(self):
		self.cmd.rcRoll =1490
		self.command_pub.publish(self.cmd)	
	def right(self):
		self.cmd.rcRoll =1510
		self.command_pub.publish(self.cmd)
	def reset(self):
		self.cmd.rcRoll =1500
		self.cmd.rcThrottle =1500
		self.cmd.rcPitch =1500
		self.cmd.rcYaw = 1500
		self.command_pub.publish(self.cmd)
	def reset_x(self):
		self.cmd.rcRoll =1500
		self.cmd.rcYaw = 1500
		self.command_pub.publish(self.cmd)
	def reset_y(self):
		self.cmd.rcPitch =1500
		self.cmd.rcYaw = 1500
		self.command_pub.publish(self.cmd)
	def reset_z(self):
		self.cmd.rcThrottle =1500
		self.cmd.rcYaw = 1500
		self.command_pub.publish(self.cmd)
	
	def increase_height(self):
		self.cmd.rcThrottle = 1600
		self.command_pub.publish(self.cmd)
	def decrease_height(self):
		self.cmd.rcThrottle =1450
		self.command_pub.publish(self.cmd)
		
	def error(self,msg):
		global err
		err[0]=dest_x-msg.data[0]
		err[1]=dest_y-msg.data[1]
		err[2]=dest_z-msg.data[2]		
		
		
			
	def motion(self):
		#self.PID(err)
		if(err[0]>3):
			self.right()
		elif(err[0]<-3):
			self.left()
		else:
			self.reset_x()
		if(err[1]>3):
			self.forward()
		elif(err[1]<-3):
			self.backward()
		else:
			self.reset_y()
		if(err[2]>3):
			self.increase_height()
		elif(err[2]<-3):
			self.decrease_height()
		else:
			self.reset_z()
		self.command_pub.publish(self.cmd)
		
if __name__ == '__main__':
	while not rospy.is_shutdown():
		test = send_data()
		#test.disarm()
			#print 1
		#test.motion()
		rospy.spin()
		sys.exit(1)


