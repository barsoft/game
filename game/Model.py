import numpy as np
from OpenGL.GL import *
from OpenGL.GLE import *
from OpenGL.GLUT import *
import game.Camera
import game.Math
import game.Light
from game.Material import *


class Model:
    def __init__(self, modelType, texture, shader):
        self.modelType = modelType
        self.texture = texture
        self.shader = shader
        self.x = 0
        self.y = 0
        self.z = 0
        self.modelMatrix = game.Math.translate([self.x, self.y, self.z])
        self.material = Material()

    def draw(self):
        glUseProgram(self.shader)

        self.texture.bind()
        self.modelMatrix = game.Math.translate([self.x, self.y, self.z])

        loc = glGetUniformLocation(self.shader, "Projection")
        glUniformMatrix4fv(loc, 1, False, np.asfortranarray(game.Camera.projectionMatrix.transpose()))

        loc = glGetUniformLocation(self.shader, "View")
        glUniformMatrix4fv(loc, 1, False, np.asfortranarray(game.Camera.viewMatrix.transpose()))

        loc = glGetUniformLocation(self.shader, "Model")
        glUniformMatrix4fv(loc, 1, False, np.asfortranarray(self.modelMatrix.transpose()))

        loc = glGetUniformLocation(self.shader, "myTextureSampler")
        glUniform1i(loc, 0)

        loc = glGetUniformLocation(self.shader, 'LightPosition_worldspace')
        glUniform3f(loc, game.Light.lightPos[0], game.Light.lightPos[1], game.Light.lightPos[2])

        loc = glGetUniformLocation(self.shader, 'LightColor')
        glUniform3f(loc, game.Light.lightColor[0], game.Light.lightColor[1], game.Light.lightColor[2])

        loc = glGetUniformLocation(self.shader, 'LightPower')
        glUniform1i(loc, game.Light.lightPower)

        loc = glGetUniformLocation(self.shader, 'MaterialDiffuseColor')
        glUniform3f(loc, self.material.diffuseColor[0], self.material.diffuseColor[1], self.material.diffuseColor[2])

        loc = glGetUniformLocation(self.shader, 'MaterialAmbientColor')
        glUniform3f(loc, self.material.ambientColor[0], self.material.ambientColor[1], self.material.ambientColor[2])

        loc = glGetUniformLocation(self.shader, 'MaterialSpecularColor')
        glUniform3f(loc, self.material.specularColor[0], self.material.specularColor[1], self.material.specularColor[2])

        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)

        self.modelType.indexPositions.bind()

        self.modelType.vertexPositions.bind()
        glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)

        self.modelType.uvPositions.bind()
        glVertexAttribPointer(1, 2, GL_FLOAT, False, 0, None)

        self.modelType.normalPositions.bind()
        glVertexAttribPointer(2, 3, GL_FLOAT, False, 0, None)

        glDrawElements(GL_TRIANGLES, len(self.modelType.indexList), GL_UNSIGNED_INT, None)

        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)

        glUseProgram(0)
