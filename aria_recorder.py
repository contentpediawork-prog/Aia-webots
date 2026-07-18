"""
ARIA recorder (Supervisor controller) - CO7316 Robotics Part 2

Starts an MP4 recording of the 3D view at simulation start and stops it
after RECORD_SECONDS of *simulation* time, then quits Webots so a
headless/Colab run terminates cleanly instead of hanging.

Docs for the recording API (check against your installed Webots version -
method names have changed slightly between releases, e.g. R2023b uses
Supervisor.movieStartRecording / movieStopRecording):
https://cyberbotics.com/doc/reference/supervisor
"""

from controller import Supervisor

TIME_STEP = 16
RECORD_SECONDS = 25          # how much sim time to capture
OUTPUT_FILE = "/content/aria_demo.mp4"   # change path if not on Colab
RESOLUTION = [1280, 720]
CODEC = 0                    # 0 = default codec in most Webots versions
QUALITY = 90                 # 1-100

supervisor = Supervisor()

started = False
steps_recorded = 0
max_steps = int((RECORD_SECONDS * 1000) / TIME_STEP)

while supervisor.step(TIME_STEP) != -1:
    if not started:
        supervisor.movieStartRecording(
            OUTPUT_FILE,
            RESOLUTION[0],
            RESOLUTION[1],
            CODEC,
            QUALITY,
            1,          # numberOfThreads
            False,      # caption
        )
        started = True
        print(f"Recording started -> {OUTPUT_FILE}")

    steps_recorded += 1
    if steps_recorded >= max_steps:
        supervisor.movieStopRecording()
        # give Webots a moment to flush the file before exiting
        for _ in range(5):
            supervisor.step(TIME_STEP)
        print("Recording stopped. Exiting simulation.")
        supervisor.simulationQuit(0)
        break
