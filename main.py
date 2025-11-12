from pybricks import runloop, motor, force_sensor, motor_pair, port, light_matrix, button
import time, math, movement

def moveForward(distance, mode, speed):
    if mode == 'forward':
        motor.run_for_degrees(port.C, distance * -1, speed) ## Right wheel
        motor.run_for_degrees(port.D, distance, speed) ## Left wheel

def stopMove():
    motor.stop(port.C) ## stop right wheel
    motor.stop(port.D) ## stop left wheel

def square(): ## Doesn't work
    times = 4
    while times != 0:
        motor.run_for_degrees(port.C, 360, 1000)
        motor.run_for_degrees(port.D, 240, 750)
        times -= 1


async def main():
    while True:
        if force_sensor.force(port.B) >= 50: ## Manual hard press function on green button
            moveForward(1000, 'forward', 1000) ## runs the move function for 1000 degrees forward @ 1000 speed
        if force_sensor.force(port.A) >= 5: ## detects red button press
            stopMove() ## stops moving

    
runloop.run(main())