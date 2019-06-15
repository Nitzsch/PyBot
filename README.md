# PyBot
Framework of a Raspberry Pi Robot written in Python for private use

## Motivation
This Project is my Bachelor-Thesis in Computer Science (University of Tuebingen, Germany). 
I asked my Prof to build a Swarm of little Mobile Robots for it, he encouraged me not only, but helped a lot in getting started and finishing crucial parts of the code. So this is the result of my work from the 1. April to the 31. July. 

## Robot Base
The robot was build with left-over parts of an old c’t-Bot from 2006. Please do not laugh. It worked perfectly ;D

## Status
Please note that this code is still not finished. I am still working on : 

*Mapping: 
the drive-to is not working correct if the robot has to go left or right. The problem seems to be a bigger one. I noticed that the transformation of the opti-flow-sensor-frame to the robot-middle-frame is still bugy. Currently thats my task for the next week. 

*View: 
The view app sometimes crashes. I Do not know if it is a problem of the view code itself (to big, to lousy coded) or if the pi does not like it to do all the stuff it has to if we look at the view. 
The view acitvates not only all the deamons of the robot itself, but also the map, the cam and stream, but also a lot of dynamic graphics for the frames. I need to refactor this as a hole. More classes? Less classes? Break it into more pieces? I will try to solve this. 
Big problem with it: 
Crashes only sometimes. I could not provoke it. So… Yeah. 


## Getting Started

This hole Framework is coded for a Raspberry Pi 3. The Sensors used, the Board-Layout and so on, can be found in the Hardware section. 
If you do not like to solder, do not go there. It took a lot of tin to get me a working Board. If you are interested in this kind of stuff, please be kind with me. As a computer science student we never ever learn to really solder anything. You get a task, you code some java. Or you are asked on paper to design a chip layout for doing stuff. But to build it and code it… No. 
So this is all learned by watching myself fail. And our janitor in my dorm. He is great and 
taught me how to cut wood without cutting my fingers and many other useful stuff. 

If you already have a robot and just need some code here you go. 

### Installing

For the Framework to work you will need a working Raspberry Pi with Rasbian. Please install a fresh version and update it, so it can work properly. 
This is not explained here. You will find great Tutorials for this stuff on the Page of the Raspberry Pi Foundation. They are doing a great job (especially for beginners). 

Just the basic: 
##### Python
The Framework will run on 2.7 or higher. Please note, that the names of some packages changed from 2.x to 3.x ! Like PIL and CV. 
If you need help to find your version: google. 
What you will need: 
* PIL
* CV
* numpy
* Tkinter
* smbus
* Adafruit_ADS1x15

Easy install with pip. You need to keep track of what Python Version your running the code.
You also can use a different version of l293D but then you need to change the code in the drivers. Same goes for the mcp23017

If something in the imports go wrong: Check your version of Python and the versions of your downloads. If thats ok, check the folder structure. The import in the scripts are based on the given structure. If you change it, it will fail. 

## Pins
First you have to declare the pins you are using in 
Main – Drivers – pin_belegung.py
Here you will find all the pins for the sensors. 
Please note that there are two different pin sorts: 
* pins directly at the Pi.
* pins connected to the MCP23017. This chip is used to create more pins for the LCD. These pins are a lot slower then the PI pins (working with I2C). Also our Cliff-Sensors are connected to this.

## Tests

In the main folder you will find a file called test. Here you can play around with the robot. 

```
rob = robot.Pybot()
```
creates an instance of the robot. 
Now you can use the class-methodes of the robot class to work with it

```
print(rob.x_pos.value)
print(rob.front_distance.value)

```
You need to keep in mind, that the atributes of the robot are multiprocess values. So to call them it is enough to say 
```
rob.x_pos
```
but to actually see a value: 
```
rob.x_pos.value
```


## Version
This is Version 2. It will be upgraded and changed constantly. So if it breaks, I will try to fix it. 

## Authors

* **Tolga Demir** - *Initial work* - [Nitzsch](https://github.com/Nitzsch)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Prof. Zell
* Haile, the Janitor
* C’t-Magazine. 
