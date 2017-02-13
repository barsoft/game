import numpy
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLE import *
from OpenGL.GLUT import *


class Texture:
    texture = None
    imgData = None

    def __init__(self, path):
        img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
        width, height = img.size
        self.imgData = numpy.array(list(img.getdata()), numpy.uint8)
        self.texture = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, self.texture)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.imgData)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)
        glGenerateMipmap(GL_TEXTURE_2D)

    def bind(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
