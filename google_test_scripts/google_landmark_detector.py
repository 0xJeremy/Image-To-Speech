import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="PennApps 2018-c1bab6b19fa1.json"

from google.cloud import vision

def detect_landmarks(path):
	client = vision.ImageAnnotatorClient()

	with io.open(path, 'rb') as image_file:
		content = image_file.read()

	image = vision.types.Image(content=content)

	response = client.landmark_detection(image=image)
	landmarks = response.landmark_annotations
	print('Landmarks:')

	for landmark in landmarks:
		print(landmark.description)
		for location in landmark.locations:
			lat_lng = location.lat_lng
			print('Latitude {}'.format(lat_lng.latitude))
			print('Longitude {}'.format(lat_lng.longitude))