import pMeD
import unittest
from test import test_support


class TestLoadFileFunctions(unittest.TestCase):

    def setUp(self):
        pMeD.Employee.employees = []
        pMeD.Request.count = 0
        pMeD.Request.requests = []
        
    def test_loadFile(self):
        pMeD.Employee.load_employees()
        self.assertTrue(pMeD.Employee.employees.__len__() == 5)

    def test_incorrect_dates(self):
        emp1 = pMeD.Employee(1, 1, "Emp", "1234", 0, 0)
        self.assertRaises(pMeD.Business_Contraint, pMeD.Request.add_Request, emp1, "Baja", "26/11/2013", "2/12/2013", "1/12/2013", False)
        self.assertRaises(pMeD.Business_Contraint, pMeD.Request.add_Request, emp1, "Asuntos personales", "26/11/2013", "2/12/2013", "3/12/2013", False)
        self.assertRaises(pMeD.Business_Contraint, pMeD.Request.add_Request, emp1, "Vacaciones", "26/11/2013", "2/12/2013", "3/12/2013", False)
        

    def test_caso_1(self):
        # 25/11
        jose_garcia = pMeD.Employee(2, 1, "Jose Garcia", "1234", 10, 0)
        pMeD.Employee.add_Employee(jose_garcia)
        
        self.assertTrue(jose_garcia.holidayDays, 10)
        solicitud_jose_garcia = pMeD.Request.add_Request(jose_garcia, "Vacaciones", "25/11/2013", "2/12/2013", "5/12/2013", False)
        self.assertTrue(jose_garcia.holidayDays, 6)
        
        # 26/11
        ana_gomez = pMeD.Employee(3, 1, "Ana Gomez", "1234", 0, 0)
        pMeD.Employee.add_Employee(ana_gomez)
        solicitud_ana_gomez = pMeD.Request.add_Request(ana_gomez, "Baja", "26/11/2013", "2/12/2013", "3/12/2013", False)
        
        # 27/11
        luis_fernandez = jose_garcia = pMeD.Employee(4, 1, "Luis Fernandez", "1234", 0, 3)
        pMeD.Employee.add_Employee(luis_fernandez)
        solicitud_ana_gomez = pMeD.Request.add_Request(jose_garcia, "Asuntos personales", "27/11/2013", "3/12/2013", "3/12/2013", False)
        

"""
class TestEmployeeObject(unittest.TestCase):

    def test_loadFile(self):
        self.assertTrue(pMeD.employees.__len__() == 0)
"""


def test_main():
    test_support.run_unittest(TestLoadFileFunctions,
                              """TestEmployeeObject""")

if __name__ == '__main__':
    test_main()
