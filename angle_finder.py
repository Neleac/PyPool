
class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

class Ball:
  def __init__(self, loc, rad, balltype):
    self.loc = loc
    self.rad = rad
    self.balltype = balltype

class Hole:
  def __init__(self, loc, rad):
    self.loc = loc
    self.rad = rad

class Board:
  def __init__(self, w, h, holes, balls, pockets):
    self.w = w
    self.h = h
    self.balls = balls
    self.pockets = pockets

# returns a mapping of pockets to balls that can be pocketed there with a direct shot
# if black is specified, will exclude balls that include the black ball in the shot path
def hits_direct(white, black=None, balls, pockets, eps):
  ret = {}
  for pocket in pockets:
    ret[pocket] = []
    for ball in balls:
      if online(white, ball, pocket, eps):
        if (not black) or (black and not online(black, ball, pocket, eps))
          ret[pocket].append(ball)

# returns true if the shortest distance between point p0 and the line through p1 and p2 is within eps
def online(p0, p1, p2, eps):
  dist = pdist(p0, p1, p2)
  if (dist <= eps):
    return True
  print('dist ' + str(dist) + ' exceeds ' + str(eps))
  return False

# finds the distance between point p0 and the line though p1 and p2
# https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points
def pdist(p0, p1, p2):
  return abs(((p2.y-p1.y)*p0.x) - ((p2.x-p1.x)*p0.y) + (p2.x*p1.y) - (p1.x*p2.y)) / (((p2.y-p1.y)**2 + (p2.x-p1.x)**2)**0.5)
