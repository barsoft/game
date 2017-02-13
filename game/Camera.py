import numpy as np

from game.Math import *

projectionMatrix = None
viewMatrix = None

eye = np.array([0, 0, -15])
target = np.array([0, 0, 0])
up = np.array([0, 1, 0])


cameraRotX = 0
cameraRotY = 0