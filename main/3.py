from djitellopy import Tello
tello = Tello()
move_commands = {
    "forward": tello.move_forward,
    "back": tello.move_back,
    "left": tello.move_left,
    "right": tello.move_right,
    "up": tello.move_up,
    "down": tello.move_down,
    "clockwise":  tello.rotate_clockwise,
    "counter_clockwise": tello.rotate_counter_clockwise
}

tello.connect()
tello.takeoff()
direction = ""
i = 1
if(i%2 == 0):
    direction = "forward"
else:
    direction = "back"

move_commands[direction](30)

tello.land()