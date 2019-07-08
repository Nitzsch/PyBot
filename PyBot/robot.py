"""
Version : 20.05.19
Coded by Tolga Demir

Robot class. 
so. this class creates an instance of a robot with values of the drivers. 
it is used to controll all the actuators and sensors. 
The sensor values are updated as daemons, so no returns here. also to remember if calling 
things like x_pos to do it like rob_instance.x_pos.value

MAP:
The map has its own class. The robot has no attribute of a map. but the map has a atribute of robot. 
so they are kept seperate for organization. I find that useful, but this can be changed if wanted. 

"""
# all the driver scripts are comming in 
import time
import multiprocessing
import drivers.distance_sonar as distance_sonar_driver
import drivers.acc as acc_driver
import drivers.distance_infrared as distance_infrared_driver
import drivers.if_sensors as IF_Sensors_driver
import drivers.lcd_display as lcd_display_driver
import drivers.mouse_sens as mouse_driver
import RPi.GPIO as GPIO
import drivers.driver as driver
import math

class Pybot:
	"""
	Use instructions: 
	The Robot has instance variables for the sensors. This are all controlled as
	multiprocess daemons. So once initialized, the values get updatet by themselfs. 
	there is no need for user control. They are completly handled by the class instance.
	For execution time: keep in mind not to initialize a lot of robots. first: this would
	make no sense, second: the pi cant handle them. It will crash fast and hard. 
	
	"""
	def __init__(self, name = "Pybot"):
		#map resolution
		self.resolution = 1
		self.name = name 
		self.circle_value = 768
		#distance vars
		self.distance_front = multiprocessing.Value("i",0)
		self.distance_left = multiprocessing.Value("i",0)
		self.distance_right = multiprocessing.Value("i",0)
		self.distance_IF_left = multiprocessing.Value("f",0)
		self.distance_IF_right = multiprocessing.Value("f",0)
		self.wheel_encoder_left = multiprocessing.Value("i",0)
		self.wheel_encoder_right = multiprocessing.Value("i",0)
		self.cliff_left = multiprocessing.Value("i",0)
		self.cliff_right = multiprocessing.Value("i",0)
		#pos vars
		self.yaw_angle = multiprocessing.Value("f",0)
		self.yaw_angle_dif= multiprocessing.Value("f",0)
		self.x_pos = multiprocessing.Value("f",0)
		self.y_pos = multiprocessing.Value("f",0)
		self.dx = multiprocessing.Value("i",0)
		self.dy = multiprocessing.Value("i",0)
		
		# def the locks
		self.lock_distance_sonar = multiprocessing.Lock()
		self.lock_distance_IF = multiprocessing.Lock()
		self.lock_cliff = multiprocessing.Lock()            
		self.lock_wheel = multiprocessing.Lock()
		self.lock_yaw = multiprocessing.Lock()
		self.lock_dx_dy = multiprocessing.Lock()
		self.lock_odometry = multiprocessing.Lock()
        #def the daemon processes
		self.distance_sonar_daemon_process = multiprocessing.Process(target = self.distance_sonar_daemon, args=(self.lock_distance_sonar,1))
		self.distance_IF_daemon_process = multiprocessing.Process(target = self.distance_IF_daemon, args=(self.lock_distance_IF,1))
		self.cliff_daemon_process = multiprocessing.Process(target = self.cliff_daemon, args=(self.lock_cliff,1))
		self.wheel_daemon_process = multiprocessing.Process(target = self.wheel_daemon, args=(self.lock_wheel,1))
		self.yaw_angel_daemon_process = multiprocessing.Process(target = self.yaw_angel_daemon, args=(self.lock_yaw,1))
		self.x_y_daemon = multiprocessing.Process(target = self.x_y_multiproc, args=(self.lock_dx_dy,1))
		self.odometry_process = multiprocessing.Process(target = self.odometry, args=(self.lock_odometry,1))

        
		self.distance_sonar_daemon_process.daemon = True
		self.distance_IF_daemon_process.daemon = True
		self.cliff_daemon_process.daemon = True
		self.wheel_daemon_process.daemon = True
		self.yaw_angel_daemon_process.daemon= True
		self.x_y_daemon.daemon = True
		self.odometry_process.daemon = True
		#start the daemons and whish not to crash
		
		self.distance_sonar_daemon_process.start()
		self.distance_IF_daemon_process.start()
		self.cliff_daemon_process.start()
		self.wheel_daemon_process.start()
		self.yaw_angel_daemon_process.start() 
		self.x_y_daemon.start()  
		self.odometry_process.start()
		
	"""
	the class attributes need to be up to date at every time. 
	because of this, they are defined as daemons. This daemons are running constantly. 
	They read the sensor data and update the values of the robot, without any user or 
	script input. 
	The daemons start by creating one instance of the robot and run of with the end 
	of the last instance. 
	Therefor they can take up to 10-20% of the cpu power the little rasp has to offer. 
	keep that in mind, while doing crazy picture stuff
	"""
	# first we define all the "Geter and Seter" Methodes
	def distance_sonar_daemon(self,lock_distance_sonar,par):
		while True:
			with lock_distance_sonar:
				#there is time build in between the sensing to prevent interference between the sensors
				#this is held pretty short
				self.distance_front.value = distance_sonar_driver.distance("front")
				time.sleep(0.05)
				self.distance_left.value = distance_sonar_driver.distance("left")
				self.distance_right.value = distance_sonar_driver.distance("right")
				time.sleep(0.05)
				
	def distance_IF_daemon(self, lock_distance_IF,par):
		while True:
			with lock_distance_IF:
				self.distance_IF_left.value = distance_infrared_driver.distance_channels("left")
				self.distance_IF_right.value = distance_infrared_driver.distance_channels("right")
				time.sleep(0.05)
	
	def cliff_daemon(self,lock_cliff,par):
		while True:
			with lock_cliff:
				self.cliff_left.value = IF_Sensors_driver.cliff_left()
				self.cliff_right.value = IF_Sensors_driver.cliff_right() 
				time.sleep(0.05)
	
	def wheel_daemon(self,lock_wheel,par):
		GPIO.add_event_detect(32, GPIO.BOTH, callback=lambda channel, s = self: self.if_sens_worker_left(s))
		GPIO.add_event_detect(23, GPIO.BOTH, callback=lambda channel, s = self: self.if_sens_worker_right(s))
		while True:
			pass
			
	def if_sens_worker_left(channel,self):
		self.wheel_encoder_left.value +=1
		
		
	def if_sens_worker_right(channel,self):
		self.wheel_encoder_right.value +=1
		
	def yaw_angel_daemon(self,lock_yaw,par):
		while True:
			with lock_yaw:
				self.yaw_angle.value += acc_driver.yaw() 	
				self.yaw_angle.value = self.yaw_angle.value % self.circle_value
				time.sleep(0.05)
				

		#this function is a multiprocess and works as a daemon
        # updates the values of x,y infitly
	def x_y_multiproc(self,lock,par):
    #init mouse
		mouse_driver.dx()
		mouse_driver.dy()
        #go for it
		while True:
			with lock:
				x = mouse_driver.fromSensToINT(mouse_driver.dx())
				y = mouse_driver.fromSensToINT(mouse_driver.dy())
				self.dx.value += x
				self.dy.value += y
	
	def odometry(self, lock, par):
		with lock:
			while True:
				yaw = self.yaw_angle.value
				#bring yaw angle from 764 circle of mpu6080 to 360 circle for calculation
				yaw = yaw * 360 /self.circle_value
				# get yaw from deg to rad
				yaw = (math.pi / 180) * yaw
				#get the changes since last iteration and reset the values for dx, dy
				# scale dx and dy to 1 cm by dividing with 170
				dx = self.dx.value 
				dy = self.dy.value / (170*self.resolution)
				
				self.dx.value = 0
				self.dy.value = 0
				
				x_new = (dx*math.cos(yaw) - dy*math.sin(yaw) )/ (170*self.resolution)
				y_new = (dx* math.sin(yaw) + dy*math.cos(yaw)) / (170*self.resolution)
				
				self.x_pos.value = x_new + self.x_pos.value
				self.y_pos.value = y_new + self.y_pos.value

				time.sleep(0.05)
				
	def forward(self, t = 0.001):
		driver.forward(t)
	def leftturn(self, t = 0.001):
		driver.leftturn(t)
	def rightturn(self, t = 0.001):
		driver.rightturn(t)
	def backward(self, t = 0.001):
		driver.backward(t)
	def circle (self):
		driver.circle()
	def square(self):
		driver.square()		

