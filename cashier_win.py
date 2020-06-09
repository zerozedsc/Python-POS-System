import errno
import os
import shutil
import sqlite3
import time
import tkinter as tk
import tkinter.simpledialog as sd
from datetime import datetime, date, timedelta
from sys import exit
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from tkinter.ttk import Style
import tkcalendar
import pyttsx3 as tts
from pprint import pprint
import openpyxl as pyxl
import xlrd
from openpyxl.styles import Alignment


# server
from server import SERVER_PATH as PATH


class CashierWin():
    def __init__(self, master, ID=''):
        self.cashWin = master
        self.cashWin.resizable(0, 0)
        self.cashWin.protocol("WM_DELETE_WINDOW", False)
        self.windowHeight = int(self.cashWin.winfo_reqheight())
        self.windowWidth = int(self.cashWin.winfo_reqwidth())
        self.positionRight = int(self.cashWin.winfo_screenwidth() / 2 - (self.windowWidth / 2))
        self.positionDown = int(self.cashWin.winfo_screenheight() / 2 - (self.windowHeight / 2))
        self.cashWin.iconphoto(False, PhotoImage(file='images/rozeriya.png'))
        self.cashWin.geometry(f"1400x800")
        self.cashWin.title("ADMIN FORM")
        style = Style()
        style.configure('W.TButton', font=('Comic sans ms', 15, 'normal', 'italic'), foreground='black')
        style1 = 'W.TButton'

        # Setup Var
        self.IDcashier = ID.upper()
        self.dateNow = datetime.now().strftime("%d/%b/%Y")
        self.n = 0
        self.k = 0
        self.p = 0
        self.d = 0
        self.dbPath = PATH
        self.totalMoney = 0
        self.totalBuy = 0
        self.printIntro = True
        self.buy = []
        self.counting = True
        self.cache_code2 = []
        self.cache_code1 = []
        self.memberDeal = []
        self.calcChoice = True
        self.dealDiscount = 0
        self.memberDiscount = 0
        self.showDiscount = 0

        # TTS
        self.engine = tts.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate', 120)

        # Cashier Name
        def name():
            try:
                conn = sqlite3.connect(PATH)
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM EMPLOYEE_DATA ORDER BY EMPLOYEE_ID;")
                query1 = cursor.fetchall()
                name = []
                for i in query1:
                    for x in i:
                        name.append(str(x))

                cashierName = 'NAME: ' + str(name[name.index(self.IDcashier.upper()) + 1])
                nameLen = len(list(map(len, cashierName)))
                wordLen = list(map(len, cashierName.split(" ")))

                namelbl = Label(self.cashWin, text=cashierName, font=('comic sans ms', 13, 'bold'),
                                foreground='blue')
                namelbl.place(relx=0, rely=0.041)
            except (Exception, sqlite3.Error) as error:
                messagebox.showerror('ERROR', error + ' Please contact Service Team')

        # product detail
        def productDetail(*args):
            conn = sqlite3.connect(self.dbPath)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PRODUCT_DATA ORDER BY PRODUCT_ID;")
            query1 = cursor.fetchall()
            product = []
            for i in query1:
                for x in i:
                    product.append(str(x))

            try:
                self.Qty_entry.config(state='normal')
                self.Price_entry.config(state='normal')
                self.ID_entry.config(state='disabled')
                self.cancelButton.config(state='normal')
                self.Qty_entry.focus_set()
                self.productName = str(product[product.index(self.getPrdID.get()) + 1])
                self.namePrd = Label(self.cashWin, text="Product Name: " + self.productName + "                       ",
                                     font=('comic sans ms', 15, 'bold'))
                self.namePrd.place(relx=0, rely=0.4)
                productQty = int(product[product.index(self.getPrdID.get()) + 4])
                self.qtyPrd = Label(self.cashWin,
                                    text="KUANTITI: " + str(productQty) + "     ",
                                    font=('comic sans ms', 15, 'bold'))
                if productQty <= 20:
                    self.qtyPrd.config(foreground='red')
                    messagebox.showwarning("Stok", "ISI STOK DENGAN SEGERA")
                elif productQty <= 0:

                    self.qtyPrd.config(foreground='red')
                    messagebox.showwarning("Stok", "ITEM SUDAH KEHABISAN STOK")
                self.qtyPrd.place(relx=0, rely=0.45)
                productPrice = float(product[product.index(self.getPrdID.get()) + 3])
                self.getPrdPrice.set(productPrice)

            except:
                self.getPrdID.set('')
                self.Qty_entry.config(state='disabled')
                self.Price_entry.config(state='disabled')
                self.ID_entry.config(state='normal')
                self.cancelButton.config(state='disabled')
                messagebox.showerror("ERROR", "PRODUCT ID NOT FOUND OR ENTRY EMPTY")
                self.ID_entry.focus_force()

        # background
        background_image = tk.PhotoImage(master=self.cashWin, file='images/cashierbg.png')
        background_label = Label(self.cashWin, background='gold', image=background_image)
        background_label.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # ID
        self.idCashlbl = Label(self.cashWin, text='ID: ' + self.IDcashier, font=('comic sans ms', 15, 'bold'),
                               foreground='green')
        self.idCashlbl.place(relx=0, rely=0, width=238)
        name()

        # TIME
        self.timeString = StringVar()
        Label(self.cashWin, text='TIME: ', font=('comic sans ms', 12, 'bold'),
              foreground='black').place(relx=0.6, rely=0.041)
        self.timelbl = Label(self.cashWin, text='', textvariable=self.timeString, font=('comic sans ms', 12, 'bold'),
                             foreground='green')
        self.timelbl.place(relx=0.64, rely=0.041, width=238)
        self.timelbl.after(1, self.updateTime)

        # DATE
        Label(self.cashWin, text='DATE: ' + datetime.now().strftime("%d/%b/%Y"), font=('comic sans ms', 13, 'bold'),
              foreground='black').place(relx=0.6, rely=0.005)

        # back button
        self.backButton = Button(self.cashWin, text='BACK', style=style1, command=self.backChoice)
        self.backButton.place(relx=0.84, rely=0, relwidth=0.08)

        # exit button
        self.exitButton = Button(self.cashWin, text='EXIT', style=style1, command=self.exitWindow)
        self.exitButton.place(relx=0.92, rely=0, relwidth=0.08)

        # total button
        self.totalButton = Button(self.cashWin, text='TOTAL', style=style1, command=self.payWindow)
        self.totalButton.place(relx=0.5, rely=0.95)

        # cancel sale button
        self.cancelSaleButton = Button(self.cashWin, text='SALE CANCEL', style=style1, command=self.saleCancel)
        self.cancelSaleButton.place(relx=0.5, rely=0.85)

        # print report button
        self.printReportButton = Button(self.cashWin, text='REPORT', style=style1, command=self.printExcel)
        self.printReportButton.place(relx=0.5, rely=0.65)

        # add stock button
        self.printReportButton = Button(self.cashWin, text='ADD STOCK', style=style1, command=self.addStockWindow)
        self.printReportButton.place(relx=0.5, rely=0.45)

        # Intro
        self.scrollbar = Scrollbar(self.cashWin)
        # self.scrollbar.place(relx=0.8, rely=0.5, height=400)
        self.outputArea = Text(self.cashWin)
        self.outputArea.config(state='disabled', yscrollcommand=self.scrollbar.set)
        self.outputArea.place(relx=0.6, rely=0.2, relwidth=0.4, relheight=0.15)

        # Treeview buy
        cols = ('ID', 'PRODUK', 'QTY', 'HARGA', 'TOTAL', 'OFF')
        self.buyScreen = Treeview(self.cashWin, columns=cols, show='headings')
        i = 0
        for col in cols:
            i = i + 1
            if i == 1:
                self.buyScreen.heading(col, text=col, )
                self.buyScreen.column(col, minwidth=0, width=130, stretch=False)
            elif i == 2:
                self.buyScreen.heading(col, text=col, )
                self.buyScreen.column(col, minwidth=0, width=210, stretch=False)
            elif i == 3:
                self.buyScreen.heading(col, text=col, )
                self.buyScreen.column(col, minwidth=0, width=35, stretch=False)
            elif i == 4:
                self.buyScreen.heading(col, text=col, )
                self.buyScreen.column(col, minwidth=0, width=65, stretch=False)
            elif i == 5:
                self.buyScreen.heading(col, text=col, )
                self.buyScreen.column(col, minwidth=0, width=65, stretch=False)
            elif i == 6:
                self.buyScreen.heading(col, text=col, )
                self.buyScreen.column(col, minwidth=0, width=65, stretch=False)

        # insert to buy

        self.buyScreen.place(relx=0.6, rely=0.35, relwidth=0.4, relheight=0.35)
        vsb = Scrollbar(self.cashWin, orient="vertical", command=self.buyScreen.yview)
        # vsb.place(relx=0.98, rely=0.1, relheight=0.5)
        hrz = Scrollbar(self.cashWin, orient="horizontal", command=self.buyScreen.xview)
        # hrz.place(relx=0.6, rely=0.7, relwidth=0.4)
        self.buyScreen.configure(yscrollcommand=vsb.set, xscrollcommand=hrz.set)

        # TOTAL PRICE
        self.scrollbarPrice = Scrollbar(self.cashWin)
        # self.scrollbar.place(relx=0.8, rely=0.5, height=400)
        self.totalPrice = Text(self.cashWin)
        self.totalPrice.config(state='disabled', yscrollcommand=self.scrollbarPrice.set)
        self.totalPrice.place(relx=0.6, rely=0.7, relwidth=0.4, relheight=0.35)

        # PRODUCT ID
        self.getPrdID = StringVar()
        Label(self.cashWin, text="ID", font=('arial', 15, 'bold')).place(relx=0, rely=0.28)
        self.ID_entry = Entry(self.cashWin, textvariable=self.getPrdID, font=('comic sans ms', 12, 'bold'))
        self.ID_entry.place(relx=0, rely=0.32, height=30, width=200)
        self.ID_entry.focus_set()

        # QUANTITY
        self.getPrdQty = IntVar()
        Label(self.cashWin, text="QTY", font=('arial', 15, 'bold')).place(relx=0.18, rely=0.28)
        self.Qty_entry = Entry(self.cashWin, textvariable=self.getPrdQty, font=('comic sans ms', 12, 'bold'),
                               state='disabled')
        self.Qty_entry.place(relx=0.18, rely=0.32, height=30, width=50)

        def q(*args):
            self.Qty_entry.selection_range(0, END)

        self.Qty_entry.bind("<FocusIn>", q)

        # PRICE
        self.getPrdPrice = DoubleVar()
        Label(self.cashWin, text="PRICE", font=('arial', 15, 'bold')).place(relx=0.25, rely=0.28)
        self.Price_entry = Entry(self.cashWin, textvariable=self.getPrdPrice, font=('comic sans ms', 12, 'bold'),
                                 state='disabled')
        self.Price_entry.place(relx=0.25, rely=0.32, height=30, width=100)

        def a(*args):
            self.Price_entry.selection_range(0, END)

        self.Price_entry.bind("<FocusIn>", a)

        self.ID_entry.bind("<Return>", productDetail)
        self.cashWin.bind("<Return>", self.insertBuy)

        # cancel button
        self.cancelButton = Button(self.cashWin, text='cancel', command=self.cancel, state='disabled')
        self.cancelButton.place(relx=0.35, rely=0.32)

        # buy count and total money
        Label(self.cashWin, text="TOTAL TODAY: RM" + str(self.totalMoney), font=('comic sans ms', 15, 'bold')).place(
            relx=0.6, rely=0.15)
        Label(self.cashWin, text="SALE NO: " + str(self.n), font=('comic sans ms', 15, 'bold')).place(relx=0.85,
                                                                                                      rely=0.15)

        # MEMBERCARD ENTRY AND DEAL ENTRY
        self.getMemberID = StringVar()
        Label(self.cashWin, text="MEMBERCARD ID", font=('arial', 15, 'bold')).place(relx=0, rely=0.78)
        self.member_entry = Entry(self.cashWin, textvariable=self.getMemberID, font=('comic sans ms', 12, 'bold'),
                                  state='normal')
        self.member_entry.place(relx=0, rely=0.82, height=30, width=180)

        def c(*args):
            if self.getMemberID.get() != '' and len(self.memberDeal) != 1:
                self.memberDeal.append(self.getMemberID.get())
                self.member_entry.delete(0, END)
                messagebox.showinfo("SUCESS", "MEMBER ID ENTERED")
            else:
                messagebox.showwarning("EMPTY", "EMPTY ENTRY OR MEMBER ID EXIST")



        self.member_entry.bind("<Return>", c)


        self.cashWin.mainloop()

    # receipt
    def receiptIntro(self):
        dirname = "data/Receipt Data/" + str(date.today())  # "//Zerozed-pc/shared/DB/temp/resit.txt"
        try:
            # Create target Directory
            os.mkdir(dirname)
            print("Directory ", dirname, " Created ")  # debug check directory created
        except FileExistsError:
            # print("Directory ", dirname, " already exists")     #debug check dir exists
            pass

        if self.counting == True:
            self.n = self.n + 1
            self.p = self.p + 1
        self.outputArea.config(state='normal', yscrollcommand=self.scrollbar.set)
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM EMPLOYEE_DATA ORDER BY EMPLOYEE_ID;")
        query1 = cursor.fetchall()
        name = []
        for i in query1:
            for x in i:
                name.append(str(x))

        cashierName = 'NAME: ' + str(name[name.index(self.IDcashier) + 1])
        nameLen = len(list(map(len, cashierName)))
        wordLen = list(map(len, cashierName.split(" ")))
        # print(wordLen)
        # print(self.n, self.p, self.k)
        self.sellID = 'RZ0000S00' + str(self.p)
        if self.n >= 10:
            self.sellID = 'RZ0000S0' + str(self.p)
        if self.n >= 100:
            self.sellID = 'RZ0000S' + str(self.p)
            if self.p == 1000:
                self.k = self.k + 1
                self.p = 0
        if self.n >= 1000:
            if self.p == 1000:
                self.k = self.k + 1
                self.p = 0
            self.sellID = 'RZ000' + str(self.k) + 'S' + str(self.p)
        if self.n >= 10000:
            if self.p == 1000:
                self.k = self.k + 1
                self.p = 0
            self.sellID = 'RZ00' + str(self.k) + 'S' + str(self.p)
        if self.n >= 100000:
            if self.p == 1000:
                self.k = self.k + 1
                self.p = 0
            self.sellID = 'RZ0' + str(self.k) + 'S' + str(self.p)
        if self.n >= 100000:
            if self.p == 1000:
                self.k = self.k + 1
                self.p = 0
            self.sellID = 'RZ' + str(self.k) + 'S' + str(self.p) + "\n"
        self.counting = True

        self.filename = dirname + "/" + str(self.sellID) + ".txt"  # "//Zerozed-pc/shared/DB/temp/resit.txt"
        if not os.path.exists(os.path.dirname(self.filename)):
            try:
                os.makedirs(os.path.dirname(self.filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        # print(self.n, '', self.sellID)

        def insertData():
            intro = """ROZERIYA ENTERPRISE\nTEL +60172208214""" + \
                    "\n__________________________________________________________" \
                    ""
            resitComp = """__________________________________\n
item\t       Qty   S/Price   Total  Off"""  # 2/slash

            self.outputArea.insert(1.0, intro, 'CENTER')
            date = f"DATE&TIME: {str(self.dateNow)} {str(time.strftime('%H:%M:%S%p'))} \n"
            self.outputArea.insert(INSERT, "")
            self.outputArea.insert(INSERT, f"\nID:{self.IDcashier}\n")
            self.outputArea.insert(INSERT, f"CASHIER:{str(name[name.index(self.IDcashier) + 1])}\n")
            self.outputArea.insert(INSERT, date)
            self.outputArea.insert(INSERT, f"SELL ID:{self.sellID}\n")
            self.outputArea.insert(INSERT, resitComp)
            self.outputArea.config(state='disabled', yscrollcommand=self.scrollbar.set)
            self.introGet = self.outputArea.get(1.0, END)
            with open(self.filename, "w") as f:
                f.write(self.introGet)
                f.close()

        # print(self.outputArea.get(1.0, END))
        insertData()
        # print(self.outputArea.get(1.0, END))

    # total SEND
    def payWindow(self):

        def paying():
            try:
                for i in self.buyScreen.get_children():
                    pass
                if i is not None:
                    self.totalCalc()
                    self.payWin = Toplevel(self.cashWin)
                    self.payWin.lift(aboveThis=self.cashWin)
                    self.payWin.resizable(0, 0)
                    self.payWin.protocol("WM_DELETE_WINDOW", False)
                    self.payWin.iconphoto(False, PhotoImage(file='images/rozeriya.png'))
                    self.payWin.geometry(f"800x500")
                    self.payWin.title("ADMIN FORM")
                    style = Style()
                    style.configure('Fun.TButton', font=('arial', 12, 'normal', 'italic'), foreground='black')
                    style1 = 'Fun.TButton'
                    # background
                    # background_image = tk.PhotoImage(master=self.payWin, file='images/cashierbg.png')
                    background_label = Label(self.payWin, background='silver')
                    # background_label.image = background_image
                    background_label.place(x=0, y=0, relwidth=1, relheight=1)

                    # main frame
                    payFrame = Frame(self.payWin)
                    payFrame.place(relheight=1, relwidth=0.8, relx=0.2)
                    payFrame_bg = Label(payFrame, background='dark blue')
                    payFrame_bg.place(x=0, y=0, relwidth=1, relheight=1)

                    def cash():

                        filename = self.filename  # "//Zerozed-pc/shared/DB/temp/resit.txt"
                        if not os.path.exists(os.path.dirname(filename)):
                            try:
                                os.makedirs(os.path.dirname(filename))
                            except OSError as exc:  # Guard against race condition
                                if exc.errno != errno.EEXIST:
                                    raise
                        Label(payFrame, text="TOTAL:RM" + str(self.actualTotal),
                              font=('comic sans ms', 18, 'bold')).place(relx=0.35, rely=0.15)
                        self.getCash = DoubleVar()
                        Label(payFrame, text="RM:", font=('arial', 20, 'bold')).place(relx=0.15, rely=0.35)
                        self.payCash_entry = Entry(payFrame, textvariable=self.getCash,
                                                   font=('comic sans ms', 20, 'bold'),
                                                   state='enabled')
                        self.payCash_entry.place(relx=0.25, rely=0.35, height=30, width=200)
                        self.payCash_entry.focus_set()
                        self.engine.say(f"Your Total is RM {self.actualTotal}")
                        self.engine.runAndWait()

                        def a(*args):
                            if self.getCash.get() >= self.actualTotal:
                                calcChange = round(self.getCash.get(), 2) - self.actualTotal
                                self.totalPrice.config(state='normal', yscrollcommand=self.scrollbarPrice.set)
                                self.totalPrice.insert(INSERT, f"CASH \t=\tRM{self.getCash.get()}\n")
                                self.totalPrice.insert(INSERT, f"CHANGE\t=\tRM{round(calcChange, 2)}\n")
                                self.totalPrice.insert(INSERT, f"\nTerima Kasih")
                                self.totalGet = self.totalPrice.get(1.0, END)
                                self.totalPrice.config(state='disabled', yscrollcommand=self.scrollbarPrice.set)
                                with open(filename, "a") as f:
                                    f.write(self.totalGet)
                                    f.close()
                                self.totalCmd()
                                self.payWin.destroy()
                                self.saveExcel()  # save at excel
                                self.cache_code2.clear()
                                self.d = 0
                                self.fix_count = 0
                                self.totalMoney = self.totalMoney + self.actualTotal
                                Label(self.cashWin, text="TOTAL TODAY: RM" + str(self.totalMoney),
                                      font=('comic sans ms', 15, 'bold')).place(
                                    relx=0.6, rely=0.15)
                            else:
                                messagebox.showwarning("less cash", "cash is not enough")
                                self.payWin.lift(aboveThis=self.cashWin)

                        self.payCash_entry.bind("<Return>", a)

                        def b(*args):
                            self.payCash_entry.selection_range(0, END)

                        self.payCash_entry.bind("<FocusIn>", b)

                    def back():
                        self.totalPrice.config(state='normal', yscrollcommand=self.scrollbarPrice.set)
                        self.totalPrice.delete(1.0, END)
                        self.totalPrice.config(state='disabled', yscrollcommand=self.scrollbarPrice.set)
                        self.payWin.destroy()

                    # CASH BUTTON
                    self.payCash_Button = Button(self.payWin, text='CASH', command=cash, state='enabled', style=style1)
                    self.payCash_Button.place(relx=0, rely=0.15, height=50, width=160)

                    # CARD BUTTON
                    self.payCard_Button = Button(self.payWin, text='''CREDIT/DEBIT\nCARD''', command=None,
                                                 state='disabled', style=style1)
                    self.payCard_Button.place(relx=0, rely=0.3, height=50, width=160)

                    # CHEQUE BUTTON
                    self.payCheque_Button = Button(self.payWin, text='CHEQUE', command=None, state='disabled',
                                                   style=style1)
                    self.payCheque_Button.place(relx=0, rely=0.45, height=50, width=160)

                    # CHEQUE BUTTON
                    self.payInstallment_Button = Button(self.payWin, text='INSTALLMENT', command=None, state='disabled',
                                                        style=style1)
                    self.payInstallment_Button.place(relx=0, rely=0.6, height=50, width=160)

                    # BACK BUTTOn
                    self.backPayWin_Button = Button(self.payWin, text='BACK', command=back, state='normal',
                                                    style=style1)
                    self.backPayWin_Button.place(relx=0, rely=0.75, height=50, width=160)
                else:
                    messagebox.showwarning("SALE INPUT", "NO SALE INPUT TO TOTAL")
            except:
                messagebox.showwarning("SALE INPUT", "NO SALE INPUT TO TOTAL")

        try:
            for i in self.buyScreen.get_children():
                pass
            if i is not None:
                if len(self.memberDeal) == 0 or len(self.memberDeal) == 1:
                    if len(self.memberDeal) == 0:
                        findMember = messagebox.askquestion("MEMBER ID", "MEMBER ID?", icon='info')
                        if findMember == 'yes':
                            findMemberID = sd.askstring(title="MEMBER ID ", prompt="INSERT MEMBER ID")
                            self.memberDeal.append(str(findMemberID))

                    # findDeal = messagebox.askquestion("DEAL ID", "DEAL ID?", icon='info')
                    # if findDeal == 'yes':
                    #     findDealID = sd.askstring(title="DEAL ID ", prompt="INSERT DEAL ID")
                    #     if len(self.memberDeal) == 0:
                    #         self.memberDeal.append("")
                    #     self.memberDeal.append(str(findDealID))
                    # for i in range(2):
                    #     if self.memberDeal != 2:
                    #         self.memberDeal.append("")

                # print(self.memberDeal)    #debug
                self.fixBuyScreen()
                paying()


            else:
                messagebox.showwarning("SALE INPUT", "NO SALE INPUT TO TOTAL Else")
        except Exception as e:
            messagebox.showwarning("SALE INPUT", e)

    def totalCmd(self):
        def printResult():
            result = messagebox.askquestion("RECEIPT", "Print The Receipt?", icon='info')
            if result == 'yes':
                # print("sent to the printer")  #debug
                self.outputArea.config(state='normal')
                self.outputArea.delete(1.0, END)
                self.outputArea.config(state='disabled', yscrollcommand=self.scrollbar.set)
                self.totalPrice.config(state='normal', yscrollcommand=self.scrollbarPrice.set)
                self.totalPrice.delete(1.0, END)
                self.totalPrice.config(state='disabled', yscrollcommand=self.scrollbarPrice.set)
                for i in self.buyScreen.get_children():
                    self.buyScreen.delete(i)
                printfile = os.path.abspath(self.filename)
                try:
                    os.startfile(rf"{printfile}", 'print')
                except Exception as error:
                    messagebox.showerror("Printer error", error)
                self.engine.say("Thank you for buying, and please come again")
                self.engine.runAndWait()
            else:
                # print("not sent to the printer")    #debug not sent to the Printer
                self.outputArea.config(state='normal')
                self.outputArea.delete(1.0, END)
                self.outputArea.config(state='disabled', yscrollcommand=self.scrollbar.set)
                self.totalPrice.config(state='normal', yscrollcommand=self.scrollbarPrice.set)
                self.totalPrice.delete(1.0, END)
                for i in self.buyScreen.get_children():
                    self.buyScreen.delete(i)
                self.totalPrice.config(state='disabled', yscrollcommand=self.scrollbarPrice.set)
                self.engine.say("Thank you for buying, and please come again")
                self.engine.runAndWait()

        self.ID_entry.focus_set()
        self.updateDb()
        self.printIntro = True
        self.counting = True
        Label(self.cashWin, text="SALE NO: " + str(self.n), font=('comic sans ms', 15, 'bold')).place(relx=0.85,
                                                                                                      rely=0.15)
        self.buy.clear()
        self.memberDeal.clear()
        self.outputArea.after(1000, printResult)

    # insert, cancel and calc config
    def insertBuy(self, *args):
        self.showDiscount = 0
        try:
            if self.printIntro is True:
                self.receiptIntro()
                self.printIntro = False
            if self.getPrdQty.get() != 0 and self.getPrdID != '':
                # print("PRODUCT INSERT")   #debug check product insert
                self.ID_entry.focus_set()
                priceRound = round(float(self.getPrdPrice.get()), 2)
                self.calc = self.getPrdQty.get() * round(self.getPrdPrice.get(), 2)
                self.deals()
                self.buyScreen.insert("", END,
                                      values=(
                                          self.getPrdID.get(), self.productName, int(self.getPrdQty.get()),
                                          str(priceRound),
                                          str(round(self.calc, 2)), self.showDiscount))
                self.buy.append(str(self.getPrdID.get()))
                self.buy.append(str(self.getPrdQty.get()))
                self.cancel()

            else:
                print(" ")  # debug blank

        except Exception as e:
            messagebox.showerror("WRONG INPUT", "TRY AGAIN")
            print(e)

    def totalCalc(self, *args):
        filename = self.filename
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        component = []
        test = ''
        totalPrice = 0.00
        for child in self.buyScreen.get_children():
            component.append(float(self.buyScreen.item(child)["values"][4]) + float(self.buyScreen.item(child)["values"][5]))
        for i in component:
            # print(component)  #debug
            totalPrice += float(i)
        calcRounding = round(totalPrice - round(totalPrice, 1), 2)
        if calcRounding < 0:
            a = ''
        else:
            a = '-'
        self.totalPrice.config(state='normal', yscrollcommand=self.scrollbarPrice.set)
        self.totalPrice.insert(INSERT, f"\nSUBTOTAL: \tRM{totalPrice}\n")
        self.totalPrice.insert(INSERT, f"ROUNDING:\tRM{a}{calcRounding}\n")
        self.totalPrice.insert(INSERT, "========================================\n ")
        tax = open("data/tax.cfg")
        n = ''
        for i in tax.read():
            n = n + i
        self.actualTotal = totalPrice - calcRounding - self.dealDiscount
        self.totalPrice.insert(INSERT, f"\nTAX: {n} %\n")
        self.totalPrice.insert(INSERT, f"DISCOUNT =\t-RM{self.dealDiscount}\n")
        self.totalPrice.insert(INSERT, f"TOTAL\t=\tRM{round(self.actualTotal, 2)}\n")
        # self.totalPrice.insert(INSERT, f"MEMBER ID:{self.memberCard()}\n")
        self.totalPrice.config(state='disabled', yscrollcommand=self.scrollbarPrice.set)

        self.dealDiscount = 0

    def updateDb(self, *args):
        n = 0
        p = 1
        from data.callDB import callDB
        # print(self.buy)   #debug
        for i in range(0, len(self.buy)):
            if len(self.buy) > n:
                db = callDB()
                db.cursor.execute(f"SELECT QUANTITY FROM PRODUCT_DATA WHERE PRODUCT_ID = '{self.buy[n]}'")
                db.conn.commit()
                rawValue = db.cursor.fetchone()
                for i in rawValue:
                    count = int(i) - int(self.buy[p])
                db.cursor.execute(f"UPDATE PRODUCT_DATA SET QUANTITY=? WHERE PRODUCT_ID = ?", (count, self.buy[n],))
                db.conn.commit()
                p = p + 2
                n = n + 2

    def saleCancel(self):
        self.ID_entry.focus_set()
        self.counting = False
        self.fix_count = 0
        self.cache_code2 = []
        try:
            for i in self.buyScreen.get_children():
                self.buyScreen.delete(i)
            if i is not None:
                self.memberDeal.clear()
                self.outputArea.config(state='normal')
                self.outputArea.delete(1.0, END)
                self.outputArea.config(state='disabled', yscrollcommand=self.scrollbar.set)
                self.totalPrice.config(state='normal', yscrollcommand=self.scrollbarPrice.set)
                self.totalPrice.delete(1.0, END)
                self.totalPrice.config(state='disabled', yscrollcommand=self.scrollbarPrice.set)
                self.printIntro = True
            else:
                messagebox.showwarning("SALE INPUT", "NO SALE INPUT TO DELETE")
        except:
            messagebox.showwarning("SALE INPUT", "NO SALE INPUT TO DELETE")

    def addStockWindow(self):
        conn = sqlite3.connect(PATH)  # \\Zerozed-pc\shared\DB
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PRODUCT_DATA ORDER BY PRODUCT_ID;")
        query = cursor.fetchall()
        # pprint(query) #debug

        try:
            self.adjust = sd.askstring('REGISTER ITEM', f'PRODUCT ID ')

            if self.adjust is None:
                pass
            else:
                for i in query:
                    if self.adjust.upper() in i:
                        check_productID = self.adjust.upper()
                        break

                if self.adjust.upper() in check_productID:
                    if "RZ" and 'P' in self.adjust.upper() or len(self.adjust) >= 10:
                        self.addWin = Toplevel(self.cashWin)
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
                        self.ID_entry.focus_force()

                    else:
                        messagebox.showerror("WRONG ID", "PUT THE CORRECT PRODUCT ID")



                else:
                    messagebox.showerror("WRONG ID", "ID NOT FOUND")

        except Exception as e:
            messagebox.showwarning("ERROR", f"error: {e}")

    # data manipulate config
    def memberCard(self, *args, id=''):
        if id == '':
            pass
        else:
            try:
                try:
                    from data.callDB import callDB
                    db = callDB()
                    db.cursor.execute(f"SELECT * FROM MEMBER WHERE MEMBER_ID = '{id}'")
                    db.conn.commit()
                    rawValue = db.cursor.fetchone()

                    # print(rawValue)   #debug Search rawValue

                    # 3 types of members Premium, Gold, Bronze
                    # premium discount -
                    # gold discount -
                    # bronze discount -

                    def Premium():
                        print("premium member")  # debug

                        rawItem = []
                        getType = []  # [0] id, [1] quantity,[2] price ,[3] total
                        n = 0
                        p = 0
                        for child in self.buyScreen.get_children():
                            for i in self.buyScreen.item(child)["values"]:
                                rawItem.append(i)
                        for a in range(0, len(rawItem)):
                            if len(rawItem) > n:
                                db.cursor.execute(f"SELECT * FROM PRODUCT WHERE PRODUCT_ID = '{rawItem[n]}'")
                                db.conn.commit()

                    try:
                        if rawValue[1] == "PREMIUM":
                            Premium()
                    except:
                        messagebox.showerror("MEMBER ID", "MEMBER ID NOT FOUND")


                except Exception as e:
                    messagebox.showerror("ERROR", f"MEMBER ID NOT FOUND")
            except Exception as e:
                messagebox.showerror("ERROR", f"ERROR: {e}")

    def deals(self, *args):  # remove old def deals
        from data.callDB import callDB
        db = callDB()

        def checkDeals(id='', type=''):
            db.cursor.execute(f"SELECT * FROM DEAL_DATA WHERE DEAL_ID = '{id}'")
            db.conn.commit()
            rawValue = db.cursor.fetchone()

            # print(rawValue)   #debug

            #@ BELI X DAPAT Y
            def CODE1():
                try:
                    if 'BELI' in str(rawValue[6]) and 'MANA' in str(rawValue[6]) and 'DAPAT' in str(rawValue[6]):
                        # print("CODE 1")   #debug Check Code
                        rawItem = [self.getPrdID.get(), self.productName, str(self.getPrdQty.get()),
                                   str(round(float(self.getPrdPrice.get()), 2)),
                                   str(self.getPrdQty.get() * round(self.getPrdPrice.get(), 2))]
                        getType = []  # [0] id, [1] quantity,[2] price ,[3] total
                        n = 0
                        p = 0

                        for a in range(0, len(rawItem)):
                            if len(rawItem) > n:
                                db.cursor.execute(f"SELECT * FROM PRODUCT WHERE PRODUCT_ID = '{rawItem[n]}'")
                                db.conn.commit()
                                # rawValue[1] = product_types, rawValue[2] = product_name
                                if rawValue[2] != None:
                                    if db.cursor.fetchone()[1] == str(rawValue[2]):
                                        getType.append(rawItem[n])
                                        getType.append(rawItem[n + 2])

                                elif rawValue[1] != None:
                                    if db.cursor.fetchone()[1] == str(rawValue[1]):
                                        # print(db.cursor.fetchall())   #check db fetchall
                                        getType.append(rawItem[n])  # prd id
                                        getType.append(rawItem[n + 2])  # prd qty
                                        getType.append(rawItem[n + 3])  # prd price
                                        getType.append(rawItem[n + 4])  # prd total

                                n = n + 5

                        # print(getType)    #debug check type
                        # if getType == []:
                        #     print(False)
                        n = 0
                        search_x = 0
                        for i in range(0, len(getType)):
                            if len(getType) > n:
                                print('buy 3 :', getType[n + 1])
                                p = p + int(getType[n + 1])
                                n = n + 4

                        x = int(rawValue[3])
                        y = float(rawValue[4])
                        toDiscount = (p - (p % x))
                        if toDiscount == 0:
                            self.cache_code1.append([self.getPrdID.get(), self.getPrdQty.get()])
                            for i in self.cache_code1:
                                search_x += int(i[1])
                                print(search_x)
                                if search_x > x:
                                    toDiscount = (search_x - (search_x % x))
                                    code1Discount = (toDiscount / x) * ((float(getType[2]) * x) - y)
                                    self.showDiscount = code1Discount
                                    self.cache_code1.clear()
                                    self.cache_code1.append([self.getPrdID.get(), search_x-x])
                                if search_x == x:
                                    toDiscount = (search_x - (search_x % x))
                                    code1Discount = (toDiscount / x) * ((float(getType[2]) * x) - y)
                                    self.showDiscount = code1Discount
                                    self.cache_code1.clear()
                        elif toDiscount == p:
                            code1Discount = (toDiscount / x) * ((float(getType[2]) * x) - y)
                            self.showDiscount = code1Discount
                        else:
                            self.cache_code1.append([self.getPrdID.get(), p])
                            for i in self.cache_code1:
                                search_x += int(i[1])
                                print(search_x)
                                if search_x > x:
                                    toDiscount = (search_x - (search_x % x))
                                    code1Discount = (toDiscount / x) * ((float(getType[2]) * x) - y)
                                    self.showDiscount = code1Discount
                                    self.cache_code1.clear()
                                    self.cache_code1.append([self.getPrdID.get(), search_x-x])
                                if search_x == x:
                                    toDiscount = (search_x - (search_x % x))
                                    code1Discount = (toDiscount / x) * ((float(getType[2]) * x) - y)
                                    self.showDiscount = code1Discount
                                    self.cache_code1.clear()

                        print(self.cache_code1)
                        # print(f"n {n}, p {p}, x {x}, y {y}")
                        # print(f"Discount: {code1Discount}, toDiscount: {toDiscount}")
                        # print(code1Discount,'BELI ' + str(x) ,'DAPAT ' + str(y))  #debug Tell About The Code

                    else:
                        # print("find 1 else")   #debug
                        pass
                except Exception as e:
                    # print("find 1 : ", e)  # debug
                    pass

            #@ BELI LEBIH X 1 DAPAT Y
            def CODE2():
                try:
                    if 'LEBIH' in str(rawValue[6]) and 'DAPAT' in str(rawValue[6]):
                        # print("CODE 2")   #debug
                        rawItem = [self.getPrdID.get(), self.productName, str(self.getPrdQty.get()),
                                   str(round(float(self.getPrdPrice.get()), 2)),
                                   str(self.getPrdQty.get() * round(self.getPrdPrice.get(), 2))]
                        getType = []  # [0] id, [1] quantity,[2] price ,[3] total
                        n = 0
                        p = 0

                        for a in range(0, len(rawItem)):
                            if len(rawItem) > n:
                                db.cursor.execute(f"SELECT * FROM PRODUCT WHERE PRODUCT_ID = '{rawItem[n]}'")
                                db.conn.commit()
                                # rawValue[1] = product_types, rawValue[2] = product_name
                                if rawValue[2] != None:
                                    if db.cursor.fetchone()[1] == str(rawValue[2]):
                                        getType.append(rawItem[n])
                                        getType.append(rawItem[n + 2])

                                elif rawValue[1] != None:
                                    if db.cursor.fetchone()[1] == str(rawValue[1]):
                                        # print(db.cursor.fetchall())   #debug fetchall
                                        getType.append(rawItem[n])  # prd id
                                        getType.append(rawItem[n + 2])  # prd qty
                                        getType.append(rawItem[n + 3])  # prd price
                                        getType.append(rawItem[n + 4])  # prd total

                                n = n + 5

                        # print(getType)    #debug
                        n = 0
                        for i in range(0, len(getType)):
                            if len(getType) > n:
                                p += int(getType[n + 1])
                                n = n + 4


                        k = 0
                        x = int(rawValue[3])
                        y = float(rawValue[4])


                        for c in self.cache_code2:
                            # print('RUN FOR ', type)
                            if type in c:
                                if self.cache_code2[self.cache_code2.index(c)][1] == 'end':
                                    k = k + (float(getType[2]) - y)
                                    toDiscount = k * int(getType[1])
                                    # print(code1Discount, 'LEBIH ' + str(x), '1 DAPAT ' + str(y))  #debug
                                    self.showDiscount = toDiscount
                                    # self.dealDiscount += toDiscount
                                    break

                                else:

                                    self.cache_code2[self.cache_code2.index(c)][1] += int(getType[1])



                                if p >= x or int(self.cache_code2[self.cache_code2.index(c)][1]) >= x:
                                    k = k + (float(getType[2]) - y)
                                    toDiscount = k * int(getType[1])
                                    # print(code1Discount, 'LEBIH ' + str(x), '1 DAPAT ' + str(y))  #debug
                                    self.showDiscount = toDiscount
                                    # self.dealDiscount += toDiscount
                                    if int(self.cache_code2[self.cache_code2.index(c)][1]) >= x:
                                        self.cache_code2[self.cache_code2.index(c)][1] = 'end'
                                    break

                                else:
                                    k = k + (float(getType[2]) - y)
                                    self.cache_code2.append([self.getPrdID.get(), k*int(getType[1])])
                                    break

                            else:
                                pass




                    else:
                        # print("find 2 else")    #debug
                        pass
                except Exception as e:
                    # print(n, k, x, y)   #debug Show n, x, k, y value Ignored
                    # print('find 2 :', e)  # debug
                    pass


            CODE1()
            CODE2()


        try:
            db.cursor.execute(f"SELECT * FROM DEAL")
            db.conn.commit()
            rawValue = db.cursor.fetchall()
            db.cursor.execute(f"SELECT * FROM PRODUCT_DATA WHERE PRODUCT_ID = '{self.getPrdID.get()}'")
            db.conn.commit()
            catch_data = db.cursor.fetchone()
            # print(rawValue)   #debug
            # print(catch_data)

            for i in rawValue:
                if catch_data[2] in i:
                    if self.cache_code2 == []:
                        self.cache_code2.append([catch_data[2], 0])
                    for cache in self.cache_code2:
                        if catch_data[2] in cache:
                            break
                        else:
                            self.cache_code2.append([catch_data[2], 0])
                            break

                    # print("found", self.cache_code2)
                    checkDeals(i[0], catch_data[2])
                    break

                #TODO Need to fix more, slack everywhere




        except Exception as e:
            messagebox.showerror("ERROR", f"ERROR: {e}")

    def fixBuyScreen(self):
        base = []
        calc_disc = []
        for child in self.buyScreen.get_children():
            base.append([self.buyScreen.item(child)["values"][i] for i in range(6)])
            self.buyScreen.delete(child)

        for i in base:
            for k in self.cache_code2:
                if str(k[0]) in str(i[0]):
                    if base[base.index(i)][5] == 0:
                        base[base.index(i)][5] = float(k[1])
                        self.cache_code2.pop(self.cache_code2.index(k))


            base[base.index(i)][4] = float(base[base.index(i)][4]) - float(base[base.index(i)][5])

        for g in base:
            for p in base:
                if base[base.index(g)] == base[base.index(p)]:
                    pass
                elif g[0] in base[base.index(p)]:
                    base[base.index(g)][5] = float(base[base.index(g)][5]) + float(base[base.index(p)][5])
                    base[base.index(g)][4] = float(base[base.index(g)][4]) + float(base[base.index(p)][4])
                    base[base.index(g)][2] = int(base[base.index(g)][2]) + int(base[base.index(p)][2])
                    base.pop(base.index(p))
                    # print(base)   #debug

        for t in base:
            self.buyScreen.insert("", END, value=t)

        for child1 in self.buyScreen.get_children():
            calc_disc.append([self.buyScreen.item(child1)["values"][i] for i in range(6)])

        for k in calc_disc:
            with open(self.filename, "a") as f:
                productApd = f"""{calc_disc[calc_disc.index(k)][1]}\n{calc_disc[calc_disc.index(k)][0]}  {str(calc_disc[calc_disc.index(k)][2])}  RM{calc_disc[calc_disc.index(k)][3]}  RM{calc_disc[calc_disc.index(k)][4]} -{calc_disc[calc_disc.index(k)][5]}\n"""
                f.write(productApd)
                f.close()
            self.dealDiscount += float(k[5])
        # pprint(base)
        # pprint(self.cache_code2)  #debug

    # misc config
    def updateTime(self):
        self.timeGet = time.strftime('%H:%M:%S %p')
        self.timeString.set(self.timeGet)
        self.timelbl.after(1000, self.updateTime)

    def cancel(self, *args):
        self.Qty_entry.config(state='disabled')
        self.Price_entry.config(state='disabled')
        self.ID_entry.config(state='normal')
        self.ID_entry.focus_set()
        self.namePrd.destroy()
        self.qtyPrd.destroy()
        self.cancelButton.config(state='disabled')
        self.getPrdID.set('')
        self.getPrdPrice.set(0)
        self.getPrdQty.set(0)
        # print("destroy")  #debug

    def backChoice(self):
        # print("Back") #debug
        self.checkExcel()
        self.saveExit()
        from session_start import SessionStart
        self.cashWin.destroy()
        start_choice = SessionStart().auth(Tk())
        return start_choice

    def exitWindow(self):
        self.checkExcel()
        self.saveExit()
        exit()

    # report GET
    def saveExcel(self):
        try:

            SAVE_PATH = 'data/Report Data/'
            BASE_FILE = SAVE_PATH + '/daily_report_example.xlsx'
            EXCEL_FILE = SAVE_PATH + str(date.today()) + '.xlsx'
            base = []

            # Precaution if BASE_FILE not found
            if not os.path.exists(os.path.abspath(BASE_FILE)):
                try:
                    wb = pyxl.Workbook()
                    ws = wb.active
                    ws.sheet_view.showGridLines = True
                    ws.title = "MAIN"
                    ws.column_dimensions['A'].width = 20
                    ws.column_dimensions['B'].width = 30
                    ws.column_dimensions['C'].width = 10
                    ws.column_dimensions['D'].width = 10
                    ws.column_dimensions['E'].width = 10
                    ws['D1'].alignment = Alignment(wrap_text=True)
                    ws['E1'].alignment = Alignment(wrap_text=True)
                    ws['A1'].value = 'Code'
                    ws['B1'].value = 'Name'
                    ws['C1'].value = 'Qty Sold'
                    ws['D1'].value = """Total Sales\nAmount\n(Gross RM)"""
                    ws['E1'].value = """Average\nUnit Price\nRM"""
                    wb.save(filename=BASE_FILE)
                    wb.close()
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            # OPEN AND COPY FILE
            if not os.path.exists(os.path.abspath(EXCEL_FILE)):
                try:
                    shutil.copyfile(os.path.abspath(BASE_FILE), os.path.abspath(EXCEL_FILE))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            self.checkExcel()  # check if saveExit existed or not

            for child in self.buyScreen.get_children():
                base.append([self.buyScreen.item(child)["values"][i] for i in range(6)])

            # print(base)   #debug
            '''EXCEL FOR REPORT DATA A.Code B.Name C.Qty D.Total E.Avg'''
            theFile = pyxl.load_workbook(EXCEL_FILE)
            allSheetNames = theFile.sheetnames
            qty_adj = 'C'
            total_adj = 'D'
            avg_adj = 'E'

            for sheet in allSheetNames:
                # print("Current sheet name is {}".format(sheet))   #debug find sheet
                currentSheet = theFile[sheet]

            def find_cell(value="", show="row"):
                for row in range(1, currentSheet.max_row + 1):
                    for column in "ABCDE":  # Here you can add or reduce the columns
                        cell_name = "{}{}".format(column, row)

                        if currentSheet[cell_name].value == value:
                            # print("{1} cell is located on {0}" .format(cell_name, currentSheet[cell_name].value))
                            # print("cell position {} has value {}".format(cell_name, currentSheet[cell_name].value))   #debug
                            # print(column, row)
                            if show.lower() == "row":
                                return row
                            elif show.lower() == "column":
                                return column
                            elif show.lower() == "cell":
                                return cell_name
                            else:
                                return 'Only row, column, cell'

            def add_cell(value=['x', 'x', 1, 1.1, 1.1], column="ABCDE"):
                '''value Must depends on columns like 5 value for "ABCDE" '''

                wb = xlrd.open_workbook(EXCEL_FILE)
                sheet = wb.sheet_by_index(0)

                check_row = sheet.nrows
                i = 0
                for col in column:  # Here you can add or reduce the columns
                    cell_name = "{}{}".format(col, (check_row + 1))
                    currentSheet[cell_name].value = value[i]
                    i += 1

                # print("Successfully add new item")  #debug
                theFile.save(EXCEL_FILE)
                theFile.close()

            k = 0
            for data in base:
                row_adj = str(find_cell(value=data[k], show='row'))
                if row_adj == 'None':
                    add_cell(value=[str(data[0]), data[1], data[2], float(data[4]) - float(data[5]),
                                    (float(data[4]) - float(data[5])) / float(data[2])])
                else:
                    currentSheet[qty_adj + row_adj].value = int(currentSheet[qty_adj + row_adj].value) + int(data[2])
                    currentSheet[total_adj + row_adj].value = float(
                        float(currentSheet[total_adj + row_adj].value) + (float(data[4]) - float(data[5])))
                    currentSheet[avg_adj + row_adj].value = (float(currentSheet[total_adj + row_adj].value) + float(
                        data[4]) - float(data[5])) / \
                                                            (int(currentSheet[qty_adj + row_adj].value) + int(data[2]))

                    theFile.save(EXCEL_FILE)
                    theFile.close()


        except Exception as e:
            messagebox.showerror("ERROR", f"{e} . PLS CONTACT PROVIDER TO FIX IT")

    def saveExit(self):
        try:
            SAVE_PATH = 'data/Report Data/'
            BASE_FILE = SAVE_PATH + '/daily_report_example.xlsx'
            EXCEL_FILE = SAVE_PATH + str(date.today()) + '.xlsx'

            # Precaution if BASE_FILE not found
            if not os.path.exists(os.path.abspath(BASE_FILE)):
                try:
                    wb = pyxl.Workbook()
                    ws = wb.active
                    ws.sheet_view.showGridLines = True
                    ws.title = "MAIN"
                    ws.column_dimensions['A'].width = 20
                    ws.column_dimensions['B'].width = 30
                    ws.column_dimensions['C'].width = 10
                    ws.column_dimensions['D'].width = 10
                    ws.column_dimensions['E'].width = 10
                    ws['D1'].alignment = Alignment(wrap_text=True)
                    ws['E1'].alignment = Alignment(wrap_text=True)
                    ws['A1'].value = 'Code'
                    ws['B1'].value = 'Name'
                    ws['C1'].value = 'Qty Sold'
                    ws['D1'].value = """Total Sales\nAmount\n(Gross RM)"""
                    ws['E1'].value = """Average\nUnit Price\nRM"""
                    wb.save(filename=BASE_FILE)
                    wb.close()
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            # OPEN AND COPY FILE
            if not os.path.exists(os.path.abspath(EXCEL_FILE)):
                try:
                    shutil.copyfile(os.path.abspath(BASE_FILE), os.path.abspath(EXCEL_FILE))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            # openpyxl
            theFile = pyxl.load_workbook(EXCEL_FILE)
            allSheetNames = theFile.sheetnames
            for sheet in allSheetNames:
                # print("Current sheet name is {}".format(sheet))   #debug find sheet
                currentSheet = theFile[sheet]

            # xlrd
            wb = xlrd.open_workbook(EXCEL_FILE)
            sheetwb = wb.sheet_by_index(0)

            target_row = sheetwb.nrows + 4

            raw_data = [value for value in currentSheet.iter_rows(min_row=1,
                                                                  max_row=sheetwb.nrows,
                                                                  min_col=1,
                                                                  max_col=5,
                                                                  values_only=True)]
            raw_data.pop(0)
            # pprint(raw_data)    #debug

            qty = price = 0
            for data in raw_data:
                # pprint(data)  #debug
                qty += data[2]
                price += data[3]
            # print(qty, price)   #debug

            currentSheet['A' + str(target_row)].alignment = Alignment(wrap_text=True)
            currentSheet['A' + str(target_row + 1)].alignment = Alignment(wrap_text=True)
            currentSheet['A' + str(target_row)].value = "Total Product\nSold Today"
            currentSheet['A' + str(target_row + 1)].value = "Total Cash\nToday(RM)"
            currentSheet['A' + str(target_row + 3)].value = "Date"
            currentSheet['B' + str(target_row)].value = qty
            currentSheet['B' + str(target_row + 1)].value = float(price)
            currentSheet['B' + str(target_row + 3)].value = date.today()
            theFile.save(EXCEL_FILE)
            theFile.close()





        except Exception as e:
            messagebox.showerror("ERROR", f"{e} . PLS CONTACT PROVIDER TO FIX IT")

    def checkExcel(self):
        SAVE_PATH = 'data/Report Data/'
        BASE_FILE = SAVE_PATH + '/daily_report_example.xlsx'
        EXCEL_FILE = SAVE_PATH + str(date.today()) + '.xlsx'

        if os.path.exists(os.path.abspath(EXCEL_FILE)):
            theFile = pyxl.load_workbook(EXCEL_FILE)
            allSheetNames = theFile.sheetnames

            for sheet in allSheetNames:
                # print("Current sheet name is {}".format(sheet))   #debug find sheet
                currentSheet = theFile[sheet]

                # xlrd
                wb = xlrd.open_workbook(EXCEL_FILE)
                sheetwb = wb.sheet_by_index(0)

                raw_data = [value for value in currentSheet.iter_rows(min_row=1,
                                                                      max_row=sheetwb.nrows,
                                                                      min_col=1,
                                                                      max_col=5,
                                                                      values_only=True)]

                footer = 7
                header = sheetwb.nrows - footer
                # pprint(raw_data)  #debug

                for data in raw_data:
                    if 'Date' in data:
                        currentSheet.delete_rows(header + 1, footer)
                        print('Footer found and deleted')
                        theFile.save(EXCEL_FILE)
                        theFile.close()

        else:
            messagebox.showwarning("No Data Found", f"Report for {date.today()} saved but no data inside")

    def printExcel(self):
        self.calendar_win = Toplevel(self.cashWin)
        Label(self.calendar_win, text='Choose date').pack(padx=10, pady=10)
        style = Style()
        style.configure('W.TButton', font=('Comic sans ms', 15, 'normal', 'italic'), foreground='black')
        style1 = 'W.TButton'

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


#TODO add order window and function
#TODO will use and research for DELIVERY_FLOW
#TODO use FLOW_CACHE
#TODO try to think how to setup member data
#TODO small bug for code1


CashierWin(Tk(), ID='RZ0000E005')  # debug for one cashier_win.py

