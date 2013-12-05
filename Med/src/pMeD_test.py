import pMeD
import unittest
from test import test_support


class TestLoadFileFunctions(unittest.TestCase):

    # def setUp(self):
    #    requests = []
        
    def test_loadFile(self):
        pMeD.Employee.load_employees()
        
        print pMeD.Employee.employees.__len__()
        self.assertTrue(pMeD.Employee.employees.__len__() == 5)

    def caso_1(self):
        #25/11
        jose_garcia = pMeD.Employee(2, 1, "Jose Garcia", "1234", 10, 0)
        pMeD.Employee.add_Employee(jose_garcia)
        
        self.assertTrue(jose_garcia.holidayDays, 10)
        solicitud_jose_garcia = pMeD.Request.add_Request(jose_garcia, "Vacaciones", "25/11/2013", "2/12/2013", "5/12/2013", False)
        self.assertTrue(jose_garcia.holidayDays, 6)
        
        #26/11
        ana_gomez = pMeD.Employee(3, 1, "Ana Gomez", "1234", 0, 0)
        pMeD.Employee.add_Employee(ana_gomez)
        solicitud_ana_gomez = pMeD.Request.add_Request(jose_garcia, "Baja", "26/11/2013", "2/12/2013", "3/12/2013", False)
        
        #27/11
        luis_fernandez = jose_garcia = pMeD.Employee(4, 1, "Luis Fernandez", "1234", 0, 3)
        pMeD.Employee.add_Employee(luis_fernandez)
        solicitud_ana_gomez = pMeD.Request.add_Request(jose_garcia, "Asuntos Personales", "27/11/2013", "3/12/2013", "3/12/2013", False)
        

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