import os
import cv2
import speech_recognition as sr
from gtts import gTTS as text_to_speech
from skimage.measure import structural_similarity as ssim
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


def recognize_person():
    face_cascade = cv2.CascadeClassifier('face_detection_xml/face_cascade_classifier.xml')
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.imshow('img', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


def initialise_talk():
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


recognize_person()
