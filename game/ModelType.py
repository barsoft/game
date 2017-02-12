import numpy
from OpenGL.GL import *
from OpenGL.GLE import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo


class ModelType:
    def __init__(self, path):
        self.vertexList = []
        self.uvList = []
        self.normalList = []
        self.indexList = []
        self.vertexPositions = None
        self.uvPositions = None
        self.normalPositions = None
        self.indexPositions = None

        self.readObj(path)
        self.load()

    def readObj(self, path):
        objFile = open(path, 'r')
        initVertexList = []
        initUvList = []
        initNormalList = []

        for line in objFile:
            split = line.split()
            # if blank line, skip
            if not len(split):
                continue
            if split[0] == "v":
                initVertexList.append(split[1:])
            elif split[0] == "vt":
                initUvList.append(split[1:])
            elif split[0] == "vn":
                initNormalList.append(split[1:])
            elif split[0] == "f":
                for i in range(0, 3):
                    vertex = split[i + 1].split('/')
                    self.vertexList += (initVertexList[int(vertex[0]) - 1])
                    self.uvList += (initUvList[int(vertex[1]) - 1])
                    self.normalList += (initNormalList[int(vertex[2]) - 1])
                    self.indexList.append(len(self.indexList))

        objFile.close()

    def load(self):
        self.vertexPositions = vbo.VBO(numpy.array(self.vertexList, dtype=numpy.float32))
        self.uvPositions = vbo.VBO(numpy.array(self.uvList, dtype=numpy.float32))
        self.normalPositions = vbo.VBO(numpy.array(self.normalList, dtype=numpy.float32))
        self.indexPositions = vbo.VBO(numpy.array(self.indexList, dtype=numpy.int32), target=GL_ELEMENT_ARRAY_BUFFER)

    def destroy(self):
        self.vertexPositions.delete()
        self.uvPositions.delete()
        self.normalPositions.delete()
        self.indexPositions.delete()
