from googletrans import Translator

#Returns the translated text and the language
def translate(string):
	translator = Translator()
	translation = translator.translate(string)
	return translation.text, translation.src


def main():
	text = raw_input("What do you want to translate?\n")
	translation_eng, translation_lang = translate(text)
	print(translation_eng)


if __name__=='__main__':
	main()