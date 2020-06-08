import numpy as np

from functools import reduce

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    return "Point(x=" + str(self.x) + ", y=" + str(self.y) + ")"

def np_coord_to_point(coord):
  return Point(coord[0], coord[1])

def np_coords_to_points(coords):
  return [np_coord_to_point(c) for c in coords]

def point_to_np_coord(point):
  return np.array([point.x, point.y])

# params:
#   see find_direct_shots
# returns:
#   the coords of a stripes ball and a pocket, and the distance between them.
#   a direct shot is possible from cue -> ball -> pocket without hitting
#   other balls, and this is the minimal distance shot across all possible such shots
def find_closest_shot(white, black, stripes, solids, pockets, eps):
  shots = find_direct_shots(white, black, stripes, solids, pockets, eps)
  if not shots:  # no shots
    return (None, None, float('inf'))
  minDist = float('inf')
  argMin = None
  for pocket, ball in shots.items():
    if argMin is None or dist(pocket, ball) < minDist:
      minDist = dist(pocket, ball)
      argMin = pocket
  return (shots[argMin], argMin, minDist)  # stripes ball, pocket, distance between them (minimal over all shots)

# params:
#   white - x, y coordinate of white / cue ball
#   black - x, y coordinate of black ball
#   stripes - list of coords of striped balls
#   solids - list of coords of solid balls
#   pockets - list of coords of pockets
#   eps - error margin for marking a ball as lying on a line (on the line if shortest dist between ball and line is within eps)
# returns:
#   map from pocket to stripes that can be directly pocketed there
#   to get the same but for solids, pass in stripes for solids and solids for stripes
def find_direct_shots(white, black, stripes, solids, pockets, eps):
  # print("white", str(white), "black", str(black), "stripes", [str(e) for e in stripes], "solids", [str(e) for e in solids], "pockets", [str(e) for e in pockets], "eps", eps)
  shots = {}
  for pocket in pockets:
    for ball1 in stripes:
      # skip if ball1 isn't on the line through white and pocket
      if not online(ball1, white, pocket, eps):
        continue
      # skip if ball1 isn't between white and pocket
      if dist(white, pocket) < dist(ball1, pocket):
        continue
      # skip if the black is between ball1 and pocket
      if black and online(black, white, pocket, eps) and dist(black, pocket) < dist(white, pocket):  # black ball is anywhere between white and pocket
        continue
      # skip if any other balls are between ball1 and pocket or between white and ball1
      if reduce((lambda x, y: x or y), \
        [((ball2 is not ball1) \
          and online(ball2, white, pocket, eps) \
          and ((dist(ball2, pocket) < dist(ball1, pocket)) or (dist(ball2, pocket) < dist(white, pocket)))) \
          for ball2 in (solids + stripes)]):
        continue
      # found candidate; next pocket
      shots[pocket] = ball1
      break
  return shots

# returns true if the shortest distance between point p0 and the line through p1 and p2 is within eps
def online(p0, p1, p2, eps):
  dist = pdist(p0, p1, p2)
  if (dist <= eps):
    return True
  # print('dist ' + str(dist) + ' exceeds ' + str(eps))
  return False

# finds the distance between point p0 and the line though p1 and p2
# https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_two_points
def pdist(p0, p1, p2):
  # print("pdist", p0, p1, p2)
  return abs(((p2.y-p1.y)*p0.x) - ((p2.x-p1.x)*p0.y) + (p2.x*p1.y) - (p1.x*p2.y)) / (((p2.y-p1.y)**2 + (p2.x-p1.x)**2)**0.5)

# returns the euclidean distance betwen points p0 and p1
def dist(p0, p1):
  return ((p1.y-p0.y)**2 + (p1.x-p0.x)**2)**0.5
