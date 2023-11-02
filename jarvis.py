import speech_recognition as aa
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import requests
import math
from chatgpt import Conversation
import os


chatGptKey = "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"
listener = aa.Recognizer()
listener.energy_threshold = 400
machine = pyttsx3.init()
conversation = Conversation()

machine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enUS_MarkM')


def getWeather(cityName):
    weatherKey = "21c78f2c0aa41e9218d13c43522d8ad5"
    url = f'http://api.openweathermap.org/data/2.5/weather?q={cityName},{"CO"},{"+1"}&appid={weatherKey}&units=imperial'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        #temp = ((temp-273.15) * (9/5) + 32)
        #temp = math.trunc(temp)
        temp = str(temp)
        talk(f'The temperature is ' + temp + 'degrees Farenheit. and it is ' + desc + '.')

    else:
        print('Error fetching weather data')
    

def write():
    talk("What is the name of the note?")
    noteName = input_instruction()
    noteName = noteName.replace(" ", "")
    talk("I got " + noteName + " is this correct?")
    confirmation = input_instruction()
    if "yes" in confirmation:
        talk("What would you like the note to say?")
        noteContent = input_instruction()
    else:
        return
    file1 = open("C:\\Users\\Carter\\JarvisNotes\\" + noteName + ".txt", "w")
    file1.writelines(noteContent)
    file1.close()

def talk(text):
    machine.say(text)

    machine.runAndWait()

def input_instruction():
    global instruction
    try:
        with aa.Microphone() as origin:
            print("listening...")
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
                
            print(instruction)



    except:
        pass
    return instruction

def play_Jarvis():

    instruction = input_instruction()
    print(instruction)
    if "play" in instruction:
        song = instruction.replace('play', "")
        talk("playing" + song)
        pywhatkit.playonyt(song)
    elif "time" in instruction:
        time = datetime.datetime.now().strftime("%I:%M%p")
        talk("Current Time" + time)

    elif "date" in instruction:
        date = datetime.datetime.now().strftime("%d/%m/%Y")
        talk ("Today's date is " + date)

    elif "how are you" in instruction:
        talk("I am fine, how are you")
    elif "what is your name" in instruction:
        talk ("My name is Jarvis")
    elif "who is" in instruction:
        human = instruction.replace("who is", " ")
        info = wikipedia.summary(human, 1)
        print (info)
        talk(info)
    elif "i need you to write a note" in instruction:
        write()
    elif "weather" in instruction:
        talk("Where are you located?")
        location = input_instruction()
        getWeather(location)
    elif "shut down" in instruction:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    else:
        talk("I'm sorry I didn't get that")
while True:
    instruction = input_instruction()
    if "jarvis" in instruction:
        play_Jarvis()
    elif instruction == "stop":
        break
    else:
        True