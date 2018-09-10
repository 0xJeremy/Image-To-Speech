import pyttsx

def speak(string, engine):
	engine.say(string)
	engine.runAndWait()

def main():
	engine = pyttsx.init()
	text = raw_input('What do you want me to say?\n')
	speak(text, engine)


if __name__=='__main__':
	main()