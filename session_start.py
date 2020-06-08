import tkinter as tk
from sys import exit
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import tkinter.simpledialog as sd
from datetime import datetime, date
import os
import tkcalendar
import sqlite3
import babel
from pprint import pprint
from server import SERVER_PATH


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
            # print(type(self.POS_grab))    #debug
            choice = Tk()
            if authDisplay.pos == 'MANAGER':
                #print('MANAGER')   #debug
                sessionChoice = SessionChoice(master=choice, cashier='normal', admin='enabled', ID=self.ID_grab, POS=self.POS_grab)
                if sessionChoice.swapUser == True:
                    restart = Tk()
                    self.auth(restart)

            elif authDisplay.pos == 'SUPERVISOR':
                # print('SUPERVISOR')   #debug
                sessionChoice = SessionChoice(master=choice, cashier='normal', admin='enabled', ID=self.ID_grab, POS=self.POS_grab)
                if sessionChoice.swapUser == True:
                    restart = Tk()
                    self.auth(restart)

            elif authDisplay.pos == 'EMPLOYEE':
                # print('EMPLOYEE')     #debug
                sessionChoice = SessionChoice(master=choice, cashier='normal', admin='disabled', ID=self.ID_grab, POS=self.POS_grab)
                if sessionChoice.swapUser == True:
                    restart = Tk()
                    self.auth(restart)

            else:
                messagebox.showerror("Position not recognize", "Pls call the support to fix it")

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

        # ADD STOCK BUTTON
        self.admin = Button(self.sessionWin, text='ADD STOCK', style=style1, command=self.addStockWindow, state=admin)
        self.admin.place(relx=0.35, rely=0.6, width=200, height=50)

        # EXIT Button
        self.closeWin = Button(self.sessionWin, text='EXIT', style=style1, state='normal', command=exit)
        self.closeWin.place(relx=0.8, rely=0.85)

        # CHANGE USER BUTTON
        self.swapUser_button = Button(self.sessionWin, text='CHANGE USER', style=style1, state='normal', command=self.swap)
        self.swapUser_button.place(relx=0.65, rely=0.85)

        # PRINT REPORT BUTTON
        self.printReport_button = Button(self.sessionWin, text='PRINT REPORT', style=style1, state='normal',
                                      command=self.printExcel)
        self.printReport_button.place(relx=0.15, rely=0.4, height=50)

        # ID GRAB
        self.grabbedID = ID
        self.grabbedPOS = POS
        self.grabbedTime = datetime.now()
        if self.grabbedID != '':
            self.sessionTemp = open('Config/sessionStart.ini', 'w+')
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
        self.readSession = open('Config/sessionStart.ini', 'r')
        sessionGet = [i.strip("\n") for i in self.readSession.readlines()]
        # print(sessionGet)     #debug
        self.readSession.close()
        admin_start = Tk()
        if self.grabbedID != '':
            adminWin = AdminWin(master=admin_start, ID=self.grabbedID, POS=self.grabbedPOS)
        else:
            # print("grabbedID = 0")    #debug
            adminWin = AdminWin(master=admin_start, ID=sessionGet[0], POS=sessionGet[1])
        if adminWin.adminWin.destroy:
            restart = Tk()
            if sessionGet[1] == 'MANAGER':
                SessionChoice(master=restart, cashier='normal', admin='normal', ID=sessionGet[0], POS=sessionGet[1])
                self.swapUser = True
                # print(self.swapUser)  #debug
            elif sessionGet[1] == 'SUPERVISOR':
                SessionChoice(master=restart, cashier='normal', admin='normal', ID=sessionGet[0], POS=sessionGet[1])
                self.swapUser = True
                # print(self.swapUser)  #debug
            elif sessionGet[1] == 'EMPLOYEE':
                SessionChoice(master=restart, cashier='normal', admin='disabled', ID=sessionGet[0], POS=sessionGet[1])
                self.swapUser = True
                # print(self.swapUser)  #debug
            else:
                messagebox.showerror("ERROR", "ERROR IN RETURNING SESSION CHOICE WINDOW")

    def cashierWindow(self):
        from cashier_win import CashierWin
        self.sessionWin.destroy()
        self.readSession = open('Config/sessionStart.ini', 'r')
        sessionGet = [i.strip("\n") for i in self.readSession.readlines()]
        cashWin = Tk()
        return CashierWin(cashWin, sessionGet[0])

    def printExcel(self):
        self.calendar_win = Toplevel(self.sessionWin)
        Label(self.calendar_win, text='Choose date').pack(padx=10, pady=10)



        today = date.today()

        mindate = date(year=2010, month=1, day=1)
        maxdate = today
        check_validate = StringVar()
        validate = Label(self.calendar_win, text='Report Exist', textvariable=check_validate, font=('comic sans ms', 13, 'bold'), foreground='Green')

        cal = tkcalendar.Calendar(self.calendar_win, font=('comic sans ms', 15, 'bold'), selectmode='day', locale='en_US',
                       mindate=mindate, maxdate=maxdate, disabledforeground='red',
                       cursor="hand1", year=today.year, month=today.month, day=today.day)


        def print_report():
            SAVE_PATH = 'data/Report Data/'
            get_date = cal.selection_get()
            EXCEL_FILE = SAVE_PATH + str(get_date)  + '.xlsx'

            if os.path.exists(os.path.abspath(EXCEL_FILE)):
                printfile = os.path.abspath(EXCEL_FILE)
                try:
                    os.startfile(rf"{printfile}", 'print')
                    self.calendar_win.destroy()
                    messagebox.showinfo("Printing", f"Report on {get_date} Printed Successfully")
                except Exception as error:
                    messagebox.showerror("Printer error", error)
                    self.calendar_win.destroy()
            else:
                messagebox.showerror("Not Found", "Your Report NOT FOUND")
                self.calendar_win.focus_force()


        def is_validate(event):
            SAVE_PATH = 'data/Report Data/'
            get_date = cal.selection_get()
            EXCEL_FILE = SAVE_PATH + str(get_date) + '.xlsx'

            if os.path.exists(os.path.abspath(EXCEL_FILE)):
                validate.config(foreground='green')
                check_validate.set(f"Report {get_date} Exist")
            else:
                validate.config(foreground='red')
                check_validate.set(f"Report {get_date} Not Exist")


        self.calendar_win.bind("<Button-1>", is_validate)
        cal.pack(fill="both", expand=True)
        Button(self.calendar_win, text="Print", style='W.TButton' ,command=print_report).pack()
        validate.pack()

    def addStockWindow(self):
        conn = sqlite3.connect(SERVER_PATH)  # \\Zerozed-pc\shared\DB
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PRODUCT_DATA ORDER BY PRODUCT_ID;")
        query = cursor.fetchall()
        # pprint(query) #debug

        try:
            self.adjust = sd.askstring('REGISTER ITEM', f'PRODUCT ID ')


            for i in query:
                if self.adjust.upper() in i:
                    check_productID = self.adjust.upper()
                    break

            if self.adjust.upper() in check_productID:
                if "RZ" and 'P' in self.adjust.upper() or len(self.adjust) >= 10:
                    self.addWin = Toplevel(self.sessionWin)
                    self.addWin.resizable(0, 0)
                    self.windowHeight = int(self.addWin.winfo_reqheight())
                    self.windowWidth = int(self.addWin.winfo_reqwidth())
                    self.positionRight = int(self.addWin.winfo_screenwidth() / 2 - (self.windowWidth / 2))
                    self.positionDown = int(self.addWin.winfo_screenheight() / 2 - (self.windowHeight / 2))
                    self.addWin.iconphoto(False, PhotoImage(file='images/rozeriya.png'))
                    self.addWin.geometry(f"400x200+{self.positionRight - 400}+{self.positionDown - 300}")
                    self.addWin.title("ADD ITEM")

                    Label(self.addWin, text="REGISTER ITEM", font=('comic sans ms', 18, 'italic', 'bold')).pack()


                    self.getQtyA = IntVar()
                    qty_before = 0

                    # ID DISABLED
                    Label(self.addWin, text='PRODUCT ID', font=('Comic sans ms', 12, 'normal', 'italic')).place(
                        relx=0,
                        rely=0.2)
                    reg_entry = Label(self.addWin, font=('Comic sans ms', 12, 'normal', 'italic'),
                                      text=self.adjust)
                    reg_entry.place(relx=0.38, rely=0.2, width=240)

                    # NAME
                    Label(self.addWin, text='PRODUCT NAME',
                          font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.35)
                    self.name_entry = Entry(self.addWin, state='disabled')

                    for k in query:
                        if self.adjust.upper() in k:
                            self.name_entry.config(state='normal')
                            self.name_entry.insert(0, k[1])
                            qty_before = int(k[4])
                            Label(self.addWin, text=f'QUANTITY NOW: {qty_before}',
                                  font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.48)
                            self.name_entry.config(state='disabled')
                            break
                    self.name_entry.place(relx=0.38, rely=0.35, width=240)

                    # QUANTITY
                    Label(self.addWin, text='ADD STOCK',
                          font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.6)
                    self.qty_entry = Entry(self.addWin, textvariable=self.getQtyA)
                    self.qty_entry.place(relx=0.38, rely=0.6, width=240)

                    def query_update():
                        ID = self.adjust.upper()

                        if str(self.getQtyA.get()).isdigit():
                            STOCK = qty_before + int(self.getQtyA.get())
                        else:
                            STOCK = qty_before
                            messagebox.showerror("Number Only", "Number only except")

                        try:
                            cursor.execute("""UPDATE PRODUCT_DATA
                                                                                                                            SET QUANTITY = ?
                                                                                                                           WHERE 
                                                                                                                                   PRODUCT_ID = ?""",
                                       (STOCK, ID))
                            conn.commit()
                            messagebox.showinfo("SUCCESS", f"ADD INTO {ID} DONE")
                            self.addWin.destroy()


                        except (Exception, sqlite3.Error) as error:
                            messagebox.showerror("FAILED", f"error: {error}")
                            self.addWin.destroy()

                    # add button
                    self.all_button = Button(self.addWin, text='ADD', command=query_update)
                    self.all_button.place(relx=0.5, rely=0.7)

                else:
                    messagebox.showerror("WRONG ID", "PUT THE CORRECT PRODUCT ID")

            else:
                messagebox.showerror("WRONG ID", "ID NOT FOUND")

        except Exception as e:
            messagebox.showwarning("ERROR", f"error: {e}")









if __name__ == '__main__':
    SessionStart().checkServer()
