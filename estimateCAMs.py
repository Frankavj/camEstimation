import math


# Returns the number of CAMs for this vehicle
def vehicle_cams(fps, frame_amount, positionList, velocityList, directionList):
    # We must keep track of which index of data we must compare to
    # The framerate of the data determines which index we must look at for
    # the next possible CAM
    prev_cam = 0
    minimum_wait = math.ceil(100/(1000/fps))
    maximum_wait = math.ceil(1000/(1000/fps))
    cams = 1

    i = prev_cam + minimum_wait

    while i < frame_amount:
        if cam_conditions_are_met(prev_cam, i, positionList, velocityList, directionList) or (i >= prev_cam + maximum_wait):
            # The CAM conditions are met or the maximum_wait has been reached
            cams += 1
            prev_cam = i
            i = prev_cam + minimum_wait
        else:
            # The CAM conditions are not met, and the maximum_wait has not been reached
            i += 1

    return cams


def cam_conditions_are_met(old, new, positions, velocities, directions):
    return change(positions[old], positions[new]) >= 4 \
           or change(velocities[old], velocities[new]) >= 0.5 \
           or directional_change(old, new, directions, positions) >= 4


def change(old, new):
    dx = abs(old[0] - new[0])
    dy = abs(old[1] - new[1])
    return math.sqrt(pow(dx, 2) + pow(dy, 2))


def directional_change(old, new, directions, positions):
    direction_old = directions[old]
    direction_new = directions[new]

    if direction_old is None and direction_new is None:
        # There is no change since the vehicle is not moving in both cases
        return 0
    elif direction_new is None:
        # Take the last direction before the vehicle stopped moving
        i = new - 1
        while i > old:
            if directions[i] is None:
                i -= 1
            else:
                direction_new = directions[i]
                break
        if i == old:
            return 0
    elif direction_old is None:
        # Take the last direction before the vehicle stopped moving
        i = old - 1
        while i >= 0:
            if directions[i] is None:
                i -= 1
            else:
                direction_old = directions[i]
                break
        if i == -1:
            # The vehicle has been static from the first frame until now:
            return 0

    return abs(direction_old - direction_new)


