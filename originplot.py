#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 23:21:19 2020

@author: poojaconsul
"""
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import collections  as mc
#import pylab as pl
 
class CenteredFormatter(mpl.ticker.ScalarFormatter):
    """Acts exactly like the default Scalar Formatter, but yields an empty
    label for ticks at "center"."""
    center = 0
    def __call__(self, value, pos=None):
        if value == self.center:
            return ''
        else:
            return mpl.ticker.ScalarFormatter.__call__(self, value, pos)
        
def center_spines(lc = None, ax=None, centerx=0, centery=0):
    """Centers the axis spines at <centerx, centery> on the axis "ax", and
    places arrows at the end of the axis spines."""
    if ax is None:
        ax = plt.gca()
        
    if lc is not None:
        ax.add_collection(lc)
        ax.add_collection(lc)
    # Set the axis's spines to be centered at the given point
    # (Setting all 4 spines so that the tick marks go in both directions)
    ax.spines['left'].set_position(('data', centerx))
    ax.spines['bottom'].set_position(('data', centery))
    ax.spines['right'].set_position(('data', centerx - 1))
    ax.spines['top'].set_position(('data', centery - 1))

#    # Draw an arrow at the end of the spines
#    ax.spines['left'].set_path_effects([EndArrow()])
#    ax.spines['bottom'].set_path_effects([EndArrow()])

    # Hide the line (but not ticks) for "extra" spines
    for side in ['right', 'top']:
        ax.spines[side].set_color('none')

    # On both the x and y axes...
    for axis, center in zip([ax.xaxis, ax.yaxis], [centerx, centery]):
        # Turn on minor and major gridlines and ticks
        axis.set_ticks_position('both')
        axis.grid(True, 'major', ls='solid', lw=0.5, color='gray')
        axis.grid(True, 'minor', ls='solid', lw=0.1, color='gray')
        axis.set_minor_locator(mpl.ticker.AutoMinorLocator())

        # Hide the ticklabels at <centerx, centery>
        formatter = CenteredFormatter()
        formatter.center = center
        axis.set_major_formatter(formatter)

    # Add offset ticklabels at <centerx, centery> using annotation
    # (Should probably make these update when the plot is redrawn...)
    xlabel, ylabel = map(formatter.format_data, [centerx, centery])
    ax.annotate('(%s, %s)' % (xlabel, ylabel), (centerx, centery),
            xytext=(-4, -4), textcoords='offset points',
            ha='right', va='top')
    
def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 10))  # outward by 10 points
            spine.set_smart_bounds(True)
        else:
            spine.set_color('none')  # don't draw spine

    # turn off ticks where there is no spine
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        # no yaxis ticks
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        # no xaxis ticks
        ax.xaxis.set_ticks([])
        
#http://matplotlib.org/examples/pylab_examples/spine_placement_demo.html
def plot_cenetered(x, y):
    fig = plt.figure()    
    ax = fig.add_subplot(2, 2, 1)
    ax.plot(x, y, clip_on=False)
    adjust_spines(ax, ['left', 'bottom'])
    plt.show()

#https://stackoverflow.com/questions/4694478/center-origin-in-matplotlib
def treeplot(x, y, edges = None, itr = 0):
#    https://stackoverflow.com/questions/21352580/matplotlib-plotting-numerous-disconnected-line-segments-with-different-colors
#    lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
#    c = np.array([(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
#    lc = mc.LineCollection(lines, colors=c, linewidths=2)
    
#    line, = plt.plot(x, y, '.', color = 'green')
    line, = plt.plot(x, y, '.', color = 'green')  #for states
    line2, = plt.plot([8], [8], 'o', color = 'black')
    rect1 = [[4, 4, 5, 5, 4], [-4, 9, 9, -4, -4]]
    rect2 = [[-6, -6, 0, 0, -6], [-5, -4, -4, -5, -5]]
    plt.plot(rect1[0], rect1[1], color = 'magenta')
    plt.plot(rect2[0], rect2[1], color = 'magenta')
#    plt.savefig('./steps/scatter_%d.png'%(itr))
#    rect = [[(4, -4), (4, 9)], [(4, 9), (5, 9)], [(5, -4), (5, 9)], [(4, -4), (5, -4)],\
#               [(-6, -4), (0, -4)], [(0, -4), (0, -5)], [(-6,-5),(0,-5)], [(-6,-4), (-6,-5)]]
#    lc = mc.LineCollection(rect, colors=np.array([(0, 0, 1, 1)]), linewidths=1)
    lc = mc.LineCollection(edges, colors=np.array([(0, 0, 1, 1)]), linewidths=1)
    center_spines(lc) #for edges
    plt.axis('equal')
    plt.xlim(-15,15)
    plt.ylim(-15,15)
#    fig1 = plt.gcf()
    plt.savefig('./steps/tree_%d.png'%(itr))
    plt.show()

def treepath(x, y, edges = None, path = None, itr = 0):
#    line, = plt.plot(x, y, '.', color = 'green')  #for states
    line2, = plt.plot([8], [8], 'o', color = 'black')
    rect1 = [[4, 4, 5, 5, 4], [-4, 9, 9, -4, -4]]
    rect2 = [[-6, -6, 0, 0, -6], [-5, -4, -4, -5, -5]]
    plt.plot(rect1[0], rect1[1], color = 'magenta')
    plt.plot(rect2[0], rect2[1], color = 'magenta')
#    rect = [[(4, -4), (4, 9)], [(4, 9), (5, 9)], [(5, -4), (5, 9)], [(4, -4), (5, -4)],\
#               [(-6, -4), (0, -4)], [(0, -4), (0, -5)], [(-6,-5),(0,-5)], [(-6,-4), (-6,-5)]]
    lc = None
    if edges:
        lc = mc.LineCollection(edges, colors=np.array([(0, 0, 1, 1)]), linewidths=0.1)
    plt.plot(path[0], path[1], color = 'red') #for path
#    lc = mc.LineCollection(edges, colors=c, linewidths=1)
    center_spines(lc) #for edges
    plt.axis('equal')
    plt.xlim(-15,15)
    plt.ylim(-15,15)
#    fig1 = plt.gcf()
    plt.savefig('./steps/path_%d.png'%(itr))
    plt.show()
    
def costplot(costs, step):
    costs = np.array(costs)
#    costs = costs[costs < 100]
    y = np.arange(1000, len(costs)-1, step, dtype = np.int16)

    try:
        plt.plot(y, costs[y])
        plt.savefig('./res/goalcost.jpg')
    except:
        print('Error: Invalid iterations or step size')
#x = np.random.randint(-10,10,20)
#x = np.linspace(0, 2*np.pi, 100)
#y = 2*np.sin(x)
#treepath(x[:10], x[10:], None, [x[:5], x[10:15]], 4) 
#lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]
#treeplot(x[:10], x[10:], lines, 0) 
#treeplot(x,y) 