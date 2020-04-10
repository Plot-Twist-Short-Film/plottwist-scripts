#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cleaner for surfacing scenes
"""

from __future__ import print_function, division, absolute_import

__author__ = "Titouan Perrot"
__license__ = "MIT"
__maintainer__ = "Titouan Perrot"
__email__ = ""


import maya.cmds as mc

def delete_lockednodes(nodes):
    mc.lockNode(nodes, lock=False)
    mc.delete(nodes)


def Clean_RenderLayers():
    renderlayers_scene = mc.ls(type='renderLayer') #Gather all Renderlayers in the scene
    renderlayers_scene.remove('defaultRenderLayer') # Remove defaultRenderLayer of the list  
    renderlayers_to_del = [i for i in renderlayers_scene if not mc.referenceQuery( i, isNodeReferenced=True)] # Remove Renderlayers from a reference file         
    renderlayers_nb = len(renderlayers_to_del)
    if renderlayers_nb:
        delete_lockednodes(renderlayers_to_del)
    print('Cleaned {} Render layers'.format(renderlayers_nb))


def Clean_Aovs():  
    aov_scene = mc.ls(type='aiAOV') #Gather all AOVs in the scene
    aov_to_del = [i for i in aov_scene if not mc.referenceQuery( i, isNodeReferenced=True)] # Remove AOVs from a reference file    
    aov_nb = len(aov_to_del)
    if aov_nb:
        delete_lockednodes(aov_to_del)
    print('Cleaned {} AOVs'.format(aov_nb))


def Clean_LightEditor():    
    lightEditor_scene = mc.ls(type='lightEditor') #Gather all LightEditor in the scene
    lighteditor_to_del = [i for i in lightEditor_scene if not mc.referenceQuery( i, isNodeReferenced=True)] # Remove LightEditor from a reference file    
    lightEditor_nb = len(lighteditor_to_del)
    if lightEditor_nb:
        delete_lockednodes(lighteditor_to_del)
    print('Cleaned {} LightEditors'.format(lightEditor_nb))


def Clean_Nodes():
    intermediate_nodes = mc.ls(intermediateObjects=True) #Gather all Intermediate Nodes in the scene
    group_ID = [i for i in intermediate_nodes if mc.objectType(i, isType='groupId') or mc.objectType(i, isType='GroupParts')] # Gather Group ID info
    anim_layer = [i for i in intermediate_nodes if mc.objectType(i, isType='animLayer')] # Gather Anim layers info
    layers = [i for i in intermediate_nodes if mc.objectType(i, isType='displayLayer')] # Gather Display layers info
    layers.remove('defaultLayer') # Get rid of default layer. We don't want to delete it
    ai_nodes = [i for i in intermediate_nodes if mc.objectType(i, isType='aiOptions') or mc.objectType(i, isType='aiAOVFilter') or mc.objectType(i, isType='aiAOVDriver')] # Gather Ai Nodes info
    
    refs_file = mc.file(q=True, l=True, shn=True) # Gather Ref type info
    ref_namespace = [ref.replace('.ma', 'RN') for ref in refs_file if '.ma' in ref] # Check references files 
    
    ref_type_nodes = [i for i in intermediate_nodes if mc.objectType(i, isType='reference')] # Check reference nodes type
    ref_type_nodes = [i for i in ref_type_nodes if i not in ref_namespace] # Exclude reference files from references node type    
    poly_nodes = [i for i in intermediate_nodes if 'kPoly' in mc.nodeType(i, apiType=True)] # Gather Poly nodes 
    
    nodes_to_del = group_ID + anim_layer + layers + ref_type_nodes + poly_nodes + ai_nodes
    nodes_nb = len(nodes_to_del)
    if nodes_nb:
        delete_lockednodes(nodes_to_del)
    print('Cleaned {} Nodes'.format(nodes_nb))
    
    
def Clean_CustomNodes():
    intermediate_nodes = mc.ls(intermediateObjects=True)
    custom_nodes = ['sceneConfigurationScriptNode', 
                    'uiConfigurationScriptNode',
                    'TurtleDefaultBakeLayer',
                    'TurtleBakeLayerManager',
                    'TurtleRenderOptions',
                    'TurtleUIOptions']
    
    for i in custom_nodes:
        if i in intermediate_nodes:
            mc.lockNode(i, lock=False)
            mc.delete(i)
            print('Cleaned {}'.format(i))


def Clean_Cameras():
    cameras = mc.ls(type=('camera'), l=True) # Get all cameras first
    startup_cameras = [cam for cam in cameras if mc.camera(mc.listRelatives(cam, parent=True)[0], startupCamera=True, q=True)] # Filter all startup / default cameras
    non_startup_cameras_shapes = list(set(cameras) - set(startup_cameras)) # List Non-default cameras
    non_startup_cameras_shapes = [i for i in non_startup_cameras_shapes if not mc.referenceQuery( i, isNodeReferenced=True)] # Remove cameras from a reference file        
    non_startup_cameras = [mc.listRelatives(cam, parent=True)[0] for cam in non_startup_cameras_shapes]  
    if non_startup_cameras:
        mc.delete(non_startup_cameras)
        print('Cleaned {} non startup camera(s)'.format(len(non_startup_cameras)))
        
def Clean_Tesselation():
    mc.listRelatives('root', ad=True)
    selection = mc.filterExpand(ex=True, sm=12)
    
    for i in selection :
        mc.setAttr(i + '.aiSubdivType', 0)
    
    print('Set Subdivision to 0 on all meshes')

if __name__ == '__main__':
    Clean_RenderLayers()
    Clean_Aovs()
    Clean_LightEditor()
    Clean_Nodes()
    Clean_CustomNodes()
    Clean_Cameras()
    Clean_Tesselation()