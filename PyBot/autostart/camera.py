"""
This file only activates the camera. It is needed if the camera is not on as default setting by the pi. This is done via 
sudo raspi-config, go to interface settings and turn on camera. 
If this is not possible, make this file excutable, write it as a cron-job or into etc/rc.local befor the &end 
or or or. Just so that the file is started before any of the scripts. If not done, the view will not show the video stream. 

to the file itself: 
it calles the subprocess and writes out in shell to turn on the cam. 
"""

from subprocess import call

call("sudo modprobe bcm2835-v4l2", shell=True)
