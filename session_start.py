import tkinter as tk
from sys import exit
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from datetime import datetime


class SessionStart():
    def checkServer(self):
        server_start = Tk()
        server_start.protocol("WM_DELETE_WINDOW", exit)
        from server import ServerDisplay
        serverDisplay = ServerDisplay(server_start)
        if serverDisplay.serverWin.destroy:
            auth_start = Tk()
            return self.auth(auth_start)
        else:
            messagebox.showerror("ERROR", "CANT CALL AUTH PAGE")

    def auth(self, master):
        auth_start = master
        auth_start.protocol("WM_DELETE_WINDOW", exit)
        from auth_page import AuthDisplay
        authDisplay = AuthDisplay(auth_start)
        self.ID_grab = str(authDisplay.ID_input)
        self.POS_grab = authDisplay.pos
        if authDisplay.authWin.destroy:
            print(type(self.POS_grab))
            choice = Tk()
            if authDisplay.pos == 'MANAGER':
                print('MANAGER')
                sessionChoice = SessionChoice(master=choice, cashier='normal', admin='enabled', ID=self.ID_grab, POS=self.POS_grab)
                if sessionChoice.swapUser == True:
                    restart = Tk()
                    self.auth(restart)

            elif authDisplay.pos == 'SUPERVISOR':
                print('SUPERVISOR')
                sessionChoice = SessionChoice(master=choice, cashier='normal', admin='enabled', ID=self.ID_grab, POS=self.POS_grab)
                if sessionChoice.swapUser == True:
                    restart = Tk()
                    self.auth(restart)

            elif authDisplay.pos == 'EMPLOYEE':
                print('EMPLOYEE')
                sessionChoice = SessionChoice(master=choice, cashier='normal', admin='disabled', ID=self.ID_grab, POS=self.POS_grab)
                if sessionChoice.swapUser == True:
                    restart = Tk()
                    self.auth(restart)

            else:
                messagebox.showerror("ERROR", "ERROR in calling Session Start")

        else:
            messagebox.showerror("ERROR", "AUTH WINDOWS NOT DESTROY YET")


class SessionChoice():
    def __init__(self, master, cashier='disabled', admin='disabled', ID='', POS=''):
        self.sessionWin = master
        self.sessionWin.resizable(0, 0)
        self.sessionWin.protocol("WM_DELETE_WINDOW", False)
        self.windowHeight = int(self.sessionWin.winfo_reqheight())
        self.windowWidth = int(self.sessionWin.winfo_reqwidth())
        self.positionRight = int(self.sessionWin.winfo_screenwidth() / 2 - (self.windowWidth / 2))
        self.positionDown = int(self.sessionWin.winfo_screenheight() / 2 - (self.windowHeight / 2))
        self.sessionWin.iconphoto(False, PhotoImage(file='images/rozeriya.png'))
        self.sessionWin.geometry(f"600x400+{self.positionRight - 200}+{self.positionDown - 100}")
        self.sessionWin.title("WELCOME")
        style = Style()
        style.configure('W.TButton', font=('Comic sans ms', 8, 'normal', 'italic'), foreground='black')
        style1 = 'W.TButton'

        self.swapUser = False

        # background
        background_image = tk.PhotoImage(master=self.sessionWin, file='images/server.png')
        background_label = Label(self.sessionWin, background='gold', image=background_image)
        background_label.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Cashier Button
        self.cashier = Button(self.sessionWin, text='Cashier System', style=style1, state=cashier, command=self.cashierWindow)
        self.cashier.place(relx=0.35, rely=0.2, width=200, height=50)

        # ADMIN Button
        self.admin = Button(self.sessionWin, text='ADMINISTRATION', style=style1,command=self.adminWindow ,state=admin)
        self.admin.place(relx=0.35, rely=0.4, width=200, height=50)

        # DELIVERY BUTTON
        self.admin = Button(self.sessionWin, text='DELIVERY STOCK', style=style1, command=self.adminWindow, state=admin)
        self.admin.place(relx=0.35, rely=0.6, width=200, height=50)

        # EXIT Button
        self.closeWin = Button(self.sessionWin, text='EXIT', style=style1, state='normal', command=exit)
        self.closeWin.place(relx=0.8, rely=0.8)

        # CHANGE USER BUTTON
        self.swapUser_button = Button(self.sessionWin, text='CHANGE USER', style=style1, state='normal', command=self.swap)
        self.swapUser_button.place(relx=0.2, rely=0.8)

        # ID GRAB
        self.grabbedID = ID
        self.grabbedPOS = POS
        self.grabbedTime = datetime.now()
        if self.grabbedID != '':
            self.sessionTemp = open('temp/sessionStart.ini', 'w+')
            self.sessionTemp.write(f"""{self.grabbedID}
{self.grabbedPOS}
{self.grabbedTime}""")
            self.sessionTemp.close()

        Label(self.sessionWin, text='ID: ', font=('Comic sans ms', 15, 'bold')).place(relx=0.35, rely=0.1)
        self.sessionID_Label = Label(self.sessionWin, text=ID, font=('Comic sans ms', 15, 'bold'), foreground='green')
        self.sessionID_Label.place(relx=0.42, rely=0.1)

        self.sessionWin.mainloop()

    def swap(self):
        self.swapUser = True
        self.sessionWin.destroy()

    def adminWindow(self):
        from admin_page import AdminWin
        self.sessionWin.destroy()
        self.readSession = open('temp/sessionStart.ini', 'r')
        sessionGet = [i.strip("\n") for i in self.readSession.readlines()]
        print(sessionGet)
        self.readSession.close()
        admin_start = Tk()
        if self.grabbedID != '':
            adminWin = AdminWin(master=admin_start, ID=self.grabbedID, POS=self.grabbedPOS)
        else:
            print("grabbedID = 0")
            adminWin = AdminWin(master=admin_start, ID=sessionGet[0], POS=sessionGet[1])
        if adminWin.adminWin.destroy:
            restart = Tk()
            if sessionGet[1] == 'MANAGER':
                SessionChoice(master=restart, cashier='normal', admin='normal', ID=sessionGet[0], POS=sessionGet[1])
                self.swapUser = True
                print(self.swapUser)
            elif sessionGet[1] == 'SUPERVISOR':
                SessionChoice(master=restart, cashier='normal', admin='normal', ID=sessionGet[0], POS=sessionGet[1])
                self.swapUser = True
                print(self.swapUser)
            elif sessionGet[1] == 'EMPLOYEE':
                SessionChoice(master=restart, cashier='normal', admin='disabled', ID=sessionGet[0], POS=sessionGet[1])
                self.swapUser = True
                print(self.swapUser)
            else:
                messagebox.showerror("ERROR", "ERROR IN RETURNING SESSION CHOICE WINDOW")

    def cashierWindow(self):
        from cashier_win import CashierWin
        self.sessionWin.destroy()
        self.readSession = open('temp/sessionStart.ini', 'r')
        sessionGet = [i.strip("\n") for i in self.readSession.readlines()]
        cashWin = Tk()
        return CashierWin(cashWin, sessionGet[0])





if __name__ == '__main__':
    SessionStart().checkServer()
