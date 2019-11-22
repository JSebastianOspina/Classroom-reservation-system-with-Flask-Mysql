
# How it Works ?
This system consist on a Flask-based Python website connected with a MySQL database, that contain all the information needed for the tools that the system offer.

It will allow you to make reservations for the classrooms, auditoriums and any 
sports stage. Also, any problematic that requires the scheduling of any place or service, can implement this system.

*There are two things that we need to set up, the data base, and the Flask application*

# Requirements
### Hardware 
There are no extra Hardware requirements.

### Software 
- Windows or Ubuntu.
- Python 3+.
- Xampp or host.

# Database 
A MySQL database needs to be created, there are two options: using phpMyAdmin, or MySQL directly. 

If you want to use just MySQL, there is a good option: you can create the database, tables , registers and all the initial set-up with phpMyAdmin, then , you import it to your MySQL server.

## Using phpMyAdmin
- Download xampp server, it will contain a local phpMyAdmin server.

- Start the server.

- Then, go to web browser and enter to [localhost](http://localhost). It will show you a menu, then, click phpMyAdmin option.

- Create database. If you want to use our test files [(available on repository)](https://github.com/JSebastianOspina/Classroom-reservation-system-with-Flask-Mysql) you must use 'salones' as the database name.

- Then click import , in the top part of the website.

![enter image description here](https://i.ibb.co/VBK3yKZ/descarga.png)

- Select the 'full-database.sql' file and upload it. 

phpMyAdmin Will automatically create all the tables and registers.

## Using pure MySQL.
- Go to your MySQL console.
- Create data base named 'salones'
- Upload to your server, the MySQL file, it can be done through the cpanel from your host, the file manager , or through ftp, using a ftp client like FileZilla.
- Use the following line 

```source full-database.mysql;```

![enter image description here](https://i.ibb.co/QjnNK2j/descarga-1.png)
All the tables and registers, will be created.

# Flask server 
Before we start, a Python 3+ version is needed for running all the code lines without any syntax error.

Install Flask, type on console

`pip3 install Flask`

Then, install the library 'Flask MySQL-DB'

`pip3 install flask-mysqldb`

The application send emails to the users and administrator. You can create an email account specially for this task. Also, you can use an already-created one, but it's not recommended.

### Configurating Gmail.
*Before we can send the emails, we need to set up the Gmail account.*

Go to https://support.google.com/a/answer/6260879?hl=es and allow external application to access your Google account.

## Setting up data base in app. py file.
Modify the following lines (105-110)
Change the values inside the colons for your MySQL server ones.

```app = Flask(__name__)
app.config['MYSQL_HOST'] = 'HOST'
app.config['MYSQL_USER'] = 'USER'
app.config['MYSQL_PASSWORD'] = 'PASSWORD'
app.config['MYSQL_DB'] = 'salones'
db = MySQL(app) #Configuramos la base de datos
```

Note: if you are using xampp, host, user and password will be 'localhost', 'root',''.

During the whole project, multiple email-send methods were created. You should use sublime-text3 code editor or any other with the ability of finding and replacing text.

### On sublime-text3 
- Click view in the top panel.
- Select Find option, click Replace

![Sublime Text](https://i.ibb.co/313CgT6/descarga-2.png)
- Find 'yourmail@gmail.com'(without colons) and remplace it with your Gmail account(previously configured)

![enter image description here](https://i.ibb.co/8B8RqCL/descarga-3.png)
- Find 'yourpassword' (without colons) and remplace it with your Gmail account password.
- Go to line 80 and change the address provided, for yours.

Finally use the console and type (Ubuntu)
`ifconfig`
for Windows.
`
ipconfig
` 

And remplace your ip in the following line (320)
```
if(1==1):
app.run(host='YOUR IP',port=8000,debug=True
```

Now you are ready !

For starting the Flask server , you have to go to the folder where the files are, **with the cd command.** Then, run the app.py file:

`
cd yourProyectDirectory
`
`
Python3 app.py
`

The server is running now.

If you go to your web browser and type http://YourIp:8000

You will be able to see the hole site working.

**Full video**: [https://www.youtube.com/watch?v=GV-QhQJ_jkk&t=6s](https://www.youtube.com/watch?v=GV-QhQJ_jkk&t=6s)
