from django.test import TestCase
from qp_generator.models import *
from django.urls import reverse
from qp_generator.forms import *

class home_view_tests(TestCase):

    
    def setUp(self):
        pass

    def test_response_code_200(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code,200) 
    
    def test_response_template(self):
        resp = self.client.get(reverse('home'))
        self.assertTemplateUsed(resp,"home.html")    

class sign_up_view_tests(TestCase):
    
    def setUp(self):
        pass

    def test_response_code_200_a(self):
        resp = self.client.get(reverse('signup'))
        self.assertEqual(resp.status_code,200)
    
    def test_response_template(self):
        resp=self.client.get(reverse('signup'))
        self.assertTemplateUsed(resp,'signup.html')

    def test_response_empty_form(self):
        empty_user_form = SignupForm()
        empty_profile_form = ProfileForm()
        resp=self.client.get(reverse('signup'))
        self.assertContains(resp,empty_user_form)
        self.assertContains(resp,empty_profile_form)
    def test_valid_input(self):
        pass