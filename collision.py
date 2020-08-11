#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 18:36:22 2020

@author: poojaconsul
"""
import math

def line_line_collision(x1, y1, x2, y2, x3, y3, x4, y4):
    #http://www.jeffreythompson.org/collision-detection/line-line.php
    d1 = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    d2 = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    if d1 >= 0 and d1 <= 1 and d2 >= 0 and d2 <= 1:
        return True
    return False

def line_rect_collision(x1, y1, x2, y2, rect):
    rx, ry, rw, rh = rect[:4]
    left = line_line_collision(x1, y1, x2, y2, rx, ry, rx, ry + rh)
    right = line_line_collision(x1, y1, x2, y2, rx + rw, ry, rx + rw, ry + rh)
    top = line_line_collision(x1, y1, x2, y2, rx , ry + rh, rx + rw, ry + rh)
    bottom = line_line_collision(x1, y1, x2, y2, rx, ry, rx + rw, ry)
    if left or right or bottom or top:
        return True
    return False

def circle_rect_collision(cx, cy, rect, radius): #bottom left is origin
    rx, ry, rw, rh = rect[:4]
    testx, testy = cx, cy
    #to left
    if(cx < rx): 
        testx = rx
    #to right
    elif(cx > rx + rw):
        testx = rx + rw
    
    #top
    if(cy < ry):
        testy = ry
    #bottom
    elif(cy > ry + rh):
        testy = ry + rh
    
#    print(testx, testy, obj_radius)    
    dx, dy = cx - testx, cy - testy
    d = math.sqrt(dx**2 + dy**2)
#    print(dx, dy, d, obj_radius)
    if d <= radius:
        return True
    return False

def circle_circle_collision(x1, y1, r1, x2, y2, r2):
    if x1 == x2 and y1 == y2:
        return True
    if math.sqrt((x1 - x2)**2 + (y1 - y2)**2) <= r1 + r2:
        return True
    return False

def point_circle_collision(x1, y1, cx, cy, r):
    if math.sqrt((x1 - cx)**2 + (cy - y1)**2) <= r:
        return True
    return False
    