# PyPool - Pool Aim Bot

![Cover Photo](https://github.com/21WANGC/pool_aimbot/blob/master/pool.png)

The game of pool, also known as billiards or snooker, is commonly played around the world. The
game consists of a rectangular table with 6 pockets, and 15 balls (plus cue ball) that players would
like to send ("pot") to the pockets by hitting shots using their cue sticks. In 8-ball pool, there are 4
ball types: solids (solid-colored, numbered 1-7), stripes (partially solid-colored and partially white,
numbered 9-15), the 8-ball (solid black, numbered 8), and the cue ball (solid white). There are 2
players, each with a style of ball that they would like to pot by hitting the cue-ball, while only potting
the 8-ball on the last shot.

We present an application to find all possible shots in a game state that would pot balls of the desired
style (solids or stripes). This system takes as input an RGB image of the pool table from the player’s
perspective and outputs that image with a visual overlay that indicates at which angle to hit which ball
into which pocket. We imagine this being used as an Augmented Reality (AR) system, which informs
the player of the best shots available. We implement this project using Python, mainly utilizing the
OpenCV and PyTorch frameworks.

See [PyPool.pdf](https://github.com/21WANGC/pool_aimbot/blob/master/PyPool.pdf) for more details.
