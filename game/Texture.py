import numpy
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLE import *
from OpenGL.GLUT import *


class Texture:
    textureId = None
    imgData = None

    def __init__(self, path):
        img = Image.open(path)
        width, height = img.size
        self.imgData = numpy.array(list(img.getdata()), numpy.uint8)
        self.textureId = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.textureId)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.imgData)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)

    def bind(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textureId)
        #glUniform1i(self.textureId, 0);
