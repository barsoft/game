import numpy
from OpenGL.GL import *
from OpenGL.GLE import *
from OpenGL.GLUT import *


class Model:
    vbo = None
    VAO = None

    def __init__(self, vbo):
        self.vbo = vbo
        vertexData = numpy.array([
            # Vertex Positions
            0.0, 0.5, 0.0, 1.0,
            0.5, -0.366, 0.0, 1.0,
            -0.5, -0.366, 0.0, 1.0,

            # Vertex Colours
            1.0, 0.0, 0.0, 1.0,
            0.0, 1.0, 0.0, 1.0,
            0.0, 0.0, 1.0, 1.0,
        ], dtype=numpy.float32)
        # Core OpenGL requires that at least one OpenGL vertex array be bound
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        # Need VBO for triangle vertices and colours
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertexData.nbytes, vertexData,
                     GL_STATIC_DRAW)

        # enable array and set up data
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0,
                              None)
        # the last parameter is a pointer
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, 0,
                              ctypes.c_void_p(48))

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def draw(self):
        # glEnableVertexAttribArray(0)
        # glBindBuffer(GL_ARRAY_BUFFER, self.vbo.vertexBuffer)
        # glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        #
        # glEnableVertexAttribArray(1)
        # glBindBuffer(GL_ARRAY_BUFFER, self.vbo.uvBuffer)
        # glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)
        #
        # glEnableVertexAttribArray(2)
        # glBindBuffer(GL_ARRAY_BUFFER, self.vbo.normalBuffer)
        # glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 0, None)
        #
        # glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.vbo.indexBuffer)
        # glColor3f(1.0, 0.0, 0.0)
        # glDrawElementsus(GL_TRIANGLES, self.vbo.indicesList)
        glBindVertexArray(self.VAO)

        # draw triangle
        glDrawArrays(GL_TRIANGLES, 0, 3)
