from hub import port, light_matrix, button, motion_sensor, sound
import runloop, motor, time, force_sensor, motor_pair, math

# Pair the drive motors on ports C (right) and D (left)
motors = motor_pair.pair(motor_pair.PAIR_1, port.C, port.D)

# MOVE FORWARD FUNCTION
def move(distance, mode, speed):
    if mode == 'forward': # Rotates wheels in oposite directions to go straight
        motor.run_for_degrees(port.C, -distance, speed)# Right wheel
        motor.run_for_degrees(port.D, distance, speed)# Left wheel
    elif mode == 'turn': # Rotates wheels in the same direction to turn
        motor.run_for_degrees(port.C, distance, speed)# Right wheel
        motor.run_for_degrees(port.D, distance, speed)# Left wheel

### STOP MOVEMENT
def stopMove():
    motor.stop(port.C)
    motor.stop(port.D)

# Test square function, can remove before submission
def square():
    for i in range(4):
        print("turning")
        move(200, "turn", 800)
        time.sleep(0.5)
        print("moving forwards")
        move(1000, "forward", 800)
        time.sleep(2)

class InputManager:
    # Call getInput(key) to see if the key was *pressed this frame*.

    def __init__(self):
        # key states stored as: 0 = idle; 1 = pressed this tick; 2 = held
        self.states = {
            'green': 0,
            'red': 0,
            'left': 0,
            'right': 0
        }

    def _updateState(self, key, is_pressed):
        # Internal state machine:

        # 0 + press = 1
        # 1 next tick = 2
        # 2 + release = 0

        # Return True ONLY on state == 1 (just pressed)

        state = self.states[key]
        if state == 1: # Transition from 1 to 2 automatically
            self.states[key] = 2
        if is_pressed: # Handle press
            if state == 0:
                self.states[key] = 1 # just pressed
                return True # return True for this frame only
        else: # Handle release
            if state == 2:
                self.states[key] = 0

        return False # not a new press this frame

    def getInput(self, keyname):
        # Pass keyname as a string:
        # - 'green'
        # - 'red'
        # - 'left'
        # - 'right'

        if keyname == 'green':
            is_pressed = force_sensor.force(port.A) >= 50
        elif keyname == 'red':
            is_pressed = force_sensor.force(port.B) >= 50
        elif keyname == 'left':
            is_pressed = button.pressed(button.LEFT)
        elif keyname == 'right':
            is_pressed = button.pressed(button.RIGHT)
        # Add more buttons if needed
        else:
            raise ValueError('Invalid key name for getInput()')

        return self._updateState(keyname, is_pressed)

# Screen Module containing functions for button detection and updating the screen
class Screen:

    screenUpdate = False
    mode = "grid"
    num = 0
    gridSideLengths = 5

    # 0 = empty space; 1 = obstical; 2 = start point; 3 = end point
    # All zero when program starts
    matrix = [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    # Converts mode strings to numbers that we can use to change the value of a cell in the matrix
    modeDict = {
        "grid" : 1, # main obstical adding mode
        "start" : 2, # Add the starting point
        "end" : 3, # add the ending point
        # Add more modes if needed e.g. - yes hayden I added these to the list but didn't make them, these could be useful and are really quite easy to make. :)
        # "remove" : 4, # lets the user remove points
        "clear" : 5, # clears the entire grid
        # "minorObstructions" : 6 - stuff like carpets and rugs
    }


    numToMode = {v: k for k, v in modeDict.items()} # Creates the reverse of the above dictionary to use in the mode swapper on the red button

    def __init__(self, x, y):
        self.pointX = x
        self.pointY = y
        self.input = InputManager()

    # Main screen function: Gets inputs and acts upon them
    def getInputs(self):
        # ALL BUTTONS HAVE A SET ALGORITHIM TO PREVENT MULTIPLE PRESSES
        # Pressed and state is 0 -> state is changed to 1 (Just Pressed)
        # Next frame -> state is changed to 2 (Held) This is what prevents multiple presses as 2 is not classified as a press
        # It will not set back to 1 until it has been fully reset (Unpressed) to 0 and then pressed again
        # When unpressed -> State is set to 0
        # Cycle repeats
        self.screenUpdate = False


        # GREEN BUTTON-Toggle/Set matrix pixels
        if self.input.getInput('green'):
            value = self.modeDict[self.mode]
            self.matrix[self.pointY][self.pointX] = value

            if value == 5:
                self.matrix = [
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0]
                ]

            self.screenUpdate = True
            sound.beep(400, 550, 100)
            print('the matrix is now:', self.matrix)

        # RED BUTTON-Mode changer
        if self.input.getInput('red'):
            self.num += 1
            if self.num >= max(self.numToMode.keys()): # loops back to the first mode if the number gets higher than the number of modes
                self.num = 0
            self.mode = self.numToMode[self.num]

            self.screenUpdate = True
            print('Red Pressed: the mode is now', self.mode)
            sound.beep(400, 550, 100)

        #LEFT BUTTON-Scrolls X-Axis
        if self.input.getInput('left'):
            self.pointX += 1
            self.screenUpdate = True
            print('Left Pressed: the X is now', self.pointX)
            sound.beep(400, 550, 100)

        ## RIGHT BUTTON-Scrolls Y-Axis
        if self.input.getInput('right'):
            self.pointY += 1
            self.screenUpdate = True
            print('Right Pressed: the Y is now', self.pointX)
            sound.beep(400, 550, 100)

        # Wraps values down to 0-4, preventing overflow and allowing scrolling
        self.pointX %= self.gridSideLengths
        self.pointY %= self.gridSideLengths

    def showSetLights(self):
        light_matrix.clear() # Clears matrix for drawing
        # Draws matrix to screen
        for x in range(self.gridSideLengths):
            for y in range(self.gridSideLengths):
                if self.matrix[y][x] == 1:
                    light_matrix.set_pixel(x, y, 100)

def consoleLogDiscussion():
    print('Hayden! I added some new comments at lines 61/2/3/4/8, and 102') # 18/11
    print('Hayden, I think that the input system I made should work, we\'ll need to test it out next lesson')
    # write any messages you want to say here and we will remove them prior to submitting.

### MAIN ENTRY
async def main():
    screen = Screen(2, 2) ## Starts the light matrix at the centre instead of 0, 0
    light_matrix.set_pixel(screen.pointX, screen.pointY, 100)
    while True:
        screen.getInputs()
        if screen.screenUpdate:
            light_matrix.clear()
            screen.showSetLights()
            light_matrix.set_pixel(screen.pointX, screen.pointY, 100)

runloop.run(main())
