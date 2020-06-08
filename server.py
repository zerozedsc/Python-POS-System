import urllib.request
import psycopg2
from tkinter.ttk import *
import random
from tkinter import *
import tkinter as tk
import sqlite3

SERVER_PATH = '//Zerozed-pc/shared/DB/ROZERIYA-DB.db'

class Server():
    def __init__(self):

        try:
            self.conn = sqlite3.connect(SERVER_PATH)  # \\Zerozed-pc\shared\DB
            self.cursor = self.conn.cursor()
            print("YOU ARE CONNECTED TO -", "DATABASE" , "\n")
            self.test = True
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL ", error)
            self.test = False
            self.found = error

    def internet(self, host='http://google.com'):
        try:
            urllib.request.urlopen(host)  # Python 3.x
            return True
        except:
            return False


class ServerDisplay():
    def __init__(self, master):
        self.serverWin = master
        self.serverWin.resizable(0, 0)
        self.windowHeight = int(self.serverWin.winfo_reqheight())
        self.windowWidth = int(self.serverWin.winfo_reqwidth())
        self.positionRight = int(self.serverWin.winfo_screenwidth() / 2 - (self.windowWidth / 2))
        self.positionDown = int(self.serverWin.winfo_screenheight() / 2 - (self.windowHeight / 2))
        self.serverWin.iconphoto(False, PhotoImage(file='images/rozeriya.png'))
        self.serverWin.geometry(f"600x400+{self.positionRight - 200}+{self.positionDown - 100}")
        self.serverWin.title("CHECK CONNECTION")
        style = Style()
        style.configure('W.TButton', font=('Comic sans ms', 8, 'normal', 'italic'), foreground='black')
        style1 = 'W.TButton'
        self.call = Server()



        # background
        background_image = tk.PhotoImage(master=self.serverWin, file='images/server.png')
        background_label = Label(self.serverWin, background='gold', image=background_image)
        background_label.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Status Label
        self.mainShow = Label(self.serverWin, text='WAITING FOR SERVER', font=('roboto', 18, 'bold'),
                     foreground='silver')
        self.mainShow.place(relx=0, rely=0.4)
        self.mainShow.after(1, self.callInternet())

        self.serverWin.mainloop()

    def callInternet(self):
        self.mainShow.config(foreground='silver')

        if self.call.internet():
            self.mainShow.config(text="CONNECTED TO THE INTERNET")
            self.serverWin.after(3000, self.callServer)
        else:
            blank = ['.', '..', '...', '....', '....']
            pick = blank[random.randint(0, 4)]
            self.mainShow.config(text="NO INTERNET CONNECTION" + pick, foreground='red')
            self.serverWin.after(3000, self.callInternet)

    def callServer(self):
        self.mainShow.config(foreground='silver')
        if self.call.test:
            self.mainShow.config(text="SERVER CONNECTED")
            self.serverWin.after(3000, self.serverWin.destroy)
        else:
            self.mainShow.config(text="DATABASE NOT FOUND, CHECK THE PARAM BACK", foreground='red')
            self.found = Label(self.serverWin, text=self.call.found, font=('roboto', 12, 'bold'),
                  foreground='silver')
            self.found.place(relx=0, rely=0.6)

            self.serverWin.after(3000, self.callInternet)

# ServerDisplay().serverWin.mainloop()
