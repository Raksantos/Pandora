#!/usr/bin/env python3

from gtts import gTTS
import speech_recognition as sr
from subprocess import call #Mac e Linux
import requests
from bs4 import BeautifulSoup
import webbrowser as browser
import json

##### CONFIGURATION #####
hotword = 'pandora'
base_url_weather = "http://api.openweathermap.org/data/2.5/weather?id=6320645&appid="
url_google = 'https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419'

with open('weather-key.txt') as weather_api_key:
    weather_api_key = weather_api_key.read()
    
with open('pandora-278522-516d86bce88c.json') as credential_google:
    credential_google = credential_google.read()


##### FUNCTIONS #####
def make_audio(audio, file_name):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/{}.mp3'.format(file_name))

    call(['mpg123', 'audios/{}.mp3'.format(file_name)]) #Linux
    #call(['afplay', 'audios/hello.mp3']) #OSX
    #playsound('audios/hello.mp3') #Windows

def watch_microphone():

    microphone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print('Waiting for orders!')
            audio = microphone.listen(source)

            try:
                trigger = microphone.recognize_google_cloud(audio, credentials_json=credential_google, language='pt-BR')
                trigger = trigger.lower()
                
                if hotword in trigger:
                    print('Comando: ', trigger)
                    
                    speak('feedback')
                    execute_commands(trigger)
                    
                    break
                
            except sr.UnknownValueError:
                print("Google Cloud Speech could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))

    return trigger

def speak(file_name):
    call(['mpg123', 'audios/{}.mp3'.format(file_name)]) #Linux
    #call(['afplay', 'audios/hello.mp3']) #OSX
    #playsound('audios/hello.mp3') #Windows

def execute_commands(trigger):
    if 'notícias' in trigger:
        last_news()    
    
    elif 'me ame' in trigger:
        speak('refuse_master')
    
    elif 'rap' in trigger:
        playlists('nigga_music')
    
    elif 'rock' in trigger:
        playlists('rock')
    
    elif 'transar' in trigger:
        playlists('sexy')
    
    elif 'brega funk' in trigger:
        playlists('brega_funk')
    
    elif 'tempo agora' in trigger:
        weather(tempo=True)
        
    elif 'temperatura hoje' in trigger: 
        weather(minmax=True)
        
    else:
        print(trigger)
        speak('erro')

###### CONTROL FUNCTIONS ######
        
def last_news():
    response = requests.get(url_google)
    
    if response.status_code == 200:
        
        news = BeautifulSoup(response.text, 'html.parser')

        count = 1

        list_news = [item.title.text for item in news.findAll('item')]
        
        for item in news.findAll('item')[:10]:
            message = item.title.text
            
            make_audio(message, 'noticia' + str(count))
            
            count += 1
            
        print(list_news)
        
    elif response.status_code == 400:
        print('Not found!')
    else: 
        print('An error has ocurred')
        
        
def playlists(playlist):
    
    if playlist == 'nigga_music':
        browser.open('https://open.spotify.com/playlist/1HkArASaY1CHBwM470lBAD?si=hq7eXdZASCaFBIMDX8HoFg')
    
    elif playlist == 'rock':
        browser.open('https://open.spotify.com/playlist/0OKGBSaPY8vYglqnCZrD6v?si=c1vJx_w0T4OeCx56dMaBRA')
    
    elif playlist == 'sexy':
        browser.open('https://open.spotify.com/playlist/0sgd48H6T2TdKiRGItfAc5')
        
    elif playlist == 'brega_funk':
        browser.open('https://open.spotify.com/playlist/0RMYzdGCJMeCl0KYYdyTx2?si=xmtb--K3RhiWgqW9xDx69A')


def weather(tempo=False, minmax=False):
    response = requests.get(base_url_weather + weather_api_key + '&units=metric&lang=pt')
    
    weather_status = response.json()
    
    #print(json.dumps(weather_status, indent=4))
    
    temperature = weather_status['main']['temp']
    
    min = weather_status['main']['temp_min']
    max = weather_status['main']['temp_max']

    about = weather_status['weather'][0]['description']
    
    if tempo:
        message = f'No momento fazem {temperature} graus com: {about} '
    
    if minmax:
        message = f'Mínima de {min} e máxima de {max}'
    
    make_audio(message, 'weather')
    
def main():
    
    speak('saudacao')
    
    while True:
        
        watch_microphone()
    
    
######################################################    

main()