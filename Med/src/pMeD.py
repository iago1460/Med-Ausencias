#!/usr/bin/python
# --*-- coding: utf-8 --*--
import gtk
import sys
import time
import datetime


class Business_Contraint(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

# Ventana principal
class WindowMain:
	def __init__(self, father, emp):
		self.builder = gtk.Builder()
		self.builder.add_from_file("windowmain.glade")	
		self.builder.connect_signals(self)
		self.w = self.builder.get_object("window_main")
		self.tv = self.builder.get_object("treeview")
		self.store = self.builder.get_object("liststoreTreeview")
		self.w.show_all()
		self.father = father  # se guarda el objeto padre
		self.employee = emp
		self.inicializeList(emp)

	# ventana para anadir tareas nuevas
	def on_addrequest(self, d):
		# se crea un objeto nuevo de tipo WindowRequest
		w_request = WindowRequest(self)		

	def add_request_glade(self, request):
		self.store.append([request._id, request._employee.name, request._type, request._dateRequest, request._dateIni, request._dateEnd, request._state])
		
	# metodo que añade la tarea a la lista
	def addrequest(self, typeRequest, dateRequest, dateIni, dateEnd, state):
		request = Request(self.employee, typeRequest, dateRequest, dateIni, dateEnd, state)
		days = diference(dateIni, dateEnd)
		days += 1	#se contabilizan ambos dias
		
		if (days<1):
			raise Business_Contraint("Rango de fechas incorrecta")
		else:
			if (typeRequest == "Asuntos personales"):
				if (days>self.employee.ownDays):
					raise Business_Contraint("Dias de asuntos personales insuficientes")
				else:
					self.employee.ownDays -= days
					success = True
			elif(typeRequest == "Vacaciones"):
				if (days>self.employee.holidayDays):
					raise Business_Contraint("Dias de vacaciones insuficientes")
				else:
					self.employee.holidayDays -= days
		print request
		requests.append(request)
		return request

	def inicializeList(self, emp):
		for request in requests:
			if emp.id == request._employee.id or request._employee.boss == emp.id: #or es jefe de proyecto
				add_request_glade(request)
		
		

	# metodo para eliminar una tarea seleccionada
	def on_deleterequest(self, tv):
		selec = self.tv.get_selection()
		t = selec.get_selected()
		if t[1] != None:
			for request in requests:  # buscamos la tarea en requests y la eliminamos
				reqId = t[0].get_value(t[1], 0)
				if (request._id == reqId):
					requests.remove(request)
					break
			self.store.remove(t[1])

	#*******************************************************************
	# Funcion para parsear la fecha
	def parse_date(self, f):		
		d = f._deadline.strip().split("/")
		return d


	#*******************************************************************
	# pulsar boton "cancelar" (ocultar la ventana)	
	def on_cancel(self, w):
		w.hide()
		
	# Volver a inicio
	def on_quit(self, w):
		self.w.destroy()
		self.father.show()
	def on_exit(self, w, e):
		self.w.destroy()
		self.father.show()

#***********************************************************************
# Objeto: ventana utilizada para añadir tareas nuevas
class WindowLogin:
	def __init__(self):
		self.builder = gtk.Builder()		
		self.builder.add_from_file("windowlogin_gtk2.glade")	
		self.builder.connect_signals(self)
		self.w = self.builder.get_object("window_login")
		self.w.show_all()
		self.empOb = self.builder.get_object("entryEmployee")
		self.typeOb = self.builder.get_object("entryPass")

	# pulsar boton "enviar"
	def on_sendRequest(self, dialog, *data):
		emp = self.empOb.get_text()
		passw = self.typeOb.get_text()
		emp = getEmployee(emp, passw)
		if emp is None:
			show_err_dialog("Credenciales incorrectos")
		else:
			WindowMain(self, emp)
			self.w.hide()
		
	def show(self):
		self.empOb.set_text("")
		self.typeOb.set_text("")
		self.w.show()
	
	# Cerrar
	def on_quit(self, w):
		gtk.main_quit()
		sys.exit()
	def on_exit(self, w, e):
		gtk.main_quit()
		sys.exit()

def show_err_dialog(text):
	md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, text)
	md.run()
	md.destroy()

#***********************************************************************
# Objeto: ventana utilizada para añadir tareas nuevas
class WindowRequest:
	def __init__(self, father):
		self.builder = gtk.Builder()		
		self.builder.add_from_file("windowaddrequest.glade")	
		self.builder.connect_signals(self)
		self.w = self.builder.get_object("window_addrequest")
		self.w.show_all()
		self.father = father  # se guarda el objeto padre
		self.calendar = self.builder.get_object("messagedialogCalendar")
		self.typeOb = self.builder.get_object("entryType")
		self.dateIniOb = self.builder.get_object("entryDateIni")
		self.dateEndOb = self.builder.get_object("entryDateEnd")

	# pulsar boton "enviar"
	def on_sendRequest(self, dialog, *data):
		dateReq = time.strftime("%d/%m/%Y", time.gmtime())
		dateIni = self.dateIniOb.get_text()
		dateEnd = self.dateEndOb.get_text()		

		typeReq = "Vacaciones"
		tree_iter = self.typeOb.get_active_iter()
		if tree_iter != None:
			model = self.typeOb.get_model()
			typeReq = model[tree_iter][1]  # obtenemos elemento 1: nombre del tipo
		
		
		success = False
		
		
		
		try:
			request = self.father.addrequest(typeReq, dateReq, dateIni, dateEnd, False)  # procesar datos
			self.father.add_request_glade(request)
			self.w.destroy()
		except Business_Contraint as e:
			print show_err_dialog(e.value)

	# mostrar calendario
	def on_calendarIni(self, d):
		self.builder.add_from_file("windowaddrequest.glade")	
		self.builder.connect_signals(self)
		self.calendar = self.builder.get_object("messagedialogCalendar1")
		self.calendar.show_all()

	# mostrar calendario
	def on_calendarEnd(self, d):
		self.builder.add_from_file("windowaddrequest.glade")	
		self.builder.connect_signals(self)
		self.calendar = self.builder.get_object("messagedialogCalendar2")
		self.calendar.show_all()


	# pulsar boton "enviar" del calendario
	def get_fechaIni(self, calendar):
		dateCal = calendar.get_date()
		date = str(dateCal[2]) + "/" + str(dateCal[1]+1) + "/" + str(dateCal[0])	
		self.dateIniOb.set_text(date)
		self.calendar.hide()

	# pulsar boton "enviar" del calendario
	def get_fechaEnd(self, calendar):
		dateCal = calendar.get_date()
		date = str(dateCal[2]) + "/" + str(dateCal[1]+1) + "/" + str(dateCal[0])	
		self.dateEndOb.set_text(date)
		self.calendar.hide()
		
	def str_to_date(self, date):
		fecha_servidor_tupla = time.strptime(date, "%d/%m/%Y")

	# pulsar boton "cancelar" (ocultar la ventana)
	def on_cancel(self, w):
		w.hide()



def diference(date1, date2):
	now = datetime.datetime(int(date1.split("/")[2]), int(date1.split("/")[1]), int(date1.split("/")[0]), 0, 0, 0)
	fut = datetime.datetime(int(date2.split("/")[2]), int(date2.split("/")[1]), int(date2.split("/")[0]), 0, 0, 0)
	diff = fut - now
	return diff.days


#***********************************************************************
requestId = 0

class Request(object):
	def __init__(self, employee, t, dateRequest, dateIni, dateEnd, state):
		global requestId
		self._id = requestId
		requestId = requestId + 1
		self._employee = employee
		self._type = t
		self._dateRequest = dateRequest
		self._dateIni = dateIni
		self._dateEnd = dateEnd
		self._state = state

	def __str__(self):
		return str(self._id) + "|" + self._employee.name + "|" + str(self._type) + "|" + str(self._dateRequest) + "|" + str(self._dateIni) + "|" + str(self._dateEnd) + "|" + str(self._state)


#***********************************************************************
class Employee(object):
	def __init__(self, empId, bossId, name, passw, holidayDays, ownDays):
		self.name = name
		self.id = empId
		self.passw = passw
		self.boss = bossId
		self.holidayDays = holidayDays
		self.ownDays = ownDays
		
	def __str__(self):
		return str(self.id) + "|" + str(self.boss) + "|" + self.name + "|" + self.passw + "|" + str(self.holidayDays) + "|" + str(self.ownDays)


#***********************************************************************
def print_list(requests):
	for request in requests:
		print str(request)

def load_employees():
	try:
		filename = 'employees.txt'
		f = open(filename, 'r')	
		for line in f:
			item = line.strip().split("|")
			employees.append(Employee(int(item[0]), int(item[1]), item[2], item[3], int(item[4]), int(item[5])))
		f.close()
	except IOError:
		print "Error de lectura: " + filename

def getEmployee(name, passw):
	for emp in employees:
		if (emp.name == name) & (emp.passw == passw):
			return emp
	

#***********************************************************************


requests = []
employees = []

def main():
	str = "23/2/2012"
	now = datetime.datetime(int(str.split("/")[2]), int(str.split("/")[1]), int(str.split("/")[0]), 0, 0, 0)
	fut = datetime.datetime(2012, 3, 23, 0, 0, 0)
	diff = fut - now
	print diff
	print diff.days
	print diff.seconds


	load_employees()
	print_list(employees)
	wmain = WindowLogin()
	gtk.main()


if  __name__ =='__main__':main()
