import numpy as np


class Material:
    def __init__(self):
        self.diffuseColor = np.array([0.8, 0.8, 0.8])
        self.ambientColor = np.array([0.3, 0.3, 0.3])
        self.specularColor = np.array([0, 0, 0])
