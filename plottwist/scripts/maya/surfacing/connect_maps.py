#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create needed nodes to setup Plot Twist shaders
"""

from __future__ import print_function, division, absolute_import

__author__ = "Titouan Perrot"
__license__ = "MIT"
__maintainer__ = "Titouan Perrot"
__email__ = ""


import maya.cmds as mc
import os
import mtoa.core as core


def connect_maps(selection=False):
    
    materials = mc.ls(mat=True)

    # Apply to all AI_StandardSurface shaders
    if not selection:
        shaders = [
            i for i in materials if mc.objectType(i) == 'aiStandardSurface' and mc.referenceQuery(
                i, isNodeReferenced=True) == False]

    # From a selection of shaders
    else:
        selection = mc.ls(sl=True)
        shaders = list(set(set(materials) & set(selection)))

    # Get scene_name name
    scene_name = os.path.basename(mc.file(q=True, sn=True)).split('.')[0]

    if len(shaders) == 1:
        shader = shaders[0]
    elif len(shaders) == 0:
        raise Exception('You must select a shader')
    else:
        pass

    for shader in shaders:
        shading_group = mc.rename(mc.listConnections(shader, t='shadingEngine'), shader + 'SG')
        shader_name = shader_name = shader.split('_')[1]

        # Check input BaseColor if empty connect file node
        if mc.objExists(scene_name + '_' + shader_name + '_BaseColor'):
            file_base_color = scene_name + '_' + shader_name + '_BaseColor'
            upstream_base_color = mc.listConnections(shader + '.baseColor', d=False, s=True)
            if upstream_base_color is None:
                mc.connectAttr(file_base_color + '.outColor', shader + '.baseColor')
            else: 
                pass
        else:
            upstream_base_color = mc.listConnections(shader + '.baseColor', d=False, s=True)
            if upstream_base_color ==  None :
                file_base_color = mc.shadingNode(
                    'file', asTexture=True, isColorManaged=True, name= scene_name + '_' + shader_name + '_BaseColor')
                mc.connectAttr(file_base_color + '.outColor', shader + '.baseColor')
            else: 
                pass

        # Check input Height if empty connect file node
        if mc.objExists(scene_name + '_' + shader_name + '_Height'):
            file_height = scene_name + '_' + shader_name + '_Height'
            if not mc.objExists(scene_name + '_D_' + shader_name):
                disp_node = mc.shadingNode(
                    'displacementShader', asShader=True, name=scene_name + '_D_' + shader_name)
                mc.setAttr(disp_node + '.scale', 0)
                mc.setAttr(disp_node + '.aiDisplacementZeroValue', 0.5)
            upstream_height = mc.listConnections(shading_group + '.displacementShader', d=False, s=True)
            if upstream_height is None :
                mc.connectAttr( file_height + '.outAlpha', disp_node + '.displacement')
                mc.connectAttr( disp_node + '.displacement', shading_group + '.displacementShader')
            else:
                pass
        else:
            upstream_height = mc.listConnections(shading_group + '.displacementShader', d=False, s=True)
            if upstream_height is None:
                file_height = mc.shadingNode(
                    'file', asTexture=True, isColorManaged=True, name=scene_name + '_' + shader_name + '_Height')
                mc.setAttr(file_height + '.alphaIsLuminance', 1)
                disp_node = mc.shadingNode(
                    'displacementShader', asShader=True, name=scene_name + '_D_' + shader_name)
                mc.connectAttr(file_height + '.outAlpha', disp_node + '.displacement')
                mc.connectAttr(disp_node + '.displacement', shading_group + '.displacementShader')
                mc.setAttr(disp_node + '.scale', 0)
                mc.setAttr(disp_node + '.aiDisplacementZeroValue', 0.5)
            else: 
                pass

        # Check input Metalness if empty connect file node
        if mc.objExists(scene_name + '_' + shader_name + '_Metalness'):
            file_metalness = scene_name + '_' + shader_name + '_Metalness'
            upstream_metalness = mc.listConnections(shader + '.metalness', d=False, s=True)
            if upstream_metalness is None:
                mc.connectAttr(file_metalness + '.outAlpha', shader + '.metalness')
            else:
                pass
        else:
            upstream_metalness = mc.listConnections(shader + '.metalness', d=False, s=True)
            if upstream_metalness is None:
                file_metalness = mc.shadingNode(
                    'file', asTexture=True, isColorManaged=True, name=scene_name + '_' + shader_name + '_Metalness')
                mc.setAttr(file_metalness + '.alphaIsLuminance', 1)
                mc.connectAttr(file_metalness + '.outAlpha', shader + '.metalness')
            else: 
                pass

        # Check input Roughness if empty connect file node
        if mc.objExists(scene_name + '_' + shader_name + '_Roughness'):
            file_roughness = scene_name + '_' + shader_name + '_Roughness'
            upstream_roughness = mc.listConnections(shader + '.specularRoughness', d=False, s=True)
            if upstream_roughness is None:
                mc.connectAttr(file_roughness + '.outAlpha', shader + '.specularRoughness')
            else:
                pass
        else:
            upstream_roughness = mc.listConnections(shader + '.specularRoughness', d=False, s=True)
            if upstream_roughness is None:
                file_roughness = mc.shadingNode(
                    'file', asTexture=True, isColorManaged=True, name=scene_name + '_' + shader_name + '_Roughness')
                mc.setAttr(file_roughness + '.alphaIsLuminance', 1)
                mc.connectAttr(file_roughness + '.outAlpha', shader + '.specularRoughness')
            else: 
                pass

        # Check input Normal if empty connect file node
        if mc.objExists(scene_name + '_' + shader_name + '_Normal'):
            file_normal = scene_name + '_' + shader_name + '_Normal'
            if not mc.objExists(scene_name + '_aiNormal_' + shader_name):
                normal_node = core.createArnoldNode('aiNormalMap', name=scene_name + '_aiNormal_' + shader_name)
                
            upstream_normal = mc.listConnections(shader + '.normalCamera', d=False, s=True)
            if upstream_normal is None :
                mc.connectAttr( file_normal + '.outColor', normal_node + '.input')
                mc.connectAttr( normal_node + '.outValue', shader + '.normalCamera')
            else:
                pass

        else:
            upstream_normal = mc.listConnections(shader + '.normalCamera', d=False, s=True)
            if upstream_normal ==  None :
                file_normal = mc.shadingNode(
                    'file', asTexture=True, isColorManaged=True, name=scene_name + '_' + shader_name + '_Normal')
                normal_node = core.createArnoldNode('aiNormalMap', name=scene_name + '_aiNormal_' + shader_name)
                mc.connectAttr( file_normal + '.outColor', normal_node + '.input')
                mc.connectAttr( normal_node + '.outValue', shader + '.normalCamera')
            else: 
                pass


if __name__ == '__main__':    
    connect_maps(selection=False)
