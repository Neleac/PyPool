
# returns a mapping of pockets to balls that can be pocketed there with a direct shot
# if black is specified, will exclude balls that would pocket the black ball when hit in the shot path
# (assumes full conservation of momentum between balls, arbitrary ball velocity)
def hits_direct(white, black, balls, pockets, eps):
  ret = {}
  for pocket in pockets:
    ret[pocket] = []
    for ball in balls:
      if online(white.loc, ball.loc, pocket.loc, eps) and (dist(ball.loc, pocket.loc) < dist(white.loc, pocket.loc)):
        if (not online(black.loc, ball.loc, pocket.loc, eps)) or (dist(ball.loc, pocket.loc) < dist(black.loc, pocket.loc)):
          ret[pocket].append(ball)
  return ret

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
