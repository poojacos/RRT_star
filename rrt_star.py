#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 09:43:00 2020

@author: poojaconsul
"""
import os
import shutil
from space import Space
from node import Node
import numpy as np
import math
import collision
import originplot
from animate import make_gif
from scipy.spatial import KDTree

def sample(xmin, xmax, ymin, ymax):
# returns a state x that is sampled uniformly randomly from the domain
    x = np.random.uniform(xmin, xmax)
    y = np.random.uniform(ymin, ymax)
    return Node(-1, x, y, float('inf'), None, [])

def calc_distance_and_angle(from_node, to_node):
    dx = to_node.x - from_node.x
    dy = to_node.y - from_node.y
    d = math.hypot(dx, dy)
    theta = math.atan2(dy, dx)
    return d, theta

def steer_extend(from_node, to_node, epsilon = 1):
    d, theta = calc_distance_and_angle(from_node, to_node)
    d = epsilon
    to_node.cost = d + from_node.cost
    num_pts = math.floor(d/space.resolution)
    
    x, y = from_node.x, from_node.y
    path_x, path_y = [x], [y]
    
    for i in range(num_pts):
        x += space.resolution * math.cos(theta)
        y += space.resolution * math.sin(theta)
        path_x.append(x)
        path_y.append(y)
    return to_node.cost, [path_x, path_y], Node(-1, x, y, to_node.cost, None, [])
    
    
def steer(from_node, to_node):
# returns the optimal control trajectory of traveling from x1 to x2 # and the cost
    d, theta = calc_distance_and_angle(from_node, to_node)
    to_node.cost = d + from_node.cost
    num_pts = math.floor(d/space.resolution)
    
    x, y = from_node.x, from_node.y
    path_x, path_y = [x], [y]
    
    for i in range(num_pts):
        x += space.resolution * math.cos(theta)
        y += space.resolution * math.sin(theta)
        path_x.append(x)
        path_y.append(y)
    return to_node.cost, [path_x, path_y], to_node
        
def is_in_collision(node):
# returns True if state x of the robot is incollision with any of the
    for o in space.obstacles:
        hit = collision.circle_rect_collision(node.x, node.y, o, obj_radius)
        if hit:
            print('collision found for ',node)
            return True
    return False
    
def nearest(node, num = 1):
# finds a node in the tree that is closest to the state x (closest in what
#metric?)
    _, nearest_ind = kdtree.query(np.array([node.x, node.y]).reshape(1,-1), k = num)
    if is_in_obstacle(node, space.occ_nodes[nearest_ind[0]]):
        return None
    return space.occ_nodes[nearest_ind[0]]
 
def get_neighbours(node, gamma = 10, eta = 5):
    neigh = []
    v = len(space.occ)
    try:
        boundary = min(gamma * pow(math.log(v)/v, 0.5), eta)
    except:
        print('error in boundary radius calc')
    kdtree = KDTree(np.array(space.occ))
    idx = kdtree.query_ball_point([node.x, node.y], boundary)
    
    for i in idx:
        if not is_in_obstacle(node, space.occ_nodes[i]):
            neigh.append(space.occ_nodes[i])
    return neigh
    
def is_in_obstacle(from_node, to_node):
    for o in space.obstacles:
        hit = collision.line_rect_collision(from_node.x, from_node.y, to_node.x, to_node.y, o)
        if hit:
            return True
    return False
          
def connect(new_node, nearest_node, cost):
# add state x to the tree
# cost of state x = cost of the parent + cost of steer(parent, x)
    #find most optimal connection for new_node
    closest_node, min_cost = nearest_node, cost
    for neigh in neighbours:
        cost_to_check = neigh.cost + new_node.dist(neigh) #cost of steer(parent, x) = distance bwn nodes?
        if cost_to_check < min_cost:
            closest_node, min_cost = neigh, cost_to_check
            
    #add new_node, update it's edges, update it's parent's edges
    new_node.parent = closest_node
    new_node.cost = min_cost
    new_node.edges.append(closest_node)
    closest_node.edges.append(new_node)
    new_node.n = len(space.occ)
    space.occ.append([new_node.x, new_node.y])
    space.occ_nodes.append(new_node)

def update_children_cost(node):
    for child in node.edges:
        if child.parent.n == node.n:
            child.cost = node.cost + node.dist(child)
            update_children_cost(child)
            

def rewire(new_node, neighbours):
# rewire all nodes in the tree within the O(gamma (log n/n)ˆ{1/d}} ball 
# near the state x, update the costs of all rewired neighbors
    rewire = 0
    for neigh in neighbours:
        cost_to_check = new_node.cost + new_node.dist(neigh) #cost of steer(parent, x) = distance bwn nodes?
        if cost_to_check < neigh.cost:
            rewire += 1
            neigh.cost = cost_to_check
            old_parent = neigh.parent
            neigh.parent = new_node
        
            #remove the parent, child connection
            for node in neigh.edges:
                if node.x == old_parent.x and node.y == old_parent.y:
                    neigh.edges.remove(node)
                    break
                
            for node in old_parent.edges:
                if node.x == neigh.x and node.y == neigh.y:
                    old_parent.edges.remove(node)
                    break
                
            neigh.edges.append(new_node)
            new_node.edges.append(neigh)
            update_children_cost(node)
    print('rewire count: {}, neighbours: {}'.format(rewire, len(neighbours)))
            
def min_goal_cost(nodes_in_goal):
    m, n, idx  = pow(10,7), len(nodes_in_goal), -1

    if n == 0:
        return m, -1
    
    for i in range(n):
        if nodes_in_goal[i].cost < m:
            m = nodes_in_goal[i].cost
            idx = i
    return nodes_in_goal[idx].cost, idx
            
    
def get_path():
    #finding path
    goal, idx = min_goal_cost(nodes_in_goal)
    if idx == -1:
        print('Cannot make path, no goal state reached!')
        return []
    
    path = [[nodes_in_goal[idx].x], [nodes_in_goal[idx].y]]
    start_not_reached = True
    nxt = nodes_in_goal[idx]
    sx, sy = space.start.x, space.start.y
    while start_not_reached:
        nxt = nxt.parent
        if nxt.x == sx and nxt.y == sy:
            start_not_reached = False
        
        path[0] = [nxt.x] + path[0]
        path[1] = [nxt.y] + path[1]
        
    return path
        
def get_edges():
    lc = []
    for i in range(len(space.occ_nodes)):
        sx, sy = space.occ_nodes[i].x, space.occ_nodes[i].y
        neigh = space.occ_nodes[i].edges
        for node in neigh:
            lc.append([(sx, sy), (node.x, node.y)])
    return lc

if __name__ == "__main__":
    iterations = 10000
    obj_radius = 0.6
    obstacle_list = [[-6, -5, 6, 1], [4, -4, 1, 13]] #bottom-left origin
    start = [0,0]
    goal = [8,8]
    xmin, xmax, ymin, ymax = -10, 10, -10, 10
    
    nodes_in_goal = []
    min_path_cost = []  #store this at every iteration
    space = Space(start, goal, obstacle_list, 1)
    kdtree = space.kdtree_update()
    spacex = [space.start.x]
    spacey = [space.start.y]
    
    try:
        shutil.rmtree(os.path.join(os.getcwd(), 'steps'))
    except:
        print('Steps directory dne')
    os.mkdir(os.path.join(os.getcwd(), 'steps'))
    
    for i in range(iterations):
        print('--------iteration %d---------'%i)
        rand = sample(xmin, xmax, ymin, ymax) #rand initialized with x, y and cost = None
        nearest_node = nearest(rand)
        if nearest_node == None:
            continue
        cost, path, new_node = steer_extend(nearest_node, rand)
        if is_in_collision(new_node) or new_node.notinspace(xmin, xmax, ymin, ymax):
            continue
        spacex.append(new_node.x)
        spacey.append(new_node.y)
        neighbours = get_neighbours(new_node)  #obstacle free neighbours
        connect(new_node, nearest_node, cost)
        rewire(new_node, neighbours)
        
        if collision.point_circle_collision(new_node.x, new_node.y, space.goal.x,\
                                            space.goal.y, space.goal_radius) == True:
            nodes_in_goal.append(new_node)
            
        kdtree = space.kdtree_update()
        mingoal, _ = min_goal_cost(nodes_in_goal)
        min_path_cost.append(mingoal)
        edges = get_edges()
        if i%50 == 0 or i == iterations - 1:
#            originplot.treeplot(spacex, spacey, edges, i)
            path = get_path()
            if path:
                originplot.treepath(spacex, spacey, edges, path, i)
    
    make_gif()
    originplot.costplot(min_path_cost, 50)