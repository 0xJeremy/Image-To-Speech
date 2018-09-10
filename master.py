#-----------------------------------------------------------------------------
#						Import Statements
#-----------------------------------------------------------------------------
import io
import os
import pyttsx
from googletrans import Translator
import numpy as np
import cv2
import pytesseract
from pygame import mixer

from time import sleep
try:
	import Image
except ImportError:
	from PIL import Image

from google.cloud import vision
from google.cloud.vision import types
from google.cloud import vision_v1p3beta1 as vision
from google.cloud import texttospeech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="pennapps-v2-058bbf5ec640.json"

#-----------------------------------------------------------------------------
#						Google API Functions
#-----------------------------------------------------------------------------
def google_speak(string):
	client = texttospeech.TextToSpeechClient()
	synthesis_input = texttospeech.types.SynthesisInput(text=string)
	voice = texttospeech.types.VoiceSelectionParams(
    	language_code='en-US',
    	ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
	audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
	response = client.synthesize_speech(synthesis_input, voice, audio_config)
	with open('output.mp3', 'wb') as out:
		out.write(response.audio_content)
		print('Audio content written to file "output.mp3"')
	mixer.init()
	mixer.music.load('output.mp3')
	mixer.music.play()
	sleep(5)

def google_ocr(path):
	client = vision.ImageAnnotatorClient()
	with io.open(path, 'rb') as image_file:
		content = image_file.read()
	image = vision.types.Image(content=content)
	response = client.text_detection(image=image)
	texts = response.text_annotations
	print('Texts:')
	full_text = ''
	for text in texts:
		# print('\n"{}"'.format(text.description))
		full_text += text.description
		vertices = (['({},{})'.format(vertex.x, vertex.y)
					for vertex in text.bounding_poly.vertices])
		print('bounds: {}'.format(','.join(vertices)))
	return full_text

def google_vision_labels(frame):
	client = vision.ImageAnnotatorClient()
	file_name = os.path.join(os.path.dirname(__file__), frame)
	with io.open(file_name, 'rb') as image_file:
		content = image_file.read()
	image = types.Image(content=content)
	response = client.label_detection(image=image)
	labels = response.label_annotations
	return labels

def google_localize_objects(path):
	client = vision.ImageAnnotatorClient()
	with open(path, 'rb') as image_file:
		content = image_file.read()
		image = vision.types.Image(content=content)
		objects = client.object_localization(
			image=image).localized_object_annotations
		print('Number of objects found: {}'.format(len(objects)))
		for object_ in objects:
			print('\n{} (confidence: {})'.format(object_.name, object_.score))
			print('Normalized bounding polygon vertices: ')
			for vertex in object_.bounding_poly.normalized_vertices:
				print(' - ({}, {})'.format(vertex.x, vertex.y))
	return objects

def google_detect_logos(path):
	client = vision.ImageAnnotatorClient()
	with io.open(path, 'rb') as image_file:
		content = image_file.read()
	image = vision.types.Image(content=content)
	response = client.logo_detection(image=image)
	logos = response.logo_annotations
	print('Logos:')
	for logo in logos:
		print(logo.description)
	return logos

def google_detect_landmarks(path):
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
	return landmarks

#-----------------------------------------------------------------------------
#						Google Helper Functions
#-----------------------------------------------------------------------------
def read_vision_labels(labels):
	print('Labels:')
	for label in labels:
		print(label.description)
		speak(label.description)

def read_scene(image):
	labels = vision_labels(image)
	print('Labels:')
	speak("I currently see")
	for label in labels:
		speak(label.description)
		print(label.description)
	return labels

def contains_text(labels):
	for label in labels:
		if(label == text or label == word or label == words):
			return True
	return False

def parse_objects(objects):
	count = 0
	for object_ in objects:
		if(object_.score >= 0.5):
			google_speak("I see a " + object_.name + " with " + str(round(object_.score, 2)) + "\% confidence.")
			count = count +1
			if(count == 4):
				return

def read_landmarks(landmarks):
	for landmark in landmarks:
		if (landmark.description != ""):
			google_speak("I believe I see " + landmark.description)
			return

#-----------------------------------------------------------------------------
#						Legacy Functions
#-----------------------------------------------------------------------------
def speak(string):
	engine = pyttsx.init()
	rate = engine.getProperty('rate')
	engine.setProperty('rate', rate)
	voices= engine.getProperty('voices')                                                                                    
	engine.setProperty('voice', 'english-us')
	engine.say(string)
	engine.runAndWait()

def translate(string):
	translator = Translator()
	translation = translator.translate(string)
	return translation.text, translation.src

def ocr(image):
	return pytesseract.image_to_string(Image.open(image))

def read_text(image):
	text = ocr(image)
	translation, initial_lang = translate(text)
	if(initial_lang != en):
		speak('The initial language was ' + initial_lang)
	speak('The text reads')
	speak(translation)

#-----------------------------------------------------------------------------
#						Main
#-----------------------------------------------------------------------------
def main():

	while(True):
		file = raw_input("Please Enter a File Path:\n")
		# labels = google_vision_labels(file)
		# read_vision_labels(labels)
		objects = google_localize_objects(file)
		parse_objects(objects)
		landmarks = google_detect_landmarks(file)
		read_landmarks(landmarks)
		ocr = google_ocr(file)
		ocr, lang = translate(ocr)
		google_speak(ocr)


	# cap = cv2.VideoCapture(0)
	# success, frame = cap.read()
	# cv2.imwrite('vision.jpg', frame)

	# while(True):
	# 	sleep(5)
	# 	cv2.imwrite('vision.jpg', frame)
	# 	success, image = cap.read()
	# 	print("New frame read and stored.")
	# 	labels = read_scene('vision.jpg')
	# 	if(contains_text(labels)):
	# 		read_text('vision.jpg')

	# read_scene('testocr.png')
	# read = raw_input("What do you want me to say?\n")
	# google_speak(read)
	# objects = localize_objects('download.jpeg')
	# parse_objects(objects)

if __name__=='__main__':
	main()