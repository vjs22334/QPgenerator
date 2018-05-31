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

class School_test(TestCase):

    def create_school(self,name="test_school",addr="test_addr",max_grade="10"):
        return School.objects.create(school_name=name,address=addr,max_grade=max_grade)
    
    def test_school_creation(self):
        s = self.create_school()
        self.assertTrue(isinstance(s,School))
        self.assertEqual(s.__str__(),s.school_name)

class chapter_test(TestCase):

    def create_chapter(self,name="test_chapter"):
        grade = Grade.objects.create(grade_name=1)
        subject = Subject.objects.create(subject_name="test",grade=grade)
        school = School.objects.create(school_name="abc",address="def",max_grade=10)
        return Chapter.objects.create(ch_name=name,school=school,grade=grade,subject=subject)
    
    def test_chapter_creation(self):
        c = self.create_chapter()
        self.assertTrue(isinstance(c,Chapter))
        self.assertEqual(c.__str__(),c.ch_name)
