# Hardware
<img src="https://cdn.website-editor.net/5eacb7d2f6da4c0dab9b3c16306e15f4/dms3rep/multi/tablet/Ctbot_jetzt.jpg" width="400" height="600">

Or say hello to… what is this?! The 80ies?
Maybe not. 
It is called C’t-Bot. A robot created by the computer magazine C’t. It was widly known in Germany, back when people read papers. Yeah, I know. Papers. 
It was sold for about 200 Euros (wow). It was fully programmable with a self-implemented language (something between c and Arduinos ). It was capable of not so much. A little (mostly not working) wheel-odom., some sensors for distance and light (put directly in front of a LED…yeah, really) and an old Atmel AVR ATmega16 Microcontroller for the computing. 

Most of this stuff is straight trash. But there are some gold nuggets: 

## IR-Sensors
The two IR-Sensors located at the front are from Sharp (GP2D12). They are still sold for around 10-15 Euro each and are quite good for distances between 10-80 cm. 
And, most important: They work perfectly even after laying around for 15 years. 

## Opti-Flow-Sensor
The Opti-Flow- Sensor from Avago (ADNS- 26010) is a perfect piece of unknown sensor that almost every person on earth at least once held in the tip of there palm. It was build in a lot – really a lot – of computer mouses around the world. In the newest version it is still in use for mouse today. 
Why would someone build this thing in a robot? 
For the Odometry! And it works. Even after that long it reacts to a resolution of under 1mm in change of the x-y-frame. Thats so great. 

## The Engine: 
Faulhaber 2619 SR 006 DC-Motor (5-6V). Made in Germany. Why should they ever fail? 

##L293D Chip
Still working, still in use. 

## Most annoying
C’t – Bot used a plug-in cable that was lost and is not on the market anymore. No way to change any of the code on the robot. It was used for a PhD in the 2006s and then left to die. 

##And now? 
I had to think about new Sensors, that would fulfill modern Algorithms and – maybe – were able to use some cable I could plug into my laptop. 
So thatstuff can be found here: [Hardware to future](Hardware2.md)
