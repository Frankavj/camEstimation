import math


# Returns the number of CAMs for this vehicle
def vehicle_cams(fps, vehicle, frame_amount, positionList, velocityList):
    # We must keep track of which index of data we must compare to
    # The framerate of the data determines which index we must look at for
    # the next possible CAM
    prev_cam = 0
    minimum_wait = math.ceil(100/(1000/fps))
    maximum_wait = math.ceil(1000/(1000/fps))
    cams = 1

    i = prev_cam + minimum_wait

    while i < frame_amount:
        if cam_conditions_are_met(prev_cam, i, positionList, velocityList) or (i >= prev_cam + maximum_wait):
            # The CAM conditions are met or the maximum_wait has been reached
            cams += 1
            prev_cam = i
            i = prev_cam + minimum_wait
        else:
            # The CAM conditions are not met, and the maximum_wait has not been reached
            i += 1

    # print("Vehicle " + str(vehicle) + " has " + str(frame_amount) + " frames and " + str(cams) + " cams.")
    return cams


def cam_conditions_are_met(old, new, positions, velocities):
    return change(positions[old], positions[new]) >= 4 \
           or change(velocities[old], velocities[new]) >= 0.5 \
           # or change(directions[old], directions[new]) >= 4


def change(old, new):
    dx = abs(old[0] - new[0])
    dy = abs(old[1] - new[1])
    return math.sqrt(pow(dx, 2) + pow(dy, 2))
