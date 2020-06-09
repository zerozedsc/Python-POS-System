import random
import sqlite3
import tkinter as tk
import tkinter.simpledialog as sd
from datetime import datetime
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
from tkinter.ttk import Style
from PIL import Image, ImageTk
import os
from sys import exit
import time
from server import SERVER_PATH

#Path
EMPLOYEE_PHOTO_PATH = "data/Employee Data/Employee_Photos/"

class AdminWin():
    def __init__(self, master, ID='', POS=''):
        self.adminWin = master
        self.adminWin.resizable(0, 0)
        self.adminWin.protocol("WM_DELETE_WINDOW", exit)
        self.windowHeight = int(self.adminWin.winfo_reqheight())
        self.windowWidth = int(self.adminWin.winfo_reqwidth())
        self.positionRight = int(self.adminWin.winfo_screenwidth() / 2 - (self.windowWidth / 2))
        self.positionDown = int(self.adminWin.winfo_screenheight() / 2 - (self.windowHeight / 2))
        self.adminWin.iconphoto(False, PhotoImage(file='images/rozeriya.png'))
        self.adminWin.geometry(f"1200x800+{self.positionRight - 400}+{self.positionDown - 300}")
        self.adminWin.title("ADMIN FORM")
        style = Style()
        style.configure('W.TButton', font=('Comic sans ms', 15, 'normal', 'italic'), foreground='black')
        style1 = 'W.TButton'

        self.check = True

        # background
        background_image = tk.PhotoImage(master=self.adminWin, file='images/adminBg.png')
        background_label = Label(self.adminWin, background='gold', image=background_image)
        background_label.image = background_image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # FRAME
        test = Frame(master=self.adminWin)
        test.place(relwidth=0.8, relheight=1, relx=0.2)
        frame_image = tk.PhotoImage(master=test, file='images/frameBg.png')
        frame_label = Label(test, background='gold', image=frame_image)
        frame_label.image = frame_image
        frame_label.place(x=0, y=0, relwidth=1, relheight=1)

        # ID LABEL
        self.IDGrab = ID
        self.POSGrab = POS
        Label(self.adminWin, text='ID: ' + self.IDGrab, font=('comic sans ms', 15, 'bold'), foreground='green').place(relx=0, rely=0.05, width=238)
        Label(self.adminWin, text='POS: ' + self.POSGrab, font=('comic sans ms', 15, 'bold'), foreground='green').place(
            relx=0, rely=0.1, width=238)


        # SHOW STOCK BUTTON
        self.stockShow_button = Button(self.adminWin, text='Show Stock', command=self.showStock, state='normal',
                                       style=style1)
        self.stockShow_button.place(relx=0, rely=0.2, width=238)

        # REGISTER ITEM BUTTON
        self.regItem_button = Button(self.adminWin, text='Register New Item', command=self.registerItem,
                                     state='disabled',
                                     style=style1)
        self.regItem_button.place(relx=0, rely=0.3, width=238)

        # DELETE ITEM BUTTON
        self.delItem_button = Button(self.adminWin, text='Delete Item', command=self.deleteItem, state='disabled',
                                     style=style1)
        self.delItem_button.place(relx=0, rely=0.4, width=238)

        # ADJUST STOCK BUTTON
        self.adjustStock_button = Button(self.adminWin, text='Adjust item', command=self.adjustItem, state='disabled',
                                         style=style1)
        self.adjustStock_button.place(relx=0, rely=0.5, width=238)

        # REPORT STOCK BUTTON
        self.report_button = Button(self.adminWin, text='Report GAIN LOSS', command=None, state='disabled',
                                    style=style1)
        self.report_button.place(relx=0, rely=0.7, width=238)

        # EMPLOYEE DATA BUTTON
        self.showEmployee_button = Button(self.adminWin, text='Employee Data', command=self.showEmployee,
                                          state='normal', style=style1)


        if POS == 'MANAGER':
            self.showEmployee_button.config(state='normal')
            self.showEmployee_button.place(relx=0, rely=0.8, width=238)
        else:
            self.showEmployee_button.config(state='disabled')
            self.showEmployee_button.place(relx=0, rely=0.8, width=238)

        # EXIT BUTTON
        self.exit_button = Button(self.adminWin, text='Exit', command=self.adminWin.destroy,
                                  state='normal', style=style1)
        self.exit_button.place(relx=0, rely=0.95, width=238)


        self.adminWin.mainloop()

    # show stock
    def queryStock(self, data='product_data'):

        try:
            conn = sqlite3.connect(SERVER_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PRODUCT ORDER BY PRODUCT_ID;")
            query1 = cursor.fetchall()

            if self.sortRead.get() == 'product id':
                cursor.execute("SELECT * FROM PRODUCT ORDER BY PRODUCT_ID;")
                query1 = cursor.fetchall()
                cursor.execute("SELECT * FROM PRODUCT_DATA ORDER BY PRODUCT_ID;")
                query2 = cursor.fetchall()
            elif self.sortRead.get() == 'product name':
                cursor.execute("SELECT * FROM PRODUCT_DATA ORDER BY PRODUCT_NAME;")
                query2 = cursor.fetchall()
            elif self.sortRead.get() == 'product type':
                cursor.execute("SELECT * FROM PRODUCT_DATA ORDER BY PRODUCT_TYPE;")
                query2 = cursor.fetchall()
            elif self.sortRead.get() == 'price':
                cursor.execute("SELECT * FROM PRODUCT_DATA ORDER BY PRICE;")
                query2 = cursor.fetchall()
            elif self.sortRead.get() == 'quantity':
                cursor.execute("SELECT * FROM PRODUCT_DATA ORDER BY QUANTITY;")
                query2 = cursor.fetchall()
            else:
                cursor.execute("SELECT * FROM PRODUCT_DATA ORDER BY PRODUCT_ID;")
                query2 = cursor.fetchall()
            product = []
            product_data = []
            # print("YOU ARE CONNECTED TO DATABASE")    #debug
            if data == 'product':
                for i in query1:
                    for x in i:
                        product.append(str(x))
                self.check = True
                return product
            elif data == 'product_data':
                for y in query2:
                    for k in y:
                        product_data.append(str(k))
                self.check = True
                return product_data
            else:
                self.check = False
                return 'NOT FOUND'

        except (Exception, sqlite3.Error) as error:
            self.check = False
            print("Error while connecting to database ", error)
            messagebox.showerror("Database Error", error)

    def showStock(self, param=None):
        # FRAME
        show = Frame(master=self.adminWin)
        show.place(relwidth=0.8, relheight=1, relx=0.2)
        frame_image = tk.PhotoImage(master=show, file='images/frameBg.png')
        frame_label = Label(show, background='gold', image=frame_image)
        frame_label.image = frame_image
        frame_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.regItem_button.config(state='normal')
        self.delItem_button.config(state='normal')
        self.adjustStock_button.config(state='normal')

        Label(show, text="STOCK", font=('comic sans ms', 18, 'italic', 'bold')).pack()

        list = ['product id', 'product name', 'product type', 'price', 'quantity']
        self.sortRead = StringVar()
        # combobox choice
        Label(show, text='Sort by', font=('arial black', 10)).place(relx=0, rely=0.05)
        self.sortChoice = Combobox(show, textvariable=self.sortRead, values=list, state='disabled')
        self.sortChoice.bind('<<ComboboxSelected>>', self.queryStock)
        self.sortChoice.place(relx=0.1, rely=0.05)

        try:
            product = [i.strip(" ") for i in self.queryStock('product')]  # PRODUCT_ID[0], PRODUCT_TYPE[1], EXIST[2]
            product_data = [i.strip(" ") for i in
                            self.queryStock('product_data')]  # PRODUCT_ID[0], PRODUCT_NAME[1], PRICE[2], QUANTITY[3]

        except:
            self.check = False

        if self.check:
            self.check_productID = []
            chk = 0
            for i in product:
                if len(product) > chk:
                    self.check_productID.append(product[chk])
                    chk = chk + 3
            id_count = 1
            for i in self.check_productID:
                id_count = id_count + 1
            if id_count < 10:
                self.prd_id = "RZ0000P00" + str(id_count)
            elif id_count < 100:
                self.prd_id = "RZ0000P0" + str(id_count)
            else:
                self.prd_id = "RZ0000P" + str(id_count)
            self.p_id = []
            self.p_type = []
            name = []
            price = []
            qty = []
            # print(product)
            # print(product_data)
            xt = 2
            xd = 0
            for i in product_data:
                if len(product_data) > xd:
                    self.p_id.append(product_data[xd])
                    xd = xd + 5
                if len(product_data) > xt:
                    self.p_type.append(product_data[xt])
                    xt = xt + 5

            yn = 1
            yp = 3
            yq = 4
            for i in product_data:
                if len(product_data) > yn:
                    name.append(product_data[yn])
                    yn = yn + 5
                if len(product_data) > yp:
                    price.append(product_data[yp])
                    yp = yp + 5
                if len(product_data) > yq:
                    qty.append(product_data[yq])
                    yq = yq + 5

            # DATA TABLE
            cols = ('ID', 'NAMA', 'JENIS', 'HARGA', 'STOCK')
            self.data_table = Treeview(show, columns=cols, show='headings')
            for col in cols:
                self.data_table.heading(col, text=col)
            k = 0
            for i in range(len(self.p_id)):
                self.data_table.insert("", END,
                                       values=(self.p_id[k], name[k], self.p_type[k], 'RM ' + price[k], int(qty[k])))
                k = k + 1

            self.data_table.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.9)
            vsb = Scrollbar(show, orient="vertical", command=self.data_table.yview)
            vsb.place(relx=0.98, rely=0.1, relheight=0.9)
            hrz = Scrollbar(show, orient="horizontal", command=self.data_table.xview)
            hrz.place(relx=0, rely=0.98, relwidth=1)
            self.data_table.configure(yscrollcommand=vsb.set, xscrollcommand=hrz.set)
            component = []
            for child in self.data_table.get_children():
                component.append(child)
            #     print(self.data_table.item(child)["values"][4])
            # print("comp: ", component)

        else:
            Label(show, text="""CAN'T CONNECT DATABASE, 
            PLEASE PRESS THE BUTTON AGAIN""", font=('comic sans ms', 18, 'italic', 'bold'), foreground='red').place(
                relx=0, rely=0.5)

    # register new item
    def queryReg(self):
        ID = self.reg.upper()
        JENIS = self.getType.get().upper()
        NAMA = self.getName.get().upper()
        HARGA = self.getPrice.get()
        STOCK = self.getQty.get()
        d = datetime.now()
        self.timestamp = d.timestamp()
        try:
            conn = conn = sqlite3.connect(SERVER_PATH)  # \\Zerozed-pc\shared\DB
            cursor = conn.cursor()
            # print("YOU ARE CONNECTED TO DATABASE")   #debug
            # print(ID, NAMA, JENIS, HARGA, STOCK)  #debug
            try:
                cursor.execute("SELECT REGISTER_ID FROM REGISTER_CACHE")
                reg_table = cursor.fetchall()
                reg_id_count = 1
                for i in reg_table:
                    reg_id_count = reg_id_count + 1
                if reg_id_count < 10:
                    reg_id = "RZ0000R00" + str(reg_id_count)
                elif reg_id_count < 100:
                    reg_id = "RZ0000R0" + str(reg_id_count)
                else:
                    reg_id = "RZ0000R" + str(reg_id_count)
                cursor.execute("INSERT INTO PRODUCT VALUES(?,?,?)", (ID, JENIS, True))
                conn.commit()
                cursor.execute("INSERT INTO PRODUCT_DATA VALUES(?,?,?,?,?)", (ID, NAMA, JENIS, HARGA, STOCK))
                conn.commit()
                cursor.execute("INSERT INTO REGISTER_CACHE VALUES(?,?,?)", (reg_id, ID, self.timestamp))
                conn.commit()
                messagebox.showinfo("SUCCESS", f"REGISTER {ID} DONE")
                self.showStock()
                self.reg_itemWin.destroy()
            except:
                messagebox.showerror("FAILED", "ID ALREADY REGISTERED")

        except (Exception, sqlite3.Error) as error:
            self.check = False
            messagebox.showerror("FAILED", "NO DATABASE DETECTED")
            self.reg_itemWin.destroy
            print("Error while connecting to DATABASE ", error)

    def registerItem(self):
        try:
            self.reg = sd.askstring(title="Register Item", prompt="PRESS OK", initialvalue=self.prd_id)
        except:
            messagebox.showwarning("CAUTION", "YOU MUST PRESS SHOW STOCK FIRST")

        try:
            if self.reg not in self.check_productID:
                if "RZ" and 'P' in self.reg or len(self.reg) >= 10:
                    self.reg_itemWin = Toplevel(self.adminWin)
                    self.reg_itemWin.resizable(0, 0)
                    self.windowHeight = int(self.reg_itemWin.winfo_reqheight())
                    self.windowWidth = int(self.reg_itemWin.winfo_reqwidth())
                    self.positionRight = int(self.reg_itemWin.winfo_screenwidth() / 2 - (self.windowWidth / 2))
                    self.positionDown = int(self.reg_itemWin.winfo_screenheight() / 2 - (self.windowHeight / 2))
                    self.reg_itemWin.iconphoto(False, PhotoImage(file='images/rozeriya.png'))
                    self.reg_itemWin.geometry(f"400x400+{self.positionRight - 400}+{self.positionDown - 300}")
                    self.reg_itemWin.title("REGISTER ITEM")
                    style = Style()
                    style.configure('W.TButton', font=('Comic sans ms', 15, 'normal', 'italic'), foreground='black')
                    style1 = 'W.TButton'

                    Label(self.reg_itemWin, text="REGISTER ITEM", font=('comic sans ms', 18, 'italic', 'bold')).pack()

                    self.getName = StringVar()
                    self.getType = StringVar()
                    self.getPrice = DoubleVar()
                    self.getQty = IntVar()

                    # ID DISABLED
                    Label(self.reg_itemWin, text='PRODUCT ID', font=('Comic sans ms', 12, 'normal', 'italic')).place(
                        relx=0,
                        rely=0.2)
                    reg_entry = Label(self.reg_itemWin, font=('Comic sans ms', 12, 'normal', 'italic'), text=self.reg)
                    reg_entry.place(relx=0.38, rely=0.2, width=240)

                    # NAME
                    Label(self.reg_itemWin, text='PRODUCT NAME',
                          font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.3)
                    name_entry = Entry(self.reg_itemWin, textvariable=self.getName)
                    name_entry.place(relx=0.38, rely=0.3, width=240)

                    # JENIS
                    Label(self.reg_itemWin, text='TYPE OF PRODUCT',
                          font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.4)
                    type_entry = Entry(self.reg_itemWin, textvariable=self.getType)
                    type_entry.place(relx=0.38, rely=0.4, width=240)

                    # PRICE
                    Label(self.reg_itemWin, text='PRICE',
                          font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.5)
                    type_entry = Entry(self.reg_itemWin, textvariable=self.getPrice)
                    type_entry.place(relx=0.38, rely=0.5, width=240)

                    # QUANTITY
                    Label(self.reg_itemWin, text='QUANTITY',
                          font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.6)
                    type_entry = Entry(self.reg_itemWin, textvariable=self.getQty)
                    type_entry.place(relx=0.38, rely=0.6, width=240)

                    # reg button
                    reg_button = Button(self.reg_itemWin, style=style1, text='REGISTER', command=self.queryReg)
                    reg_button.place(relx=0.5, rely=0.7)
                else:
                    messagebox.showerror("WRONG ID", "PUT THE CORRECT PRODUCT ID")
            else:
                messagebox.showerror("ID EXISTED", "PUT ANOTHER ID")



        except:
            print("CANCELED or Database not connected")

    # DELETE ITEM
    def deleteItem(self):
        try:
            del_item = sd.askstring(title="Product ID", prompt=f"PUT PRODUCT ID IN FORMAT '{self.prd_id}' OR BARCODE")
        except:
            messagebox.showwarning("CAUTION", "YOU MUST PRESS SHOW STOCK FIRST")

        try:
            if del_item in self.check_productID:
                if "RZ" and 'P' in del_item or len(del_item) >= 10:
                    getDel = str(del_item).upper()
                    try:
                        conn = sqlite3.connect('//Zerozed-pc/shared/DB/ROZERIYA-DB.db')
                        cursor = conn.cursor()
                        print("YOU ARE CONNECTED TO DATABASE")
                        try:
                            cursor.execute(f"DELETE FROM PRODUCT_DATA WHERE PRODUCT_ID = '{getDel}'")
                            conn.commit()
                            cursor.execute(f"UPDATE PRODUCT SET EXIST ={False} WHERE PRODUCT_ID = '{getDel}'")
                            conn.commit()
                            messagebox.showinfo("SUCCESS", f"{getDel} DELETED ")
                            self.showStock()
                        except:
                            messagebox.showerror("FAILED", "ID NOT FOUND")
                    except (Exception, sqlite3.Error) as error:
                        self.check = False
                        messagebox.showerror("FAILED", "NO DATABASE DETECTED")
                        print("Error while connecting to database ", error)
        except:
            print("CANCELED or Database not connected")

    # ADJUST ITEM
    def queryAdjust(self):
        ID = self.adjust.upper()
        JENIS = self.getTypeA.get().upper()
        NAMA = self.getNameA.get().upper()
        HARGA = self.getPriceA.get()
        STOCK = self.getQtyA.get()
        try:
            conn = sqlite3.connect(SERVER_PATH)  # \\Zerozed-pc\shared\DB
            cursor = conn.cursor()
            # print("YOU ARE CONNECTED TO DATABASE")    #debug
            # print(ID, NAMA, JENIS, HARGA, STOCK)  #debug
            try:
                if self.adjustRead.get() == 'all':
                    cursor.execute("""UPDATE PRODUCT_DATA
                     SET PRODUCT_NAME = ?,
                            PRODUCT_TYPE= ?,
                            PRICE = ?,
                            QUANTITY = ?
                    WHERE 
                            PRODUCT_ID = ?""", (NAMA, JENIS, HARGA, STOCK, ID))
                    conn.commit()
                    cursor.execute("UPDATE PRODUCT SET PRODUCT_TYPE = ? WHERE PRODUCT_ID = ?", (JENIS, ID))
                    conn.commit()
                    messagebox.showinfo("SUCCESS", f"ADJUST {ID} DONE")
                    self.adjustWin.destroy()
                elif self.adjustRead.get() == 'product name':
                    cursor.execute("""UPDATE PRODUCT_DATA
                                        SET PRODUCT_NAME = ?
                                       WHERE 
                                               PRODUCT_ID = ?""", (NAMA, ID))
                    conn.commit()
                    messagebox.showinfo("SUCCESS", f"ADJUST {ID} DONE")
                    self.adjustWin.destroy()
                elif self.adjustRead.get() == 'product type':
                    cursor.execute("""UPDATE PRODUCT_DATA
                                        SET 
                                            PRODUCT_TYPE = ?
                                       WHERE 
                                               PRODUCT_ID = ?""", (JENIS, ID))
                    conn.commit()
                    cursor.execute("""UPDATE PRODUCT
                                                            SET PRODUCT_TYPE = ?
                                                           WHERE 
                                                                   PRODUCT_ID = ?""", (JENIS, ID))
                    conn.commit()
                    messagebox.showinfo("SUCCESS", f"ADJUST {ID} DONE")
                    self.adjustWin.destroy()
                elif self.adjustRead.get() == 'price':
                    cursor.execute("""UPDATE PRODUCT_DATA
                                        SET PRICE = ?
                                       WHERE 
                                               PRODUCT_ID = ?""", (HARGA, ID))
                    conn.commit()
                    messagebox.showinfo("SUCCESS", f"ADJUST {ID} DONE")
                    self.adjustWin.destroy()
                elif self.adjustRead.get() == 'quantity':
                    cursor.execute("""UPDATE PRODUCT_DATA
                                        SET QUANTITY = ?
                                       WHERE 
                                               PRODUCT_ID = ?""", (STOCK, ID))
                    conn.commit()
                    messagebox.showinfo("SUCCESS", f"ADJUST {ID} DONE")
                    self.showStock()
                    self.adjustWin.destroy()
                else:
                    messagebox.showerror("NOT FOUND", "CATEGORY NOT FOUND")

            except:
                messagebox.showerror("FAILED", "ADJUST FAILED")

        except (Exception, sqlite3.Error) as error:
            self.check = False
            messagebox.showerror("FAILED", "NO DATABASE DETECTED")
            self.adjustWin.destroy
            print("Error while connecting to database", error)

    def hideButton(self, null=None):
        self.all_button.config(state='normal')
        self.name_entry.config(state='disabled')
        self.qty_entry.config(state='disabled')
        self.price_entry.config(state='disabled')
        self.type_entry.config(state='disabled')
        if self.adjustRead.get() == 'all':
            self.name_entry.config(state='normal')
            self.qty_entry.config(state='normal')
            self.price_entry.config(state='normal')
            self.type_entry.config(state='normal')
        elif self.adjustRead.get() == 'product name':
            self.name_entry.config(state='normal')
        elif self.adjustRead.get() == 'product type':
            self.type_entry.config(state='normal')
        elif self.adjustRead.get() == 'quantity':
            self.qty_entry.config(state='normal')
        elif self.adjustRead.get() == 'price':
            self.price_entry.config(state='normal')
        else:
            messagebox.showerror("WRONG CATEGORY", "CHECK CATEGORY")

    def adjustItem(self):
        try:
            self.adjust = sd.askstring('REGISTER ITEM', f'PRODUCT ID (exp:{self.prd_id})')
        except:
            messagebox.showwarning("CAUTION", "YOU MUST PRESS SHOW STOCK FIRST")

        try:
            if self.adjust.upper() in self.check_productID:
                if "RZ" and 'P' in self.adjust.upper() or len(self.adjust) >= 10:
                    self.adjustWin = Toplevel(self.adminWin)
                    self.adjustWin.resizable(0, 0)
                    self.windowHeight = int(self.adjustWin.winfo_reqheight())
                    self.windowWidth = int(self.adjustWin.winfo_reqwidth())
                    self.positionRight = int(self.adjustWin.winfo_screenwidth() / 2 - (self.windowWidth / 2))
                    self.positionDown = int(self.adjustWin.winfo_screenheight() / 2 - (self.windowHeight / 2))
                    self.adjustWin.iconphoto(False, PhotoImage(file='images/rozeriya.png'))
                    self.adjustWin.geometry(f"400x400+{self.positionRight - 400}+{self.positionDown - 300}")
                    self.adjustWin.title("ADJUST ITEM")
                    style = Style()
                    style.configure('W.TButton', font=('Comic sans ms', 15, 'normal', 'italic'), foreground='black')
                    style1 = 'W.TButton'

                    Label(self.adjustWin, text="REGISTER ITEM", font=('comic sans ms', 18, 'italic', 'bold')).pack()

                    self.getNameA = StringVar()
                    self.getTypeA = StringVar()
                    self.getPriceA = DoubleVar()
                    self.getQtyA = IntVar()

                    # ID DISABLED
                    Label(self.adjustWin, text='PRODUCT ID', font=('Comic sans ms', 12, 'normal', 'italic')).place(
                        relx=0,
                        rely=0.2)
                    reg_entry = Label(self.adjustWin, font=('Comic sans ms', 12, 'normal', 'italic'), text=self.adjust)
                    reg_entry.place(relx=0.38, rely=0.2, width=240)

                    # NAME
                    Label(self.adjustWin, text='PRODUCT NAME',
                          font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.3)
                    self.name_entry = Entry(self.adjustWin, textvariable=self.getNameA, state='disabled')
                    self.name_entry.place(relx=0.38, rely=0.3, width=240)

                    # JENIS
                    Label(self.adjustWin, text='TYPE OF PRODUCT',
                          font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.4)
                    self.type_entry = Entry(self.adjustWin, textvariable=self.getTypeA, state='disabled')
                    self.type_entry.place(relx=0.38, rely=0.4, width=240)

                    # PRICE
                    Label(self.adjustWin, text='PRICE',
                          font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.5)
                    self.price_entry = Entry(self.adjustWin, textvariable=self.getPriceA, state='disabled')
                    self.price_entry.place(relx=0.38, rely=0.5, width=240)

                    # QUANTITY
                    Label(self.adjustWin, text='QUANTITY',
                          font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.6)
                    self.qty_entry = Entry(self.adjustWin, textvariable=self.getQtyA, state='disabled')
                    self.qty_entry.place(relx=0.38, rely=0.6, width=240)

                    # reg button
                    self.all_button = Button(self.adjustWin, style=style1, text='ADJUST', command=self.queryAdjust,
                                             state='disabled')
                    self.all_button.place(relx=0.5, rely=0.7)

                    list = ['product name', 'product type', 'price', 'quantity', 'all']
                    self.adjustRead = StringVar()
                    # combobox choice
                    Label(self.adjustWin, text='CATOGERY', font=('arial black', 10)).place(relx=0, rely=0.7)
                    self.adjustChoice = Combobox(self.adjustWin, textvariable=self.adjustRead, values=list)
                    self.adjustChoice.bind('<<ComboboxSelected>>', self.hideButton)
                    self.adjustChoice.place(relx=0, rely=0.75)


                else:
                    messagebox.showerror("WRONG ID", "PUT THE CORRECT PRODUCT ID")

            else:
                messagebox.showerror("WRONG ID", "ID NOT FOUND")

        except:
            print("CANCELED")

    # EMPLOYEE DATA
    def employeeQuery(self, data):
        try:
            conn = sqlite3.connect(SERVER_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM EMPLOYEE ORDER BY EMPLOYEE_ID;")
            query1 = cursor.fetchall()
            cursor.execute("SELECT * FROM EMPLOYEE_DATA ORDER BY EMPLOYEE_ID;")
            query2 = cursor.fetchall()
            product = []
            product_data = []
            print("YOU ARE CONNECTED TO DATABASE")
            if data == 'employee':
                for i in query1:
                    for x in i:
                        product.append(str(x))
                self.check = True
                return product
            elif data == 'employee_data':
                for y in query2:
                    for k in y:
                        product_data.append(str(k))
                self.check = True
                return product_data
            else:
                self.check = False
                return 'NOT FOUND'

        except (Exception, sqlite3.Error) as error:
            self.check = False
            print("Error while connecting to PostgreSQL ", error)
            messagebox.showerror("Database Error", error)

    def employeeProfile(self):
        self.empProfile = sd.askstring(title='ADJUST EMPLOYEE', prompt=f'ENTER SAME WITH THIS FORMAT exp:{self.emp_id}')

        if self.empProfile is None:
            pass
        else:
            try:
                if self.empProfile in self.check_employeeID:
                    if "RZ" and 'E' in self.empProfile and len(self.empProfile) >= 10:
                        show = Frame(master=self.adminWin)
                        show.place(relwidth=0.8, relheight=1, relx=0.2)
                        frame_image = tk.PhotoImage(master=show, file='images/frameBg.png')
                        frame_label = Label(show, background='gold', image=frame_image)
                        frame_label.image = frame_image
                        frame_label.place(x=0, y=0, relwidth=1, relheight=1)
                        style = Style()
                        style.configure('W.TButton', font=('Comic sans ms', 15, 'normal', 'italic'), foreground='black')
                        style.configure('C.TButton', font=('Comic sans ms', 15, 'normal', 'italic'), foreground='red')
                        style1 = 'W.TButton'
                        style2 = 'C.TButton'

                        Label(show, text="EMPLOYEE PROFILE", font=('comic sans ms', 18, 'italic', 'bold')).pack()

                        def employeeQuery(data):
                            try:
                                conn = sqlite3.connect(SERVER_PATH)
                                cursor = conn.cursor()
                                cursor.execute("SELECT * FROM EMPLOYEE ORDER BY EMPLOYEE_ID;")
                                query1 = cursor.fetchall()
                                cursor.execute("SELECT * FROM EMPLOYEE_DATA ORDER BY EMPLOYEE_ID;")
                                query2 = cursor.fetchall()
                                product = []
                                product_data = []
                                # print("YOU ARE CONNECTED TO DATABASE")    #debug
                                if data == 'employee':
                                    for i in query1:
                                        for x in i:
                                            product.append(str(x))
                                    self.check = True
                                    return product
                                elif data == 'employee_data':
                                    for y in query2:
                                        for k in y:
                                            product_data.append(str(k))
                                    self.check = True
                                    return product_data
                                else:
                                    self.check = False
                                    return 'NOT FOUND'

                            except (Exception, sqlite3.Error) as error:
                                self.check = False
                                print("Error while connecting to Database ", error)
                                messagebox.showerror("Database Error", error)

                        def getPhoto():
                            try:
                                conn = sqlite3.connect(SERVER_PATH)
                                cursor = conn.cursor()
                                cursor.execute("SELECT * FROM EMPLOYEE_DATA ORDER BY EMPLOYEE_ID;")
                                query1 = cursor.fetchall()
                                employee = []
                                for i in query1:
                                    for x in i:
                                        employee.append(str(x))
                                # print("YOU ARE CONNECTED TO DATABASE")    #debug

                                photoBlob = employee[employee.index(self.empProfile) + 6]
                                print(photoBlob)
                                photo = ImageTk.PhotoImage(Image.open(photoBlob))
                                return photo

                            except (Exception, sqlite3.Error) as error:
                                self.check = False
                                print("Error while connecting to database ", error)
                                messagebox.showerror("Database Error", error)

                        # PHOTO

                        # pathName = "//Zerozed-pc/shared/DB/gambar_pekerja/" + self.empProfile +".jpg"
                        photo = getPhoto()
                        self.photoFrame = Label(show, background='white', image=photo)
                        self.photoFrame.image = photo
                        self.photoFrame.place(width=200, height=250, relx=0.8)

                        employee = [i.strip(" ") for i in
                                    employeeQuery(
                                        'employee_data')]  # EMPLOYEE_ID[0], NAME[1], POS[2], ADDRESS[3], PHONE[4], SALARY[5]
                        employee_stamp = [i.strip(" ") for i in
                                          employeeQuery(
                                              'employee')]
                        readableDate = time.ctime(float(employee_stamp[employee_stamp.index(self.empProfile) + 3]))

                        # time hire
                        Label(show, text='START DATE OF WORK: ', font=('arial', 15, 'bold')).place(relx=0, rely=0.1)
                        dateLabel = Label(show, text=str(readableDate),
                                          font=('arial', 17, 'bold', 'italic'), background='silver')
                        dateLabel.place(relx=0.3, rely=0.1)

                        # NAME
                        Label(show, text='NAME: ', font=('arial', 15, 'bold')).place(relx=0, rely=0.2)
                        nameLabel = Label(show, text=employee[employee.index(self.empProfile) + 1],
                                          font=('comic sans ms', 17, 'bold', 'italic'))
                        nameLabel.place(relx=0.1, rely=0.2)

                        # POSITION
                        Label(show, text='POSITION: ', font=('arial', 15, 'bold')).place(relx=0, rely=0.3)
                        posLabel = Label(show, text=employee[employee.index(self.empProfile) + 2],
                                         font=('arial', 15, 'bold'))
                        posLabel.place(relx=0.12, rely=0.3)

                        # ADDRESS
                        Label(show, text='ADDRESS: ', font=('arial', 15, 'bold')).place(relx=0, rely=0.4)
                        addressLabel = Label(show, text=employee[employee.index(self.empProfile) + 3],
                                             font=('arial', 14, 'bold'))
                        addressLabel.place(relx=0.12, rely=0.4)

                        # PHONE NUMBER
                        Label(show, text='PHONE NUM: ', font=('arial', 15, 'bold')).place(relx=0, rely=0.5)
                        phoneLabel = Label(show, text=employee[employee.index(self.empProfile) + 4],
                                           font=('arial', 14, 'bold'))
                        phoneLabel.place(relx=0.15, rely=0.5)

                        # SALARY
                        Label(show, text='SALARY: ', font=('arial', 15, 'bold')).place(relx=0, rely=0.6)
                        salaryLabel = Label(show, text='RM ' + str(employee[employee.index(self.empProfile) + 5]),
                                            font=('arial', 18, 'bold'))
                        salaryLabel.place(relx=0.12, rely=0.6)

                        # ID
                        Label(show, text='ID: ', font=('arial', 22, 'bold')).place(relx=0.4, rely=0.7)
                        salaryLabel = Label(show, text=str(employee[employee.index(self.empProfile)]),
                                            font=('arial', 22, 'bold'), background='silver', foreground='gold')
                        salaryLabel.place(relx=0.45, rely=0.7)

                        # back button
                        backButton = Button(show, text='BACK', style=style1, command=self.showEmployee)
                        backButton.place(relx=0, rely=0)

                        def promotion():
                            try:
                                promote = sd.askstring(title='PROMOTION',
                                                       prompt=f'WHAT POSITION?')
                                up_salary = sd.askfloat(title='PROMOTION',
                                                        prompt=f'HOW MUCH SALARY?')
                            except:
                                messagebox.showwarning("CAUTION", "YOU MUST PRESS SHOW EMPLOYEE FIRST")

                            try:
                                conn = sqlite3.connect(SERVER_PATH)
                                cursor = conn.cursor()
                                cursor.execute("""UPDATE EMPLOYEE_DATA SET EMPLOYEE_POS = ?,SALARY = ? WHERE EMPLOYEE_ID = ?""",
                                               (promote, up_salary, self.empProfile))
                                conn.commit()
                                cursor.execute("""UPDATE EMPLOYEE SET EMPLOYEE_POS = ? WHERE EMPLOYEE_ID = ?""",
                                               (promote, self.empProfile))
                                conn.commit()
                                messagebox.showinfo("SUCCESSFUL",
                                                    f"{self.empProfile} PROMOTED TO {promote} WITH SALARY RM {up_salary}")
                                self.showEmployee()
                            except (Exception, sqlite3.Error) as error:
                                self.check = False
                                print("Error while connecting to database ", error)
                                messagebox.showerror("Database Error", error)

                        def demotion():
                            try:
                                promote = sd.askstring(title='PROMOTION',
                                                       prompt=f'WHAT POSITION?')
                                up_salary = sd.askfloat(title='PROMOTION',
                                                        prompt=f'HOW MUCH SALARY?')
                            except:
                                messagebox.showwarning("CAUTION", "YOU MUST PRESS SHOW EMPLOYEE FIRST")

                            try:
                                conn = sqlite3.connect(SERVER_PATH)
                                cursor = conn.cursor()
                                cursor.execute("""UPDATE EMPLOYEE_DATA
                                                                                                                            SET EMPLOYEE_POS = ?,
                                                                                                                                    SALARY = ?
                                                                                                                            WHERE EMPLOYEE_ID = ?""",
                                               (promote, up_salary, self.empProfile))
                                conn.commit()
                                cursor.execute("""UPDATE EMPLOYEE
                                                                                                                                                        SET EMPLOYEE_POS = ?
                                                                                                                                                        WHERE EMPLOYEE_ID = ?""",
                                               (promote, self.empProfile))
                                conn.commit()
                                messagebox.showwarning("SUCCESSFUL", f"{self.empProfile} DEMOTED TO {promote}")
                                self.showEmployee()
                            except (Exception, sqlite3.Error) as error:
                                self.check = False
                                print("Error while connecting to database ", error)
                                messagebox.showerror("Database Error", error)

                        # promotion button
                        promoteButton = Button(show, text='PROMOTION', style=style1, command=promotion)
                        promoteButton.place(relx=0.85, rely=0.4)

                        # demotion button
                        promoteButton = Button(show, text='DEMOTION', style=style1, command=demotion)
                        promoteButton.place(relx=0.85, rely=0.5)

                        # fired button
                        promoteButton = Button(show, text='FIRED', style=style2, command=self.deleteEmployee)
                        promoteButton.place(relx=0.85, rely=0.7)

                        # adjust employee
                        adjustEmp_button = Button(show, text='ADJUST', style=style1, command=self.adjustEmployee)
                        adjustEmp_button.place(relx=0.85, rely=0.6)


                    else:
                        messagebox.showerror("WRONG ID", "PUT THE CORRECT PRODUCT ID")
                else:
                    messagebox.showerror("ID NOT EXIST", "PUT ANOTHER ID")
            except:
                print("canceled")

    def showEmployee(self):
        show = Frame(master=self.adminWin)
        show.place(relwidth=0.8, relheight=1, relx=0.2)
        frame_image = tk.PhotoImage(master=show, file='images/frameBg.png')
        frame_label = Label(show, background='gold', image=frame_image)
        frame_label.image = frame_image
        frame_label.place(x=0, y=0, relwidth=1, relheight=1)
        style = Style()
        style.configure('W.TButton', font=('Comic sans ms', 15, 'normal', 'italic'), foreground='black')
        style1 = 'W.TButton'

        self.regItem_button.config(state='disabled')
        self.delItem_button.config(state='disabled')
        self.adjustStock_button.config(state='disabled')

        Label(show, text="EMPLOYEE DATA", font=('comic sans ms', 18, 'italic', 'bold')).pack()

        # add employee
        addEmp_button = Button(show, text='add', style=style1, command=self.addEmployee)
        addEmp_button.place(relx=0, rely=0.05)

        # SHOW PROFILE
        profileEmp_button = Button(show, text='profile', style=style1, command=self.employeeProfile)
        profileEmp_button.place(relx=0.2, rely=0.05)

        try:
            employee = [i.strip(" ") for i in
                        self.employeeQuery('employee')]  # PRODUCT_ID[0], PRODUCT_TYPE[1], EXIST[2]
            employee_data = [i.strip(" ") for i in
                             self.employeeQuery(
                                 'employee_data')]  # PRODUCT_ID[0], PRODUCT_NAME[1], PRICE[2], QUANTITY[3]

        except:
            self.check = False

        if self.check:
            if self.check:
                self.check_employeeID = []
                chk = 0
                for i in employee:
                    if len(employee) > chk:
                        self.check_employeeID.append(employee[chk])
                        chk = chk + 4
                id_count = 1
                self.emp_id_count = ''
                for i in self.check_employeeID:
                    id_count = id_count + 1
                if id_count < 10:
                    self.emp_id = "RZ0000E00" + str(id_count)
                    self.emp_id_count = str(id_count)
                elif id_count < 100:
                    self.emp_id = "RZ0000E0" + str(id_count)
                    self.emp_id_count = str(id_count)
                else:
                    self.emp_id = "RZ0000E" + str(id_count)
                    self.emp_id_count = str(id_count)
            self.e_id = []
            self.pos = []
            name = []
            address = []
            phone = []
            salary = []
            # print(employee)   #debug
            # print(employee_data)  #debug
            xt = 2
            xd = 0
            for i in employee_data:
                if len(employee_data) > xd:
                    self.e_id.append(employee_data[xd])
                    xd = xd + 7
                if len(employee_data) > xt:
                    self.pos.append(employee_data[xt])
                    xt = xt + 7

            yn = 1
            yp = 3
            yq = 4
            yz = 5
            for i in employee_data:
                if len(employee_data) > yn:
                    name.append(employee_data[yn])
                    yn = yn + 7
                if len(employee_data) > yp:
                    address.append(employee_data[yp])
                    yp = yp + 7
                if len(employee_data) > yq:
                    phone.append(employee_data[yq])
                    yq = yq + 7
                if len(employee_data) > yz:
                    salary.append(employee_data[yz])
                    yz = yz + 7

            # DATA TABLE
            cols = ('ID', 'NAMA', 'JAWATAN', 'ALAMAT', 'NO.TELEFON', 'GAJI')
            self.data_table = Treeview(show, columns=cols, show='headings')
            for col in cols:
                self.data_table.heading(col, text=col)
            k = 0
            for i in range(len(self.e_id)):
                self.data_table.insert("", END,
                                       values=(
                                           self.e_id[k], name[k], self.pos[k], address[k], int(phone[k]),
                                           'RM ' + str(salary[k])))
                k = k + 1

            self.data_table.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.9)
            vsb = Scrollbar(show, orient="vertical", command=self.data_table.yview)
            vsb.place(relx=0.98, rely=0.1, relheight=0.9)
            hrz = Scrollbar(show, orient="horizontal", command=self.data_table.xview)
            hrz.place(relx=0, rely=0.98, relwidth=1)
            self.data_table.configure(yscrollcommand=vsb.set, xscrollcommand=hrz.set)

        else:
            Label(show, text="""CAN'T CONNECT DATABASE, 
                       PLEASE PRESS THE BUTTON AGAIN""", font=('comic sans ms', 18, 'italic', 'bold'),
                  foreground='red').place(
                relx=0, rely=0.5)

    def deleteEmployee(self):
        try:
            fired = messagebox.askyesnocancel(f"{self.empProfile}", f"FIRED {self.empProfile}")
            if fired == True:
                deleteEMP = self.empProfile
            elif fired == None:
                pass
            else:
                messagebox.showinfo("CANCELED", f"FIRED {self.empProfile} CANCELED")

        except:
            messagebox.showwarning("CAUTION", "YOU MUST PRESS SHOW EMPLOYEE FIRST")

        try:
            if deleteEMP in self.check_employeeID:
                if "RZ" and 'E' in deleteEMP and len(deleteEMP) >= 10:
                    getDel = str(deleteEMP).upper()
                    try:
                        conn = sqlite3.connect(SERVER_PATH)
                        cursor = conn.cursor()
                        print("YOU ARE CONNECTED TO DATABASE")
                        try:
                            cursor.execute(f"DELETE FROM EMPLOYEE_DATA WHERE EMPLOYEE_ID = '{getDel}'")
                            conn.commit()
                            cursor.execute(f"UPDATE EMPLOYEE SET EXIST ={False} WHERE EMPLOYEE_ID = '{getDel}'")
                            conn.commit()
                            pathName = "//Zerozed-pc/shared/DB/gambar_pekerja/" + deleteEMP + ".jpg"
                            os.remove(pathName)
                            self.showEmployee()
                            messagebox.showinfo("SUCCESS", f"{getDel} DELETED ")
                        except:
                            messagebox.showerror("FAILED", "ID NOT FOUND")
                    except (Exception, sqlite3.Error) as error:
                        self.check = False
                        messagebox.showerror("FAILED", "NO DATABASE DETECTED")
                        print("Error while connecting to database ", error)
        except:
            print("CANCELED or Database not connected")

    def addEmployee(self):
        try:
            self.addEMP = sd.askstring(title='REGISTER EMPLOYEE', prompt=f'PRESS OK', initialvalue=self.emp_id)
        except:
            messagebox.showwarning("CAUTION", "YOU MUST PRESS SHOW EMPLOYEE FIRST")

        try:
            if self.addEMP not in self.check_employeeID:
                if "RZ" and 'E' in self.addEMP and len(self.addEMP) >= 10:
                    try:
                        self.addEMPWin = Toplevel(self.adminWin)
                        self.addEMPWin.resizable(0, 0)
                        self.addEMPWin.lift(aboveThis=self.adminWin)
                        self.windowHeight = int(self.addEMPWin.winfo_reqheight())
                        self.windowWidth = int(self.addEMPWin.winfo_reqwidth())
                        self.positionRight = int(self.addEMPWin.winfo_screenwidth() / 2 - (self.windowWidth / 2))
                        self.positionDown = int(self.addEMPWin.winfo_screenheight() / 2 - (self.windowHeight / 2))
                        self.addEMPWin.iconphoto(False, PhotoImage(file='images/rozeriya.png'))
                        self.addEMPWin.geometry(f"400x400+{self.positionRight - 400}+{self.positionDown - 300}")
                        self.addEMPWin.title("ADD EMPLOYEE")
                        style = Style()
                        style.configure('W.TButton', font=('Comic sans ms', 15, 'normal', 'italic'), foreground='black')
                        style1 = 'W.TButton'

                        Label(self.addEMPWin, text="REGISTER ITEM", font=('comic sans ms', 18, 'italic', 'bold')).pack()

                        getNameB = StringVar()
                        getAdress = StringVar()
                        getPhone = IntVar()
                        getPhoto = StringVar()
                        getSalary = IntVar()
                        self.getPhotoBlob = ''

                        def empPhoto():
                            self.addEMPWin.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                                                 filetypes=(
                                                                                     ("jpeg files", "*.jpg"),
                                                                                     ("all files", "*.*")))
                            self.addEMPWin.focus_force()
                            photo = str(self.addEMPWin.filename)
                            getPhoto.set(photo)
                            foo = Image.open(photo)
                            foo = foo.resize((200, 250), Image.ANTIALIAS)
                            pathName = EMPLOYEE_PHOTO_PATH + self.addEMP +".jpg"
                            self.getPhotoBlob = pathName
                            foo.save(os.path.abspath(pathName), quality=100)

                        def query_emp():
                            ID = self.addEMP.upper()
                            ADDRESS = getAdress.get().upper()
                            NAMA = getNameB.get().upper()
                            PHONE = getPhone.get()
                            PHOTO = self.getPhotoBlob
                            SALARY = getSalary.get()
                            d = datetime.now()
                            self.timestamp = d.timestamp()
                            try:
                                conn = sqlite3.connect(SERVER_PATH)  # \\Zerozed-pc\shared\DB
                                cursor = conn.cursor()
                                # print("YOU ARE CONNECTED TO DATABASE")    #debug
                                print(ID, NAMA, 'EMPLOYEE', ADDRESS, PHONE, SALARY, getPhoto.get()) #debug
                                try:
                                    cursor.execute("INSERT INTO EMPLOYEE VALUES(?,?,?,?)",
                                                   (ID, 'EMPLOYEE', True, self.timestamp))
                                    conn.commit()
                                    cursor.execute("INSERT INTO EMPLOYEE_DATA VALUES(?,?,?,?,?,?,?)",
                                                   (ID, NAMA, 'EMPLOYEE', ADDRESS, PHONE, SALARY, PHOTO))
                                    conn.commit()
                                    messagebox.showinfo("SUCCESS", f"REGISTER {ID} DONE")
                                    self.showEmployee()
                                    self.addEMPWin.destroy()
                                except:
                                    messagebox.showerror("FAILED", "ID ALREADY REGISTERED")

                            except (Exception, sqlite3.Error) as error:
                                self.check = False
                                messagebox.showerror("FAILED", "NO DATABASE DETECTED")
                                self.addEMPWin.destroy()
                                print("Error while connecting to DATABASE ", error)

                        # ID DISABLED
                        Label(self.addEMPWin, text='EMPLOYEE ID', font=('Comic sans ms', 12, 'normal', 'italic')).place(
                            relx=0,
                            rely=0.2)
                        reg_entry = Label(self.addEMPWin, font=('Comic sans ms', 12, 'normal', 'italic'),
                                          text=self.addEMP)
                        reg_entry.place(relx=0.38, rely=0.2, width=240)

                        # NAME
                        Label(self.addEMPWin, text='NAME',
                              font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.3)
                        self.empName_entry = Entry(self.addEMPWin, textvariable=getNameB, state='normal')
                        self.empName_entry.place(relx=0.38, rely=0.3, width=240)

                        # ADDRESS
                        Label(self.addEMPWin, text='ADDRESS',
                              font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.4)
                        self.address_entry = Entry(self.addEMPWin, textvariable=getAdress, state='normal')
                        self.address_entry.place(relx=0.38, rely=0.4, width=240)

                        # PHONE NUMBER
                        Label(self.addEMPWin, text='PHONE',
                              font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.5)
                        self.phone_entry = Entry(self.addEMPWin, textvariable=getPhone, state='normal')
                        self.phone_entry.place(relx=0.38, rely=0.5, width=240)

                        # PHOTO
                        Label(self.addEMPWin, text='PHOTO',
                              font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.6)
                        self.photo_entry = Entry(self.addEMPWin, textvariable=getPhoto, state='disabled')
                        self.photo_entry.place(relx=0.38, rely=0.6, width=240)
                        Button(self.addEMPWin, text='BROWSE', command=empPhoto).place(relx=0.15, rely=0.6)

                        # SALARY
                        Label(self.addEMPWin, text='SALARY',
                              font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.7)
                        self.salary_entry = Entry(self.addEMPWin, textvariable=getSalary, state='normal')
                        self.salary_entry.place(relx=0.38, rely=0.7, width=240)

                        # add button
                        self.empAdd_button = Button(self.addEMPWin, style=style1, text='HIRE', command=query_emp,
                                                    state='normal')
                        self.empAdd_button.place(relx=0.5, rely=0.8)
                    except:
                        print("CANCELED")
                else:
                    messagebox.showerror("WRONG ID", "PUT THE CORRECT PRODUCT ID")
            else:
                messagebox.showerror("ID EXISTED", "PUT ANOTHER ID")
        except:
            print("CANCELED")

    def adjustEmployee(self):
        try:
            self.adjustEMP = self.empProfile
        except:
            messagebox.showwarning("CAUTION", "YOU MUST PRESS SHOW EMPLOYEE FIRST")

        try:
            if self.adjustEMP in self.check_employeeID:
                if "RZ" and 'E' in self.adjustEMP and len(self.adjustEMP) >= 10:
                    try:
                        self.adjustEMPWin = Toplevel(self.adminWin)
                        self.adjustEMPWin.resizable(0, 0)
                        self.adjustEMPWin.lift(aboveThis=self.adminWin)
                        self.windowHeight = int(self.adjustEMPWin.winfo_reqheight())
                        self.windowWidth = int(self.adjustEMPWin.winfo_reqwidth())
                        self.positionRight = int(self.adjustEMPWin.winfo_screenwidth() / 2 - (self.windowWidth / 2))
                        self.positionDown = int(self.adjustEMPWin.winfo_screenheight() / 2 - (self.windowHeight / 2))
                        self.adjustEMPWin.iconphoto(False, PhotoImage(file='images/rozeriya.png'))
                        self.adjustEMPWin.geometry(f"400x400+{self.positionRight - 400}+{self.positionDown - 300}")
                        self.adjustEMPWin.title("ADD EMPLOYEE")
                        style = Style()
                        style.configure('W.TButton', font=('Comic sans ms', 15, 'normal', 'italic'), foreground='black')
                        style1 = 'W.TButton'

                        Label(self.adjustEMPWin, text="ADJUST EMPLOYEE DATA", font=('comic sans ms', 18, 'italic', 'bold')).pack()

                        getNameB = StringVar()
                        getAdress = StringVar()
                        getPhone = IntVar()
                        getPhoto = StringVar()
                        getSalary = IntVar()
                        getPhone.set(60)
                        self.getPhotoBlobAdj = ''

                        def empPhoto():
                            #bug here
                            try:
                                self.adjustEMPWin.filename = filedialog.askopenfilename(initialdir="/",
                                                                                        title="Select file",
                                                                                        filetypes=(
                                                                                            ("jpeg files", "*.jpg"),
                                                                                            ("all files", "*.*")))
                                self.adjustEMPWin.focus_force()
                                photo = str(self.adjustEMPWin.filename)
                                getPhoto.set(photo)
                                foo = Image.open(photo)
                                foo = foo.resize((200, 250), Image.ANTIALIAS)
                                pathName = EMPLOYEE_PHOTO_PATH + self.adjustEMP + ".jpg"
                                self.getPhotoBlobAdj = pathName
                                foo.save(os.path.abspath(pathName), quality=100)
                            except:
                                print("exited") #debug

                        def query_emp():
                            ID = self.adjustEMP.upper()
                            ADDRESS = getAdress.get().upper()
                            NAMA = getNameB.get().upper()
                            PHONE = getPhone.get()
                            PHOTO = self.getPhotoBlobAdj
                            SALARY = getSalary.get()
                            d = datetime.now()
                            self.timestamp = d.timestamp()
                            try:
                                conn = sqlite3.connect(
                                    SERVER_PATH)  # \\Zerozed-pc\shared\DB
                                cursor = conn.cursor()
                                # print("YOU ARE CONNECTED TO DATABASE")    #debug
                                # print(ID, NAMA, 'EMPLOYEE', ADDRESS, PHONE, SALARY, getPhoto.get())   #debug
                                try:
                                    if self.adjustEmpRead.get() == 'all':
                                        cursor.execute("""UPDATE EMPLOYEE_DATA
                                        SET NAME = ?,
                                                ADDRESS = ?,
                                                PHONE = ?,
                                                SALARY=?,
                                                PHOTO = ?
                                        WHERE EMPLOYEE_ID = ?""",
                                                       (NAMA, ADDRESS, PHONE, SALARY, PHOTO, ID))
                                        conn.commit()
                                        messagebox.showinfo("SUCCESS", f"REGISTER {ID} DONE")
                                        self.showEmployee()
                                        self.adjustEMPWin.destroy()
                                    elif self.adjustEmpRead.get() == 'employee name':
                                        cursor.execute("""UPDATE EMPLOYEE_DATA
                                                                               SET NAME = ?
                                                                               WHERE EMPLOYEE_ID = ?""",
                                                       (NAMA, ID))
                                        conn.commit()
                                        messagebox.showinfo("SUCCESS", f"REGISTER {ID} DONE")
                                        self.showEmployee()
                                        self.adjustEMPWin.destroy()
                                    elif self.adjustEmpRead.get() == 'address':
                                        cursor.execute("""UPDATE EMPLOYEE_DATA
                                                                SET ADDRESS = ?
                                                                WHERE EMPLOYEE_ID = ?""",
                                                       (ADDRESS, ID))
                                        conn.commit()
                                        messagebox.showinfo("SUCCESS", f"REGISTER {ID} DONE")
                                        self.showEmployee()
                                        self.adjustEMPWin.destroy()
                                    elif self.adjustEmpRead.get() == 'phone number':
                                        cursor.execute("""UPDATE EMPLOYEE_DATA
                                                                    SET
                                                                     PHONE = ?
                                                                    WHERE EMPLOYEE_ID = ?""",
                                                       (PHONE, ID))
                                        conn.commit()
                                        messagebox.showinfo("SUCCESS", f"REGISTER {ID} DONE")
                                        self.showEmployee()
                                        self.adjustEMPWin.destroy()
                                    elif self.adjustEmpRead.get() == 'photo':
                                        cursor.execute("""UPDATE EMPLOYEE_DATA
                                                                    SET PHOTO = ?
                                                                    WHERE EMPLOYEE_ID = ?""",
                                                       (PHOTO, ID))
                                        conn.commit()
                                        messagebox.showinfo("SUCCESS", f"REGISTER {ID} DONE")
                                        self.showEmployee()
                                        self.adjustEMPWin.destroy()
                                    elif self.adjustEmpRead.get() == 'salary':
                                        cursor.execute("""UPDATE EMPLOYEE_DATA
                                                                SET SALARY = ?
                                                                WHERE EMPLOYEE_ID = ?""",
                                                       (SALARY, ID))
                                        conn.commit()
                                        messagebox.showinfo("SUCCESS", f"REGISTER {ID} DONE")
                                        self.showEmployee()
                                        self.adjustEMPWin.destroy()
                                    else:
                                        messagebox.showerror("FAILED", "NOT IN LIST")
                                except (Exception, sqlite3.Error) as error:
                                    messagebox.showerror("FAILED", error)

                            except (Exception, sqlite3.Error) as error:
                                self.check = False
                                messagebox.showerror("FAILED", "NO DATABASE DETECTED")
                                self.reg_itemWin.destroy()
                                print("Error while connecting to DATABASE ", error)

                        def hideButton(null=None):
                            self.empAdj_button.config(state='disabled')
                            self.empAdjName_entry.config(state='disabled')
                            self.addressAdj_entry.config(state='disabled')
                            self.phoneAdj_entry.config(state='disabled')
                            self.submitPhoto.config(state='disabled')
                            self.salaryAdj_entry.config(state='disabled')
                            if self.adjustEmpRead.get() == 'all':
                                self.empAdj_button.config(state='normal')
                                self.empAdjName_entry.config(state='normal')
                                self.addressAdj_entry.config(state='normal')
                                self.phoneAdj_entry.config(state='normal')
                                self.submitPhoto.config(state='normal')
                                self.salaryAdj_entry.config(state='normal')
                            elif self.adjustEmpRead.get() == 'employee name':
                                self.empAdj_button.config(state='normal')
                                self.empAdjName_entry.config(state='normal')
                            elif self.adjustEmpRead.get() == 'address':
                                self.empAdj_button.config(state='normal')
                                self.addressAdj_entry.config(state='normal')
                            elif self.adjustEmpRead.get() == 'photo':
                                self.empAdj_button.config(state='normal')
                                self.submitPhoto.config(state='normal')
                            elif self.adjustEmpRead.get() == 'phone number':
                                self.empAdj_button.config(state='normal')
                                self.phoneAdj_entry.config(state='normal')
                            elif self.adjustEmpRead.get() == 'salary':
                                self.empAdj_button.config(state='normal')
                                self.salaryAdj_entry.config(state='normal')
                            else:
                                messagebox.showerror("WRONG CATEGORY", "CHECK CATEGORY")

                        # ID DISABLED
                        Label(self.adjustEMPWin, text='EMPLOYEE ID', font=('Comic sans ms', 12, 'normal', 'italic')).place(
                            relx=0,
                            rely=0.2)
                        reg_entry = Label(self.adjustEMPWin, font=('Comic sans ms', 12, 'normal', 'italic'),
                                          text=self.adjustEMP)
                        reg_entry.place(relx=0.38, rely=0.2, width=240)

                        # NAME
                        Label(self.adjustEMPWin, text='NAME',
                              font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.3)
                        self.empAdjName_entry = Entry(self.adjustEMPWin, textvariable=getNameB, state='disabled')
                        self.empAdjName_entry.place(relx=0.38, rely=0.3, width=240)

                        # ADDRESS
                        Label(self.adjustEMPWin, text='ADDRESS',
                              font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.4)
                        self.addressAdj_entry = Entry(self.adjustEMPWin, textvariable=getAdress, state='disabled')
                        self.addressAdj_entry.place(relx=0.38, rely=0.4, width=240)

                        # PHONE NUMBER
                        Label(self.adjustEMPWin, text='PHONE',
                              font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.5)
                        self.phoneAdj_entry = Entry(self.adjustEMPWin, textvariable=getPhone, state='disabled')
                        self.phoneAdj_entry.place(relx=0.38, rely=0.5, width=240)

                        # PHOTO
                        Label(self.adjustEMPWin, text='PHOTO',
                              font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.6)
                        self.photoAdj_entry = Entry(self.adjustEMPWin, textvariable=getPhoto, state='disabled')
                        self.photoAdj_entry.place(relx=0.38, rely=0.6, width=240)
                        self.submitPhoto = Button(self.adjustEMPWin, text='BROWSE', command=empPhoto, state='disabled')
                        self.submitPhoto.place(relx=0.15, rely=0.6)

                        # SALARY
                        Label(self.adjustEMPWin, text='SALARY',
                              font=('Comic sans ms', 12, 'normal', 'italic')).place(relx=0, rely=0.7)
                        self.salaryAdj_entry = Entry(self.adjustEMPWin, textvariable=getSalary, state='disabled')
                        self.salaryAdj_entry.place(relx=0.38, rely=0.7, width=240)

                        # adjust button
                        self.empAdj_button = Button(self.adjustEMPWin, style=style1, text='ADJUST', command=query_emp,
                                                    state='disabled')
                        self.empAdj_button.place(relx=0.5, rely=0.8)

                        list = ['employee name', 'address', 'phone number', 'photo','salary' ,'all']
                        self.adjustEmpRead = StringVar()
                        # combobox choice
                        Label(self.adjustEMPWin, text='CATOGERY', font=('arial black', 10)).place(relx=0, rely=0.8)
                        self.adjustEmpChoice = Combobox(self.adjustEMPWin, textvariable=self.adjustEmpRead, values=list)
                        self.adjustEmpChoice.bind('<<ComboboxSelected>>', hideButton)
                        self.adjustEmpChoice.place(relx=0, rely=0.85)

                    except:
                        print("CANCELED")
                else:
                    messagebox.showerror("WRONG ID", "PUT THE CORRECT PRODUCT ID")
            else:
                messagebox.showerror("ID NOT EXIST", "PUT ANOTHER ID")
        except:
            print("CANCELED")


#TODO try using ADJUST_FLOW AND ADJUST_CACHE
#TODO REGISTER_CACHE for new product will be used

# AdminWin(master=Tk(), ID='TEST1234', POS='MANAGER')   #test debug for admin_page.py
