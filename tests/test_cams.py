from unittest import *
from estimateCAMs import *


class TestCams(TestCase):
    def setUp(self):
        self.fps = 25
        self.frame_amount = 25

        # Static position, velocity and direction list
        self.positionList = []
        self.velocityList = []
        self.directionList = []
        for i in range(25):
            self.positionList.append((0, 0))
            self.velocityList.append((0, 0))
            self.directionList.append(None)

    def test_change(self):
        # No change:
        old = (0, 0)
        new = (0, 0)
        self.assertEqual(change(old, new), 0)

        # Change along x-axis
        new = (4, 0)
        self.assertEqual(change(old, new), 4)

        # Change along y-axis
        new = (0, -4)
        self.assertEqual(change(old, new), 4)

        # Change along x-axis and y-axis
        new = (-1, 1)
        self.assertEqual(change(old, new), math.sqrt(2))

    def test_cam_conditions_are_met(self):
        old, new = 0, 3

        # Static vehicle
        self.assertEqual(cam_conditions_are_met(old, new, self.positionList, self.velocityList, self.directionList), False)

        # Position change of 3m or 4m
        self.positionList[new] = (3, 0)
        self.assertEqual(cam_conditions_are_met(old, new, self.positionList, self.velocityList, self.directionList), False)

        self.positionList[new] = (4, 0)
        self.assertEqual(cam_conditions_are_met(old, new, self.positionList, self.velocityList, self.directionList), True)
        self.positionList[new] = (0, 0)

        # Velocity change of 0.4m/s or 0.5m/s
        self.velocityList[new] = (0.4, 0)
        self.assertEqual(cam_conditions_are_met(old, new, self.positionList, self.velocityList, self.directionList), False)

        self.velocityList[new] = (0.5, 0)
        self.assertEqual(cam_conditions_are_met(old, new, self.positionList, self.velocityList, self.directionList), True)
        self.velocityList[new] = (0, 0)

        # Direction change of 3° or 4°
        self.directionList[old + 1] = 0
        self.directionList[new] = 3
        self.assertEqual(cam_conditions_are_met(old, new, self.positionList, self.velocityList, self.directionList), False)

        self.directionList[new] = 4
        self.assertEqual(cam_conditions_are_met(old, new, self.positionList, self.velocityList, self.directionList), False)
        self.assertEqual(cam_conditions_are_met(old+1, new+1, self.positionList, self.velocityList, self.directionList), True)

        # Several parameters changed
        self.positionList[new] = (1, 1)
        self.velocityList[new] = (1.2, 0)
        self.assertEqual(cam_conditions_are_met(old, new, self.positionList, self.velocityList, self.directionList), True)

    def test_vehicle_cams(self):
        self.assertEqual(vehicle_cams(self.fps, self.frame_amount, self.positionList, self.velocityList, self.directionList), 1)

        # Add one frame to get to the maximum wait of 1000ms
        self.positionList.append((0, 0))
        self.velocityList.append((0, 0))
        self.directionList.append(0)
        self.frame_amount = 26
        self.assertEqual(vehicle_cams(self.fps, self.frame_amount, self.positionList, self.velocityList, self.directionList), 2)

        # Use data with just 3 frames. Only one CAM should be generated regardless of the positional,
        # directional and velocity changes
        position_short = [(0, 0), (2, 0), (4, 1)]
        velocity_short = [(0, 0), (1, 0), (2, 0.7)]
        direction_short = [0, 4, 6]
        self.assertEqual(vehicle_cams(self.fps, 3, position_short, velocity_short, direction_short), 1)

        # The maximum number of CAMs should be (the frame amount / 3) + 1
        pos = 0
        v = 0
        d = 0
        for i in range(self.frame_amount):
            self.positionList[i] = (pos, pos)
            self.velocityList[i] = (v, v)
            self.directionList[i] = d

            pos += 4
            v += 0.5
            d += 4

        self.assertEqual(vehicle_cams(self.fps, self.frame_amount, self.positionList, self.velocityList, self.directionList),
                         math.floor((self.frame_amount / 3) + 1))



