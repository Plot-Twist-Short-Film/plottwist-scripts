#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Activate Arnold tesselation for a mesh selection
"""

from __future__ import print_function, division, absolute_import

__author__ = "Titouan Perrot"
__license__ = "MIT"
__maintainer__ = "Titouan Perrot"
__email__ = ""


import maya.cmds as mc

def Tesselate(selection=False):

    if not selection: # Check Selection
        selection = mc.ls(sl=True)       

    mc.filterExpand(ex =True, sm=12) # Extract only polymesh
    if len(selection) == 1: # Check how many elements are present in the list
        selection = [selection[0]]
    elif len(selection) == False:
        raise Exception ('You must select a mesh')
    else:
        pass
    
    for i in selection :
        mc.setAttr(i + '.aiSubdivType', 1) # Type : 0 = None, 1 = Catclark, 2 = Linear
        mc.setAttr(i + '.aiSubdivIterations', 2) # Subdivsion Iterations
        mc.setAttr(i + '.aiSubdivAdaptiveMetric', 1) # Adaptive Metric : 0 = Auto, 1 = Edge_length, 2 = Flatness
       
Tesselate()   