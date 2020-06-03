
class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    return "Point(x=" + str(self.x) + ", y=" + str(self.y) + ")"

class Ball:
  def __init__(self, loc, rad, balltype):
    self.loc = loc
    self.rad = rad
    self.balltype = balltype
  
  def __str__(self):
    return "Ball(loc=" + str(self.loc) + ", rad=" + str(self.rad) + ", balltype=" + str(self.balltype) + ")"

class Hole:
  def __init__(self, loc, rad):
    self.loc = loc
    self.rad = rad
  
  def __str__(self):
    return "Hole(loc=" + str(self.loc) + ", rad=" + str(self.rad) + ")"

class Board:
  def __init__(self, w, h, holes, balls, pockets):
    self.w = w
    self.h = h
    self.balls = balls
    self.pockets = pockets
  
  def __str__(self):
    return "Board(w=" + str(self.w) + ", h=" + str(self.h) + ", balls=" + str(self.balls) + ", pockets=" + str(self.pockets) + ")"
