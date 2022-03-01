import unittest

from pyEpiabm.utility import DistanceFunctions


class TestDistanceFunctions(unittest.TestCase):
    """Test the 'DistanceFunctions' class.
    """

    def test_dist_euclid(self):
        dist = DistanceFunctions.dist_euclid((3, 0))
        self.assertTrue(dist == 3)

        dist = DistanceFunctions.dist_euclid((-3, 0))
        self.assertTrue(dist == 3)

        dist = DistanceFunctions.dist_euclid((-3, 0), (3, 0))
        self.assertTrue(dist == 6)


if __name__ == '__main__':
    unittest.main()