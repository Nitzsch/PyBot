"""
This files only purpose is to pretty print the given map. 
Input to printer is a map, the path the robot took and a planned path
if there is no path the robot took or planned path, they args can be left

printer(map, rob_path, planned_path)

result is nothing. 
is saves the file in this folder. the name is by default test.png
(this two things could be changed if wanted. 

"""

import numpy as np
from PIL import Image

def printer(m, rob_path=[], planned_path=[]):
    maxV = m.maxV()
    minV = m.lowestV()
    x_range = maxV[0] + abs(minV[0])
    y_range = maxV[1] + abs(minV[1])

    arr = np.zeros([x_range +1,y_range + 1])

    for i in m.d:
        if(m.d[i]):
            arr[(i[0]+ abs(minV[0]), i[1] + abs(minV[1]))] = 255
        else:
            arr[(i[0]+ abs(minV[0]), i[1] + abs(minV[1]))] = 125

    image = Image.fromarray(arr)
    image = image.convert("L")

    pixels = image.load()
    for i in rob_path:
        pixels[i] = 0
    pixels = image.load()
    for i in planned_path:
        pixels[i] = (50)


    image = image.resize([350,350],Image.NEAREST)
    filename = "test.png"
    image.save(filename)
    image.show()


