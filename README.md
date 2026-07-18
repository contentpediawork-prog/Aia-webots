# ARIA Webots project (CO7316 Part 2)

## What's in here
- `worlds/aria_world.wbt` — a simple home-task arena, a table with a small
  target object, and the ARIA robot (differential-drive base, telescoping
  torso, 2-DOF arm, 2-finger gripper, pan-tilt head with camera + lidar), plus
  a Supervisor node used only for recording.
- `controllers/aria_keyboard/aria_keyboard.py` — keyboard teleoperation of
  ARIA (matches the "keyboard-controlled in the simulation" line in the
  report).
- `controllers/aria_recorder/aria_recorder.py` — a Supervisor controller that
  starts/stops the built-in Webots movie recorder.
- `colab_setup.sh` — best-effort script to run all of this headlessly on
  Google Colab.

## Important: this hasn't been run in a live Webots instance
I don't have Webots (or a display) available in this sandbox, so none of this
has actually been executed or visually verified — only checked against the
Webots API/world-syntax documentation. Treat it as a first draft, not a
finished, working project. Expect to spend time in Webots' own error console
fixing things like:
- PROTO URLs that have moved or point to a different Webots version than
  what you have installed (swap `R2023b` in the EXTERNPROTO lines for your
  installed version if needed).
- Joint anchor/axis values that need nudging once you can see the robot
  (it's easy to get a torso or arm segment slightly misaligned).
- The differential-drive turning behaviour will need tuning — this is a
  simplified two-wheel-plus-caster base, not a true omnidirectional base
  (Webots doesn't have a built-in mecanum wheel primitive, so a fully
  faithful omnidirectional base is a bigger undertaking than a first pass).

## Recommended path: run it locally first
1. Install Webots normally (https://cyberbotics.com/#download) on your own
   machine or a lab PC.
2. Open `worlds/aria_world.wbt` directly in Webots — this alone gets you a
   real-time 3D view, which makes debugging far easier than doing it
   headlessly.
3. Fix whatever the console flags as errors (there will likely be some).
4. Play the simulation, drive ARIA with the keyboard controls listed at the
   top of `aria_keyboard.py`.
5. Record with Webots' own **File > Make Movie** menu option, or with OBS
   Studio capturing the window — both are simpler and more reliable than the
   headless/Colab route.

## If you specifically need the Colab route
`colab_setup.sh` is a best-effort attempt at:
Xvfb (virtual display) + software OpenGL rendering + Webots in fast/batch
mode + the Supervisor controller triggering `movieStartRecording`/
`movieStopRecording`.

Before running it:
- Upload this whole `webots_project` folder to `/content/webots_project` in
  your Colab session.
- Check the Webots release URL in the script against the current releases
  page — release filenames change between versions.
- Run it a cell at a time rather than all at once, so you can see where it
  breaks.

Realistic expectations: Colab sessions aren't designed for GUI/3D apps, so
this may simply not work, or may be very slow (software-rendered physics +
graphics). If it fails, running Webots locally (or in a university lab) and
recording normally is the reliable fallback — and is also what the module
brief's own suggestions (Webots' built-in recorder, or OBS Studio) assume
you'll do.
