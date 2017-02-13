#!/usr/bin/python

# This is statement is required by the build system to query build info


if __name__ == '__build__':
    raise Exception

import sys
import game.Camera
from OpenGL.GL import *
from OpenGL.GLE import *
from OpenGL.GLUT import *
from OpenGL.raw.GLU import gluPerspective
from game.ModelType import *
from game.Model import *
from game.Texture import *
from game.Math import *
import platform
import game.Shaders
import numpy as np
import game.Controls

cube = None
snowman = None
grasses = []

windowWidth = 500
windowHeight = 500

lightID = None


def JoinStyle(msg):
    sys.exit(0)


def main():
    global cube, snowman, grass, grasses
    global lightID
    # initialize glut
    glutInit(sys.argv)
    print(platform.system())

    if (platform.system() == 'Darwin'):
        glutInitDisplayMode(GLUT_3_2_CORE_PROFILE | GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    else:
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    glutInitWindowSize(windowWidth, windowHeight)
    glutCreateWindow(b"basic demo")
    glutDisplayFunc(draw)
    glutReshapeFunc(reshape)
    glutMouseFunc(game.Controls.mouseClick)
    glutMotionFunc(game.Controls.mouseMotion)

    game.Camera.projectionMatrix = perspective(45.0, float(windowWidth) / float(windowHeight), 0.1, 100.0)

    # initialize GL */
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    print(glGetString(GL_VERSION))

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    game.Shaders.loadShaders()

    type = ModelType('assets/snowman.obj')
    texture = Texture('assets/snowman.bmp')
    snowman = Model(type, texture, game.Shaders.shaderProgram)

    type = ModelType('assets/grass.obj')
    texture = Texture('assets/grass.jpg')

    size = 5
    for i in range(-size, size + 1):
        for j in range(-size, size + 1):
            g = Model(type, texture, game.Shaders.shaderProgram)
            g.x = i * 2
            g.z = j * 2
            grasses.append(g)

    snowman.y += 1
    game.Camera.cameraRotY = -90
    game.Camera.cameraRotX = -30

    glutMainLoop()


# draw the polycone shape
def draw():
    global cube, snowman, grasses
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    game.Camera.viewMatrix = lookat(game.Camera.eye, game.Camera.target, game.Camera.up)
    game.Camera.viewMatrix = game.Camera.viewMatrix * rotate(game.Camera.cameraRotX, np.array([1, 0, 0]))
    game.Camera.viewMatrix = game.Camera.viewMatrix * rotate(game.Camera.cameraRotY, np.array([0, 1, 0]))

    for g in grasses:
        g.draw()
    snowman.draw()

    glutSwapBuffers()
    glutPostRedisplay()


def reshape(width, height):
    global windowWidth, windowHeight

    windowWidth = width
    windowHeight = height
    glViewport(0, 0, windowWidth, windowHeight)
    game.Camera.projectionMatrix = perspective(45.0, float(windowWidth) / float(windowHeight), 0.1, 100.0)


main()
