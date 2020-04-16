# type/draw a text string to the default printer
# needs the win32 extensions package  pywin32-204.win32-py2.4.exe
# from: http://starship.python.net/crew/mhammond/win32/Downloads.html
# make sure the printer is turned on and ready ...
# tested with Python24    vegaseat    14oct2005
import tempfile

import win32api
import win32ui
import win32print
import win32con


filename = tempfile.mktemp ("test.txt")
# test = open (filename, "w+")
# resit = open('temp/resit.txt', 'r')
# test.write(str([i.strip('\n') for i in resit.readlines()]))
# win32api.ShellExecute (
#   0,
#   "print",
#   filename,
#   #
#   # If this is None, the default printer will
#   # be used anyway.
#   #
#   '/d:"%s"' % win32print.GetDefaultPrinter (),
#   ".",
#   0ADMIN_POS
# )

from data.callDB import callDB
db = callDB()
db.cursor.execute(f"SELECT * FROM MEMBER WHERE MEMBER_ID = 'RZ0000M001'")
db.conn.commit()
rawValue = db.cursor.fetchone()
print(rawValue)