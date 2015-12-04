from printClient import *

print('--------------------------------------------------------------------------------')
print('uploadFile:')
file_id = uploadFile('./box.stl')
print ("file_id = " + file_id)

print('--------------------------------------------------------------------------------')
print('importMesh:')
uuid = importMesh(file_id)
print('uuid = ' + uuid)

print('--------------------------------------------------------------------------------')
print('importMeshResponse:')
uuid = importMeshResponse(uuid)
print('uuid = ' + uuid)

print('--------------------------------------------------------------------------------')
print('transformMesh:')
uuid = transformMesh(uuid,  [[1,0,0,-9], [0,1,0,-9], [0,0,1,0] ])
print('uuid = ' + uuid)
mesh_id = uuid

print('--------------------------------------------------------------------------------')
print('Analyze and Repair Mesh:')
uuid = analyzeMesh(mesh_id)
if uuid == '':
	print('analyze mesh finished with no problem, do not need repair')
elif uuid != 'timeout':
	uuid = reqairMesh(uuid)

print('--------------------------------------------------------------------------------')
print('createTray:')
print('uuid : '+uuid)
printer_id = '4A0F7523-071B-4F1E-A527-9DA49AECB807'
profile_id = 'EF6D5047-0D09-4F6A-AC06-9EF09638D2C9'
uuid = createTray(printer_id=printer_id, profile_id=profile_id, mesh_ids=[mesh_id])

print('--------------------------------------------------------------------------------')
print('createTrayResponse:')
uuid = createTrayResponse(uuid)
print('uuid : '+uuid)
tray_id = uuid

print('--------------------------------------------------------------------------------')
print('prepareTray:')
uuid = prepareTray(tray_id)
print('uuid : '+uuid)

print('--------------------------------------------------------------------------------')
print('prepareTrayResponse:')
uuid = prepareTrayResponse(uuid)
print('uuid : '+uuid)

print('--------------------------------------------------------------------------------')
print('generateGcode:')
uuid = generateGcode(uuid)
print('uuid : '+uuid)
 
print('--------------------------------------------------------------------------------')
print('generateGcodeResponse:')
uuid = generateGcodeResponse(uuid)
print('uuid : '+uuid)

print('--------------------------------------------------------------------------------')
print('downloadGcode:')
downloadGcode(uuid, "./box.gcode")
 

