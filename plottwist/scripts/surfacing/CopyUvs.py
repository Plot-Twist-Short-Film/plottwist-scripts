#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copy Uvs Component Mode for Multiple Meshes
"""

from __future__ import print_function, division, absolute_import

__author__ = "Titouan Perrot"
__license__ = "MIT"
__maintainer__ = "Titouan Perrot"
__email__ = ""


import maya.cmds as mc


def copy_uvs():
    """
    Copy Uvs Component Mode for Multiple Meshes
    """

    # grab all the selected objects
    selected_objects = mc.ls(sl=True)

    # save first one into variable
    # pop first one out of the selected objects list
    driver = selected_objects.pop(0)

    # for each object in the selected objects list
    for object in selected_objects:
        mc.select([driver, object])

        #transfer attributes
        mc.transferAttributes(sampleSpace=4,transferUVs=2, transferColors=0)
