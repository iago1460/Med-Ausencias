import pMeD
import unittest
from test import test_support


class TestLoadFileFunctions(unittest.TestCase):

    def setUp(self):
        pMeD.Employee.employees = []
        pMeD.Request.count = 0
        pMeD.Request.requests = []
        pMeD.Project.count = 0
        pMeD.Project.projects = []
        
        
        
    def test_loadFile(self):
        pMeD.Employee.load_employees()
        self.assertEqual(len(pMeD.Employee.employees), 5)


    def test_visible_request(self):
        director = pMeD.Employee(1, 0, "Director", "1234", 0, 0)
        pMeD.Employee.add_Employee(director)
        
        emp1 = pMeD.Employee(2, 1, "Emp 1", "1234", 10, 0)
        pMeD.Employee.add_Employee(emp1)
        solicitud_emp1 = pMeD.Request(emp1, "Vacaciones", "25/11/2013", "2/12/2013", "5/12/2013")
        pMeD.Request.add_request(solicitud_emp1)
        
        emp2 = pMeD.Employee(3, 1, "Emp 2", "1234", 10, 0)
        pMeD.Employee.add_Employee(emp2)
        solicitud_emp2 = pMeD.Request(emp2, "Vacaciones", "25/11/2013", "2/12/2013", "5/12/2013")
        pMeD.Request.add_request(solicitud_emp2)
        
        self.assertEqual(len(pMeD.Request.get_visible_requests(emp1)), 1)
        self.assertEqual(len(pMeD.Request.get_visible_requests(emp2)), 1)
        self.assertEqual(len(pMeD.Request.get_visible_requests(director)), 2)
        

    def test_request_exception(self):
        emp1 = pMeD.Employee(1, 1, "Emp", "1234", 0, 0)
        self.assertRaises(pMeD.Date_Violation, pMeD.Request, emp1, "Baja", "26/11/2013", "2/12/2013", "1/12/2013")
        self.assertRaises(pMeD.Business_Contraint, pMeD.Request, emp1, "Asuntos personales", "26/11/2013", "2/12/2013", "3/12/2013")
        self.assertRaises(pMeD.Business_Contraint, pMeD.Request, emp1, "Vacaciones", "26/11/2013", "2/12/2013", "3/12/2013")
        
        
    def test_projects_exception(self):
        self.assertRaises(pMeD.Date_Violation, pMeD.Project, "Proyecto", "2/9/2013", "1/9/2013", 0, [], None)
    
    
    def test_checking_request_fail_1(self):
        emp1 = pMeD.Employee(1, 1, "Emp", "1234", 0, 1)
        pMeD.Employee.add_Employee(emp1)
        solicitud_emp1 = pMeD.Request(emp1, "Asuntos personales", "27/11/2013", "3/12/2013", "3/12/2013")
        project1 = pMeD.Project("Proyecto 1", "1/9/2013", "22/12/2013", 1, [emp1], None)
        self.assertRaises(pMeD.Business_Contraint, project1.check_employee_request, solicitud_emp1)
    
    
    def test_checking_request_pass(self):
        emp1 = pMeD.Employee(1, 1, "Emp 1", "1234", 0, 1)
        pMeD.Employee.add_Employee(emp1)
        emp2 = pMeD.Employee(2, 1, "Emp 2", "1234", 0, 1)
        pMeD.Employee.add_Employee(emp2)
        
        solicitud_emp1 = pMeD.Request(emp1, "Asuntos personales", "27/11/2013", "3/12/2013", "3/12/2013")
        project1 = pMeD.Project("Proyecto 1", "1/9/2013", "22/12/2013", 1, [emp1, emp2], None)
        self.assertTrue(project1.check_employee_request(solicitud_emp1))
        
        
    def test_checking_request_fail_2(self):
        emp1 = pMeD.Employee(1, 1, "Emp 1", "1234", 0, 3)
        pMeD.Employee.add_Employee(emp1)
        emp2 = pMeD.Employee(2, 1, "Emp 2", "1234", 0, 1)
        pMeD.Employee.add_Employee(emp2)
        
        solicitud_emp1 = pMeD.Request(emp1, "Asuntos personales", "27/11/2013", "3/12/2013", "5/12/2013")
        pMeD.Request.add_request(solicitud_emp1)
        project1 = pMeD.Project("Proyecto 1", "1/9/2013", "22/12/2013", 1, [emp1, emp2], None)
        self.assertTrue(project1.check_employee_request(solicitud_emp1))
        solicitud_emp1.accept()
        
        
        solicitud_emp2 = pMeD.Request(emp2, "Asuntos personales", "27/11/2013", "5/12/2013", "5/12/2013")
        self.assertRaises(pMeD.Business_Contraint, project1.check_employee_request, solicitud_emp2)
        
        
    def test_caso_1(self):
        # 25/11
        jose_garcia = pMeD.Employee(2, 1, "Jose Garcia", "1234", 10, 0)
        pMeD.Employee.add_Employee(jose_garcia)
        
        self.assertTrue(jose_garcia.holidayDays, 10)
        solicitud_jose_garcia = pMeD.Request(jose_garcia, "Vacaciones", "25/11/2013", "2/12/2013", "5/12/2013")
        pMeD.Request.add_request(solicitud_jose_garcia)
        self.assertTrue(jose_garcia.holidayDays, 6)
        
        # 26/11
        ana_gomez = pMeD.Employee(3, 1, "Ana Gomez", "1234", 0, 0)
        pMeD.Employee.add_Employee(ana_gomez)
        solicitud_ana_gomez = pMeD.Request(ana_gomez, "Baja", "26/11/2013", "2/12/2013", "3/12/2013")
        pMeD.Request.add_request(solicitud_ana_gomez)
        
        # 27/11
        luis_fernandez = pMeD.Employee(4, 1, "Luis Fernandez", "1234", 0, 3)
        pMeD.Employee.add_Employee(luis_fernandez)
        solicitud_luis_fernandez = pMeD.Request(luis_fernandez, "Asuntos personales", "27/11/2013", "3/12/2013", "3/12/2013")
        pMeD.Request.add_request(solicitud_luis_fernandez)
        
        # personas adicionales
        director = pMeD.Employee(1, 0, "Director", "1234", 0, 0)
        pMeD.Employee.add_Employee(director)
        emp1 = pMeD.Employee(5, 1, "Emp 1", "1234", 0, 0)
        pMeD.Employee.add_Employee(emp1)
        emp2 = pMeD.Employee(6, 1, "Emp 2", "1234", 0, 0)
        pMeD.Employee.add_Employee(emp2)
        # proyecto
        project1 = pMeD.Project("Proyecto 1", "1/9/2013", "22/12/2013", 3, [jose_garcia, ana_gomez, luis_fernandez, emp1, emp2], director)
        pMeD.Project.add_project(project1)
        
        # 28/11
        solicitudes_a_revisar = pMeD.Request.get_visible_requests(director)
        self.assertEqual(len(solicitudes_a_revisar), 3)
        # Ana Gomez
        self.assertTrue(project1.check_employee_request(solicitud_ana_gomez))
        solicitud_ana_gomez.accept()
        # Luis Fernandez
        self.assertTrue(project1.check_employee_request(solicitud_luis_fernandez))
        solicitud_luis_fernandez.accept()
        # Jose Garcia
        self.assertRaises(pMeD.Business_Contraint, project1.check_employee_request, solicitud_jose_garcia)
        solicitud_jose_garcia.denny("Lo siento no puedo concederle ese dia")
        
"""
class TestEmployeeObject(unittest.TestCase):

    def test_loadFile(self):
        self.assertTrue(pMeD.employees.__len__() == 0)
"""


def test_main():
    test_support.run_unittest(TestLoadFileFunctions)

if __name__ == '__main__':
    test_main()
