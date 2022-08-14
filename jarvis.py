'''Author: Muhammad Muneeb Ul Haq
Date started: 29 March 2022
Date completed: 26 april 2022'''

import pyttsx3#python text to speech library
import datetime
import speech_recognition as sr
import pyaudio
import wikipedia
import webbrowser
import os
import random
import smtplib

class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict()
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value

def write_to_file(filename, text):#takes name of file and write some text into it in a new line
    filename = str(filename+".txt")
    with open(filename, "a") as filename:
        filename.write(text )
        filename.write("\n")

def read_file(filename):#returns list of all lines of a file
    filename = str(filename)
    with open(filename, "r") as filename:
        file_content = filename.read()
        list_of_content = file_content.split("\n")
    return list_of_content

engine = pyttsx3.init('sapi5')
#from the engine initiated from sapi5 the voices property is got
voices = engine.getProperty('voices')
#the property voice of pyttsx3 is set to the voice at index 0 in voices
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)#to set rate of speaking
#engine.setProperty('volume', 1)#to set volume 

def speak(audio):
    engine.say(audio)  
    # to make the audio said by engine audible
    engine.runAndWait()

def publish(str):
    print(str)
    speak(str)

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak('good morning')
    elif hour >= 12 and hour <= 15:
        speak('good afternoon')
    elif hour > 15 and hour < 19:
        speak('good evening')
    elif hour >= 19 :
        speak('good night') 

    speak('salaam I am jarvis how may i help you ')

def takecommand():
    r = sr.Recognizer()    
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1 
        #waits for one second before a sentence is considered complete
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-Pk")
        print(f"User said: {query}")
    except Exception as e:
        print("Please speak again")
        query = ''
    return query

def send_email(reciever, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    with open('my_email.txt', 'r') as mail:
        my_email = mail.read()
    with open('password.txt', 'r') as passcode:
        password = decrypt(passcode.read())
    server.login(my_email, password)
    server.sendmail(my_email, reciever, content)
    server.close()

def encrypt(text):
    encrypted = map(lambda c: chr(ord(c) + 2), text)
    return ''.join(encrypted)

def decrypt(text):
    decrypted = map(lambda c: chr(ord(c) - 2), text)
    return ''.join(decrypted)


if __name__ == "__main__":
    wishme()
    while True:
        query = takecommand().lower()
        #query = str(input("Please give command:\n")).lower()
        if 'wikipedia' in query:
            #replacing the word wikipedia in query to easily search for requirements
            query = query.replace('wikipedia', '')
            #returns two sectences to the variable results
            results = wikipedia.summary(query, sentences=2)
            publish('According to wikipedia')
            speak(results)
        elif 'open youtube' in query:
            publish("Opening YouTube")
            webbrowser.open('https:\\youtube.com')
        elif 'open google' in query:
            publish('Opening google') 
            webbrowser.open('https:\\google.com')
        elif 'the time' in query:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            publish(f'The time is {time}')
        elif 'the date' in query:
            datetoday = datetime.date.today()
            publish(str(datetoday))
        elif 'listen quran' in query:
            quran_dir = 'D:\\Quran'
            #converting the files in the directory 'Quran' 
            tilawat = os.listdir(quran_dir)
            #randomly generate a number from the indices of the list 
            index = random.randint(0, int(len(tilawat))-1)
            publish('Now listen carefully to the quran')
            #joins the file at the generated index with the directory
            os.startfile(os.path.join(quran_dir, tilawat[index]))
        elif 'register email' in query:
            publish('Please enter your email:')
            email = str(input())
            with open('my_email.txt', 'w') as mail:
                mail.write(email)
            publish('Please enter your password:')
            password = str(input())
            with open('password.txt', 'w') as passcode:
                passcode.write(encrypt(password))
        elif 'send email' in query:
            try:
                publish('Who do you want to send email to:')
                reciever = str(input())
                publish('Would you like to speak your mail or type it:')
                option = str(input()).lower()
                if option == 'speak':
                    content = takecommand()
                else:
                    content = str(input('Type your message here:\n'))
                send_email(reciever, content)
            except Exception as e:
                print(e)  
        elif 'add something new' in query:
            publish("What do you want to add:\n 1. A website\n 2. A file\n 3. A folder")
            #to_do = str(input().lower())
            to_do = takecommand().lower() 
            if 'website' in to_do:
                speak('Enter name of website with the type of domain')
                website = str(input('Enter name of website with the type of domain:\n'))
                publish(f'Adding {website} to placeable orders') 
                write_to_file("my_websites", website)
                write_to_file('url_of_my_websites', f'https:\\{website}')
                publish('Successfully added')
                publish(f"Now opening {website}")
                webbrowser.open(f'https:\\{website}')
            elif 'file' in to_do:
                speak('Enter exact name of file with type')
                name_of_file = str(input('Enter exact name of file with type:\n'))
                speak('Enter name of file with which you want to call it for later use ')
                nick_name_of_file = str(input('Enter name of file with which you want to call it for later use(use lower case letters) :\n'))
                write_to_file('my_files', nick_name_of_file)
                speak('Enter path of file')
                path = input('Enter path of file:\n')
                file = os.path.join(path, name_of_file)
                publish(f'Adding {file}')
                write_to_file('path_of_my_files', file)
                publish('Successfully added')
                publish(f'Now opening {name_of_file}')
                os.startfile(file)
                
            elif 'folder' in to_do:
                speak('Enter name of folder')
                name_of_folder = str(input('Enter name of folder\n')).lower()
                write_to_file('my_folders', name_of_folder)
                speak('Enter path of folder')
                folder = input('Enter path of folder :\n')
                publish(f'Adding {name_of_folder} ') 
                write_to_file('path_of_my_folders',folder)
                publish('Successfully added')
                publish(f'Now opening {name_of_folder}')
                os.startfile(folder)
        elif 'quit' in query:
            exit()
        elif query == '':
            pass
        else:
            #splitting query to make it iterable in accordance with the words
            query_list = query.split(' ')
            task_done = True
            for word in query_list:
                if task_done:
                    websites = read_file('my_websites.txt')
                    url_my_websites = read_file('url_of_my_websites.txt')
                    for website in websites:    
                        if word == website:
                            publish(f'Opening {website}') 
                            webbrowser.open(url_my_websites[websites.index(website)])#finds the index of the website in list of my_websites and then gets and opens the url at that index in list of urls
                            task_done = False
                            break
                if task_done:        
                    folders = read_file('my_folders.txt')
                    path_of_folders = read_file('path_of_my_folders.txt')
                    for folder in folders:
                        if query == folder:
                            publish(f'Opening {folder}')
                            os.startfile(path_of_folders[folders.index(folder)])
                            task_done = False
                            break
                if task_done:
                    files = read_file('my_files.txt')
                    path_of_files = read_file('path_of_my_files.txt')            
                    for file in files:
                        if  query == file:
                            publish(f'Opening {file}')
                            os.startfile(path_of_files[files.index(file)])
                            task_done = False
                            break
                if not task_done:
                    break
            else:
                publish("Please assign me a task I can perform")
            