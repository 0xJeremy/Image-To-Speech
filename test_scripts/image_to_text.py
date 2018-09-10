try:
	import Image
except ImportError:
	from PIL import Image
import pytesseract

def ocr(image):
	return pytesseract.image_to_string(Image.open(image))

def main():
	image = raw_input("What is the name of the image?\n")
	text_from_image = ocr(image)
	print(text_from_image)


if __name__=='__main__':
	main()