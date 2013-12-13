#!/usr/bin/python
# --*-- coding: utf-8 --*--
import gtk
import sys
import time
import datetime
import pickle

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
		
		"""
		liststore_request_states = gtk.ListStore(str)
		request_states = ["En espera", "En tramitacion", "Aceptada"]
		for item in request_states:
			liststore_request_states.append([item])
            
		column_combo = gtk.TreeViewColumn("Estado de la peticion")
		self.tv.append_column(column_combo)
		cellrenderer_combo = gtk.CellRendererCombo()
		cellrenderer_combo.set_property("editable", True)
		cellrenderer_combo.set_property("model", liststore_request_states)
		cellrenderer_combo.set_property("text-column", 0)
		column_combo.pack_start(cellrenderer_combo, False)
		column_combo.add_attribute(cellrenderer_combo, "text", 1)
		cellrenderer_combo.connect("edited", self.combo_changed, self.store)
		"""
		
		# self.builder.get_object("tv_state").connect("cliked", self.row_cliked)
		
		self.w.show_all()
		self.father = father  # se guarda el objeto padre
		self.employee = emp
		self.inicialize_list()

		addbutton = self.builder.get_object("toolbuttonAdd")
		removebutton = self	
		if (self.employee.is_boss()):
			addbutton.hide()
			
		
		
	def row_cliked(self, _, __=None, ___=None):
		request = self.__get_request_from_glade()
		if request is not None:
			w_details = WindowDetails(self, request)
			
	# ventana para anadir tareas nuevas
	def on_addrequest(self, d):
		w_request = WindowRequest(self)		

	def add_request_glade(self, request):
		self.store.append([request._id, request._employee.name, request._type, request._dateRequest, request._dateIni, request._dateEnd, request._state])
		
	def inicialize_list(self):
		self.store.clear()
		for request in Request.get_visible_requests(self.employee):
			self.add_request_glade(request)

	def __get_request_from_glade(self):
		selec = self.tv.get_selection()
		t = selec.get_selected()
		if t[1] != None:
			for request in Request.requests:  # buscamos la tarea en requests
				reqId = int(t[0].get_value(t[1], 0))
				if (request._id == reqId):
					return request
	
	# metodo para eliminar una tarea seleccionada
	def on_deleterequest(self, tv):		
		selec = self.tv.get_selection()
		t = selec.get_selected()
		if t[1] != None:
			for request in Request.requests:  # buscamos la tarea en requests y la eliminamos
				reqId = int(t[0].get_value(t[1], 0))
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
# Objeto: ventana utilizada para ver los detalles
class WindowDetails:
	def __init__(self, father, request):
		self.father = father  # se guarda el objeto padre
		self.request = request
		self.builder = gtk.Builder()		
		self.builder.add_from_file("windowdetails_gtk2.glade")	
		self.builder.connect_signals(self)
		self.w = self.builder.get_object("window_details")
		self.w.show_all()
		self.request_details = self.builder.get_object("textviewDetails")
		self.request_details.set_text(request._reason)
		self.request_combo = self.builder.get_object("comboboxEstado")
		self.inicializate_combo()
		
		if (father.employee.is_boss()):
			self.request_details.set_editable(True)
			try:
				project = request._employee.get_project()
				if project is None:
					show_err_dialog("Este empleado no esta en ningun proyecto")
				else:
					project.check_employee_request(request)
			except (Business_Contraint) as e:
				show_err_dialog("Si acepta la solicitud: " + e.value)
		else:
			self.request_details.set_editable(False)
			# self.request_combo.set_property("can_focus", False)
		
	
	def inicializate_combo(self):
		listaelementos = gtk.ListStore(str)
		listaelementos.append(["En espera"])
		listaelementos.append(["En tramitacion"])
		listaelementos.append(["Aceptada"])
		listaelementos.append(["Rechazada"])
		self.request_combo.set_model(listaelementos)
		render = gtk.CellRendererText()
		self.request_combo.pack_start(render, True)
		self.request_combo.add_attribute(render, 'text', 0)
		
		if self.request._state == "En espera":
			self.request_combo.set_active(0)
		elif self.request._state == "En tramitacion":
			self.request_combo.set_active(1)
		elif self.request._state == "Aceptada":
			self.request_combo.set_active(2)
		elif self.request._state == "Rechazada":
			self.request_combo.set_active(3)
		else:
			self.request_combo.set_active(0)
		
	# pulsar boton "enviar"
	def on_apply(self, dialog, *data):
		if (self.father.employee.is_boss()):
			typeState = "En tramitacion"
			tree_iter = self.request_combo.get_active_iter()
			if tree_iter != None:
				model = self.request_combo.get_model()
				typeState = model[tree_iter][0]
			
			self.request._state = typeState
			self.request._reason = self.request_details.get_text()
			
		self.on_cancel(None)
		# print self.request_details.get_text()
		
	# Cerrar
	def on_cancel(self, w):
		self.father.inicialize_list()
		self.w.hide()

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
	def on_exit(self, w, e):
		save_all()
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
		self.avaliableDays = self.builder.get_object("avaliableDays")
		self.avaliableDays.set_text(str(self.father.employee.holidayDays))
		# set Vacaciones
		self.typeOb.set_active(0)
		
		projectDays = self.builder.get_object("projectDays")
		projectDays.set_text(str(self.father.employee.get_project().dateIni) + " - " + str(self.father.employee.get_project().dateEnd))

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
			request = Request(self.father.employee, typeReq, dateReq, dateIni, dateEnd)  # procesar datos
			Request.add_request(request)
			self.father.add_request_glade(request)
			self.w.destroy()
		except (Business_Contraint, Date_Violation) as e:
			show_err_dialog(e.value)

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

	# mostrar el número de días que se pueden pedir
	def on_changeComboBox(self, w):
		tree_iter = self.typeOb.get_active_iter()
		if tree_iter != None:
			model = self.typeOb.get_model()
			typeReq = model[tree_iter][1]

		if (typeReq == "Vacaciones"):
			self.avaliableDays.set_text(str(self.father.employee.holidayDays))
		elif typeReq == "Baja":
			self.avaliableDays.set_text("-")
		elif typeReq == "Asuntos personales":
			self.avaliableDays.set_text(str(self.father.employee.ownDays))	

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

def dates_in(date1, date2, date_start, date_end):
	return (str_to_datetime(date1) >= str_to_datetime(date_start) and str_to_datetime(date2) <= str_to_datetime(date_end))
			
#***********************************************************************

class Request(object):
	count = 0
	requests = []
	
	def __init__(self, employee, typeRequest, dateRequest, dateIni, dateEnd, state="En espera", reason=""):
		if employee.get_project() is not None:
			if not dates_in(dateIni, dateEnd, employee.get_project().dateIni, employee.get_project().dateEnd):
				raise Business_Contraint("Las fechas no estan dentro del proyecto")
		
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
		self.__state = state
		self._reason = reason
	
	def accept(self):
		self._state = "Aceptada"
		
	def denny(self, reason):
		self._state = "Rechazada"
		self._reason = reason

	@property
	def _state(self):
		return self.__state
	
	@_state.setter
	def _state(self, value):
		days = diference(self._dateIni, self._dateEnd)
		days += 1
		if self.__state != "Rechazada":
			if value == "Rechazada":
				if self._type == "Asuntos personales":
					self._employee.ownDays += days
				elif self._type == "Vacaciones":
					self._employee.holidayDays += days
		elif value != "Rechazada":
			if self._type == "Asuntos personales":
				self._employee.ownDays -= days
			elif self._type == "Vacaciones":
				self._employee.holidayDays -= days
		self.__state = value
		print str(self._employee)
	
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
	
	@staticmethod
	def get_approved_requests(emp):
		list = []
		for request in Request.requests:
			if request._state == "Aceptada" and (emp.id == request._employee.id or request._employee.boss == emp.id):  # or es jefe de proyecto
				list.append(request)
		return list
	
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
	
	@staticmethod
	def get_employee_by_id(id):
		for emp in Employee.employees:
			if emp.id == id:
				return emp
	
	def get_employees(self):
		employees = []
		for emp in Employee.employees:
			if (emp.boss == self.id):
				employees.append(emp)
		return employees
			
	def get_project(self):
		for project in Project.projects:
			if (self in project.employees):
				return project
	
	def is_boss(self):
		return self.boss == 0

#***********************************************************************
class Project(object):
	count = 0
	projects = []
	
	def __init__(self, name, dateIni, dateEnd, min, employees, boss):
		if (diference(dateIni, dateEnd) < 1):
			raise Date_Violation("Fechas de proyecto incorrectas")
		self.__class__.count += 1
		self._id = Project.count
		self.name = name
		self.dateIni = dateIni
		self.dateEnd = dateEnd
		self.min = min
		self.employees = employees
		self.boss = boss
		
	def add_Employee(self, employee):
		self.employees.append(employee)

	def check_employee_request(self, request):
		requests = []
		for emp in self.employees:
			requests += Request.get_approved_requests(emp)
		try:
			requests.remove(request)  # en caso de que mires la misma solicitud
		except ValueError:
			pass
		
		date = str_to_datetime(request._dateIni)
		for _ in range(diference(request._dateIni, request._dateEnd) + 1):
			active_people = len(self.employees)
			for req in requests:
				if str_to_datetime(req._dateIni) <= date <= str_to_datetime(req._dateEnd):  # Si el dia esta en una solictud aceptada anteriormente
					active_people -= 1
			if active_people <= self.min:
				raise Business_Contraint("Número mínimo de empleados el día " + date.strftime("%d/%m/%Y"))
			date += datetime.timedelta(days=1)
		return True
		
	@staticmethod
	def add_project(project):
		Project.projects.append(project)

	@staticmethod
	def remove_project(project):
		Project.projects.remove(project)
		
	def __str__(self):
		string = str(self._id) + "|" + self.name + " |" + str(self.min)
		for emp in self.employees:
			string += " | " + str(emp)
		string += " |" + str(self.boss)
		return string

#***********************************************************************


def print_list(list):
	for item in list:
		print str(item)

def save_objects(objs, filename):
	with open(filename, 'wb') as output:
		for obj in objs:
			pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def load_objects(filename):
	list = []
	try:
		with open(filename, 'rb') as input:
			try:
				while True:
					list.append(pickle.load(input))
			except EOFError:
				pass
	except IOError:
		print "Not found " + filename
	return list

def save_all():
	save_objects(Request.requests, "requests")
	save_objects(Employee.employees, "employees")
	# save_objects(Project.projects, "projects")
		
def load_all():
	Employee.employees = load_objects("employees")
	Request.requests = load_objects("requests")
	# Project.projects = load_objects("projects")
	
	length = len(Employee.employees)
	if length == 0:
		Employee.load_employees()  # first start
	
	length = len(Request.requests)
	if length > 0:
		Request.count = Request.requests[length - 1]._id
		
	length = len(Project.projects)
	if length > 0:
		Project.count = Project.projects[length - 1]._id
	
	# update references
	for ref in Request.requests:
		ref._employee = Employee.get_employee(ref._employee.name, ref._employee.passw)
	"""	
	for pro in Project.projects:
		pro_employees = []
		for emp in pro.employees:
			pro_employees.append(Employee.get_employee(emp.name, emp.passw))
		pro.employees = pro_employees
		pro.boss = Employee.get_employee(pro.boss.name, pro.boss.passw)
	"""
#***********************************************************************


def main():
	load_all()
	print_list(Employee.employees)
	print_list(Request.requests)
	print_list(Project.projects)
	
	# crear proyecto
	boss = Employee.employees[0]
	employees = boss.get_employees()
	project1 = Project("Proyecto 1", "1/1/2013", "1/1/2015", 3, employees, boss)
	Project.add_project(project1)
	
	wmain = WindowLogin()
	gtk.main()

if  __name__ == '__main__':main()
