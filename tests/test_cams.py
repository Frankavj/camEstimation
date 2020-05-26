from unittest import *
from estimateCAMs import *


class TestCams(TestCase):
    def setUp(self):
        self.fps = 25
        self.frame_amount = 25

        # Static position list
        self.positionList = []
        for i in range(25):
            self.positionList.append((0, 0))

        # Static velocity list
        self.velocityList = []
        for i in range(25):
            self.velocityList.append((0, 0))

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
        self.assertEqual(cam_conditions_are_met(old, new, self.positionList, self.velocityList), False)

        # Position change of 3m or 4m
        self.positionList[new] = (3, 0)
        self.assertEqual(cam_conditions_are_met(old, new, self.positionList, self.velocityList), False)

        self.positionList[new] = (4, 0)
        self.assertEqual(cam_conditions_are_met(old, new, self.positionList, self.velocityList), True)
        self.positionList[new] = (0, 0)

        # Velocity change of 0.4m/s or 0.5m/s
        self.velocityList[new] = (0.4, 0)
        self.assertEqual(cam_conditions_are_met(old, new, self.positionList, self.velocityList), False)

        self.velocityList[new] = (0.5, 0)
        self.assertEqual(cam_conditions_are_met(old, new, self.positionList, self.velocityList), True)
        self.velocityList[new] = (0, 0)

        # TODO: direction change of 3° or 4°

        # Several parameters changed
        self.positionList[new] = (1, 1)
        self.velocityList[new] = (1.2, 0)
        self.assertEqual(cam_conditions_are_met(old, new, self.positionList, self.velocityList), True)

    def test_vehicle_cams(self):
        self.assertEqual(vehicle_cams(self.fps, self.frame_amount, self.positionList, self.velocityList), 1)

        # Add one frame to get to the maximum wait of 1000ms
        self.positionList.append((0, 0))
        self.velocityList.append((0, 0))
        self.frame_amount = 26
        self.assertEqual(vehicle_cams(self.fps, self.frame_amount, self.positionList, self.velocityList), 2)

        # Use data with just 3 frames. Only one CAM should be generated regardless of the positional,
        # directional and velocity changes
        position_short = [(0, 0), (2, 0), (4, 1)]
        velocity_short = [(0, 0), (1, 0), (2, 0.7)]
        self.assertEqual(vehicle_cams(self.fps, 3, position_short, velocity_short), 1)

        # The maximum number of CAMs should be (the frame amount / 3) + 1
        pos = 0
        v = 0
        for i in range(self.frame_amount):
            self.positionList[i] = (pos, pos)
            self.velocityList[i] = (v, v)

            pos += 4
            v += 0.5

        self.assertEqual(vehicle_cams(self.fps, self.frame_amount, self.positionList, self.velocityList),
                         math.floor((self.frame_amount / 3) + 1))



