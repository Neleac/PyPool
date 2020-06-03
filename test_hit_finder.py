import unittest
from board import *
from hit_finder import *

class TestHitFinder(unittest.TestCase):
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
    self.assertTrue(online(p0, p1, p2, eps))
  
  def test_not_online(self):
    p1 = Point(0, 0)
    p2 = Point(1, 1)
    eps = 1e-5

    p0 = Point(1, 1.1)
    self.assertFalse(online(p0, p1, p2, eps))

  def test_hits_direct(self):
    pockets = []
    p1 = Hole(Point(0, 0), 0)
    p2 = Hole(Point(0, 1), 0)
    p3 = Hole(Point(1, 0), 0)
    p4 = Hole(Point(1, 1), 0)
    pockets.append(p1)
    pockets.append(p2)
    pockets.append(p3)
    pockets.append(p4)

    balls = []
    b1 = Ball(Point(0.1, 0.9), 0, "stripes")
    b2 = Ball(Point(0.9, 0.9), 0, "stripes")
    b3 = Ball(Point(0.9, 0.1), 0, "stripes")
    b4 = Ball(Point(0.5, 0.2), 0, "stripes")
    b5 = Ball(Point(0.5, 0.5), 0, "white")
    b6 = Ball(Point(0.7, 0.7), 0, "black")
    balls.append(b1)
    balls.append(b2)
    balls.append(b3)
    balls.append(b4)
    # balls.append(b5)
    # balls.append(b6)

    eps = 1e-5

    hits = hits_direct(b5, b6, balls, pockets, eps)
    self.assertNotEqual(hits, None)

    self.assertNotEqual(hits[p1], None)
    self.assertEqual(len(hits[p1]), 0)

    self.assertNotEqual(hits[p2], None)
    self.assertTrue(b1 in hits[p2])
    self.assertEqual(len(hits[p2]), 1)

    self.assertNotEqual(hits[p3], None)
    self.assertTrue(b3 in hits[p3])
    self.assertEqual(len(hits[p3]), 1)

    self.assertNotEqual(hits[p4], None)
    self.assertTrue(b2 in hits[p4])
    self.assertEqual(len(hits[p4]), 1)

    b6 = Ball(Point(0.95, 0.95), 0, "black")
    hits = hits_direct(b5, b6, balls, pockets, eps)
    self.assertNotEqual(hits, None)

    self.assertNotEqual(hits[p2], None)
    self.assertTrue(b1 in hits[p2])
    self.assertEqual(len(hits[p2]), 1)

    self.assertNotEqual(hits[p3], None)
    self.assertTrue(b3 in hits[p3])
    self.assertEqual(len(hits[p3]), 1)

    self.assertNotEqual(hits[p4], None)
    self.assertEqual(len(hits[p4]), 0)

if __name__ == '__main__':
    unittest.main()
