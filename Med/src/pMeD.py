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

class Date_Violation(Exception):
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
		self.inicialize_list(emp)

	# ventana para anadir tareas nuevas
	def on_addrequest(self, d):
		w_request = WindowRequest(self)		

	def add_request_glade(self, request):
		self.store.append([request._id, request._employee.name, request._type, request._dateRequest, request._dateIni, request._dateEnd, request._state])
		
	def inicialize_list(self, emp):
		for request in Request.get_visible_requests(emp):
			self.add_request_glade(request)

	# metodo para eliminar una tarea seleccionada
	def on_deleterequest(self, tv):
		selec = self.tv.get_selection()
		t = selec.get_selected()
		if t[1] != None:
			for request in Request.requests:  # buscamos la tarea en requests y la eliminamos
				reqId = t[0].get_value(t[1], 0)
				if (request._id == reqId):
					Request.remove_request(request)
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
		emp = Employee.get_employee(emp, passw)
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
		
		try:
			request = Request(self.father.employee, typeReq, dateReq, dateIni, dateEnd, False)  # procesar datos
			Request.add_request(request)
			self.father.add_request_glade(request)
			self.w.destroy()
		except (Business_Contraint, Date_Violation) as e:
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
		date = str(dateCal[2]) + "/" + str(dateCal[1] + 1) + "/" + str(dateCal[0])	
		self.dateIniOb.set_text(date)
		self.calendar.hide()

	# pulsar boton "enviar" del calendario
	def get_fechaEnd(self, calendar):
		dateCal = calendar.get_date()
		date = str(dateCal[2]) + "/" + str(dateCal[1] + 1) + "/" + str(dateCal[0])	
		self.dateEndOb.set_text(date)
		self.calendar.hide()
		
	def str_to_date(self, date):
		fecha_servidor_tupla = time.strptime(date, "%d/%m/%Y")

	# pulsar boton "cancelar" (ocultar la ventana)
	def on_cancel(self, w):
		w.hide()


def str_to_datetime(str_date):
	return datetime.datetime(int(str_date.split("/")[2]), int(str_date.split("/")[1]), int(str_date.split("/")[0]), 0, 0, 0)

def diference(date1, date2):
	now = str_to_datetime(date1)
	fut = str_to_datetime(date2)
	diff = fut - now
	return diff.days


#***********************************************************************

class Request(object):
	count = 0
	requests = []
	
	@staticmethod
	def add_request(request):
		Request.requests.append(request)

	@staticmethod
	def remove_request(request):
		Request.requests.remove(request)
	
	@staticmethod
	def get_visible_requests(emp):
		list = []
		for request in Request.requests:
			if emp.id == request._employee.id or request._employee.boss == emp.id:  # or es jefe de proyecto
				list.append(request)
		return list
	
	def __init__(self, employee, typeRequest, dateRequest, dateIni, dateEnd, state):
		days = diference(dateIni, dateEnd)
		days += 1  # se contabilizan ambos dias
		
		if (days < 1):
			raise Date_Violation("Rango de fechas incorrecta")
		else:
			if (typeRequest == "Asuntos personales"):
				if (days > employee.ownDays):
					raise Business_Contraint("Dias de asuntos personales insuficientes")
				else:
					employee.ownDays -= days
					success = True
			elif(typeRequest == "Vacaciones"):
				if (days > employee.holidayDays):
					raise Business_Contraint("Dias de vacaciones insuficientes")
				else:
					employee.holidayDays -= days
		
		self.__class__.count += 1
		self._id = Request.count
		self._employee = employee
		self._type = typeRequest
		self._dateRequest = dateRequest
		self._dateIni = dateIni
		self._dateEnd = dateEnd
		self._state = state

	def __str__(self):
		return str(self._id) + "|" + self._employee.name + "|" + str(self._type) + "|" + str(self._dateRequest) + "|" + str(self._dateIni) + "|" + str(self._dateEnd) + "|" + str(self._state)

#***********************************************************************
class Employee(object):
	employees = []
	
	def __init__(self, empId, bossId, name, passw, holidayDays, ownDays):
		self.name = name
		self.id = empId
		self.passw = passw
		self.boss = bossId
		self.holidayDays = holidayDays
		self.ownDays = ownDays
		
	def __str__(self):
		return str(self.id) + "|" + str(self.boss) + "|" + self.name + "|" + self.passw + "|" + str(self.holidayDays) + "|" + str(self.ownDays)

	@staticmethod
	def load_employees():
		try:
			filename = 'employees.txt'
			f = open(filename, 'r')	
			for line in f:
				item = line.strip().split("|")
				Employee.add_Employee(Employee(int(item[0]), int(item[1]), item[2], item[3], int(item[4]), int(item[5])))
			f.close()
		except IOError:
			print "Error de lectura: " + filename
	
	@staticmethod
	def add_Employee(employee):
		Employee.employees.append(employee)

	@staticmethod
	def remove_Employee(employee):
		Employee.employees.remove(employee)
	
	@staticmethod
	def get_employee(name, passw):
		for emp in Employee.employees:
			if (emp.name == name) & (emp.passw == passw):
				return emp
			
	def get_project(self):
		for project in Project.projects:
			if (self in project.employees):
				return project

#***********************************************************************
class Project(object):
	count = 0
	projects = []
	
	def __init__(self, name, dateIni, dateEnd, min, employees, boss):
		self.__class__.count += 1
		self._id = Project.count
		self.name = name
		self.dateIni = dateIni
		self.dateEnd = dateEnd
		self.min = min
		self.employees = employees
		self.boss = boss
		
		if (diference(dateIni, dateEnd) < 1):
			raise Date_Violation("Fechas de proyecto incorrectas")

	def add_Employee(self, employee):
		self.employees.append(employee)

	def remove_Employee(self, employee):
		if (len(self.employees)>self.min):
			self.employees.remove(employee)
		else:
			raise Business_Contraint("No es posible, numero minimo de empleados insuficiente")
		
	@staticmethod
	def add_project(project):
		Project.projects.append(project)

	@staticmethod
	def remove_project(project):
		Project.projects.remove(project)
		
	
#***********************************************************************


def print_list(list):
	for item in list:
		print str(item)

#***********************************************************************


def main():
	Employee.load_employees()
	print_list(Employee.employees)
	wmain = WindowLogin()
	gtk.main()


if  __name__ == '__main__':main()
