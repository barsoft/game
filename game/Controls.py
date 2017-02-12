from OpenGL.GLUT import *

mousex = 0
mousey = 0
startx = 0
starty = 0


def mouseMotion(x, y):
    global mousex, mousey, startx, starty
    mousex = x - startx
    mousey = y - starty


def mouseClick(button, state, x, y):
    global startx, starty
    if (state == GLUT_DOWN):
        startx = x
        starty = y
