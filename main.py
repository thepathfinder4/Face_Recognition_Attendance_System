import tkinter as tk
import numpy as np
import face_recognition
from datetime import *
import pandas as pd
from tkinter import *
from PIL import ImageTk, Image
import cv2
import os
import threading

window=tk.Tk()
window.title("Face recognition system")
window.configure(background="white")

logo = Image.open("UI/logo.png")
logo = logo.resize((50, 47))
logo1 = ImageTk.PhotoImage(logo)
titl = tk.Label(window, bg="white", font=("arial", 35))
titl.pack(fill=X)
l1 = tk.Label(window, image=logo1, bg="white",)
l1.place(x=10, y=13)

titl = tk.Label(
    window, text="Face Recognition Attendance System", bg="white", fg="black", font=("arial", 27),
)
titl.place(x=700, y=13)


a = tk.Label(
    window,
    text="Dashboard",
    bg="white",
    fg="black",
    bd=10,
    font=("arial", 35),
)
a.pack()

r1 = Image.open("UI/entry.png")
ent = ImageTk.PhotoImage(r1)
label1 = Label(window, image=ent)
label1.image = ent
label1.place(x=300, y=400)

a1 = Image.open("UI/exit.png")
exi = ImageTk.PhotoImage(a1)
label2 = Label(window, image=exi)
label2.image = exi
label2.place(x=640, y=400)

v1 = Image.open("UI/attendance.png")
attend = ImageTk.PhotoImage(v1)
label3 = Label(window, image=attend)
label3.image = attend
label3.place(x=960, y=400)

q1 = Image.open("UI/register.png")
reg= ImageTk.PhotoImage(q1)
label4 = Label(window, image=reg)
label4.image = reg
label4.place(x=1370, y=400)

#function for entry of students
def entry():
    def Final_csv(file_name):#remove duplicates
        f = pd.read_csv(file_name)
        f = f.drop_duplicates(subset=['Name'])
        f.to_csv(file_name, index=False)

    def findEncodings(images):#find encoding
        encodeList = []

        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def markTIMEentry(name, Win_name):#record the entry time
        print("marking entry")
        Win_name += '.csv'
        with open(Win_name, 'r+') as f:
            myDataList = f.readlines()

            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
                if name not in nameList:
                    now = datetime.now()
                    dtString = now.strftime('%H:%M:%S')
                    f.writelines(f'\n{name},{dtString}')

    def cameraENTRY(img, Win_name):#input from camera
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 255, 255), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_DUPLEX, 0.75, (0, 0, 0), 2)
                markTIMEentry(name, "ENTRY")

        cv2.imshow(Win_name, img)

    path = 'Students'#path of students

    images = []
    classNames = []
    myList = os.listdir(path)
    print("my list", myList)

    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print("classnames", classNames)
    print("images", images)
    nameList = []

    encodeListKnown = findEncodings(images)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()

        cameraENTRY(img, 'ENTRY')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("calling final csv")
    Final_csv("ENTRY.csv")

    cap.release()
    cv2.destroyAllWindows()


b1 = tk.Button(window, text="Entry", font=("arial", 20), bg='white', fg='black', borderwidth=0, command=entry)
b1.place(relx=0.18, rely=0.6)

def exit():#function for exit of students
  def Final_csv(file_name):
    f = pd.read_csv(file_name)
    f = f.drop_duplicates(subset=['Name'])
    f.to_csv(file_name, index=False)


  def findEncodings(images):#find the encoding of face
    encodeList = []

    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


  def markTIMEexit(name, Win_name):#mark exit time of students in csv with the time when it was stored
    print("marking exit")
    Win_name += '.csv'
    with open(Win_name, 'r+') as f:
        myDataList = f.readlines()

        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')

    print("done")


  def cameraEXIT(img, Win_name):#function for opening the camera for exit
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()

            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (255, 255, 255), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.75, (0, 0, 0), 2)

            markTIMEexit(name, "EXIT")

    cv2.imshow(Win_name, img)


  path = 'Students'#directory of images

  images = []
  classNames = []
  myList = os.listdir(path)
  print("mylist", myList)

  for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
  print("classnames",classNames)
  print("images list:", images)

  nameList = []

  encodeListKnown = findEncodings(images)
  print('Encoding Complete')

  cap = cv2.VideoCapture(0)

  while True:
    success, img = cap.read()

    cameraEXIT(img, 'EXIT')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  print("calling final csv")
  Final_csv("EXIT.csv")

  cap.release()
  cv2.destroyAllWindows()



b2 = tk.Button(window, text="Exit", font=("aerial", 20), bg='white', fg='black', borderwidth=0, command=exit)
b2.place(relx=0.37,rely=0.6)

password_entry = tk.Entry(window, show="*")
password_entry.pack()

def attendance():#for attendance purposes
    password = password_entry.get()

    if password == "secret":
        def clear_CSV(file_name):
            file = open(file_name, "r+")
            file.truncate(16)
            file.close()

        def TOminutes(Entry, Exit):#calculate in out time
            IN = Entry.split(':')
            OUT = Exit.split(':')
            t1 = (int)(IN[0]) * 60 + (int)(IN[1])
            t2 = (int)(OUT[0]) * 60 + (int)(OUT[1])
            return t2 - t1

        df1 = pd.read_csv("ENTRY.csv")#read entry
        df2 = pd.read_csv("EXIT.csv")#read exit
        LIST = pd.read_csv("LIST.csv")#read name of students

        result = df1.merge(df2, indicator=True, how='outer').loc[lambda v: v['_merge'] == 'both']
        result.drop(['_merge'], axis=1, inplace=True)

        result['DURATION'] = 0

        for i in range(result.shape[0]):
            result['DURATION'][i] = TOminutes(result['Time_ENTRY'][i], result['Time_EXIT_'][i])

        #remove tudents who do not stay in class for certain time
        result = result.drop(result[result.DURATION < 1].index)

        for i in range(LIST.shape[0]):
            if result.shape[0] != 0:
                for j in range(result.shape[0]):
                    if result['Name'][j] == LIST['Name'][i]:
                        LIST['ATTENDANCE'][i] = "PRESENT"
                    else:
                        LIST['ATTENDANCE'][i] = "ABSENT"
            else:
                LIST['ATTENDANCE'][i] = "ABSENT"

        '''
        print(df1)
        print()
        print(df2) 
        print()
        print(result)            
        print() 
        '''

        t = date.today()

        t = t.strftime("%m-%d-%Y")
        t = t + '.csv'

        print(LIST)

        LIST.to_csv(t)

        clear_CSV("ENTRY.csv")
        clear_CSV("EXIT.csv")

    else:

        print("Invalid password")

b3 = tk.Button(window, text="Mark Attendance", font=("arial", 20), bg='white', fg='black', borderwidth=0, command=attendance)
b3.pack()
b3.place(relx=0.5,rely=0.6)


def createdatabase():#for the photo entry of students
    path = 'Students'#directory
    e = ''
    def setname():
        ret, frame = cap.read()
        name = e.get()
        name = name + ".png"
        cv2.imwrite(os.path.join(path, name), frame)

    root = Toplevel(window)
    root.geometry('644x560')
    root.configure(bg='black')

    app = Frame(root, bg="white")#create frames
    app.grid()

    lmain = Label(app)#label in frames
    lmain.grid()

    cap = cv2.VideoCapture(0)#to access camera

    def video_stream():#function for video streaming
        _, frame = cap.read()
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        lmain.imgtk = imgtk
        lmain.configure(image=imgtk)
        lmain.after(1, video_stream)

    e = Entry(root, width=20, font=('arial 15'))
    e.place(x=200, y=490, width=250, height=25)
    e.focus_set()

    b = Button(root, text='UPDATE', command=setname, width=20, font="arial 15", bg="white", fg="black")
    b.place(x=270, y=520, width=150, height=50)
    video_stream()
    root.mainloop()
    cap.release()
    cv2.destroyAllWindows()

b4 =tk.Button(window, text="Generate database", font=("arial", 20), bg='white', fg='black', borderwidth=0, command=createdatabase)
b4.place(relx=0.69,rely=0.6)


window.geometry("2000x2000")
window.mainloop()

