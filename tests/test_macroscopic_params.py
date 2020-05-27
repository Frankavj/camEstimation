from unittest import TestCase
from macroscopicParams import *


class TestMacroParams(TestCase):
    def setUp(self):
        self.vehicle_amount = 4
        self.duration = 4/25  # 4 frames
        self.headway_dict = {1: [100, 120, 80, 100],
                             2: [120, 110, 80, 90],
                             3: [50, 50, 50, 50],
                             4: [55, 50, 45, 50]}
        self.avg_speeds = [35, 33, 27, 25]

    def test_calculate_macro_params(self):
        flow, density, speed = calculate_macroscopic_params(self.vehicle_amount,
                                                            self.duration,
                                                            self.headway_dict,
                                                            self.avg_speeds)
        self.assertEqual(flow, 25)
        self.assertEqual(density, round(1 / 75, 4))
        self.assertEqual(speed, 30)


