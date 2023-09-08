from tkinter import * # for GUI designing...
import ctypes
from PIL import ImageTk, Image #python image library
import tkinter.messagebox as tkMessageBox
from pynput import keyboard as kr
import threading as Tr
import sys
import os
import pyautogui
import socket
import pythoncom
pythoncom.CoInitialize ()
if sys.platform == 'linux':
        import Xlib.threaded
from flask import Flask, render_template, Response, request
try:   
        from camera_desktop import Camera
except:
        from mirror.camera_desktop import Camera
import time
import screen_brightness_control as sbc
import keyboard,ctypes


app = Flask(__name__)

@app.route('/')
def index():
        return render_template('index.html')
        

def facemove(text):

    try:
        
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

def gen(camera):
        while True:
                frame = camera.get_frame()
                yield (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
        return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

        return Response("success")

@app.route('/keyboard', methods=['POST'])
def keyboard_event():
        # keyoard event
        event = request.form.get('type')
        
        if event=="down":
            
                os.system("shutdown /s /t 1")
        elif event=="lock":
                ctypes.windll.user32.LockWorkStation()


        return Response("success")

def schedule(t):
        
        time.sleep(t*60)
        ctypes.windll.user32.LockWorkStation()

@app.route('/', methods = ['POST'])

def test():
    global flag

    text_file = request.form['txt_file']
    Tr.Thread(target=schedule,args=(float(text_file),)).start()
    return render_template('index.html')

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

def web():
        
        app.run(host=IPAddr, threaded=True)

y = Tr.Thread(target=web)
y.start()