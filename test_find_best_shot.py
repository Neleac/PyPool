import unittest
from find_best_shot import *

class TestFindBestShot(unittest.TestCase):
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

  def test_find_direct_shots(self):
    pockets = []
    p1 = Point(0, 0)
    p2 = Point(0, 1)
    p3 = Point(1, 0)
    p4 = Point(1, 1)
    pockets.append(p1)
    pockets.append(p2)
    pockets.append(p3)
    pockets.append(p4)

    stripes = []
    b1 = Point(0.1, 0.9)
    b2 = Point(0.9, 0.9)
    b3 = Point(0.9, 0.1)
    b4 = Point(0.5, 0.2)
    stripes.append(b1)
    stripes.append(b2)
    stripes.append(b3)
    stripes.append(b4)

    solids = []

    white = Point(0.5, 0.5)
    black = Point(0.7, 0.7)

    eps = 1e-5

    hits = find_direct_shots(white, black, stripes, solids, pockets, eps)
    self.assertNotEqual(hits, None)
    self.assertFalse(p1 in hits)
    self.assertEqual(hits[p2], b1)
    self.assertEqual(hits[p3], b3)
    self.assertFalse(p4 in hits)

    black = Point(0.95, 0.95)
    hits = find_direct_shots(white, black, stripes, solids, pockets, eps)
    self.assertNotEqual(hits, None)

    self.assertFalse(p1 in hits)
    self.assertEqual(hits[p2], b1)
    self.assertEqual(hits[p3], b3)
    self.assertFalse(p4 in hits)

    solids = []
    b5 = Point(0.6, 0.4)
    b6 = Point(0.05, 0.95)
    b7 = Point(0.4, 0.5)
    solids.append(b5)
    solids.append(b6)
    solids.append(b7)

    b8 = Point(0.1, 0.1)
    stripes.append(b8)

    black = Point(0.7, 1)  # out of the way

    hits = find_direct_shots(white, black, stripes, solids, pockets, eps)
    self.assertNotEqual(hits, None)

    self.assertEqual(hits[p1], b8)
    self.assertFalse(p2 in hits)  # obstructed by b6
    self.assertFalse(p3 in hits)  # obstructed by b5
    self.assertEqual(hits[p4], b2)  # no longer obstructed by black

  def test_find_closest_shot(self):
    pockets = []
    p1 = Point(0, 0)
    p2 = Point(0, 1)
    p3 = Point(1, 0)
    p4 = Point(1, 1)
    pockets.append(p1)
    pockets.append(p2)
    pockets.append(p3)
    pockets.append(p4)

    stripes = []
    b1 = Point(0.2, 0.2)
    b2 = Point(0.3, 0.7)
    b3 = Point(0.95, 0.95)
    b4 = Point(0.6, 0.4)
    stripes.append(b1)
    stripes.append(b2)
    stripes.append(b3)
    stripes.append(b4)

    solids = []

    white = Point(0.5, 0.5)
    black = Point(0.5, 0)  # out of the way

    eps = 1e-5

    closest_ball, closest_pocket, closest_dist = find_closest_shot(white, black, stripes, solids, pockets, eps)

    self.assertEqual(b3, closest_ball)
    self.assertEqual(p4, closest_pocket)
    self.assertLessEqual(abs(closest_dist - (0.05 * (2 ** 0.5))), eps)  # distance should be abt 0.05 * sqrt(2)

    stripes = []
    b5 = Point(0.5, 1)  # not pocketable
    stripes.append(b5)

    closest_ball, closest_pocket, closest_dist = find_closest_shot(white, black, stripes, solids, pockets, eps)
    self.assertEqual(closest_ball, None)
    self.assertEqual(closest_pocket, None)
    self.assertEqual(closest_dist, float('inf'))

if __name__ == '__main__':
    unittest.main()
