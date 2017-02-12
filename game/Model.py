import numpy as np
from OpenGL.GL import *
from OpenGL.GLE import *
from OpenGL.GLUT import *

import game.Camera


class Model:
    def __init__(self, modelType, texture, shader):
        self.modelType = modelType
        self.texture = texture
        self.shader = shader

    def draw(self, angle):
        glUseProgram(self.shader)
        self.texture.bind()
        modelMatrix = game.Camera.rotate(angle, np.array([0, 1, 0]))
        # modelMatrix = modelMatrix * translate([-0.2, 0, 0])

        loc = glGetUniformLocation(self.shader, "Projection")
        glUniformMatrix4fv(loc, 1, False, np.asfortranarray(game.Camera.projectionMatrix.transpose()))

        loc = glGetUniformLocation(self.shader, "View")
        glUniformMatrix4fv(loc, 1, False, np.asfortranarray(game.Camera.viewMatrix.transpose()))

        loc = glGetUniformLocation(self.shader, "Model")
        glUniformMatrix4fv(loc, 1, False, np.asfortranarray(modelMatrix.transpose()))

        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)

        self.modelType.indexPositions.bind()

        self.modelType.vertexPositions.bind()
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)

        self.modelType.uvPositions.bind()
        glVertexAttribPointer(1, 2, GL_FLOAT, False, 0, None)

        glDrawElements(GL_TRIANGLES, len(self.modelType.indexList), GL_UNSIGNED_INT, None)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)

        self.modelType.indexPositions.unbind()
        self.modelType.vertexPositions.unbind()
        self.modelType.uvPositions.unbind()
        glUseProgram(0)
