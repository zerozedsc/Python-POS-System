# Python-Point-Of-Sale-System
I make a P.O.S system with python for my father company Rozeriya Enterprise using Python. For the database i just use SQLITE for this time because i dont have much knowledge in using cloud database like mysql. I will always update this project

_`PYTHON 3.8`To run this project you can start from session_start.py, and for the database
you can change the path at `server.py`, var `SERVER_PATH`_ to actual local db location

_~~I will add a function to access server database~~_

Actually I try to make a database server but I did not know how to do that so I just using my computer 
to become a host for local network and the database is inside network folder, because of that
, the database path it actually my network path

###### TO EDIT SQLITE DB You need to download DB BROWSER for SQLite
###### To log in you can use `RZ0000E0001` to get fully access

![face](/zerozedsc/Python-Point-Of-Sale-System/readme_img/1.webp)

v 2.0
=

cashier_win.py
- Add debugger Note and noted the print debugger
- Change Print Receipt Path using abspath
- Add report data in xlsx file (daily report only)
- The conclution of the report will be write after exit or back to the session window
-Add add stock function in cashier window


admin_page.py
- Add debugger Note and noted the print debugger
- Change path of saved employee photo to data/Employee Data/Employee_Photos


session_start.py
- Add add stock function in session choice window

