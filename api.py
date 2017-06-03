def set():
	global key
	with open('api.txt', 'r') as myfile:
		data = myfile.read()
		key = data