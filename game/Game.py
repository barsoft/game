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
grass = None
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

    if (platform.system() == 'Mac'):
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

    type = ModelType('assets/cube.obj')
    texture = Texture('assets/cube.jpg')
    cube = Model(type, texture, game.Shaders.shaderProgram)

    type = ModelType('assets/snowman.obj')
    texture = Texture('assets/snowman.bmp')
    snowman = Model(type, texture, game.Shaders.shaderProgram)

    type = ModelType('assets/grass.obj')
    texture = Texture('assets/grass.jpg')

    for i in range(-5, 6):
        for j in range(-5, 6):
            g = Model(type, texture, game.Shaders.shaderProgram)
            g.x = i
            g.z = j
            grasses.append(g)

    glutMainLoop()


# draw the polycone shape
def draw():
    global cube, snowman, grasses
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    game.Camera.viewMatrix = lookat(game.Camera.eye, game.Camera.target, game.Camera.up)
    game.Camera.viewMatrix = game.Camera.viewMatrix * rotate(game.Controls.mousex, np.array([0, 1, 0]))

    for g in grasses:
        g.draw()
    cube.draw()
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
