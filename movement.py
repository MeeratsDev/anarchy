import math

squareSize = 25

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Vector2:
    def __init__(self, point):
        self.direction = directionFromPoint(point)
        self.magnitude = pythag(point)

def directionFromPoint(point):
    angle_radiants = math.atan2(point.x, point.y)
    return math.degrees(angle_radiants)

def pythag(point):
    return math.sqrt(point.x*point.x + point.y*point.y)


inputX = int(input("Enter an X value: ")) * squareSize
inputY = int(input("Enter an Y value: ")) * squareSize

point = Point(inputX, inputY)

vector = Vector2(point)

print("Direction: " + str(vector.direction) + " Magnitude: " + str(vector.magnitude))