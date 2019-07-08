import time
import robot
import mapping.map as Map
import mapping.a_star as a_star
import mapping.map_printer as map_print
import mapping.map_creator as creator
import mapping.drive_by_mouse as drive_by_mouse


if __name__ == '__main__':
    r = robot.Pybot()
    m = Map.Map(r)
    time.sleep(0.2)
    m.addPos(0,-1,True)

    #m.startMapping()
    m.addSquare(20)
    drive_by_mouse.drive_to(r,m,(0,2))
    print(r.x_pos.value ,r.y_pos.value)
    time.sleep(2)
    drive_by_mouse.drive_to(r,m,(0,1))
    #print(r.x_pos.value ,r.y_pos.value)
    
