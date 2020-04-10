#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Change texture Path to make it relative to Plot Twist env variable.
"""

from __future__ import print_function, division, absolute_import

__author__ = "Titouan Perrot"
__license__ = "MIT"
__maintainer__ = "Titouan Perrot"
__email__ = ""


import maya.cmds as mc


def texture_path_relative():
    
    file_nodes = mc.ls(et='file')
    
    # Remove reference files from the list, we don't want to make changes on them
    ref_nodes = [i for i in file_nodes if mc.referenceQuery( i, isNodeReferenced=True)]
    file_nodes = [i for i in file_nodes if i not in ref_nodes]
        
    for i in file_nodes:
        tex_node_path = mc.getAttr('{0}.fileTextureName'.format(i))
        if tex_node_path:
            if 'Assets' in tex_node_path:
                tex_node_relative_path = tex_node_path.split('Assets', 1)[1]
                tex_node_relative_path = tex_node_relative_path.replace('/', '\\')
                tex_node_relative_path = '$PLOTTWIST_PROJECT\\\\Assets' + str(tex_node_relative_path)
                if mc.getAttr('{0}.uvTilingMode'.format(i))== 3 :
                    udim_file = tex_node_path.split('.')[-2]
                    if udim_file != '<UDIM>':
                        tex_node_relative_path = tex_node_relative_path.replace( udim_file, '<UDIM>')
                    
                mc.setAttr('{0}.fileTextureName'.format(i), str(tex_node_relative_path), typ='string')
            else : 
                raise Exception("Your maps need to be in Artella's folder")
        else:
            pass

    return
