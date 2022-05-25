import pygame
from tkinter import *
from tkinter import Tk,filedialog
import os

class MusicPlayer(Frame):
    def __init__(self,parent):
        parent.title("Music Player")
        parent.geometry("470x290")
        parent.configure(background='grey')

        self.track=[]
        self.Name=[]
        self.a = StringVar()
        self.nama = StringVar()
        self.tampungLokasi=""
        self.end=True
        self.Stopped=False
        self.ReOpen=True
        self.fileSudahDiputar=[]
        self.namaSudahDiputar=[]
        self.RePlay=True
        self.parent = parent

        self.a.set("Play")
        self.nama.set("Silakan Buka file")
        self.KolomText()
        self.Text()
        self.PlayButton()
        self.StopButton()
        self.NextButton()
        self.Open()
        self.slider()

    def File(self,file,path):
        self.track.append(path)
        self.Name.append(file)
        self.Kolom()
    def Kolom(self):
        isi = ""
        no = 1
        for i in self.Name:
            isi += str(no)+".  "+ i + "\n"
            no +=1
        self.setKolom(isi)

    def getFile(self):
        file=''
        if len(self.Name)>0 :
            file = self.track.pop(0)
            nama = self.Name.pop(0)
            self.fileSudahDiputar.append(file)
            self.namaSudahDiputar.append(nama)

            self.nama.set("Now playing : "+nama)
        self.Kolom()
        return file
        
    def PlaySong(self):
        self.end=True
        pygame.init()
        pygame.mixer.init()
        if self.Stopped:
            self.Stopped = False
            pygame.mixer.music.unpause()
            self.a.set("Pause")
        else :
            self.b = pygame.mixer.music.get_busy()
            a = len(self.track)
            if self.b :
                if self.a.get()=="Play" :
                    self.a.set("Pause")
                    pygame.mixer.music.unpause()
                elif self.a.get()=="Pause" :
                    self.a.set("Play")
                    self.pauseOrStop=False
                    pygame.mixer.music.pause()
                    self.pauseOrStop=True
            elif  a!=0 :
                ambilFile = self.getFile()
                pygame.mixer.music.load(ambilFile)
                pygame.mixer.music.play()
                self.RePlay=True
                self.Kolom()
                self.getPosisi()
                self.a.set("Pause")

    def StopSong(self):
        self.b = pygame.mixer.music.get_busy()
        self.Stopped = True
        if self.b :
            pygame.mixer.music.play(1,-1)
            pygame.mixer.music.pause()
            self.a.set("Play")
            self.end=False

    def NextButton(self):
        next = Button(text="Next", command=self.next, width=5, height=3)
        next.pack(side=LEFT)

    def next(self):
        self.b = pygame.mixer.music.get_busy()
        if self.b :
            pygame.mixer.music.stop()
            self.PlaySong()

    def Text(self):
        teks = Label(textvariable=self.nama, 
                    fg="white", bg="grey", font="Verdana 10 bold")
        teks.pack()

    def StopButton(self):
        tombol = Button(text="Stop", command=self.StopSong, width=5, height=3,)
        tombol.pack(side=LEFT)

    def Open(self):
        tombol = Button(text="Open", command=self.openFile, width=5, height=3)
        tombol.pack(side=LEFT)

    def PlayButton(self):
        tombol = Button(textvariable=self.a, command=self.PlaySong, width=5, height=3)
        tombol.pack(side=LEFT)

    def openFile(self):
        tipeFile = [('Mp3 file', '*.mp3'), ('All files', '*')]
        openFile = filedialog.askopenfilenames(filetypes=tipeFile)
        if openFile!="":
            for i in openFile :
                lokasi = i
                nama = os.path.basename(lokasi)
                self.File(nama,lokasi)

    def volume(self, nilai):
        v = float(nilai)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(v)

    def slider(self):
        w1 = Scale(from_=0.00, to=1.0,resolution=0.01, 
                command=self.volume, orient=HORIZONTAL, width=25,
                length=250, bg='grey', label='Volume :',showvalue=0)
        w1.pack()
        w1.set(0.50)
        w1.pack(side=RIGHT)

    def KolomText(self):
        self.T = Text(height=12, width=20, bg='white', fg='black')
        self.scrollBar()
        self.T.configure(state=DISABLED)
    def setKolom(self, nilai):
        self.T.config(state=NORMAL)
        self.T.delete('1.0',END)
        self.T.insert(END,nilai)
        self.T.configure(state=DISABLED)

    def scrollBar(self):
        S = Scrollbar()
        S.pack(side=RIGHT, fill=Y)
        self.T.pack(fill=X)
        S.config(command=self.T.yview)
        self.T.config(yscrollcommand=S.set)
        
    def getPosisi(self):
        pygame.init()
        pygame.mixer.init()
        posisi=pygame.mixer.music.get_pos()
        if posisi==-1 and self.end and self.RePlay:
            self.PlaySong()
        self.b = pygame.mixer.music.get_busy()
        if len(self.track) == 0 and self.b == False and self.Stopped == False :
            self.nama.set("Pemutaran selesai")
            self.a.set("Play")
            for i in self.fileSudahDiputar :
                self.track.append(i)
            for i in self.namaSudahDiputar:
                self.Name.append(i)
            self.namaSudahDiputar=[]
            self.fileSudahDiputar=[]
            self.Kolom()
            self.RePlay=False
        elif (len(self.track)>0 or self.b) and self.RePlay :
            self.timer = self.parent.after(1000, self.getPosisi)

root = Tk()
MusicPlayer(root)
mainloop()
pygame.quit()