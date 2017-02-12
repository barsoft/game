from OpenGL.GL import *
from OpenGL.GLE import *
from OpenGL.GLUT import *


class Model:
    modelType = None
    texture = None

    def __init__(self, modelType, texture):
        self.modelType = modelType
        self.texture = texture

    def draw(self):
        self.texture.bind()
        self.modelType.bind()

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, False, 0, None)
        glDrawElements(GL_TRIANGLES, len(self.modelType.indexList), GL_UNSIGNED_INT, None)
