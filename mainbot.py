import cv2,time,os,random,shutil
import numpy as np
import dlib
# imports
import matplotlib.pyplot as plt
import numpy as np
import wave, sys
from playsound import playsound
import threading as T
import soundfile 
from google.cloud import texttospeech
from google.cloud import storage
import bot
import speech_recognition as sr
import pyaudio

def speak():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source2:
            print("listing")
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)
             
            #listens for the user's input
            audio2 = r.listen(source2)
            print("recognizing")
            # Using google to recognize audio
            text = r.recognize_google(audio2,timeout=100)
    except:
        text = ''

    return text

def facemove():

    try:
        text = '''Hello! How are you'''
        gender = "male"
        imganame = "face.jpg"

        def play(f):
            playsound(f)
        # shows the sound waves

        def visualize(path: str):

            # reading the audio file
            raw = wave.open(path)
            signal = raw.readframes(-1)
            signal = np.frombuffer(signal, dtype ="int16")
            f_rate = raw.getframerate()
            time = np.linspace(
                0, # start
                len(signal) / f_rate,
                num = len(signal)
            )
          
            t2 = [time[0]]
          
            for i in time:
            
                if i-t2[-1]>0.070:
                    t2.append(i)
            ns = []
            for i in t2:
                ns.append(signal[list(time).index(i)]/250)
            return ns

        if not os.path.exists('./cache'):
                os.makedirs('cache')

        for t in text.split('.'):

            rn = str(random.randint(1000000,9999999))+"jkadbchjb" 
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './api/tts.json'  
            # Instantiates a client
            client = texttospeech.TextToSpeechClient()
            # Set the text input to be synthesized
            synthesis_input = texttospeech.SynthesisInput(text=t)
          
            if gender=='male':
                    voice = texttospeech.VoiceSelectionParams(
                        language_code='en-in', ssml_gender=texttospeech.SsmlVoiceGender.MALE )
            elif gender=='female':
                voice = texttospeech.VoiceSelectionParams( language_code='en-in', ssml_gender=texttospeech.SsmlVoiceGender.FEMALE )     
            
            else:      
                voice = texttospeech.VoiceSelectionParams(
                        language_code='en-in', ssml_gender=texttospeech.SsmlVoiceGender.MALE )

            # Select the type of audio file you want returned
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16
            )
            # Perform the text-to-speech request on the text input with the selected
            # voice parameters and audio file type
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config)
            # The response's audio_content is binary.
            with open(f'./cache/{rn}.wav', "wb") as out:
                out.write(response.audio_content)


            # Load the detector
            detector = dlib.get_frontal_face_detector()

            # Load the predictor
            predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

            # read the image
            img = cv2.imread(imganame)

            # Convert image into grayscale
            gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)

            # Use detector to find landmarks
            faces = detector(gray)
            for face in faces:
                x1 = face.left() # left point
                y1 = face.top() # top point
                x2 = face.right() # right point
                y2 = face.bottom() # bottom point

                # Create landmark object
                landmarks = predictor(image=gray, box=face)

                # Loop through all the points
                p = []
                for n in range(0, 68):
                        
                        
                        x = landmarks.part(n).x
                        y = landmarks.part(n).y

                        if n==4 or n==10 or n==64 or n==48:
                            p.append([x,y])
                          
                lip = img[p[2][1]:p[1][1],p[2][0]:p[1][0]]
                lip = lip.copy()

                lt = visualize(f'./cache/{rn}.wav')
                x = T.Thread(target=play,args=(f'./cache/{rn}.wav',))
                x.start()
                i = 0
                for n in lt:
                    if n<0:
                        n = lt[lt.index(n)]-n
                        if n<0:
                            n*=-1
                    n=int(n)

                    img = cv2.imread(imganame)

                    img = cv2.rectangle(img,[p[2][0],p[2][1]-1],[p[1][0],p[1][1]-1],(0, 0, 0),thickness=-1)
              
                    img[p[2][1]+n:p[1][1]+n,p[2][0]:p[1][0]] = lip
                # show the image
                    cv2.imshow(winname="Screen Curb", mat=img)
                    
                    time.sleep(0.05)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break


        # Close all windows
        try:
            shutil.rmtree('./cache')
        except:
            pass
        cv2.destroyAllWindows()
    except Exception as e:
        try:
            shutil.rmtree('./cache')
        except:
            pass
        try:
            cv2.destroyAllWindows()
        except:
            pass
        return

flag = False

def botmain():
    global flag
    if flag==False:
        facemove()
        flag=True
        while True:
            text = speak()
            print(text)
            if text=='':
                speak()
            text = bot.chat(text)
            gender = "male"
            imganame = "face.jpg"
            try:
                def play(f):
                    playsound(f)
                # shows the sound waves

                def visualize(path: str):

                    # reading the audio file
                    raw = wave.open(path)
                    signal = raw.readframes(-1)
                    signal = np.frombuffer(signal, dtype ="int16")
                    f_rate = raw.getframerate()
                    time = np.linspace(
                        0, # start
                        len(signal) / f_rate,
                        num = len(signal)
                    )
                
                    t2 = [time[0]]
          
                    for i in time:
                    
                        if i-t2[-1]>0.070:
                            t2.append(i)
                    ns = []
                    for i in t2:
                        ns.append(signal[list(time).index(i)]/250)
                    return ns

                if not os.path.exists('./cache'):
                        os.makedirs('cache')

                for t in text.split('.'):

                    rn = str(random.randint(1000000,9999999))+"jkadbchjb" 
                    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './api/tts.json'  
                    # Instantiates a client
                    client = texttospeech.TextToSpeechClient()
                    # Set the text input to be synthesized
                    synthesis_input = texttospeech.SynthesisInput(text=t)
                  
                    if gender=='male':
                            voice = texttospeech.VoiceSelectionParams(
                                language_code='en-in', ssml_gender=texttospeech.SsmlVoiceGender.MALE )
                    elif gender=='female':
                        voice = texttospeech.VoiceSelectionParams( language_code='en-in', ssml_gender=texttospeech.SsmlVoiceGender.FEMALE )     
                    
                    else:      
                        voice = texttospeech.VoiceSelectionParams(
                                language_code='en-in', ssml_gender=texttospeech.SsmlVoiceGender.MALE )

                    # Select the type of audio file you want returned
                    audio_config = texttospeech.AudioConfig(
                        audio_encoding=texttospeech.AudioEncoding.LINEAR16
                    )
                    # Perform the text-to-speech request on the text input with the selected
                    # voice parameters and audio file type
                    response = client.synthesize_speech(
                        input=synthesis_input, voice=voice, audio_config=audio_config)
                    # The response's audio_content is binary.
                    with open(f'./cache/{rn}.wav', "wb") as out:
                        out.write(response.audio_content)


                    # Load the detector
                    detector = dlib.get_frontal_face_detector()

                    # Load the predictor
                    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

                    # read the image
                    img = cv2.imread(imganame)

                    # Convert image into grayscale
                    gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)

                    # Use detector to find landmarks
                    faces = detector(gray)
                    for face in faces:
                        x1 = face.left() # left point
                        y1 = face.top() # top point
                        x2 = face.right() # right point
                        y2 = face.bottom() # bottom point

                        # Create landmark object
                        landmarks = predictor(image=gray, box=face)

                        # Loop through all the points
                        p = []
                        for n in range(0, 68):
                                
                                
                                x = landmarks.part(n).x
                                y = landmarks.part(n).y

                                if n==4 or n==10 or n==64 or n==48:
                                    p.append([x,y])
                                  
                        lip = img[p[2][1]:p[1][1],p[2][0]:p[1][0]]
                        lip = lip.copy()

                        lt = visualize(f'./cache/{rn}.wav')
                        x = T.Thread(target=play,args=(f'./cache/{rn}.wav',))
                        x.start()
                        i = 0
                        for n in lt:
                            if n<0:
                                n = lt[lt.index(n)]-n
                                if n<0:
                                    n*=-1
                            n=int(n)

                            img = cv2.imread(imganame)

                            img = cv2.rectangle(img,[p[2][0],p[2][1]-1],[p[1][0],p[1][1]-1],(0, 0, 0),thickness=-1)
                      
                            img[p[2][1]+n:p[1][1]+n,p[2][0]:p[1][0]] = lip
                        # show the image
                            cv2.imshow(winname="Screen curb", mat=img)
                            
                            time.sleep(0.05)
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break


                # Close all windows
                try:
                    shutil.rmtree('./cache')
                except:
                    pass
                cv2.destroyAllWindows()
            except:
                try:
                    shutil.rmtree('./cache')
                except:
                    pass
                try:
                    cv2.destroyAllWindows()   
                except:
                    pass 
                return   

    else:
        flag=False
        try:
            shutil.rmtree('./cache')
        except:
            pass
        try:
            cv2.destroyAllWindows()   
        except:
            pass 
        return


#Importing the library
from tkinter import *
from PIL import ImageTk, Image
#Create an instance of tkinter window or frame
win= Toplevel()

#Setting the geometry of window
win.geometry("100x100+1600+900")

#Create a Label
img = Image.open(r"./assets/icon.png").resize((100,100))
img = ImageTk.PhotoImage(img)
Button(win, image= img,highlightthickness=0,bd=0,command=botmain,activebackground="#f0f0f0").pack()

#Make the window jump above all
win.attributes('-topmost',True)

win.overrideredirect(True)

win.wm_attributes('-transparentcolor', '#f0f0f0')

win.configure(bg='')

win.mainloop()