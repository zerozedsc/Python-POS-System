import sqlite3
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import *
import os
from server import SERVER_PATH as PATH

class callDB():
    def __init__(self):
        pathDB = PATH
        try:
            self.conn = sqlite3.connect(pathDB)  # \\Zerozed-pc\shared\DB
            self.cursor = self.conn.cursor()
            print(f"{pathDB} found")
        except:
            getCall = messagebox.askyesnocancel("ERROR", "DATABASE NOT FOUND", icon='error')
            if getCall== True:
                filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                                     filetypes=(
                                                                         ("db files", "*.db"),
                                                                         ("all files", "*.*")))
            readPath = open("pathDB.cfg", "w+")
            readPath.write(str(filename))
            pathDB = str(readPath.read())
            readPath.close()
            self.conn = sqlite3.connect(pathDB)  # \\Zerozed-pc\shared\DB
            self.cursor = self.conn.cursor()


callDB()