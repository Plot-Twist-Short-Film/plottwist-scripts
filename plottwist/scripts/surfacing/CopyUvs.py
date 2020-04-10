import maya.cmds as mc

#Copy Uvs Component Mode for Multiple Meshes

#grab all the selected objects

selectedObjects = mc.ls(sl=True)

#save first one into variable

#pop first one out of the selected objects list

driver = selectedObjects.pop(0)

#for each object in the selected objects list

for object in selectedObjects:

    mc.select([driver,object])

    #transfer attributes

    mc.transferAttributes(sampleSpace=4,transferUVs=2, transferColors=0 )