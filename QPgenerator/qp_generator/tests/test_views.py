from django.test import TestCase
from qp_generator.models import *
from django.urls import reverse
from qp_generator.forms import *
from django.contrib.auth.models import User

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
        School.objects.create(id=1,school_name="abc",address="def",max_grade=1)

    def test_response_code_200_a(self):
        resp = self.client.get(reverse('signup'))
        self.assertEqual(resp.status_code,200)
    
    def test_response_template(self):
        resp=self.client.get(reverse('signup'))
        self.assertTemplateUsed(resp,'signup.html')

    def test_valid_input(self):
        user_count=User.objects.count()
        response = self.client.post(reverse('signup'),{
            "email"	: "abc@def.com",
            "first_name" :"",
            "last_name":"def",
            "password1":"wildmutt123",
            "password2":"wildmutt123",
            "role":	"admin",
            "school":1,
            "username":"vjs223345",
            })
        self.assertEqual(response.status_code,302)    
        self.assertEqual(User.objects.count(),user_count+1)

    def test_invalid_input(self):
        user_count=User.objects.count()
        response = self.client.post(reverse('signup'),{
            "email"	: "abc@def.com",
            "first_name" :"abc",
            "last_name":"def",
            "password1":"",
            "password2":"wildmutt123",
            "role":	"admin",
            "school":1,
            })
        self.assertContains(response,'"errorlist')

class test_manage_questions_view(TestCase):
    @classmethod
    def setUpTestData(cls):
        School.objects.create(id=1,school_name="abc",address="def",max_grade=1)
        user = User.objects.create_user(username='testuser1', password='12345')
        user.profile.role="admin"
        user.save()
        user = User.objects.create_user(username='testuser2', password='12345')
        user.profile.role="teacher"
        user.save()

    def test_redirect_to_login_if_loggedout(self):
        resp = self.client.get(reverse('manage_questions'),follow=True)
        self.assertRedirects(resp, expected_url=reverse('login')+"?next=%2Fapp%2Fmanage_questions%2F", status_code=302, target_status_code=200)
    
    def test_accessible_by_admin(self):    
        login = self.client.login(username='testuser1', password='12345')
        print(login)
        resp = self.client.get(reverse('manage_questions'),follow=True)
        self.client.logout()
        self.assertEqual(resp.status_code,200)
    
    def test_redirect_to_login_for_non_admin(self):
        login = self.client.login(username='testuser2', password="12345")
        print(login)
        resp = self.client.get(reverse('manage_questions'),follow=True)
        self.client.logout()
        self.assertRedirects(resp, expected_url=reverse('login')+"?next=%2Fapp%2Fmanage_questions%2F", status_code=302, target_status_code=200)

    def test_valid_data(self):
        login = self.client.login(username='testuser1', password='12345')
        print(login)
        resp = self.client.post(reverse('manage_questions'),{
            "question_text" : "abcd testing",
            "question_type" : "short",
            "difficulty" : "easy",
            "answer" : "abcdef",
            "grade" : 1,
            "subject" : 1,
            "chapter" : 2
        },follow=True)
        print(resp.content)
        self.assertRedirects(resp,expected_url=reverse('menu'),status_code=302,target_status_code=200)