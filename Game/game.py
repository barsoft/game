#!/usr/bin/python

# This is statement is required by the build system to query build info
from OpenGL.GL import shaders
from OpenGL.raw.GLU import gluPerspective

if __name__ == '__build__':
    raise Exception

import sys
from OpenGL.GL import *
from OpenGL.GLE import *
from OpenGL.GLUT import *
from game.ModelType import *
from game.Model import *
from game.Texture import *

model = None
shaderProgram = None
windowWidth = 500
windowHeight = 500


def main(drawFunc, reshapeFunc):
    global glutDisplayFunc, glutMotionFunc, model
    # initialize glut
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(windowWidth, windowHeight)
    glutCreateWindow(b"basic demo")
    glutDisplayFunc(drawFunc)
    glutReshapeFunc(reshapeFunc)

    # initialize GL */
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 0.0)

    loadShaders()

    MatrixID = glGetUniformLocation(programID, "MVP");

    modelType = ModelType('cube.obj')
    texture = Texture('cube.jpg')
    model = Model(modelType, texture)

    glutMainLoop()


def loadShaders():
    global shaderProgram
    vertexShader = shaders.compileShader("""
    #version 330 core
    layout(location = 0) in vec3 vertexPosition_modelspace;
    layout(location = 1) in vec2 vertexUV;
    out vec2 UV;
    uniform mat4 MVP;
    void main(){
        gl_Position =  MVP * vec4(vertexPosition_modelspace,1);
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
    glUseProgram(shaderProgram)
    glPushMatrix()
    glTranslatef(-1.5, 0.0, -6.0)
    model.draw()

    glPopMatrix()

    glutSwapBuffers()
    glutPostRedisplay()


def reshape(width, height):
    global windowWidth, windowHeight
    windowWidth = width
    windowHeight = height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(windowWidth) / float(windowHeight), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


main(draw, reshape)
