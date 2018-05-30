from django.test import TestCase
from qp_generator.models import *

class Subject_test(TestCase):

    def create_subject(self,name="test_sub"):
        grade=Grade.objects.create(grade_name="1")
        return Subject.objects.create(grade=grade,subject_name=name)
    
    def test_subject_creation(self):
        s = self.create_subject()
        self.assertTrue(isinstance(s,Subject))
        self.assertEqual(s.__str__(),s.subject_name)

class grade_test(TestCase):

    def create_grade(self,name="1"):
        grade=Grade.objects.create(grade_name=name)
        return grade
    
    def test_grade_creation(self):
        g = self.create_grade()
        self.assertTrue(isinstance(g,Grade))
        self.assertEqual(g.__str__(),g.grade_name)
    