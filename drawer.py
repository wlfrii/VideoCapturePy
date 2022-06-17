import cv2
import math
from enum import Enum # just import the necessary module

# A Color class
class Color():
    ''' A Color enumeration class '''
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (255, 0, 0)
    ORANGE = (0, 140, 255)

def drawCenterLine(img, win_width=1920, win_height=1080, color=Color.GREEN):
    '''Drawing the horizontal and vertical center lines on the input image. '''
    cv2.line(img, (0, int(win_height / 2)), (win_width, int(win_height / 2)), color)
    cv2.line(img, (int(win_width / 2), 0), (int(win_width / 2), win_height), color)
    return img

def drawDiagnalLine(img, win_width=1920, win_height=1080, color=Color.GREEN):
    '''Drawing the diagnal lines on the input image. '''
    cv2.line(img, (0, 0), (int(win_width), int(win_height)), color)
    cv2.line(img, (0, int(win_height)), (int(win_width), 0), color)
    return img

def drawDiagnalCircle(img, fov, proportion_of_fov, win_width=1920, win_height=1080,radius=8,color=Color.ORANGE,line_width=2):
    '''Drawing circle in diagnal line.
    
    @param img The input image.
    
    @param fov The field of view of the camera.

    @param proportion_of_fov The proportion of fov for determining the position of the circle in diagnal line.
    '''
    diag = math.sqrt(math.pow(win_width / 2, 2) + math.pow(win_height / 2, 2))
    diag1 = diag - diag / math.tan(fov / 2) * math.tan(proportion_of_fov * fov / 2)
    tmp1 = int(diag1/diag*win_width/2)
    tmp2 = int(diag1/diag*win_height/2)
    cv2.circle(img, (tmp1, tmp2), radius, color, line_width)
    tmp1 = win_width - int(diag1/diag*win_width/2)
    tmp2 = int(diag1/diag*win_height/2)
    cv2.circle(img, (tmp1, tmp2), radius, color, line_width)
    tmp1 = int(diag1/diag*win_width/2)
    tmp2 = win_height - int(diag1/diag*win_height/2)
    cv2.circle(img, (tmp1, tmp2), radius, color, line_width)
    tmp1 = win_width - int(diag1/diag*win_width/2)
    tmp2 = win_height - int(diag1/diag*win_height/2)
    cv2.circle(img, (tmp1, tmp2), radius, color, line_width)
    return img

def drawLineInWidth(img, win_width=1920, win_height=1080, line_len=20, color=Color.GREEN):
    '''Drawing a short prompt line in width direction, prompting the postion of image height'''
    d = int((win_width-win_height)/2)
    dup = int(win_height / 2) - line_len
    ddown = int(win_height / 2) + line_len
    cv2.line(img, (d, dup), (d, ddown), color)
    cv2.line(img, (win_width-d, dup), (win_width-d, ddown), color)
    return img