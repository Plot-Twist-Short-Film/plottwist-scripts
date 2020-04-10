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

import logging

import maya.cmds as mc

LOGGER = logging.getLogger()


def delete_locked_nodes(nodes):
    mc.lockNode(nodes, lock=False)
    mc.delete(nodes)


def clean_render_layers():
    # Gather all Renderlayers in the scene
    render_layers_scene = mc.ls(type='renderLayer')

    # Remove defaultRenderLayer of the list
    render_layers_scene.remove('defaultRenderLayer')

    # Remove Renderlayers from a reference file
    render_layers_to_del = [i for i in render_layers_scene if not mc.referenceQuery( i, isNodeReferenced=True)]
    render_layers_nb = len(render_layers_to_del)
    if render_layers_nb:
        delete_locked_nodes(render_layers_to_del)
    LOGGER.info('Cleaned {} Render layers'.format(render_layers_nb))


def clean_aovs():
    # Gather all AOVs in the scene
    aov_scene = mc.ls(type='aiAOV')

    # Remove AOVs from a reference file
    aov_to_del = [i for i in aov_scene if not mc.referenceQuery( i, isNodeReferenced=True)]
    aov_nb = len(aov_to_del)
    if aov_nb:
        delete_locked_nodes(aov_to_del)
    LOGGER.info('Cleaned {} AOVs'.format(aov_nb))


def clean_light_editor():
    light_editor_scene = mc.ls(type='lightEditor') #Gather all LightEditor in the scene
    light_editor_to_del = [i for i in light_editor_scene if not mc.referenceQuery( i, isNodeReferenced=True)] # Remove LightEditor from a reference file
    light_editor_nb = len(light_editor_to_del)
    if light_editor_nb:
        delete_locked_nodes(light_editor_to_del)
    LOGGER.info('Cleaned {} LightEditors'.format(light_editor_nb))


def clean_nodes():
    # Gather all Intermediate Nodes in the scene
    intermediate_nodes = mc.ls(intermediateObjects=True)

    # Gather Group ID info
    group_id = [
        i for i in intermediate_nodes if mc.objectType(i, isType='groupId') or mc.objectType(i, isType='GroupParts')]

    # Gather Anim layers info
    anim_layer = [i for i in intermediate_nodes if mc.objectType(i, isType='animLayer')]

    # Gather Display layers info
    layers = [i for i in intermediate_nodes if mc.objectType(i, isType='displayLayer')]

    # Get rid of default layer. We don't want to delete it
    layers.remove('defaultLayer')

    # Gather Ai Nodes info
    ai_nodes = [
        i for i in intermediate_nodes if mc.objectType(i, isType='aiOptions') or mc.objectType(
            i, isType='aiAOVFilter') or mc.objectType(i, isType='aiAOVDriver')]

    # Gather Ref type info
    refs_file = mc.file(q=True, l=True, shn=True)

    # Check references files
    ref_namespace = [ref.replace('.ma', 'RN') for ref in refs_file if '.ma' in ref]

    # Check reference nodes type
    ref_type_nodes = [i for i in intermediate_nodes if mc.objectType(i, isType='reference')]

    # Exclude reference files from references node type
    ref_type_nodes = [i for i in ref_type_nodes if i not in ref_namespace]

    # Gather Poly nodes
    poly_nodes = [i for i in intermediate_nodes if 'kPoly' in mc.nodeType(i, apiType=True)]
    
    nodes_to_del = group_id + anim_layer + layers + ref_type_nodes + poly_nodes + ai_nodes
    nodes_nb = len(nodes_to_del)
    if nodes_nb:
        delete_locked_nodes(nodes_to_del)
    LOGGER.info('Cleaned {} Nodes'.format(nodes_nb))
    

def clean_custom_nodes():
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
            LOGGER.info('Cleaned {}'.format(i))


def clean_cameras():
    # Get all cameras first
    cameras = mc.ls(type=('camera'), l=True)

    # Filter all startup / default cameras
    startup_cameras = [
        cam for cam in cameras if mc.camera(mc.listRelatives(cam, parent=True)[0], startupCamera=True, q=True)]

    # List Non-default cameras
    non_startup_cameras_shapes = list(set(cameras) - set(startup_cameras))

    # Remove cameras from a reference file
    non_startup_cameras_shapes = [
        i for i in non_startup_cameras_shapes if not mc.referenceQuery( i, isNodeReferenced=True)]
    non_startup_cameras = [mc.listRelatives(cam, parent=True)[0] for cam in non_startup_cameras_shapes]  
    if non_startup_cameras:
        mc.delete(non_startup_cameras)
        LOGGER.info('Cleaned {} non startup camera(s)'.format(len(non_startup_cameras)))


def clean_tesselation():
    mc.listRelatives('root', ad=True)
    selection = mc.filterExpand(ex=True, sm=12)
    
    for i in selection :
        mc.setAttr(i + '.aiSubdivType', 0)
    
    LOGGER.info('Set Subdivision to 0 on all meshes')


if __name__ == '__main__':
    clean_render_layers()
    clean_aovs()
    clean_light_editor()
    clean_nodes()
    clean_custom_nodes()
    clean_cameras()
    clean_tesselation()
