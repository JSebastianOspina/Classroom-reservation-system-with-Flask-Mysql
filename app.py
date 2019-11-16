from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


#import netifaces as ni
import smtplib, random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def protocoloCorreo(dia,hora,hola,user):

    anfitrion = "smtp.gmail.com"
    puerto = 587
    direccionDe = "yourmail@gmail.com"
    contrasenaDe = "yourpassword"
    direccionPara = user # PAra quien

    servidor = smtplib.SMTP(anfitrion,puerto)
    servidor.starttls()
    servidor.login(direccionDe,contrasenaDe)
    print(servidor.ehlo())


    asunto = "INFORMACION SOBRE SU RESERVA"
    correo = MIMEMultipart() # SE CREA EL OBJETO
    correo['From'] = direccionDe
    correo['To'] = direccionPara
    correo['Subject'] = asunto



    message = "Estimado usuario, se ha reservado con exito el salon "+str(hola)+" el dia "+dia+" desde las "+hora
    mensaje = MIMEText(message)
    correo.attach(mensaje)


    servidor.sendmail(direccionDe,direccionPara,correo.as_string())





def correoauditorio(correo):

    anfitrion = "smtp.gmail.com"
    puerto = 587
    direccionDe = "yourmail@gmail.com"
    contrasenaDe = "yourpassword"
    direccionPara = correo # PAra quien

    servidor = smtplib.SMTP(anfitrion,puerto)
    servidor.starttls()
    servidor.login(direccionDe,contrasenaDe)
    print(servidor.ehlo())


    asunto = "SU SOLICITUD HA SIDO ENVIADA	"
    correo = MIMEMultipart() # SE CREA EL OBJETO
    correo['From'] = direccionDe
    correo['To'] = direccionPara
    correo['Subject'] = asunto



    message = """Estimado usuario, se ha realizado con exito su solicutud para la reserva del auditorio. Se contactara con usted a este correo para confirmar o realizar ajustes a su reserva. Gracias por su comprension"""
    mensaje = MIMEText(message)
    correo.attach(mensaje)


    servidor.sendmail(direccionDe,direccionPara,correo.as_string())


def correoAdmin(nombre,correoo,fecha,hora,asistentes,razon):

    anfitrion = "smtp.gmail.com"
    puerto = 587
    direccionDe = "yourmail@gmail.com"
    contrasenaDe = "yourpassword"
    direccionPara = "2420171030@estudiantesunibague.edu.co" # PAra quien

    servidor = smtplib.SMTP(anfitrion,puerto)
    servidor.starttls()
    servidor.login(direccionDe,contrasenaDe)
    print(servidor.ehlo())


    asunto = "Solicitud de reserva : "+nombre
    correo = MIMEMultipart() # SE CREA EL OBJETO
    correo['From'] = direccionDe
    correo['To'] = direccionPara
    correo['Subject'] = asunto



    message = """Se ha realizado una nueva solicitud de reserva de auditorio, el profesor """+nombre+""" identificado con correo: """+correoo+""" desea reservar el auditorio el dia: """+str(fecha)+""" en el siguiente rango horario: """+hora+""" para una cantidad de: """+asistentes+""" Asistentes. La razon por la cual lo desea reservar es la siguiente: '"""+razon+"'."
    #message = "Se ha realizado una nueva solicitud de reserva de auditorio, el profesor "+nombre+ "identificado con el correo: "+correoo
    mensaje = MIMEText(message)
    correo.attach(mensaje)


    servidor.sendmail(direccionDe,direccionPara,correo.as_string())


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'HOST'
app.config['MYSQL_USER'] = 'USER'
app.config['MYSQL_PASSWORD'] = 'PASSWORD'
app.config['MYSQL_DB'] = 'DATA BASE NAME'
db = MySQL(app) #Configuramos la base de datos
a = None
b = None
dia = None
hora = None
prestamo = None

app.secret_key = "mysecretkey" #Para poder redireccionar

def darHora(horaa):
	partido = str.split(horaa,"-") #Se obtiene hora de inicio y fin
	primeraHora=partido[0] #Primera Hora
	segundaHora=partido[1] # Segunda hora
	primeraFinal = primeraHora
	if '30' in primeraHora: #Se verifica si es media hora, u hora exacta
		primeraFinal=str.split(primeraHora,":") #Obtenemos lo que esta antes del :
		primeraFinal = primeraFinal[0] + ".5"  # Le adjuntamos el .5
	else:
		primeraFinal=str.split(primeraHora,":") #Si no tiene, es porque es hora exacta
		primeraFinal = primeraFinal[0] + ".0" #Se colocamos .0
		#Ahora con la segunda Hora
	if '30' in segundaHora: #Se verifica si es media hora, u hora exacta
		segundaFinal=str.split(segundaHora,":") #Obtenemos lo que esta antes del :
		segundaFinal = segundaFinal[0] + ".5"  # Le adjuntamos el .5
	else:
		segundaFinal=str.split(segundaHora,":") #Si no tiene, es porque es hora exacta
		segundaFinal = segundaFinal[0] + ".0" #Se colocamos .0
	primeraNumero = float(primeraFinal)
	segundaNumero = float(segundaFinal)
	x = int((primeraNumero - 6)*2) #Convertimos a entero
	y = int((segundaNumero - 6)*2) #Convertimos a entero

	return x,y

def intermedios(primeraHora,segundaHora,aux): #Se encarga de encontrar las horas correspondientes.

	if aux == 2:
		frase = "SELECT * FROM salones WHERE "+str(dia)+" =1 AND `"+str(a)+"` = 1 AND `"+str(b)+"` = 1"
	elif aux ==1:
		frase = "SELECT * FROM salones WHERE "+str(dia)+" =1 AND tablero = '"+str(tablero)+"' AND `"+str(a)+"` = 1 AND `"+str(b)+"` = 1"
	elif aux ==3:
		frase = "SELECT * FROM salones WHERE "+str(dia)+" =1 AND videobeam = '"+str(tablero)+"' AND `"+str(a)+"` = 1 AND `"+str(b)+"` = 1"

	else:
		frase = "SELECT * FROM salones WHERE "+str(dia)+" =1 AND videobeam = '"+str(videobeam)+"' AND tablero = '"+str(tablero)+"' AND `"+str(a)+"` = 1 AND `"+str(b)+"` = 1"
	for i in range (primeraHora+1,segundaHora):
		frase+=" AND `"+str(i)+"` = 1"
	return frase
	print(frase)

def actualizarSalones(primeraHora,segundaHora): #Encuentra las horas intermedias para actualizarlas

	if (segundaHora-primeraHora) == 1:
			frase="hola"
	else:
		frase = "UPDATE salones SET `"+str(primeraHora)+"` = 0, `"+str(segundaHora)+"` = 0"
		for i in range (primeraHora+1,segundaHora):
			frase+=", `"+str(i)+"` = 0"
	return frase
	print(frase)


@app.route('/salones')
def Index():
	cursor = db.connection.cursor()
	cursor.execute('SELECT * FROM salones WHERE sabado=1')
	data = cursor.fetchall()
	cursor.close()
	return render_template('index.html',data = data)

@app.route('/consulta',methods=['POST'])
def consulta():
	global dia
	global videobeam
	global tablero

	if request.method=='POST': #Si se han enviado datos
		global dia
		global hora
		dia = request.form['dia'] #Obtenemos los datos del formulario
		videobeam = request.form['videobeam']
		tablero = request.form['tablero']
		hora = request.form['hora']
		estudiantes = request.form['estudiantes']
		global prestamo
		prestamo = request.form['prestamo']
		print (prestamo)
		aux = 4
		if videobeam == "no" and tablero == "si":
			aux = 1
		if videobeam == "no" and tablero == "no":
			aux = 2
		if tablero == "no" and videobeam =="si":
			aux = 3

		aa = darHora(hora)
		global a
		global b
		a = aa[0]
		b = aa[1]
		print(dia)
		print(videobeam)
		print(aa)
		frase = intermedios(a,b,aux)
		cursor = db.connection.cursor()
		
		cursor.execute(frase)



		#Buscamos que coincidan con la base de datos, se pregunta por el dia de disponibilidad, si tiene videobeam y tablero
		data = cursor.fetchall() #Se obtiene en una lista
		cursor.close() #Se cierra la conexion
		return render_template('consulta.html', datos = data) #Se visualizara los resultados, y se pasa a data como parametro

@app.route('/reservar/<id>')
def reservar(id):
	cursor = db.connection.cursor()
	frase=actualizarSalones(a,b)
	cursor.execute("SELECT * FROM salones WHERE id = {0}".format(id))
	data = cursor.fetchall()
	hola = data[0]
	holaa=hola[1]
	if holaa == 11:
		holaa="L1"
	if frase == "hola":
		cursor.execute("UPDATE salones SET `{0}` = 0, `{1}` = 0 WHERE id = {2}".format(a,b,id)) #Caso ideal, cero diferencia
	else:
		frase+= " WHERE id = "+id # Anadimos el id a la frase 
		cursor.execute(frase)
	db.connection.commit() #Guardamos cambios 
	cursor.close() # Cerramos la conexion
	user = email
	protocoloCorreo(dia,hora,holaa,user) # Enviamos el correo electronico 
	#Ahora, hay que guardar en la tabla de usuarios
	cursor = db.connection.cursor()
	
	cursor.execute("INSERT INTO reservas (usuario,hora,salon,razon) VALUES ('{0}','{1}','{2}','{3}');".format(user,hora,holaa,prestamo))
	db.connection.commit()
	cursor.close()
	flash('Reserva realizada. Se ha enviado un email de confirmacion.')
	return redirect(url_for('Index'))

@app.route('/validar/<id>',methods=['POST','GET'])
def validar(id):
	if request.method=='POST':
		codigo = request.form['codigo'] #Obtenemos los datos del formulario
		cursor = db.connection.cursor()
		contador = cursor.execute("SELECT * FROM usuarios WHERE codigo = '{0}'".format(codigo))
		data=cursor.fetchall()
		
		
		if contador>0:
			mail = data[0]
			global email
			email=mail[1]
			return redirect("/reservar/"+id, code=302)
		else:
			return render_template('validar.html',id=id,ola=1)
	return render_template('validar.html',id=id)

@app.route('/login',methods=['POST','GET'])
def login():
	if request.method=='POST':
		email = request.form['email'] #Obtenemos los datos del formulario
		passs = request.form['pass'] #Obtenemos los datos del formulario
		cursor = db.connection.cursor()
		contador = cursor.execute("SELECT * FROM usuarios WHERE correo = '{0}' AND pass = '{1}'".format(email,passs))
		if contador>0:
			datos = cursor.fetchall()
			datoss = datos[0]
			codigo = datoss[3]
			nombre = datoss[4]
			return render_template('login.html',codigo=codigo,nombre=nombre)
		else:
			codigo=0
			return render_template('login.html',codigo=codigo)
	codigo = 2
	return render_template('login.html',codigo=codigo)


@app.route('/')
def inicio():
	
	return render_template('inicio.html')


@app.route('/auditorio',methods=['POST','GET'])
def auditorio():
	if request.method=='POST':
		nombre = request.form['nombre'] #Obtenemos los datos del formulario
		correoo = request.form['correo'] 
		fecha = request.form['fecha'] 
		hora = request.form['hora'] 
		asistentes = request.form['asistentes'] 
		razon = request.form['razon'] 
		correoauditorio(correoo)
		correoAdmin(nombre,correoo,fecha,hora,asistentes,razon)
		return redirect(url_for('enviado'))

	return render_template('auditorios.html')


@app.route('/enviado')
def enviado():
	

	return render_template('enviado.html')


if(1==1): #Iniciamos el servidor
	app.run(host='YOUR IP',port=8000,debug=True)