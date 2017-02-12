import numpy as np

from game.Math import *

projectionMatrix = None

eye = np.array([0, 0, -15])
target = np.array([0, 0, 0])
up = np.array([0, 1, 0])

viewMatrix = lookat(eye, target, up)