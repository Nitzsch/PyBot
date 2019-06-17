"""
This file is the view
it creates an instance of an pretty old-school-looking window with all the infos of our robot that we need. 
it is huge. really. it is. And sometimes it breaks. yeah. 
So i am still working on making it faster and better. but it is a nice beginning and for testing reasons it fullfils 
all that i am wanting. 

This file could be replaced by an appache-server and an interactive website (you would also need to prepare a wlan-access point 
for the pi or a dynamic hosting page in the net, lot more complicated). If you implement it with bootstrap and CSS elements
it would look a lot better. But it would also slow down the pi in general. 

Not implemented yet:

1. Mapping Function, Mapping Test button
        need to implement it here, driver works already
2. Change circle and square drive to take a n argument as radius/side
        need to implement that stuff in the driver first
3. drive_to x,y
        need to implement it here, the driver works already

"""

from PIL import Image, ImageTk
import Tkinter as tk
import argparse
import time
import datetime
import cv2
import os
import re
import subprocess
import urllib
import robot
import mapping.map as RMap

#https://www.raspberrypi.org/forums/viewtopic.php?t=230454

class Application:
    def __init__(self, output_path = "./"):
        global rob
        """ Initialize application which uses OpenCV + tkinter. It displays
            a video stream in a tkinter window and stores current snapshot on disk """
        self.vs = cv2.VideoCapture(0) # capture video frames, 0 is your default video camera
        #pos resolutions: 6440x480, 
        self.vs.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 480)
        self.vs.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 360)
        self.output_path = output_path  # store output path
        self.current_image = None  # current image from the camera
        self.root = tk.Tk()  # initialize root window
        defaultbg = self.root.cget('bg') # set de default grey color to use in labels background
        w = 900 # width for the Tk root
        h = 545   # height for the Tk root

        ws = self.root .winfo_screenwidth() # width of the screen
        hs = self.root .winfo_screenheight() # height of the screen
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root .grid()
        self.root.title("     PyBots Eye     ")  # set window title
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        live_Data_Frame = tk.LabelFrame(self.root, background="blue", pady=10,padx=10,
        bd=3, labelanchor="n", text ="Live-Data")
        map_Data_Frame =  tk.LabelFrame(self.root, background="red", bd=3, pady=10,padx=10,
        labelanchor="n", text ="Map-Data")
        live_Data_Frame.grid(row=0, column=0, sticky="n"+"e"+"s"+"w")
        map_Data_Frame.grid(row= 0, column=1, sticky="n"+"e"+"s"+"w")


        #put here my stuff

        # ------------------------------------------------------------------------
        # set live_dataFrame and map_Data_frames with attributes
        # ------------------------------------------------------------------------

        self.live_Data_Frame = tk.LabelFrame(self.root, background="blue", pady=10, padx=10,
                                        bd=3, labelanchor="n", text="Live-Data")
        self.map_Data_Frame = tk.LabelFrame(self.root, background="red", bd=3, pady=10, padx=10,
                                       labelanchor="n", text="Map-Data")
        self.live_Data_Frame.grid(row=0, column=0, sticky="n" + "e" + "s" + "w")
        self.map_Data_Frame.grid(row=0, column=1, sticky="n" + "e" + "s" + "w")

        # ------------------------------------------------------------------------
        # set Frames in live data:
        # ------------------------------------------------------------------------
        self.video_Frame = tk.LabelFrame(self.live_Data_Frame, pady=10, padx=10,
                                    text="Camera-Stream", bd=3, labelanchor="n")
        self.video_Frame.grid(sticky="n" + "e" + "s" + "w")

        self.dist_Frame = tk.LabelFrame(self.live_Data_Frame, pady=10, padx=10,
                                   text="Data", bd=3, labelanchor="n")
        self.dist_Frame.grid(sticky="n" + "e" + "s" + "w")

        self.other_Data_Frame = tk.LabelFrame(self.live_Data_Frame, pady=10, padx=10,
                                         text="Other Stuff", bd=3, labelanchor="n")
        self.other_Data_Frame.grid(sticky="n" + "e" + "s" + "w")

        # ------------------------------------------------------------------------
        # set Frames in map_data_frame
        # ------------------------------------------------------------------------

        self.map_Frame = tk.LabelFrame(self.map_Data_Frame, pady=10, padx=10,
                                  text="Grid-Map", bd=3, labelanchor="n")
        self.map_Frame.grid(row=0, sticky="n" + "e" + "s" + "w")

        self.fun_Frame = tk.LabelFrame(self.map_Data_Frame, pady=10, padx=10,
                                  text="Functions", bd=3, labelanchor="n")
        self.fun_Frame.grid(row=1, sticky="n" + "e" + "s" + "w")

        self.drive_xy_Frame = tk.LabelFrame(self.map_Data_Frame, pady=10, padx=10,
                                       text="x-y-Order", bd=3, labelanchor="n")
        self.drive_xy_Frame.grid(row=2, sticky="n" + "e" + "s" + "w")

        self.drive_Frame = tk.LabelFrame(self.map_Data_Frame, pady=10, padx=10,
                                    text="Driving Commands direct", bd=3, labelanchor="n")
        self.drive_Frame.grid(row=3, sticky="n" + "e" + "s" + "w")

        # ------------------------------------------------------------------------
        # set Widgets in live data
        # ------------------------------------------------------------------------

        
        # ------------------------------------------------------------------------
        # def DistData
        # ------------------------------------------------------------------------
        # The Txt Vars are holders for the values out of the Sensor-Functions
        self.front_Dist_Label_txtVar = tk.StringVar()
        self.front_Dist_Label = tk.Label(self.dist_Frame, textvariable=self.front_Dist_Label_txtVar)
        self.front_Dist_Label.grid(column=0, sticky="n" + "e" + "s" + "w", padx=5, pady=5)

        self.left_Dist_Label_txtVar = tk.StringVar()
        self.left_Dist_Label = tk.Label(self.dist_Frame, textvariable=self.left_Dist_Label_txtVar)
        self.left_Dist_Label.grid(column=0, sticky="n" + "e" + "s" + "w", padx=5, pady=5)

        self.right_Dist_Label_txtVar = tk.StringVar()
        self.right_Dist_Label = tk.Label(self.dist_Frame, textvariable=self.right_Dist_Label_txtVar)
        self.right_Dist_Label.grid(column=0, sticky="n" + "e" + "s" + "w", padx=5, pady=5)

        self.IF_left_Dist_Label_txtVar = tk.StringVar()
        self.IF_left_Dist_Label = tk.Label(self.dist_Frame, textvariable=self.IF_left_Dist_Label_txtVar)
        self.IF_left_Dist_Label.grid(row=0, column=1, sticky="n" + "e" + "s" + "w", padx=5, pady=5)

        self.iF_right_Dist_Label_txtVar = tk.StringVar()
        self.iF_right_Dist_Label = tk.Label(self.dist_Frame, textvariable=self.iF_right_Dist_Label_txtVar)
        self.iF_right_Dist_Label.grid(row=1, column=1, sticky="n" + "e" + "s" + "w", padx=5, pady=5)

        self.cliff_right_Dist_Label_txtVar = tk.StringVar()
        self.cliff_right_Dist_Label = tk.Label(self.dist_Frame, textvariable=self.cliff_right_Dist_Label_txtVar)
        self.cliff_right_Dist_Label.grid(row=0, column=2, sticky="n" + "e" + "s" + "w", padx=5, pady=5)

        self.cliff_left_Dist_Label_txtVar = tk.StringVar()
        self.cliff_left_Dist_Label = tk.Label(self.dist_Frame, textvariable=self.cliff_left_Dist_Label_txtVar)
        self.cliff_left_Dist_Label.grid(row=1, column=2, sticky="n" + "e" + "s" + "w", padx=5, pady=5)

        self.wheel_right_Dist_Label_txtVar = tk.StringVar()
        self.wheel_right_Dist_Label = tk.Label(self.dist_Frame, textvariable=self.wheel_right_Dist_Label_txtVar)
        self.wheel_right_Dist_Label.grid(row=0, column=3, sticky="n" + "e" + "s" + "w", padx=5, pady=5)

        self.wheel_left_Dist_Label_txtVar = tk.StringVar()
        self.wheel_left_Dist_Label = tk.Label(self.dist_Frame, textvariable=self.wheel_left_Dist_Label_txtVar)
        self.wheel_left_Dist_Label.grid(row=1, column=3, sticky="n" + "e" + "s" + "w", padx=5, pady=5)

        # other Data frame
        self.x_Pos_other_Data_Label_txtVar = tk.StringVar()
        self.x_Pos_other_Data_Label = tk.Label(self.other_Data_Frame, textvariable=self.x_Pos_other_Data_Label_txtVar)
        self.x_Pos_other_Data_Label.grid(column =0,row=0, sticky="n" + "e" + "s" + "w", padx=5, pady=5)

        self.y_Pos_other_Data_Label_txtVar = tk.StringVar()
        self.y_Pos_other_Data_Label = tk.Label(self.other_Data_Frame, textvariable=self.y_Pos_other_Data_Label_txtVar)
        self.y_Pos_other_Data_Label.grid(column=0, row=1,sticky="n" + "e" + "s" + "w", padx=5, pady=5)
        
        self.dy_other_Data_Label_txtVar = tk.StringVar()
        self.dy_other_Data_Label = tk.Label(self.other_Data_Frame, textvariable=self.dy_other_Data_Label_txtVar)
        self.dy_other_Data_Label.grid(column=3, row=1,sticky="n" + "e" + "s" + "w", padx=5, pady=5)
        
        self.dx_other_Data_Label_txtVar = tk.StringVar()
        self.dx_other_Data_Label = tk.Label(self.other_Data_Frame, textvariable=self.dx_other_Data_Label_txtVar)
        self.dx_other_Data_Label.grid(column=3, row=0,sticky="n" + "e" + "s" + "w", padx=5, pady=5)
        
        self.yaw_Winkel_other_Data_Label_txtVar = tk.StringVar()
        self.yaw_Winkel_other_Data_Label = tk.Label(self.other_Data_Frame, textvariable=self.yaw_Winkel_other_Data_Label_txtVar)
        self.yaw_Winkel_other_Data_Label.grid(column=1, row=0, sticky="n" + "e" + "s" + "w", padx=5, pady=5)

        self.other_Robo_other_Data_Label_txtVar = tk.StringVar()
        self.other_Robo_other_Data_Label = tk.Label(self.other_Data_Frame, textvariable=self.other_Robo_other_Data_Label_txtVar)
        self.other_Robo_other_Data_Label.grid(column=1, row= 1,sticky="n" + "e" + "s" + "w", padx=5, pady=5)


        # ------------------------------------------------------------------------
        # set Widgets in Map Data
        # ------------------------------------------------------------------------
        # def all the button functions:

        def start_mapping_Fun():
            m = RMap.Map(robot)
            m.startMapping()

        def reset_mapping():
            pass
        def shutdown():
            from subprocess import call
            call("sudo shutdown -P now", shell=True)

        def drive_xy(x, y):
            pass
            
        def drive_forward():
            robot.driver.forward()

        def drive_backward():
            robot.driver.backward()

        def drive_left():
            robot.driver.leftturn()
            

        def drive_right():
            robot.driver.rightturn()

        def drive_circle():
            robot.driver.circle()

        def drive_square():
            robot.driver.square()
        
                                
        # map
        self.map_Img = ImageTk.PhotoImage(Image.open("test.png"))
        self.map_Img_Label = tk.Label(self.map_Frame, image=self.map_Img)
        self.map_Img_Label.grid(sticky="n" + "e" + "s" + "w")

        # Fun-buttons
        self.start_mapping_Button = tk.Button(self.fun_Frame, text="Start Mapping", command=start_mapping_Fun)
        self.start_mapping_Button.grid(row=0, column=0)

        self.shutdown_Button = tk.Button(self.fun_Frame, text="shutdown Pi", command=shutdown)
        self.shutdown_Button.grid(row=0, column=2)

        self.reset_Mapping_Button = tk.Button(self.fun_Frame, text="reset Mapping", command=reset_mapping)
        self.reset_Mapping_Button.grid(row=0, column=1)

        # drive xy-Labels and buttons
        self.drive_xy_Label = tk.Label(self.drive_xy_Frame, text="Drive to Pos:")
        self.drive_xy_Label.grid(row=0, column=0)

        self.drive_xy_x_Label = tk.Label(self.drive_xy_Frame, text="x:")
        self.drive_xy_x_Label.grid(row=1, column=0)
        self.drive_xy_y_Label = tk.Label(self.drive_xy_Frame, text="y:")
        self.drive_xy_y_Label.grid(row=2, column=0)

        self.drive_x_Entry = tk.Entry(self.drive_xy_Frame)
        self.drive_y_Entry = tk.Entry(self.drive_xy_Frame)

        self.drive_x_Entry.grid(row=1, column=1)
        self.drive_y_Entry.grid(row=2, column=1)

        self.go_xy_Button = tk.Button(self.drive_xy_Frame, text="Go", command=drive_xy(self.drive_x_Entry.get(), self.drive_y_Entry.get()))
        self.go_xy_Button.grid(row=2, column=2, sticky="n" + "e" + "s" + "w")

        # Drive Buttons : Functions need implementation!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.drive_forward_Button = tk.Button(self.drive_Frame, text="Forward", command=drive_forward)
        self.drive_forward_Button.grid(row=0, column=0, sticky="n" + "e" + "s" + "w")

        self.drive_backward_Button = tk.Button(self.drive_Frame, text="Backward", command=drive_backward)
        self.drive_backward_Button.grid(row=0, column=1, sticky="n" + "e" + "s" + "w")

        self.drive_left_Button = tk.Button(self.drive_Frame, text="left", command=drive_left)
        self.drive_left_Button.grid(row=0, column=2, sticky="n" + "e" + "s" + "w")

        self.drive_right_Button = tk.Button(self.drive_Frame, text="right", command=drive_right)
        self.drive_right_Button.grid(row=0, column=3, sticky="n" + "e" + "s" + "w")

        self.drive_circle_Button = tk.Button(self.drive_Frame, text="circle", command=drive_circle)
        self.drive_circle_Button.grid(row=1, column=0, sticky="n" + "e" + "s" + "w")

        self.drive_square_Button = tk.Button(self.drive_Frame, text="square", command=drive_square)
        self.drive_square_Button.grid(row=1, column=1, sticky="n" + "e" + "s" + "w")


        self.panel = tk.Label(self.video_Frame)  # initialize image panel
        self.panel.grid(row=0, rowspan=10, column=8, columnspan=25, padx=4, pady=6)

        self.video_loop()


    def video_loop(self):
        """ Get frame from the video stream and show it in Tkinter """
        #self.label_setter()
        ok, frame = self.vs.read()  # read frame from video stream
        if ok:  # frame captured without any errors
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  # convert colors from BGR to RGBA
            self.current_image = Image.fromarray(cv2image)  # convert image for PIL
            imgtk = ImageTk.PhotoImage(image=self.current_image)  # convert image for tkinter
            self.panel.imgtk = imgtk  # anchor imgtk so it does not be deleted by garbage-collector
            self.panel.config(image=imgtk)  # show the image
            
        
        self.dx_other_Data_Label_txtVar.set("Dx: %s "% rob.dx.value)
        self.dy_other_Data_Label_txtVar.set("Dy: %s"% rob.dy.value)
        self.other_Robo_other_Data_Label_txtVar.set("Other Robot seen? %s" % False)
        self.front_Dist_Label_txtVar.set("front: %s" %rob.distance_front.value)
        self.left_Dist_Label_txtVar.set("left: %s"% rob.distance_left.value)
        self.right_Dist_Label_txtVar.set("right: %s"% rob.distance_right.value)
        self.IF_left_Dist_Label_txtVar.set("IF left: %s"% rob.distance_IF_left.value)
        self.iF_right_Dist_Label_txtVar.set("IF right: %s"% rob.distance_IF_right.value)
        self.cliff_right_Dist_Label_txtVar.set("cliff right: %s"% rob.cliff_right.value)
        self.cliff_left_Dist_Label_txtVar.set("cliff left: %s"%  rob.cliff_left.value)
        self.wheel_right_Dist_Label_txtVar.set("wheel right: %s"% rob.wheel_encoder_right.value)
        self.wheel_left_Dist_Label_txtVar.set("wheel left: %s" % rob.wheel_encoder_left.value)
        self.yaw_Winkel_other_Data_Label_txtVar.set("yaw angle: %s"% rob.yaw_angle.value)
        self.root.after(30, self.video_loop)  # call the same function after 30 milliseconds
        self.y_Pos_other_Data_Label_txtVar.set("y-Pos: %s" %rob.y_pos.value)
        self.x_Pos_other_Data_Label_txtVar.set("x-Pos: %s" %rob.x_pos.value)
        

    def destructor(self):
        self.root.destroy()
        self.vs.release()  # release web camera
        cv2.destroyAllWindows()  # it is not mandatory in this application

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default="./",
    help="path to output directory to store snapshots (default: current folder")
args = vars(ap.parse_args())
rob = robot.Pybot()
# start the app
pba = Application(args["output"])
pba.root.mainloop()
