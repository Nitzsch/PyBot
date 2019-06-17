"""

Our Map class. 
This class creates a map instance
each map has a name, a dict called d that repr. nodes, a robot class instance rob, a set of unvisted nodes and a resolution (in cm)
also the class keeps track of the lowest x,y value seen and the lowest x, y

the map can be initialized with an empty suqare of nxn or a rnd filled square for testing. also it is possible to add rnd values for testing

the map can be written out to a txt file and also a txt file can be read out to create a dict d of nodes (for multi-map purposes)

the map is created in co -work with the file map_creator. 

"""

import random
import map_creator
import map_printer 

class Map:
    def __init__(self, rob, name = None, positionRobot = (0,0)):
        self.d = {}
        self.name = name
        self.positionRobot = (0,0) #(rob.x_pos.value, rob.y_pos.value)
        self.unvisitedNodes = set()
        self.path = "map.txt"
        self.rob = rob
        self.lowX = 0
        self.lowY = 0
        self.maxX = 0
        self.maxY = 0
        self.resolution = 5

    def addRandomValues(self,x,y):
        for i in range(x):
            for j in range(y):
                self.addPos(i,j,bool(random.getrandbits(1)))
    
    def addEmptySquare(self,size):
        for i in range(size):
            for j in range(size):
                self.addPos(i,j,True)
    
    def addSquare(self, size):
        for i in range(size):
            for j in range(size):
                self.addPos(i,j,False)

        for i in range(size):
            self.addPos(0, i, True)
            self.addPos(i, 0, True)
            self.addPos(i, size, True)
            self.addPos(size, i, True)
            for j in range(int(size / 2)):
                #if random.getrandbits(1):
                self.addPos(i, j * 2, True)
                #if random.getrandbits(1):
                self.addPos(j * 2, i, True)
        self.addPos(size,size,True)

    #returns the # of Pos in map
    def getLength(self):
        return self.d.__len__()
        
    def maxV(self):
        return (self.maxX, self.maxY)
        
    def lowestV(self):
        return (self.lowX,self.lowY)
        
        
    #returns a given position of the map if it is in map, else -1
    def getPos(self,x,y):
        if (x, y) in self.d:
            return self.d[(x,y)]
        else:
            return 0


    #adds a position to map, no check before. Overrides if already there.
    def addPos(self,x,y,data):
        self.d[(x,y)] = data
        if data:
            self.unvisitedNodes.add((x,y))

        #update maxX, maxY, minX, minY
        if(x > self.maxX):
            self.maxX = x
        if(y > self.maxY):
            self.maxY = y
        if(x < self.lowX):
            self.lowX = x
        if(y < self.lowY):
            self.lowY = y

    #checks a given pos if already checked
    def isChecked(self,x,y):
        if (x,y) in self.d:
            return True
        else:
            return False

    #check if map is complete. Done by checking if unvisited nodes is empty
    #IMPORTANT:
    #Robot starts with empty unvisited nodes! Means: Do not check if its the end
    # at the beginning of maping. Then the robot would do nothing.
    def end(self):
        if not self.unvisitedNodes:
            return True
        else:
            return False

    #start mapping
    def startMapping(self):
        map_creator.start(self.rob, self)


    #writes the map to a txt file at path location
    def writeOutToTXT(self):
        fo = open(self.path,"w")
        for v in self.d:
            fo.write(str(v) +" "+ str(self.d[v]) + '\n')
        fo.close()

    #reads txt from path and returns a dictMap of it
    def readFromTxt(self):

        with open(self.path) as file:
            lines = []
            for line in file:
                # The rstrip method gets rid of the "\n" at the end of each line
                lines.append(line.rstrip().split(","))

        df = {}
        for i in lines:
            if i[3][1] == "F":
                blocked = False
            else:
                blocked = True

            path = i[2].strip()
            path = path.replace("'", "")
            x = int(i[0][1])
            y = int(i[1][1])
            df[(x, y)] = (x, y, path, blocked)

        return df
