import tkinter as tk
import tkinter.simpledialog as sd
from tkinter import *
from tkinter.ttk import *
from tkinter.ttk import Style
from tkinter import messagebox
import psycopg2
from datetime import datetime
import pyodbc
import sqlite3
from sys import exit
from server import SERVER_PATH


class AuthDisplay():
    def __init__(self, master):
        self.authWin = master
        self.authWin.resizable(0, 0)
        self.authWin.protocol("WM_DELETE_WINDOW", exit)
        self.windowHeight = int(self.authWin.winfo_reqheight())
        self.windowWidth = int(self.authWin.winfo_reqwidth())
        self.positionRight = int(self.authWin.winfo_screenwidth() / 2 - (self.windowWidth / 2))
        self.positionDown = int(self.authWin.winfo_screenheight() / 2 - (self.windowHeight / 2))
        self.authWin.iconphoto(False, PhotoImage(file='images/rozeriya.png'))
        self.authWin.geometry(f"500x400+{self.positionRight - 200}+{self.positionDown - 100}")
        self.authWin.title("AUTH FORM")
        style = Style()
        style.configure('W.TButton', font=('Comic sans ms', 8, 'normal', 'italic'), foreground='black')
        style1 = 'W.TButton'

        # config
        self.manager = False
        self.supervisor = False

        # background
        background_image = tk.PhotoImage(master=self.authWin, file='images/authBg.png')
        background_label = Label(self.authWin, background='gold', image=background_image)
        background_label.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        Label(self.authWin, text='WELCOME', font=('arial black', 30, 'italic'),
              background='silver', foreground='blue').pack()

        # Button Try Again
        self.again_button = Button(self.authWin, text='Again', command=self.IDscanner, state='disabled', style=style1)
        self.again_button.place(relx=0.75, rely=0.9, anchor='w')

        # Label TAG YOUR ID
        self.tag_ID = Label(self.authWin, text='TAG ID ANDA PADA BARCODE SCANNER',
                            font=('calibri', 18, 'italic', 'bold'),
                            background='silver', foreground='black')
        self.tag_ID.place(relx=0.1, rely=0.4)
        self.authWin.after(1, self.IDscanner)

        self.authWin.mainloop()

    def authConfig(self):
        user = "postgres"
        host = "127.0.0.1"
        port = "1234"
        database = "imposs"
        password = "zerozed020822890013"
        # psycopg2.connect(user=user,
        #                  password=password,
        #                  host=host,
        #                  port=port,
        #                  database=database)


        try:
            self.conn = sqlite3.connect(SERVER_PATH)  #\\Zerozed-pc\shared\DB
            self.cursor = self.conn.cursor()

            self.cursor.execute("SELECT * FROM EMPLOYEE;")
            self.record = self.cursor.fetchall()
            # print("YOU ARE CONNECTED TO DATABASE")      # check connection to database debug
            ID_list = []
            # list the database (EMPLOYEE_ID[0], EMPLOYEE_POS[1], EXIST[2])
            for i in list(self.record):
                for x in i:
                    ID_list.append(str(x))
            self.test = True
        except (Exception, sqlite3.Error) as error:
            print("Error while connecting to database ", error)     # check connection to database debug SHOWED
            self.test = False
            self.found = error
        return ID_list

    def IDscanner(self):
        self.ID_input = sd.askstring('EMPLOYEE ID', 'TAG YOUR ID')
        undetected = Label(self.authWin, text='ID: UNDETECTED', font=('comic sans ms', 18, 'italic', 'bold'),
                           background='silver', foreground='red')
        er = Label(self.authWin, text='Tekan Butang Sekali Lagi', font=('comic sans ms', 10, 'italic', 'bold'),
                   background='silver', foreground='red')
        not_found = Label(self.authWin, text='ID: NOT FOUND', font=('comic sans ms', 18, 'italic', 'bold'),
                          background='silver', foreground='red')
        self.again_button.config(state='disabled')

        try:
            self.pos = ''
            d = datetime.now()
            date = str(d.day) + '/' + str(d.month) + '/' + str(d.year)
            time = str(d.hour) + ':' + str(d.minute) + ':' + str(d.second)
            self.timestamp = d.timestamp()
            print(date + ' ' + time)    # time debug ignore
            data_list = [i.strip(" ") for i in self.authConfig()]
            n = 0
            id_list = []
            for x in data_list:
                if n < len(data_list):
                    id_list.append(data_list[n])
                    n = n + 4  # 3 because the data start at 0 so 0, 1, 2 , 3 <- next id

            # print(str(id_list)) #debug
            if self.ID_input != '' and not None:

                if self.ID_input.upper() in id_list:
                    # print("EXIST")    # debug find existed acc
                    Label(self.authWin, text='                      ' ,
                          font=('comic sans ms', 18, 'italic', 'bold'),
                          background='silver', foreground='green').place(relx=0.3, rely=0.6)    #BLANK SPACE
                    Label(self.authWin, text='ID: ' + self.ID_input.upper(),
                          font=('comic sans ms', 18, 'italic', 'bold'),
                          background='silver', foreground='green').place(relx=0.3, rely=0.6)

                    if data_list[data_list.index(self.ID_input.upper()) + 1] == 'ADMINTESTER' or data_list[
                        data_list.index(self.ID_input.upper()) + 1] == 'MANAGER':
                        self.pos = 'MANAGER'
                        not_found.config(text='')
                        undetected.config(text='')
                        er.config(text='')
                        Label(self.authWin, text='Bersedia untuk menyambung ke MANAGER PAGE',
                              font=('comic sans ms', 14, 'italic', 'bold'),
                              background='blue', foreground='green').place(relx=0, rely=0.8)
                        self.authCache(employee_id=self.ID_input.upper(), date_in=self.timestamp)
                        self.authWin.after(3000, self.authWin.destroy)
                    elif data_list[data_list.index(self.ID_input.upper()) + 1] == 'SUPERVISOR':
                        self.pos ='SUPERVISOR'
                        not_found.config(text='')
                        undetected.config(text='')
                        er.config(text='')
                        Label(self.authWin, text='Bersedia untuk menyambung ke SUPERVISOR PAGE',
                              font=('comic sans ms', 14, 'italic', 'bold'),
                              background='blue', foreground='green').place(relx=0, rely=0.8)
                        self.authCache(employee_id=self.ID_input.upper(), date_in=self.timestamp)
                        self.authWin.after(3000, self.authWin.destroy)
                    else:
                        self.pos = 'EMPLOYEE'
                        not_found.config(text='')
                        undetected.config(text='')
                        er.config(text='')
                        self.authCache(employee_id=self.ID_input.upper(), date_in=self.timestamp)
                        Label(self.authWin, text='Bersedia untuk menyambung ke main page',
                              font=('comic sans ms', 18, 'italic', 'bold'),
                              background='blue', foreground='green').place(relx=0, rely=0.8)
                        self.authWin.after(3000, self.authWin.destroy)
                else:
                    not_found.place(relx=0.3, rely=0.6)
                    self.again_button.config(state='normal')
                    # print("ID NOT FOUND")     #debug not found id
            else:
                undetected.place(relx=0.3, rely=0.6)
                self.again_button.config(state='normal')
                print("False")      #debug False Checked
        except AttributeError as error:
            er.place(relx=0.3, rely=0.6)
            self.again_button.config(state='normal')

    def authCache(self, employee_id='', date_in = ''):
        if self.pos == 'MANAGER':
            try:
                command =""" INSERT INTO AUTH_MANAGER
                            (EMPLOYEE_ID, DATE_IN) VALUES (?,?)
                            """
                data_to_input = (employee_id, date_in)
                self.cursor.execute(command, data_to_input)
                self.conn.commit()
                count = self.cursor.rowcount
                # print(count ," INSERT SUCCESSFUL")    #debug check inserted data
            except (Exception, sqlite3.Error) as error:
                print("Error while connecting to database ", error)
                messagebox.showerror("Database Error",error)
        elif self.pos == 'SUPERVISOR':
            try:
                command =""" INSERT INTO AUTH_SUPERVISOR
                            (EMPLOYEE_ID, DATE_IN) VALUES (?,?)
                            """
                data_to_input = (employee_id, date_in)
                self.cursor.execute(command, data_to_input)
                self.conn.commit()
                count = self.cursor.rowcount
                # print(count ," INSERT SUCCESSFUL")    #debug check inserted data
            except (Exception, sqlite3.Error) as error:
                print("Error while connecting to database ", error)
                messagebox.showerror("Database Error", error)
        elif self.pos == 'EMPLOYEE':
            try:
                command =""" INSERT INTO AUTH_EMPLOYEE
                            (EMPLOYEE_ID, DATE_IN) VALUES (?,?)
                            """
                data_to_input = (employee_id, date_in)
                self.cursor.execute(command, data_to_input)
                self.conn.commit()
                count = self.cursor.rowcount
                # print(count ," INSERT SUCCESSFUL")    #debug check inserted data
            except (Exception, sqlite3.Error) as error:
                print("Error while connecting to database ", error)
                messagebox.showerror("Database Error", error)


#TODO Make a window to show report who are log in with AUTH_MANAGER, AUTH_EMPLOYEE, AUTH_SUPERVISOR


# AuthDisplay(Tk())
