"""
ARIA keyboard controller (CO7316 Robotics - Part 2)

Controls:
  W / S       - drive forward / backward
  A / D       - rotate left / right
  R / F       - raise / lower telescoping torso
  T / G       - shoulder joint up / down
  Y / H       - elbow joint up / down
  O           - open gripper
  C           - close gripper
  Q           - pan head left, E - pan head right

Run this by setting it as the ARIA robot's controller in Webots
(already wired up in aria_world.wbt).
"""

from controller import Robot, Keyboard

TIME_STEP = 16
WHEEL_SPEED = 4.0

robot = Robot()

# --- motors ---
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

# position-controlled joints: track a target and nudge it each step
torso_target = 0.0
shoulder_target = 0.0
elbow_target = 0.0
gripper_target = 0.0
head_target = 0.0

torso.setPosition(torso_target)
shoulder.setPosition(shoulder_target)
elbow.setPosition(elbow_target)
gripper_1.setPosition(gripper_target)
gripper_2.setPosition(-gripper_target)
head_pan.setPosition(head_target)

# --- sensors (not strictly needed for teleop, but on for the recording demo) ---
camera = robot.getDevice("aria_camera")
camera.enable(TIME_STEP)
lidar = robot.getDevice("aria_lidar")
lidar.enable(TIME_STEP)

keyboard = Keyboard()
keyboard.enable(TIME_STEP)

print("ARIA keyboard controller running.")
print("W/S drive, A/D turn, R/F torso, T/G shoulder, Y/H elbow, O/C gripper, Q/E head pan")

STEP = 0.01  # per-timestep increment for joint targets

while robot.step(TIME_STEP) != -1:
    left_speed = 0.0
    right_speed = 0.0

    key = keyboard.getKey()
    while key != -1:
        if key == ord("W"):
            left_speed, right_speed = WHEEL_SPEED, WHEEL_SPEED
        elif key == ord("S"):
            left_speed, right_speed = -WHEEL_SPEED, -WHEEL_SPEED
        elif key == ord("A"):
            left_speed, right_speed = -WHEEL_SPEED / 2, WHEEL_SPEED / 2
        elif key == ord("D"):
            left_speed, right_speed = WHEEL_SPEED / 2, -WHEEL_SPEED / 2
        elif key == ord("R"):
            torso_target = min(0.6, torso_target + STEP)
            torso.setPosition(torso_target)
        elif key == ord("F"):
            torso_target = max(0.0, torso_target - STEP)
            torso.setPosition(torso_target)
        elif key == ord("T"):
            shoulder_target = min(1.5, shoulder_target + STEP)
            shoulder.setPosition(shoulder_target)
        elif key == ord("G"):
            shoulder_target = max(-1.5, shoulder_target - STEP)
            shoulder.setPosition(shoulder_target)
        elif key == ord("Y"):
            elbow_target = min(1.5, elbow_target + STEP)
            elbow.setPosition(elbow_target)
        elif key == ord("H"):
            elbow_target = max(-1.5, elbow_target - STEP)
            elbow.setPosition(elbow_target)
        elif key == ord("O"):
            gripper_target = max(0.0, gripper_target - STEP)
            gripper_1.setPosition(gripper_target)
            gripper_2.setPosition(-gripper_target)
        elif key == ord("C"):
            gripper_target = min(0.03, gripper_target + STEP)
            gripper_1.setPosition(gripper_target)
            gripper_2.setPosition(-gripper_target)
        elif key == ord("Q"):
            head_target = min(1.5, head_target + STEP)
            head_pan.setPosition(head_target)
        elif key == ord("E"):
            head_target = max(-1.5, head_target - STEP)
            head_pan.setPosition(head_target)
        key = keyboard.getKey()

    left_wheel.setVelocity(left_speed)
    right_wheel.setVelocity(right_speed)
