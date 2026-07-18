#!/bin/bash
# Run these as Colab cells (prefix each line with ! if pasting into a notebook cell,
# or paste this whole file into one cell with %%bash).
#
# WARNING: this is not an officially supported Webots workflow. Colab has no
# GPU-accelerated OpenGL by default, so Webots falls back to slow software
# rendering (Mesa llvmpipe) via Xvfb. Expect this to be fragile: version
# mismatches, missing libraries, and rendering glitches are all likely.
# If you have any access to a real Ubuntu machine or Ubuntu-in-WSL, running
# Webots natively there will be far more reliable than this path.

set -e

# 1. System dependencies + a virtual display
apt-get update -qq
apt-get install -y -qq xvfb wget

# 2. Download Webots (CHECK you have the right version/link before running -
#    release assets change; browse https://github.com/cyberbotics/webots/releases
#    and swap the URL below for the current .deb)
WEBOTS_VERSION="R2023b"
wget -q "https://github.com/cyberbotics/webots/releases/download/${WEBOTS_VERSION}/webots_2023b_amd64.deb" -O webots.deb
apt-get install -y -qq ./webots.deb

# 3. Force software OpenGL rendering (no GPU on standard Colab runtimes)
export LIBGL_ALWAYS_SOFTWARE=1
export WEBOTS_HOME=/usr/local/webots

# 4. Run Webots headlessly under a virtual framebuffer, in fast mode, with
#    the recorder Supervisor controller doing the actual video capture.
#    --batch stops blocking popups; --minimize + --mode=fast keep it moving
#    without a visible window; --stdout/--stderr surface controller print()s.
xvfb-run --auto-servernum --server-args="-screen 0 1280x720x24" \
  "$WEBOTS_HOME/webots" --batch --minimize --mode=fast --stdout --stderr \
  /content/webots_project/worlds/aria_world.wbt

echo "If it worked, the video should now be at /content/aria_demo.mp4"
