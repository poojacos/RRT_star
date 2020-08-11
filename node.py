#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 09:11:58 2020

@author: poojaconsul
"""
import math 

class Node:
    """
    Node class for a tree
    """
    def __init__(self, n, x, y, cost = None, parent = None, edges = []):
        self.n = n
        self.x = x
        self.y = y
        self.cost = cost
        self.parent = parent
        self.edges = edges
        
    def __str__(self):
        return "x:{}, y:{}, cost:{}, parent:{}".format(self.x, self.y, self.cost, self.parent)
    
    def dist(self, n):
        return math.sqrt((self.x - n.x)**2 + (self.y - n.y)**2)
    
    def costsec(self, n):
        dx = self.x - n.x
        dy = self.y - n.y
        theta = math.atan2(dy, dx)
        if math.degrees(theta)/90 % 1 < 0.01:
            return self.dist(n)
        return self.dist(n)/math.cos(theta)**2
    
    def notinspace(self, xmin, xmax, ymin, ymax):
        if self.x < xmin + 0.6 or self.x > xmax - 0.6 or self.y < ymin + 0.6 or self.y > ymax - 0.6:
            return True
        return False