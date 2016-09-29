
import math

def arrRound(arr, dp=0):
    arrCopy = []
    for i in range(len(arr)):
        if dp == 0:
            arrCopy.append(int(arr[i]))
        else:
            arrCopy.append(round(arr[i], dp))
    return arrCopy

def extendLine(point, angle, length):
    xPos = point[0] + length * math.cos(angle)
    yPos = point[1] + length * math.sin(angle)
    return [xPos, yPos]

def pointInRect(point, rect):
    if rect[0] < point[0] < rect[0] + rect[2]:
        if rect[1] < point[1] < rect[1] + rect[3]:
            return True
