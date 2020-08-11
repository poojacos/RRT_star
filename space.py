#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 09:39:28 2020

@author: poojaconsul
"""
from node import Node
from scipy.spatial import KDTree
import numpy as np

class Space:
    """
    Define the environment space of the problem
    occ- all pts except start and goal
    """
    def __init__(self, start, goal, obstacles = None, resolution = None, occ = None, goal_radius = 0.5):
        self.start = Node(0, start[0], start[1], 0, None)
        self.goal = Node(-1, goal[0], goal[1], float('inf'), None)
        self.goal_radius = goal_radius
        self.obstacles = obstacles
        self.resolution = resolution
        if occ == None:
            self.occ = [start] #list of [x,y]
            self.occ_nodes = [self.start]
        else:
            self.occ = [start] + occ
            occ_nodes = [Node(i+2, occ[i][0], occ[i][1], float('inf')) for i in range(len(occ))]
            self.occ_nodes = [self.start] + occ_nodes
        
    def __str__(self):
        return 'start = {}\ngoal = {}\nobstacles = {}\nresolution = {}\nocc = {}\ngoal_radius =\
              {}'.format(self.start, self.goal, self.obstacles, self.resolution, self.occ,\
              self.goal_radius)
    
    def kdtree_update(self):
        return KDTree(np.array(self.occ))
    
    def print_path(self, start, parent):
        nxt = start
        
        while nxt != -1:
            print('node: %d, x = %d, y = %d'%(nxt, self.occ_nodes[nxt].x, self.occ_nodes[nxt].y))
            nxt = parent[nxt]
        
        print('node: %d, x = %d, y = %d'%(start, self.occ_nodes[start].x, self.occ_nodes[start].y))
    
    def min_dist_node(self, cost, updated):
        minval, minidx = pow(10,6), -1 
        for i in range(len(updated)):
            if cost[i] < minval and updated[i] == False:
                minval = cost[i]
                minidx = i
        return minidx
                
    def dijkstra(self):
        num = len(self.occ)
        assert num == len(self.occ_nodes)
        updated = [False] * num
        cost = [float('inf')] * num
#        nodes = [self.occ[i] + [i] for i in range(num)] #distance, x, y, index
        parent = []
        start_idx = 0
        if not (self.start.x == self.occ[start_idx] and self.start.y == self.occ[start_idx]):
            print('Start index not 0, returning from Dijsktra')
            return
        
        updated[0], cost[0] = True, 0
        parent.append(-1)
        goal_not_found = True
        while goal_not_found:
            minidx = self.min_dist_node(cost, updated)
            next_node = self.occ_nodes[minidx]
            updated[minidx] = True
            edges = self.occ_nodes[minidx].edges
            for i in range(len(edges)):
                neigh_idx = edges[i].n
                if updated[neigh_idx] == False and cost[neigh_idx] > cost[next_node.n] + next_node.dist(edges[i]):
                    cost[neigh_idx] = cost[next_node.n] + next_node.dist(edges[i])
                    parent.append(next_node.n)
                    
#                    if point_circle_collision(edges[i].x, edges[i].y, self.goal.x, self.goal.y, self.goal_radius) == True:
#                        goal_not_found = False
#                        break
        return parent, cost
            