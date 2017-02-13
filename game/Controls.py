from OpenGL.GLUT import *
import game.Camera

startX = 0
startY = 0
cameraLastX = None
cameraLastY = None


def mouseMotion(x, y):
    global startX, startY, cameraLastX, cameraLastY
    if (cameraLastX == None):
        cameraLastX = game.Camera.cameraRotX
    if (cameraLastY == None):
        cameraLastY = game.Camera.cameraRotY
    game.Camera.cameraRotX = cameraLastX + y - startY
    game.Camera.cameraRotY = cameraLastY + x - startX


def mouseClick(button, state, x, y):
    global startX, startY, cameraLastX, cameraLastY
    if (state == GLUT_DOWN):
        startX = x
        startY = y
    if (state == GLUT_UP):
        cameraLastX = game.Camera.cameraRotX
        cameraLastY = game.Camera.cameraRotY
