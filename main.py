import os
import speech_recognition as sr
from gtts import gTTS as text_to_speech
import subprocess

webstorm_dir = "/home/mohit/WebStorm-145.972.4/bin/"
pycharm_dir = "/home/mohit/pycharm-community-2016.1.2/bin/"
idea_dir = "/home/mohit/idea-IC-145.597.3/bin/"


def speak(audio_string):
    tts = text_to_speech(text=audio_string, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")

listener = sr.Recognizer()


def evaluate(response):
    response = response.split(' ')
    modified_response = []
    for word in response:
        word = str.lower(str(word))
        modified_response.append(word)

    print modified_response

    if "javascript" in modified_response:
        subprocess.Popen([webstorm_dir + "webstorm.sh"], shell=True)
    elif "python" in modified_response:
        subprocess.Popen([pycharm_dir + "pycharm.sh"], shell=True)
    elif "java" in modified_response:
        subprocess.Popen([idea_dir + "idea.sh"], shell=True)
    elif "terminal" in modified_response:
        os.system("gnome-terminal &")
    else:
        speak("Sorry, I didn't catch that.")

while True:
    with sr.Microphone() as recorder:
        speak("Hi, How can I help you?")
        user_response = listener.listen(recorder)

    print "Processing Your Request"

    try:
        user_response_text = listener.recognize_google(user_response)
        # speak("Did you just say " + user_response_text)
        print user_response_text
        evaluate(user_response_text)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
