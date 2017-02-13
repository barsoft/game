from OpenGL.GLUT import *

startX = 0
startY = 0
cameraX = 0
cameraY = 0
cameraLastX = 0
cameraLastY = 0


def mouseMotion(x, y):
    global startX, startY, cameraY, cameraX, cameraLastX, cameraLastY
    cameraX = cameraLastX + y - startY
    cameraY = cameraLastY + x - startX


def mouseClick(button, state, x, y):
    global startX, startY, cameraY, cameraX, cameraLastX, cameraLastY
    if (state == GLUT_DOWN):
        startX = x
        startY = y
    if (state == GLUT_UP):
        cameraLastX = cameraX
        cameraLastY = cameraY
