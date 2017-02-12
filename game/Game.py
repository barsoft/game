#!/usr/bin/python

# This is statement is required by the build system to query build info


if __name__ == '__build__':
    raise Exception

import sys
import game.Camera
from OpenGL.GL import *
from OpenGL.GLE import *
from OpenGL.GLUT import *
from OpenGL.GL import shaders
from OpenGL.raw.GLU import gluPerspective
from game.ModelType import *
from game.Model import *
from game.Texture import *
from game.Math import *

cube = None
snowman = None

shaderProgram = None
windowWidth = 500
windowHeight = 500

mousex = 0
mousey = 0
startx = 0
starty = 0


def main():
    global shaderProgram
    global cube, snowman
    # initialize glut
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_3_2_CORE_PROFILE | GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(windowWidth, windowHeight)
    glutCreateWindow(b"basic demo")
    glutDisplayFunc(draw)
    glutReshapeFunc(reshape)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)

    game.Camera.projectionMatrix = perspective(45.0, float(windowWidth) / float(windowHeight), 0.1, 100.0)

    # initialize GL */
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    print(glGetString(GL_VERSION))

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    loadShaders()

    modelType = ModelType('cube.obj')
    texture = Texture('cube.jpg')
    cube = Model(modelType, texture, shaderProgram)

    snowman = ModelType('snowman.obj')
    texture = Texture('snowman.bmp')
    snowman = Model(snowman, texture, shaderProgram)

    glutMainLoop()


def loadShaders():
    global shaderProgram
    vertexShader = shaders.compileShader("""
    #version 330 core
    layout(location = 0) in vec3 vertexPosition_modelspace;
    layout(location = 1) in vec2 vertexUV;
    out vec2 UV;
    uniform mat4 Projection;
    uniform mat4 View;
    uniform mat4 Model;
    void main(){
        gl_Position = Projection * View * Model * vec4(vertexPosition_modelspace,1);
        UV = vertexUV;
    }
    """, GL_VERTEX_SHADER)

    fragmentShader = shaders.compileShader("""
    #version 330 core
    in vec2 UV;
    out vec3 color;
    uniform sampler2D myTextureSampler;
    void main(){
        color = texture( myTextureSampler, UV ).rgb;
    }
    """, GL_FRAGMENT_SHADER)
    shaderProgram = shaders.compileProgram(vertexShader, fragmentShader)


# draw the polycone shape
def draw():
    global shaderProgram
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # cube.draw(mousex)
    snowman.draw(mousex)

    glutSwapBuffers()
    glutPostRedisplay()


def reshape(width, height):
    global windowWidth, windowHeight
    windowWidth = width
    windowHeight = height
    glViewport(0, 0, windowWidth, windowHeight)
    game.Camera.projectionMatrix = perspective(45.0, float(windowWidth) / float(windowHeight), 0.1, 100.0)


def motion(x, y):
    global mousex, mousey, startx, starty
    mousex = x - startx
    mousey = y - starty


def mouse(button, state, x, y):
    global startx, starty
    if (state == GLUT_DOWN):
        startx = x
        starty = y


main()
