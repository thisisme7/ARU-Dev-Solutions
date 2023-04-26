# ARU-Dev-Solutions
Simple API for finctional organization that consists of HTML, CSS files and a Python 3.10 script. 

These are all the modules and libraries that have to be installed:

pip install flask flask_wtf wtforms sqlalchemy talisman flask_login

This database connection string you need to reconfigure to correct username, password and database name. If you are using diffrenet DBMS, the string probalby has to have a different format.

engine = create_engine("mariadb+pymysql://username:password@127.0.0.1:3306/arudevsol")

Program uses threads that make run HTTP, HTTPS simultaneously. Once initiated, based on the credentials in databse, user can login and browse and view other users in the database.
