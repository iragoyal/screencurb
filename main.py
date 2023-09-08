import numpy as np
from tkinter import *
import threading as Tr
from PIL import ImageTk, Image
from twilio.rest import Client
import speech_recognition as sr
import tkinter.messagebox as mg
import matplotlib.pyplot as plt
from pynput import keyboard as kr
from playsound import playsound
from google.cloud import storage
import tkinter.scrolledtext as stwin
from google.cloud import texttospeech
from bing_image_downloader import downloader
import sqlite3,ctypes,os,shutil,winapps,subprocess,winapps,datetime,cv2,time,random,dlib,pyautogui,wave, sys,soundfile,bot


def monitor():
    global value,da
    data = {}
    closed = {}
    value = {'study':0,'other':0,'game':0}
    detail = eval(open('./assets/data.txt','r').read())
    while True:
        cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        app = []
        for line in proc.stdout:
            if not line.decode()[0].isspace():
                app.append(line.decode().rstrip())
        app.pop(0)
        app.pop(0)
        app = list(app)
        lt = []
        for j in winapps.list_installed():
            try:
                lt.append(str(j).split("InstalledApplication(name='")[1].split("\'")[0])
            except:
                pass
        active = []
        nn = []
        for i in app:
            for n in lt:
                if n in i or i in n:
                    if i not in active:
                        active.append(i)
                        nn.append(n)
        key = list(data.keys())
        for i in active:
            if i not in key:
                data[i]=datetime.datetime.now()
        for i in key:
            if i not in active:
                closed[i]=[data[i],datetime.datetime.now()]
                d = data[i]
                value[detail[i]]+=(float((datetime.datetime.now()-d).total_seconds()))*0.000277778
                return
                del data[i]
        _,_,st,sst,gst,ost,_ = open("./assets/cache2.txt","r").read().split(',')
        #print((float((datetime.datetime.now()-da).total_seconds()))*0.000277778)
        if (float((datetime.datetime.now()-da).total_seconds()))*0.000277778>=float(st):
            # Find your Account SID and Auth Token at twilio.com/console
            # and set the environment variables. See http://twil.io/secure
            account_sid = 'AC68830eda262fe635e7fc39f18dfc6b02'
            auth_token = '633be3aff7476c5df31fb06237cdbb01'
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                                          body='Your ward has exceeded the time',
                                          from_='+14245775280',
                                          to='+918604629998'
                                      )
            ctypes.windll.user32.LockWorkStation()
            return

        if value['study']>=float(sst):
            # Find your Account SID and Auth Token at twilio.com/console
            # and set the environment variables. See http://twil.io/secure
            account_sid = 'AC68830eda262fe635e7fc39f18dfc6b02'
            auth_token = '633be3aff7476c5df31fb06237cdbb01'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                                          body='Your ward has exceeded study time',
                                          from_='+14245775280',
                                          to='+918604629998'
                                      )
            return

        if value["game"]>=float(gst):
            account_sid = 'AC68830eda262fe635e7fc39f18dfc6b02'
            auth_token = '633be3aff7476c5df31fb06237cdbb01'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                                          body='Your ward has exceeded gaming time',
                                          from_='+14245775280',
                                          to='+918604629998'
                                      )
            ctypes.windll.user32.LockWorkStation()
            return
        if value["other"]>=float(ost):
            account_sid = 'AC68830eda262fe635e7fc39f18dfc6b02'
            auth_token = '633be3aff7476c5df31fb06237cdbb01'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                                          body='Your ward has exceeded other activity time',
                                          from_='+14245775280',
                                          to='+918604629998'
                                      )
            ctypes.windll.user32.LockWorkStation()
            return

def database():
    global conn, cursor
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    q1 = "Create table if not exists user (id integer primary key AUTOINCREMENT,username varchar(150) unique,password TEXT)"
    cursor.execute(q1)
    q2 = "Create table if not exists kid (id varchar(100) primary key ,name TEXT,age integer,mt integer,sst integer,gst integer,ost integer,fav TEXT)"
    cursor.execute(q2)

def apps():
    app = [] 
    for item in winapps.list_installed():
        try:
            app.append(str(item).split(',')[0].split('=')[-1])
        except:
            pass
    return app

def login():
    lgwin = Tk()
    img = Image.open("assets/login.png")
    img = ImageTk.PhotoImage(img)
    panel = Label(lgwin, image=img)
    panel.pack(side="top", fill="both", expand="yes")
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
    lt = [w, h]
    a = str(lt[0]//2-600)
    b= str(lt[1]//2-370)
    lgwin.title("Screen curb")
    lgwin.geometry("1200x700+"+a+"+"+b)
    lgwin.resizable(0,0)

    email = StringVar()
    passw = StringVar()

    e1 = Entry(lgwin,textvariable=email,font=("",20),width=12,bg = "#ffd4a9",relief = "solid",fg="#392e24",bd=0)
    e1.place(x=316,y=368)

    p1 = Entry(lgwin,textvariable=passw,font=("",20),width=12,bg = "#ffd4a9",relief = "solid",fg="#392e24",bd=0,show='*')
    p1.place(x=316,y=437)

    def submit():
        try:

            database()
            q = f"select * from user where username = '{email.get()}' and password = '{passw.get()}'"
            cursor.execute(q)
            result = cursor.fetchall()
            if result:
                f = open("./assets/cache.txt","w")
                f.write(email.get())
                f.close()
                lgwin.destroy()
                homewin()
            else:
                mg.showinfo("warning","wrong Id or password !!")
        except Exception as e:
            mg.showinfo("Error",e)

    def move():
        lgwin.destroy()
        signup()

    photo = Image.open("assets/2.png")
    ad3 = ImageTk.PhotoImage(photo)
    b1=Button(lgwin, highlightthickness = 0, bd = 0,activebackground="#877058", image = ad3,command=move)
    b1.place(x=210,y=616)

    photo = Image.open("assets/3.png")
    ad4 = ImageTk.PhotoImage(photo)
    b2=Button(lgwin, highlightthickness = 0, bd = 0,activebackground="#877058", image = ad4,command=submit)
    b2.place(x=200,y=513)

    lgwin.mainloop()

def live():
    import mirror.mirror

def chatb():
    import mainbot

def start():
    global home
    try:
        home.destroy()
    except:
        pass
    global value,da
    da = datetime.datetime.now()

    Tr.Thread(target=live).start()
    Tr.Thread(target=monitor).start()
    #Tr.Thread(target=popup).start()
    Tr.Thread(target=jar).start()
    #Tr.Thread(target=chatb).start()
    Tr.Thread(target=gray).start()

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
                x = Tr.Thread(target=play,args=(f'./cache/{rn}.wav',))
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

def popup():
    global da
    dval = da
    while True:
        print(float((datetime.datetime.now()-dval).total_seconds()))
        if (float((datetime.datetime.now()-dval).total_seconds()))*0.0166667>30:
            facemove("You Have Been Using screen for too long please close the screen.")
            dval=datetime.datetime.now()
            

def gray():
    global da
    dval2 = da
    while True:
        if (float((datetime.datetime.now()-dval2).total_seconds()))>5:
            dval2=datetime.datetime.now()
            pyautogui.keyDown("win")
            pyautogui.keyDown("ctrl")
            pyautogui.press("c")
            pyautogui.keyUp("win")
            pyautogui.keyUp("ctrl")  

def jar():
        global value

        if not os.path.exists('./assets/jar/p.txt'):

            file = open("p.txt","w")
            file.write('0')
            file.close()
        

        file = open("p.txt","a+")

        r = int(open("p.txt","r").read())

        #Create an instance of tkinter window or frame
        win= Tk()

        #Setting the geometry of window
        win.geometry("100x100+1650+50")


        lm = os.listdir("./assets/jar")
        lm.pop(0)
        n = 0
        _,_,st,sst,gst,ost,_ = open("./assets/cache2.txt","r").read().split(',')

        if float(sst)>=value["study"]:
            r+=100
        elif float(sst)<value["study"]:
            r-=10

        elif float(gst)>value["game"]:
            r=0
        elif float(gst)==value["game"]:
            r+=50

        elif float(gst)<value["game"]:
            r+=100

        elif float(ost)>value["other"]:
            r=0
        elif float(ost)==value["other"]:
            r+=50

        elif float(ost)<value["other"]:
            r+=100

        def show():
            facemove(f"Your candy points are {r}")


        file.write(str(r))
        file.close()



        #Create a Label
        img = Image.open(r"./assets/jar/1.png").resize((100,100))
        img = ImageTk.PhotoImage(img)
        bt = Button(win, image= img,highlightthickness=0,bd=0,command=show,activebackground="#f0f0f0")
        bt.pack()

        if r>=1000:
            img2 = Image.open(r"./assets/jar/7.png").resize((100,100))
            img2 = ImageTk.PhotoImage(img2)
            bt["image"]=img2

        elif r>=800:
            img3 = Image.open(r"./assets/jar/6.png").resize((100,100))
            img3 = ImageTk.PhotoImage(img3)
            bt["image"]=img3

        elif r>=600:
            img4 = Image.open(r"./assets/jar/5.png").resize((100,100))
            img4 = ImageTk.PhotoImage(img4)
            bt["image"]=img4

        elif r>=500:
            img5 = Image.open(r"./assets/jar/4.png").resize((100,100))
            img5 = ImageTk.PhotoImage(img5)
            bt["image"]=img5

        elif r>=300:
            img6 = Image.open(r"./assets/jar/3.png").resize((100,100))
            img6 = ImageTk.PhotoImage(img6)
            bt["image"]=img6

        elif r>=100:
            img7 = Image.open(r"./assets/jar/2.png").resize((100,100))
            img7 = ImageTk.PhotoImage(img7)
            bt["image"]=img7
 


        #Make the window jump above all
        win.attributes('-topmost',True)

        win.overrideredirect(True)

        win.wm_attributes('-transparentcolor', '#f0f0f0')

        win.configure(bg='')

        win.mainloop()

def signup():

    rgwin = Tk()
    img = Image.open("assets/signup.png")
    img = ImageTk.PhotoImage(img)
    panel = Label(rgwin, image=img)
    panel.pack(side="top", fill="both", expand="yes")
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
    lt = [w, h]
    a = str(lt[0]//2-600)
    b= str(lt[1]//2-370)
    rgwin.title("Screen curb")
    rgwin.geometry("1200x700+"+a+"+"+b)
    rgwin.resizable(0,0)

    email = StringVar()
    passw = StringVar()

    e1 = Entry(rgwin,textvariable=email,font=("",20),width=12,bg = "#ffd4a9",relief = "solid",fg="#392e24",bd=0)
    e1.place(x=316,y=368)

    p1 = Entry(rgwin,textvariable=passw,font=("",20),width=12,bg = "#ffd4a9",relief = "solid",fg="#392e24",bd=0,show='*')
    p1.place(x=316,y=437)
    

    def submit():
        database()
        try:
            q = f"Insert into user (username,password) values('{email.get()}','{passw.get()}')"
            cursor.execute(q)

            conn.commit()
            move()
        except Exception as e:
            mg.showinfo("Error",e)

    def move():
        rgwin.destroy()
        login()

    photo = Image.open("assets/1.png")
    ad3 = ImageTk.PhotoImage(photo)
    b1=Button(rgwin, highlightthickness = 0, bd = 0,activebackground="#877058", image = ad3,command=move)
    b1.place(x=208,y=605)

    photo = Image.open("assets/3.png")
    ad4 = ImageTk.PhotoImage(photo)
    b2=Button(rgwin, highlightthickness = 0, bd = 0,activebackground="#877058", image = ad4,command=submit)
    b2.place(x=200,y=513)
    rgwin.mainloop()

def dash():
    global value
    # Import libraries
    from matplotlib import pyplot as plt
    import numpy as np
     
     
    # Creating dataset
    cars = list(value.keys())
     
    data = list(value.values())
     
    # Creating plot
    fig = plt.figure(figsize =(10, 7))
    plt.pie(data, labels = cars)
     
    # show plot
    plt.show()
    
home=None
def homewin():
    global home

    home = Tk()
    imghome = Image.open("assets/home.png")
    imghome = ImageTk.PhotoImage(imghome)
    panel = Label(home, image=imghome)
    panel.pack(side="top", fill="both", expand="yes")
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
    lt = [w, h]
    a = str(lt[0]//2-600)
    b= str(lt[1]//2-370)
    home.title("Screen curb")
    home.geometry("1200x700+"+a+"+"+b)
    home.resizable(0,0)

    photo = Image.open("assets/4.png")
    ad3 = ImageTk.PhotoImage(photo)
    b1=Button(home, highlightthickness = 0, bd = 0,activebackground="#ffd4a9", image = ad3,command=start)
    b1.place(x=154,y=538)

    photo = Image.open("assets/5.png")
    ad4 = ImageTk.PhotoImage(photo)
    b1=Button(home, highlightthickness = 0, bd = 0,activebackground="#ffd4a9", image = ad4,command=dash)
    b1.place(x=465,y=538)


    photo = Image.open("assets/7.png")
    ad5 = ImageTk.PhotoImage(photo)
    b1=Button(home, highlightthickness = 0, bd = 0,activebackground="#ffd4a9", image = ad5,command=None)
    b1.place(x=964,y=27)

    def log():
        home.destroy()
        login()

    def forms():
        home.destroy()
        form()

    photo = Image.open("assets/6.png")
    ad6 = ImageTk.PhotoImage(photo)
    b1=Button(home, highlightthickness = 0, bd = 0,activebackground="#ffd4a9", image = ad6,command=log)
    b1.place(x=1038,y=27)

    photo = Image.open("assets/8.png")
    ad7 = ImageTk.PhotoImage(photo)
    b1=Button(home, highlightthickness = 0, bd = 0,activebackground="#ffd4a9", image = ad7,command=forms)
    b1.place(x=1110,y=27)

    home.mainloop()


def form():
    global home
    form = Tk()
    imgform = Image.open("assets/form.png")
    imgform = ImageTk.PhotoImage(imgform)
    panel = Label(form, image=imgform)
    panel.pack(side="top", fill="both", expand="yes")
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
    lt = [w, h]
    a = str(lt[0]//2-600)
    b= str(lt[1]//2-370)
    form.title("Screen curb")
    form.geometry("1200x700+"+a+"+"+b)
    form.resizable(0,0)

    name = StringVar()
    age = DoubleVar()
    st = DoubleVar()
    sst = DoubleVar()
    gst = DoubleVar()
    ost = DoubleVar()
    fav = StringVar()

    e1 = Entry(form,textvariable=name,font=("",20),width=12,fg = "#ffd4a9",relief = "solid",bg="#392e24",bd=0)
    e1.place(x=620,y=125)

    p1 = Entry(form,textvariable=age,font=("",20),width=12,fg = "#ffd4a9",relief = "solid",bg="#392e24",bd=0)
    p1.place(x=620,y=183)

    p1 = Entry(form,textvariable=st,font=("",20),width=12,fg = "#ffd4a9",relief = "solid",bg="#392e24",bd=0)
    p1.place(x=620,y=236)

    p1 = Entry(form,textvariable=sst,font=("",20),width=12,fg = "#ffd4a9",relief = "solid",bg="#392e24",bd=0)
    p1.place(x=620,y=292)

    p1 = Entry(form,textvariable=gst,font=("",20),width=12,fg = "#ffd4a9",relief = "solid",bg="#392e24",bd=0)
    p1.place(x=620,y=350)

    p1 = Entry(form,textvariable=ost,font=("",20),width=12,fg = "#ffd4a9",relief = "solid",bg="#392e24",bd=0)
    p1.place(x=620,y=405)

    p1 = Entry(form,textvariable=fav,font=("",20),width=12,fg = "#ffd4a9",relief = "solid",bg="#392e24",bd=0)
    p1.place(x=620,y=460)

    def manage():
        data = eval(open('./assets/data.txt','r').read())
        
        import tkinter as tk
        from tkinter import ttk



        def func(event,a,b):
            print(b)
            data[a]=b
            

        root = Tk()
        text = stwin.ScrolledText(root)
        text.pack(fill="both", expand=True)
        
        options = ["study","game","other"]
        clicked = StringVar()

        for i in list(data.keys()):
            item = i
            text.insert("end", item + "\t\n")
            button = ttk.Combobox(text, state='readonly')
            button.set(data[i])
            button["values"]=options
            
            button.bind("<<ComboboxSelected>>",lambda event, a=i, b=button.current(): func(None,a, b))
            button.config(width=10,background="white",foreground='black')
            text.window_create("end-2c", window=button)

        root.mainloop()
    try:
            a,b,c,d,e,f,g = open('./assets/cache2.txt','r').read().split(',')
            name.set(a)
            age.set(b)
            st.set(c)
            sst.set(d)
            gst.set(e)
            ost.set(f)
            fav.set(g)
    except:
        pass

    def save():
        if (sst.get()+gst.get()+ost.get())>st.get():
            mg.showinfo("Screen Curb","wrong info !!! total should be less then maximum time.")
        elif name.get()=='' or age.get()==0 or st.get()==0 or sst.get()==0 or ost.get()==0 or fav.get()=='':
                mg.showinfo("Screen Curb","all details are mendatory to fill")

        q = mg.askquestion("Screen Curb","I have checked all the details and classified apps")
        if q=='yes':

                database()
                try:
                    em = open('./assets/cache.txt','r').read()
                    q = f"Insert into kid values('{em}','{name.get()}',{age.get()},{st.get()},{sst.get()},{gst.get()},{ost.get()},'{fav.get()}')"
                    cursor.execute(q)
                    conn.commit()
                    

                    
                    #downloader.download(fav.get(), limit=2, adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
                    f = open("./assets/fav.txt",'w')
                    f.write(fav.get())
                    f.close()

                    f = open("./assets/cache2.txt","w")
                    f.write(f"{name.get()},{age.get()},{st.get()},{sst.get()},{gst.get()},{ost.get()},{fav.get()}")
                    f.close()

                    form.destroy()
                    homewin()

                except Exception as e:
                    try:
                        f = open("./assets/cache2.txt","w")
                        f.write(f"{name.get()},{age.get()},{st.get()},{sst.get()},{gst.get()},{ost.get()},{fav.get()}")
                        f.close()
                    except:

                        mg.showinfo("Error",e)

        else:

                mg.showinfo("Screen Curb","Please check again")

    photo = Image.open("assets/7.png")
    ad5 = ImageTk.PhotoImage(photo)
    b1=Button(form, highlightthickness = 0, bd = 0,activebackground="#ffd4a9", image = ad5,command=None)
    b1.place(x=964,y=27)

    def log():
        form.destroy()
        login()

    def hm():
        form.destroy()
        homewin()
        

    photo = Image.open("assets/6.png")
    ad6 = ImageTk.PhotoImage(photo)
    b1=Button(form, highlightthickness = 0, bd = 0,activebackground="#ffd4a9", image = ad6,command=log)
    b1.place(x=1040,y=27)

    photo = Image.open("assets/9.png")
    ad7 = ImageTk.PhotoImage(photo)
    b1=Button(form, highlightthickness = 0, bd = 0,activebackground="#ffd4a9", image = ad7,command=hm)
    b1.place(x=1115,y=27)


    photo = Image.open("assets/10.png")
    ad8 = ImageTk.PhotoImage(photo)
    b1=Button(form, highlightthickness = 0, bd = 0,activebackground="#ffd4a9", image = ad8,command=manage)
    b1.place(x=172,y=530)


    photo = Image.open("assets/11.png")
    ad9 = ImageTk.PhotoImage(photo)
    b1=Button(form, highlightthickness = 0, bd = 0,activebackground="#ffd4a9", image = ad9,command=save)
    b1.place(x=309,y=618)

    form.mainloop()

try:
    em = open('./assets/cache.txt','r').read()
    homewin()
except: 
    login()


def shortcut():
    with kr.GlobalHotKeys({
            '<alt>+<ctrl>+r': start,
            '<alt>+<ctrl>+y': homewin}) as h:
        h.join()



x = Tr.Thread(target=shortcut)
x.start()
