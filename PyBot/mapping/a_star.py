"""
Standart implementation of a a-star algo
this algo uses the manhat.-heuristic
Use:
call astar( Map Instance m, start point (x,y), end point (x2,y2))
short: astar(map , (x,y), (x2,y2))
return : (list, 1) if a path was found. the list starts by start and ends by end, connecting them with nodes in betwees
returns ([], 0) if no path was found

This code is a changed version of an internet page
"""
#Manhattan Heuristic
def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

#finds all 4 neighbors of a node current in a given map
def find_neighbors(m, current):
    karte = m.d
    res = []
    x = current[0]
    maxVals = m.maxV()
    lowVals = m.lowestV()
    y = current[1]

    if( (x+1 <= maxVals[0] ) and ( (x+1, y) in karte) and karte[x+1, y] ):
        res.append( (x+1, y) )
    if ( (x- 1 >= lowVals[0] ) and ( (x-1, y) in karte) and karte[x -1, y]):
        res.append( (x -1, y) )
    if ( (y+1 <= maxVals[1] ) and ( (x, y+1) in karte) and karte[x, y+1]):
        res.append( (x, y+1) )
    if ((y- 1 >= lowVals[1] ) and  ( (x, y-1) in karte) and karte[x, y-1]):
        res.append( (x, y-1) )

    return res

# for explanation look at start of file

def astar(m, start, end):
    if not m.d[end]:
        print("End-point is inside blocked Zone. Give me a driller and i find a way!")
        return ([],0)
    G = {}  # Actual movement cost to each position from the start position
    F = {}  # Estimated movement cost of start to end going via this position

    # Initialize starting values
    G[start] = 0
    F[start] = heuristic(end, start)

    closedVertices = set()
    openVertices = set([start])
    cameFrom = {}

    while len(openVertices) > 0:
        # Get the vertex in the open list with the lowest F score
        current = None
        currentFscore = None
        for pos in openVertices:
            if current is None or F[pos] < currentFscore:
                currentFscore = F[pos]
                current = pos

        # Check if we have reached the goal
        if current == end:
            # Retrace our route backward
            path = [current]
            while current in cameFrom:
                current = cameFrom[current]
                path.append(current)
            path.reverse()
            return path, F[end]  # Done!

        # Mark the current vertex as closed
        openVertices.remove(current)
        closedVertices.add(current)

        # Update scores for vertices near the current position
        for neighbour in find_neighbors(m, current):
            if neighbour in closedVertices:
                continue  # We have already processed this node exhaustively
            candidateG = G[current] + 1

            if neighbour not in openVertices:
                openVertices.add(neighbour)  # Discovered a new vertex
            elif candidateG >= G[neighbour]:
                continue  # This G score is worse than previously found

            # Adopt this G score
            cameFrom[neighbour] = current
            G[neighbour] = candidateG
            H = heuristic(end, start)
            F[neighbour] = G[neighbour] + H
    print("no way found")
    return ([],0)
