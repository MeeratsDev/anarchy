# M.E.D.S - Modular Electronic Delivery System

## Our team: 

|NAME   |ROLE   |
|---|---|
|Bodhi   |Programmer   |
|Hayden   |Programmer   |
|Nel   |Builder   |


## Purpose
This repository contains the code for a prototype delivery system that could be used for anything from maze solving to large scale delivery. M.E.D.S. is built with Lego® Spike Prime and utilises the Spike Prime Python coding API to run. This project is open source so feel free to use it to produce your own pathfinding Spike Prime robot (just make sure to credit us if you use any of our code).

## Why we made this
M.E.D.S is built for our grade 8 digital technologies assessment and is not meant to be actually produced or used in a wide spread deployment.

## How to use M.E.D.S as is
To use M.E.D.S you need to have the Spike Prime driving base built and functional with the wheels plugged into ports C & D on the prime hub, you will also need 2 force sensors plugged into ports A & B. These ports must be followed exactly otherwise the code will not run correctly, this can however be changed by altering the assigned port letters in the code. 

Once powered on a connected to the device you plan to run the code on you will see a yellow square on the hub's light matrix, this square can be moved by pressing the 2 button directly on the hub, the left button will cycle the X (horizontal) axis and the right will cycle the Y (verticle) axis, you can use the green button to create a set obsticle that the robot will avoid and the red button will cycle modes (obsticle placement, start point, end point, and clear), once the start and end points are set the robot will prompt for confirmation and after it gets permission it will calculate the most efficient path to the end point and begin its path.

Depending on the module attached it will have a different objective at the end point, once its objective is completed it will return to the start point and wait for further instructions.

|Button   |Function   |
|---|---|
|Red   |Cycle modes   |
|Green   |Apply mode to selected square   |
|Left   |Cycle horizontal axis   |
|Right   |Cycle verticle axis   |

## Future plans
- more indepth obsticle management
- more modules that can be attached

## How to modify M.E.D.S
M.E.D.S is written in Python with the Lego Spike Prime Python Coding API, the documentation for said API can be found on the left side of the screen while the project is open. There are 3 main python modules we built for this project, the input module; the Screen module; and the pathfinding module, these modules work together to operate M.E.D.S and anyone of them can be modified although we sugest to not modify the pathfinding algorithm as it could cause M.E.D.S to become inoperable. You can add more assignment modes by finding the "modeDict" and adding modes to the end as follows
```
modeDict = {
    "grid" : 1,
    "start" : 2,
    "end" : 3,
    "clear" : 5,
    ____________ <-- this is where you can add more
}
```

this change will then be adopted by the rest of the program and the mode can be used, to implement the functionality of the mode we recommend you create a new function with the mode's logic then simply call the function from the point in the Screen class where inputs for the green button are handeled (line 135).

To add more inputs to handle you can simply add them to the elif chain in the ```getInput()``` function as a part of the inputManager class (line 80) these can then be called by ```inputManager.getInput("keyname")```, the input manager can be defined in a seperate class as follows

```self.input = inputManager()``` (can be seen in line 121)

To add external Python libraries that aren't included in MicroPython or the Spike Prime API you will need to host them on a GitHub repository and import them like this

```import [url]``` or ```from [url] import [module]```

which can then be used as normal

## FAQ
**Q:** How do I use Spike Prime API?

**A:** We cannot help with that one since we haven't properly learnt it yet however the official documentation is a good place to start but we also suggest trying to learn Pybricks as it has a far more extensive catalogue of features and QoL improvements over the defualt Spike Prime API.

 
**Q:** Can I make my own M.E.D.S?

**A:** Go for it! Just make sure to credit us if you use our code.

 
**Q:** Where can I get the raw Python files?

**A:** Either by copying all the code from the .llsp3 file or just downloading it from this repository.
