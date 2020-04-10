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

def ConnectMaps_UDIM(selection=False):
    
    materials = mc.ls(mat=True)
    
    if selection == False: ### APPLY TO ALL AI_STANDARDSURFACE SHADERS ### 

        shaders = [i for i in materials if mc.objectType(i) == "aiStandardSurface"  and mc.referenceQuery( i, isNodeReferenced=True) == False]     

    else : ### FROM A SELECTION OF SHADERS ###

        selection = mc.ls(sl=True)
        shaders = list(set(set(materials) & set (selection)))

    scene_name = os.path.basename(mc.file(q=True, sn=True)).split(".")[0] # Get scene_name name

    if len(shaders) == 1:
        shader = shaders[0]
    elif len(shaders) == 0:
        raise Exception ("You must select a shader")
    else:
        pass

    for shader in shaders :
        
        shading_group = shading_group = mc.rename(mc.listConnections(shader, t='shadingEngine'), shader + "SG")
        shader_name = shader_name = shader.split('_')[1]

        if mc.objExists(scene_name + "_BaseColor"): # Check input BaseColor if empty connect file node
            file_BaseColor = scene_name + "_BaseColor"
            upstream_BaseColor = mc.listConnections(shader + ".baseColor", d= False, s=True)
            if upstream_BaseColor ==  None :
                mc.connectAttr( file_BaseColor + ".outColor", shader + ".baseColor")
            else: 
                pass
        else :
            upstream_BaseColor = mc.listConnections(shader + ".baseColor", d= False, s=True)
            if upstream_BaseColor ==  None :
                file_BaseColor = mc.shadingNode("file", asTexture=True, isColorManaged=True, name= scene_name + "_BaseColor")
                mc.connectAttr( file_BaseColor + ".outColor", shader + ".baseColor")
            else: 
                pass

        if mc.objExists(scene_name + "_Height"): # Check input Height if empty connect file node
            file_Height = scene_name + "_Height"
            if not mc.objExists(scene_name + "_D_" + shader_name):
                disp_node = mc.shadingNode("displacementShader", asShader = True, name = scene_name + "_D_" + shader_name )
                mc.setAttr(disp_node + ".scale", 0)
                mc.setAttr(disp_node + '.aiDisplacementZeroValue', 0.5)
            upstream_Height = mc.listConnections(shading_group + ".displacementShader", d= False, s=True)
            if upstream_Height ==  None :
                mc.connectAttr( file_Height + ".outAlpha", disp_node + ".displacement")
                mc.connectAttr( disp_node + ".displacement", shading_group + ".displacementShader")
            else :
                pass
        else :
            upstream_Height = mc.listConnections(shading_group + ".displacementShader", d= False, s=True)
            if upstream_Height ==  None :
                file_Height = mc.shadingNode("file", asTexture=True, isColorManaged=True, name= scene_name + "_Height")
                mc.setAttr(file_Height + ".alphaIsLuminance", 1)
                disp_node = mc.shadingNode("displacementShader", asShader = True, name = scene_name + "_D_" + shader_name )
                mc.connectAttr( file_Height + ".outAlpha", disp_node + ".displacement")
                mc.connectAttr( disp_node + ".displacement", shading_group + ".displacementShader")
                mc.setAttr(disp_node + ".scale", 0)
                mc.setAttr(disp_node + '.aiDisplacementZeroValue', 0.5)
            else: 
                pass

        if mc.objExists(scene_name + "_Metalness"): # Check input Metalness if empty connect file node
            file_Metalness = scene_name + "_Metalness"
            upstream_Metalness = mc.listConnections(shader + ".metalness", d= False, s=True)
            if upstream_Metalness ==  None :
                mc.connectAttr( file_Metalness + ".outAlpha", shader + ".metalness")
            else:
                pass
        else :
            upstream_Metalness = mc.listConnections(shader + ".metalness", d= False, s=True)
            if upstream_Metalness ==  None :
                file_Metalness = mc.shadingNode("file", asTexture=True, isColorManaged=True, name= scene_name + "_Metalness")
                mc.setAttr(file_Metalness + ".alphaIsLuminance", 1)
                mc.connectAttr( file_Metalness + ".outAlpha", shader + ".metalness")
            else: 
                pass
        
        if mc.objExists(scene_name + "_Roughness"): # Check input Roughness if empty connect file node
            file_Roughness = scene_name + "_Roughness"
            upstream_Roughness = mc.listConnections(shader + ".specularRoughness", d= False, s=True)
            if upstream_Roughness ==  None :
                mc.connectAttr( file_Roughness + ".outAlpha", shader + ".specularRoughness")
            else:
                pass
        else :
            upstream_Roughness = mc.listConnections(shader + ".specularRoughness", d= False, s=True)
            if upstream_Roughness ==  None :
                file_Roughness = mc.shadingNode("file", asTexture=True, isColorManaged=True, name= scene_name + "_Roughness")
                mc.setAttr(file_Roughness + ".alphaIsLuminance", 1)
                mc.connectAttr( file_Roughness + ".outAlpha", shader + ".specularRoughness")
            else: 
                pass

        if mc.objExists(scene_name + "_Normal"): # Check input Normal if empty connect file node
            file_Normal = scene_name + "_Normal"
            if not mc.objExists(scene_name + "_aiNormal_" + shader_name):
                normal_node = core.createArnoldNode("aiNormalMap", name = scene_name + "_aiNormal_" + shader_name)
                
            upstream_Normal = mc.listConnections(shader + ".normalCamera", d= False, s=True)
            if upstream_Normal ==  None :
                mc.connectAttr( file_Normal + ".outColor", normal_node + ".input")
                mc.connectAttr( normal_node + ".outValue", shader + ".normalCamera")
            else:
                pass

        else :
            upstream_Normal = mc.listConnections(shader + ".normalCamera", d= False, s=True)
            if upstream_Normal ==  None :
                file_Normal = mc.shadingNode("file", asTexture=True, isColorManaged=True, name= scene_name + "_Normal")
                normal_node = core.createArnoldNode("aiNormalMap", name = scene_name + "_aiNormal_" + shader_name)
                mc.connectAttr( file_Normal + ".outColor", normal_node + ".input")
                mc.connectAttr( normal_node + ".outValue", shader + ".normalCamera")
            else: 
                pass

if __name__ == '__main__':
    ConnectMaps_UDIM(selection=False)