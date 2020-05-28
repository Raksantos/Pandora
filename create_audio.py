#!/usr/bin/env python3

from gtts import gTTS
from subprocess import call #Mac e Linux
from playsound import playsound #Windows

def make_audio(audio, file_name):
    tts = gTTS(audio, lang='pt-br')
    tts.save('audios/{}.mp3'.format(file_name))

    call(['mpg123', 'audios/{}.mp3'.format(file_name)]) #Linux
    #call(['afplay', 'audios/hello.mp3']) #OSX
    #playsound('audios/hello.mp3') #Windows

if __name__ == "__main__":
    make_audio('Eu não sou paga pra isso!', 'refuse_master')
