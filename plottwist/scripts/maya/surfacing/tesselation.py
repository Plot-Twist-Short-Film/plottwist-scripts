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


def tesselate(selection=False):

    # Check Selection
    if not selection:
        selection = mc.ls(sl=True)

    # Extract only polymesh
    mc.filterExpand(ex=True, sm=12)

    # Check how many elements are present in the list
    if not selection:
        raise Exception('You must select a mesh')

    if len(selection) == 1:
        selection = [selection[0]]
    
    for i in selection:
        # Type : 0 = None, 1 = Catclark, 2 = Linear
        mc.setAttr(i + '.aiSubdivType', 1)

        # Subdivsion Iterations
        mc.setAttr(i + '.aiSubdivIterations', 2)

        # Adaptive Metric : 0 = Auto, 1 = Edge_length, 2 = Flatness
        mc.setAttr(i + '.aiSubdivAdaptiveMetric', 1)
