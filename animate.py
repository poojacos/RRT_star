#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 02:13:47 2020

@author: poojaconsul
"""

from PIL import Image
import glob

def make_gif():
    # Create the frames
    frames = []
    imgs = glob.glob("./steps/*.png")
    if len(imgs) == 0:
        return
    
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)
     
    # Save into a GIF file that loops forever
    frames[0].save('rrtstar.gif', format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=100, loop=3)
    
#make_gif()