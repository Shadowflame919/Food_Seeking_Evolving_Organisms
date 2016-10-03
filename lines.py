"""


"""

import math

def midPoint(line):
    xPos = (line[0][0] + line[1][0]) / 2
    yPos = (line[0][1] + line[1][1]) / 2
    return [xPos, yPos]

def distFromPoints(point1, point2):
    xDist = point1[0] - point2[0]
    yDist = point1[1] - point2[1]
    return math.hypot(xDist, yDist)

def lineToLineIntersect(line1, line2):  # returns whether two lines intersect
    line1 = orderLineX(line1)
    line2 = orderLineX(line2)
    #print("Testing lines " + str(line1) + " and " + str(line2))
    
    basicLineInt = basicLineIntersect(line1, line2)
    if basicLineInt == False:
        #print("Lines not colliding at all")
        return False
    #print("Lines might be colliding!")
    
    m1 = lineGradient(line1)
    m2 = lineGradient(line2)
    #print("Lines gradients are " + str(m1) + " and " + str(m2))
    if m1 == None and m2 == None:   # Parallel vertical lines
        maxY1 = max(line1[0][1], line1[1][1])
        maxY2 = max(line2[0][1], line2[1][1])
        return [line1[0][0], min(maxY1, maxY2)]
        
    if m1 == None:  # First line is vertical
        b2 = lineB(line2[0], m2)
        lineIntY = m2 * line1[0][0] + b2
        minY1 = min(line1[0][1], line1[1][1])
        minY2 = min(line2[0][1], line2[1][1])
        maxY1 = max(line1[0][1], line1[1][1])
        maxY2 = max(line2[0][1], line2[1][1])
        if lineIntY > max(minY1, minY2) and lineIntY < min(maxY1, maxY2):
            return [line1[0][0], lineIntY]
        return False
    if m2 == None:  # Second line is vertical
        b1 = lineB(line1[0], m1)
        lineIntY = m1 * line2[0][0] + b1
        minY1 = min(line1[0][1], line1[1][1])
        minY2 = min(line2[0][1], line2[1][1])
        maxY1 = max(line1[0][1], line1[1][1])
        maxY2 = max(line2[0][1], line2[1][1])
        if lineIntY > max(minY1, minY2) and lineIntY < min(maxY1, maxY2):
            return [line2[0][0], lineIntY]
        return False
    
    b1 = lineB(line1[0], m1)
    b2 = lineB(line2[0], m2)
    #print("Lines b's are " + str(b1) + " and " + str(b2))
    if m1 == m2:    # Parallel
        #print("Lines are parallel, botdistFromPoints(line[0],[x1,y1])h have gradient of " + str(m1))
        if b1 == b2:
            #print("Lines are equal")
            return line1[0]
        return False

    lineIntX = (b2 - b1) / (m1 - m2)
    #print("Lines collide at an X of " + str(lineIntX))
    if lineIntX > max(line1[0][0], line2[0][0]) and lineIntX < min(line1[1][0], line2[1][0]):
        lineIntY = m1 * lineIntX + b1
        #print("Lines Collide at " + str([lineIntX, lineIntY]) + "\n")
        return [lineIntX, lineIntY]
    #print("Lines dont collide")
    return False

def orderLineX(line):   # Orders line points with lowest x first
    if line[0][0] > line[1][0]:
        return [line[1], line[0]]
    return line

def orderLineY(line):   # Orders line points with lowest y first
    if line[0][1] > line[1][1]:
        return [line[1], line[0]]
    return line

def basicLineIntersect(line1, line2):
    minX1 = line1[0][0]
    maxX1 = line1[1][0]
    minX2 = line2[0][0]
    maxX2 = line2[1][0]
    if maxX2 > minX1 and minX2 < maxX1:
        minY1 = min(line1[0][1], line1[1][1])
        maxY1 = max(line1[0][1], line1[1][1])
        minY2 = min(line2[0][1], line2[1][1])
        maxY2 = max(line2[0][1], line2[1][1])
        if maxY2 > minY1 and minY2 < maxY1:
            return True
    return False

def lineGradient(line):
    if line[0][0] == line[1][0]:
        return None
    return (line[0][1]-line[1][1]) / (line[0][0]-line[1][0])

def lineB(point, gradient):
    return point[1] - (gradient * point[0])

def pointAlongLine(point, line):   # Takes in a point and an unordered line and returns how far along the line the point is
    m1 = lineGradient(line)
    #print("Line gradient: " + str(m1))
    if m1 == 0: # Line is horizontal
        #print("Line is horizontal...")
        if line[0][0] < line[1][0]:
            if point[0] < line[0][0]:
                return 0
            if point[0] > line[1][0]:
                return abs(line[1][0] - line[0][0])
        else:
            if point[0] > line[0][0]:
                return 0
            if point[0] < line[1][0]:
                return abs(line[0][0] - line[1][0])
        return abs(point[0] - line[0][0])
    
    if m1 == None:  # Line is vertical
        #print("Line is vertical...")
        if line[0][1] < line[1][1]:
            if point[1] < line[0][1]:
                return 0
            if point[1] > line[1][1]:
                return abs(line[1][1] - line[0][1])
        else:
            if point[1] > line[0][1]:
                return 0
            if point[0] < line[1][1]:
                return abs(line[0][1] - line[1][1])
        return abs(point[1] - line[0][1])
    
    b1 = lineB(line[0], m1)
    #print("Y intercept is " + str(b1))
    x0 = point[0]
    y0 = point[1]
    x1 = (m1 * (y0 - b1) + x0) / (m1*m1 + 1)
    y1 = m1 * x1 + b1
    #print("Collision point on the line is " + str([x1,y1]))

    if line[0][0] < line[1][0]:
        if x1 < line[0][0]:
            return 0
        if x1 > line[1][0]:
            return distFromPoints(line[0],line[1])
    else:
        if x1 > line[0][0]:
            return 0
        if x1 < line[1][0]:
            return distFromPoints(line[0],line[1])
        
    return distFromPoints(line[0],[x1,y1])

def distPointToLine(point, line):   # Takes in a point and an unordered line
    line = orderLineX(line)
    m1 = lineGradient(line)
    
    if m1 == 0: # Line is horizontal
        if point[0] < line[0][0]:
            return distFromPoints(point,line[0])
        if point[0] > line[1][0]:
            return distFromPoints(point,line[1])
        return abs(point[1] - line[0][1])
    
    if m1 == None:  # Line is vertical
        if point[1] < line[0][1]:
            return distFromPoints(point,line[0])
        if point[1] > line[1][1]:
            return distFromPoints(point,line[1])
        return abs(point[0] - line[0][0])
    
    b1 = lineB(line[0], m1)
    x0 = point[0]
    y0 = point[1]
    x1 = (m1 * (y0 - b1) + x0) / (m1*m1 + 1)
    y1 = m1 * x1 + b1

    if x1 < line[0][0]:
        return distFromPoints([x0,y0],line[0])
    if x1 > line[1][0]:
        return distFromPoints([x0,y0],line[1])
    return distFromPoints([x0,y0],[x1,y1])





















