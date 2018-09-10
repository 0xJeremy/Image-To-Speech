import io
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="PennApps 2018-c1bab6b19fa1.json"

from google.cloud import vision

def detect_logos(path):
	client = vision.ImageAnnotatorClient()

	with io.open(path, 'rb') as image_file:
		content = image_file.read()

	image = vision.types.Image(content=content)

	response = client.logo_detection(image=image)
	logos = response.logo_annotations
	print('Logos:')
	for logo in logos:
		print(logo.description)