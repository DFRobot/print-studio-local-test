import requests
import json
from time import sleep

port = 9997

debugJson = True

host = 'http://localhost:' + str(port)

# nice print response json data
def resJsonPrint(r):
	if debugJson:
		print ("body: " + json.dumps(r.json (), indent = 4))
	else:
		print()
	
########################################### ###########################################

def getTasksProgress(uuid):
	url = host+'/print/tasks/' + uuid
	r = requests.get(url)
	if 'progress' in r.json():
		progress = r.json()['progress']
		print('progress : ' + str(progress))
		return progress 
	else:
		print ("can't get progress")
		return -1

########################################### ###########################################

def printTasksProgress(uuid, delay, tryTime):
	for i in range(tryTime):
		progress = getTasksProgress(uuid)
		if progress == 1:
			break
		else:
			sleep(delay)

########################################### ###########################################
# post with files 

def uploadFile(fileName):
	url = host+'/files/upload'
	files = {'file':open (fileName, 'rb')}
	r = requests.post (url, files = files)
	print ("status code : " + str(r.status_code))
	# print ("headers : " + str(r.headers))
	# print ("text : " + str(r.text))
	resJsonPrint(r)
	file_id = r.json ()['files'][0]['file_id']
	return file_id

########################################### ###########################################

def importMesh (file_id):
	url = host+'/geom/meshes/import'
	args = {'file_id':file_id, 'name':'hello'}
	print ('args = ' + str(args))
	r = requests.post(url, data = args)
	print ("status code : " + str(r.status_code))
	resJsonPrint(r)
	uuid = r.json ()['id']
	return uuid

########################################### ###########################################


def importMeshResponse(uuid):
	printTasksProgress(uuid, 1, 60)
	return getTasksResult(uuid, 'id')

########################################### ###########################################

def transformMesh(uuid, form):
	url = host+'/geom/meshes/transform'
	args = {'id': uuid, 'transform': form }
	print('args : ' + str(args))
	headers = {'content-type': 'application/json'}
	r = requests.post(url, data = json.dumps(args), headers = headers)
	resJsonPrint(r)
	uuid = r.json()['id']
	return uuid

########################################### ###########################################

def analyzeMesh(uuid):
	url = host+'/geom/meshes/analyze'
	args = {'id': uuid }
	print ('args = ' + str(args))
	r = requests.post(url, data = args)
	# print ("status code : " + str(r.status_code))
	if 'progress' in r.json():
		print('progress : ' + str(r.json()['progress']))

	tryTime = 1
	# while r.json()['status'] != 'done':
	while 'progress' in r.json():
		sleep(1)   # sleep 1s and try again
		r = requests.post(url, data = args)
		#print ("status code : " + str(r.status_code))
		if 'progress' in r.json():
			print('progress : ' + str(r.json()['progress']))
		tryTime += 1
		if tryTime > 60:        # timeout process
			print('timeout')
			uuid = 'timeout'
			break
	resJsonPrint(r)
	if (len(r.json()['problems']) == 0):
		uuid = ''
	else:
		uuid = str(r.json ()['result']['id'])
	return uuid


########################################### ###########################################

def reqairMesh(uuid):
	url = host+'/geom/meshes/repair'
	args = {'id': uuid, 'all': True}
	print ('args = ' + str(args))
	r = requests.post(url, params = args)
	# print ("status code : " + str(r.status_code))
	tryTime = 1
	# while r.json()['status'] != 'done':
	while 'progress' in r.json():
		sleep(1)   # sleep 1s and try again
		r = requests.post(url, data = args)
		#print ("status code : " + str(r.status_code))
		if 'progress' in r.json():
			print('progress : ' + str(r.json()['progress']))
		tryTime += 1
		if tryTime > 60:        # timeout process
			print('timeout')
			uuid = 'timeout'
			break
	resJsonPrint(r)
	if (len(r.json()['problems']) == 0):
		uuid = ''
	else:
		uuid = str(r.json ()['result']['id'])
	return uuid

########################################### ###########################################

def createTray(printer_id, profile_id, mesh_ids):
	url = host+'/print/trays'
	args = {
			#"printer_type_id": "4A0F7523-071B-4F1E-A527-9DA49AECB807", 
			"printer_type_id": printer_id, 
			#"profile_id": "EF6D5047-0D09-4F6A-AC06-9EF09638D2C9",
			"profile_id": profile_id,
			"mesh_ids": mesh_ids
			}
	headers = {'content-type': 'application/json'}
	print ('args = ' + str(args))
	r = requests.post(url, data = json.dumps(args), headers = headers)
	uuid = r.json()['id']
	return uuid

########################################### ###########################################

def createTrayResponse(uuid):
	printTasksProgress(uuid, 1, 60)
	return getTasksResult(uuid, 'id')

########################################### ###########################################

def prepareTray(uuid):
	url = host+'/print/trays/prepare'
	args = {'id': uuid, 'generate_visual': True}
	headers = {'content-type': 'application/json'}
	print ('args = ' + str(args))
	r = requests.post(url, data = json.dumps(args), headers = headers)
	print('post id')
	resJsonPrint(r)

###########################################
	uuid = r.json()['id']
	return uuid


########################################### ###########################################
def prepareTrayProgress(uuid):
	url = host+'/print/tasks/' + uuid
	r = requests.get(url)
	if 'progress' in r.json():
		progress = r.json()['progress']
		print('progress : %s' %progress)
		return progress
	else:
		return 0
########################################### ###########################################
def prepareTrayResponse (uuid):
	printTasksProgress(uuid, 1, 60*10)
	return getTasksResult(uuid, 'id')

########################################### ###########################################
# generate Gcode file

def generateGcode(uuid):
	url = host+'/print/trays/generate-printable'
	args = {'id': uuid, 'generate_raw': True}
	# args = {'id': uuid}
	print ('args = ' + str(args))
	r = requests.post(url, data = args)
	print ("status code : " + str(r.status_code))
	resJsonPrint(r)
	uuid = r.json()['id']
	return uuid


########################################### ###########################################
def generateGcodeProgress(uuid):
	return getTasksProgress(uuid)

		


########################################### ###########################################
def getTasksResult(uuid, target):
	url = host+'/print/tasks/' + uuid
	r = requests.get(url)
	resJsonPrint(r)
	if 'result' in r.json() and target in r.json()['result']:
		return r.json()['result'][target]

########################################### ###########################################

def generateGcodeResponse(uuid):
	printTasksProgress(uuid, 1, 60*10)
	return getTasksResult(uuid, 'file_id')

########################################### ###########################################

def downloadGcode(file_id, path):
	url = host+'/files/' + file_id
	r = requests.get(url) 
	print('url : ' + r.url)
	# print('text : ' + r.text)
	if r.status_code == 200:
		# download_url= r.json()['download_url']
		print('path : ' + path)
		gcode = r.text
		# print (gcode)
		with open(path, 'w') as f:
			f.write(str(gcode))
			print('file write sucess' + ' "' + path + '"')

######################################### end ##########################################
def getGcode(file_id):
	url = host+'/files/' + file_id
	r = requests.get(url) 
	print('url : ' + r.url)
	if r.status_code == 200:
		gcode = r.text
		return gcode
	else:
		return 'can\'t get gcode'

######################################### end ##########################################
