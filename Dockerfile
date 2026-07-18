# Required by webots.cloud to know which Webots version to run your
# simulation with. Keep this in sync with the #VRML_SIM version line
# at the top of worlds/aria_world.wbt.
FROM cyberbotics/webots.cloud:R2023b-ubuntu22.04
ARG PROJECT_PATH
RUN mkdir -p $PROJECT_PATH
COPY . $PROJECT_PATH
