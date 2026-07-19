"""
ARIA scripted demo controller (CO7316 Part 2)

This controller does NOT need keyboard input - it runs a fixed timed
sequence of movements so that headless/automated recording (GitHub
Actions, or any run where nobody is at the keyboard) still shows ARIA
doing something. Use aria_keyboard.py instead for live, hands-on
teleoperation and recording.

Sequence: drive forward -> turn -> raise torso -> move arm -> close
gripper -> open gripper -> stop.
"""

from controller import Robot

TIME_STEP = 16
robot = Robot()

left_wheel = robot.getDevice("left_wheel_motor")
right_wheel = robot.getDevice("right_wheel_motor")
left_wheel.setPosition(float("inf"))
right_wheel.setPosition(float("inf"))
left_wheel.setVelocity(0.0)
right_wheel.setVelocity(0.0)

torso = robot.getDevice("torso_lift_motor")
shoulder = robot.getDevice("shoulder_motor")
elbow = robot.getDevice("elbow_motor")
gripper_1 = robot.getDevice("gripper_motor_1")
gripper_2 = robot.getDevice("gripper_motor_2")
head_pan = robot.getDevice("head_pan_motor")

for m in (torso, shoulder, elbow, gripper_1, gripper_2, head_pan):
    m.setPosition(0.0)

camera = robot.getDevice("aria_camera")
camera.enable(TIME_STEP)
lidar = robot.getDevice("aria_lidar")
lidar.enable(TIME_STEP)

WHEEL_SPEED = 3.0

# (start_time_s, end_time_s, action_fn) - simple timed state machine
def drive_forward(on):
    left_wheel.setVelocity(WHEEL_SPEED if on else 0.0)
    right_wheel.setVelocity(WHEEL_SPEED if on else 0.0)

def turn(on):
    left_wheel.setVelocity(WHEEL_SPEED / 2 if on else 0.0)
    right_wheel.setVelocity(-WHEEL_SPEED / 2 if on else 0.0)

elapsed = 0.0
phase_done = set()

print("ARIA scripted demo controller running (no keyboard needed).")

while robot.step(TIME_STEP) != -1:
    elapsed += TIME_STEP / 1000.0

    if elapsed < 3.0:
        drive_forward(True)
    elif elapsed < 5.0:
        drive_forward(False)
        turn(True)
    elif elapsed < 5.5:
        turn(False)
    elif elapsed < 9.0:
        torso.setPosition(0.4)
    elif elapsed < 12.0:
        shoulder.setPosition(0.6)
        elbow.setPosition(-0.4)
    elif elapsed < 14.0:
        gripper_1.setPosition(0.03)
        gripper_2.setPosition(-0.03)
    elif elapsed < 16.0:
        gripper_1.setPosition(0.0)
        gripper_2.setPosition(0.0)
    elif elapsed < 19.0:
        head_pan.setPosition(0.8)
    elif elapsed < 22.0:
        head_pan.setPosition(-0.8)
        shoulder.setPosition(0.0)
        elbow.setPosition(0.0)
        torso.setPosition(0.0)
    else:
        drive_forward(False)
        turn(False)
