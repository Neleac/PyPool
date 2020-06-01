import unittest
from angle_finder import *

class TestAngleFinder(unittest.TestCase):
  def test_online_1d(self):
    p1 = Point(0, 0)
    p2 = Point(1, 0)
    eps = 1e-5

    # test endpoints
    p0 = Point(0, 0)
    self.assertTrue(online(p0, p1, p2, eps))
    p0 = Point(1, 0)
    self.assertTrue(online(p0, p1, p2, eps))

    # test in between
    p0 = Point(0.5, 0)
    self.assertTrue(online(p0, p1, p2, eps))
  
  def test_online_2d(self):
    p1 = Point(0, 0)
    p2 = Point(1, 1)
    eps = 1e-5

    # test endpoints
    p0 = Point(0, 0)
    self.assertTrue(online(p0, p1, p2, eps))
    p0 = Point(1, 1)
    self.assertTrue(online(p0, p1, p2, eps))

    # test in between
    p0 = Point(0.5, 0.5)
    self.assertTrue(online(p0, p1, p2, eps))

    # test outside point bounds
    p0 = Point(2, 2)
    self.assertTrue(online(p0, p1, p1, eps))
  
  def test_not_online(self):
    p1 = Point(0, 0)
    p2 = Point(1, 1)
    eps = 1e-5

    p0 = Point(1, 1.1)
    self.assertFalse(online(p0, p1, p2, eps))

  def test_hits_direct(self):
    #todo

if __name__ == '__main__':
    unittest.main()
