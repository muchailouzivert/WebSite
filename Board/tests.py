from rest_framework import status
from rest_framework.test import APITestCase
from .models import Vacancy, Application, AppUser


class VacancyAPITestCase(APITestCase):
    def setUp(self):
        # Create a sample AppUser for the employer
        self.employer = AppUser.objects.create(name="Employer", email="employer@example.com", password="password123")

        # Create sample Vacancy objects
        self.full_time_vacancy = Vacancy.objects.create(
            employer=self.employer, job_type="Full-time", salary=50000.00, requirements="Experience in web development",
            status="active"
        )
        self.part_time_vacancy = Vacancy.objects.create(
            employer=self.employer, job_type="Part-time", salary=30000.00, requirements="Experience in data science",
            status="active"
        )

    def test_get_vacancy_list(self):
        url = '/api/vacancies/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_vacancy_detail(self):
        url = f'/api/vacancies/{self.full_time_vacancy.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['job_type'], 'Full-time')
        self.assertEqual(response.data['salary'], '50000.00')
        self.assertEqual(response.data['requirements'], 'Experience in web development')
        self.assertEqual(response.data['status'], 'active')

    def test_create_vacancy(self):
        url = '/api/vacancies/'
        data = {
            "employer": self.employer.id,
            "job_type": "Intern",
            "salary": "20000.00",
            "requirements": "Computer science student",
            "status": "active"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vacancy.objects.count(), 3)

    def test_update_vacancy(self):
        url = f'/api/vacancies/{self.full_time_vacancy.id}/'
        data = {
            "employer": self.employer.id,
            "job_type": "Full-time Remote",
            "salary": "55000.00",
            "requirements": "Experience in web development, remote work",
            "status": "inactive"
        }

        response = self.client.put(url, data, format='json')
        updated_vacancy = Vacancy.objects.get(id=self.full_time_vacancy.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_vacancy.job_type, "Full-time Remote")
        self.assertEqual(updated_vacancy.salary, 55000.00)
        self.assertEqual(updated_vacancy.requirements, "Experience in web development, remote work")
        self.assertEqual(updated_vacancy.status, "inactive")

    def test_delete_vacancy(self):
        url = f'/api/vacancies/{self.full_time_vacancy.id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vacancy.objects.count(), 1)


class AppUserAPITestCase(APITestCase):
    def setUp(self):
        # Create sample AppUser objects
        self.user1 = AppUser.objects.create(name="User1", email="user1@example.com", password="password123")
        self.user2 = AppUser.objects.create(name="User2", email="user2@example.com", password="password456")

    def test_get_app_users_list(self):
        url = '/api/app_user/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_app_users_detail(self):
        url = f'/api/app_user/{self.user1.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'User1')
        self.assertEqual(response.data['email'], 'user1@example.com')

    def test_create_app_users(self):
        url = '/api/app_user/'
        data = {
            "name": "NewUser",
            "email": "newuser@example.com",
            "password": "newpassword123"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AppUser.objects.count(), 3)

    def test_update_app_users(self):
        url = f'/api/app_user/{self.user1.id}/'
        data = {
            "name": "UpdatedUser1",
            "email": "updateduser1@example.com",
            "password": "updatedpassword123"
        }

        response = self.client.put(url, data, format='json')
        updated_user = AppUser.objects.get(id=self.user1.id)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_app_users(self):
        url = f'/api/app_user/{self.user2.id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AppUser.objects.count(), 1)


class ApplicationAPITestCase(APITestCase):
    def setUp(self):
        # Create sample AppUser for the employer
        self.employer = AppUser.objects.create(name="Employer", email="employer@example.com", password="password123")

        # Create sample Vacancy objects
        self.vacancy = Vacancy.objects.create(
            employer=self.employer, job_type="Full-time", salary=50000.00, requirements="Experience in web development", status="active"
        )

        # Create sample AppUser for the applicant
        self.applicant = AppUser.objects.create(name="Applicant", email="applicant@example.com", password="password123")

        # Create sample Application objects
        self.application_1 = Application.objects.create(user=self.applicant, vacancy=self.vacancy, status="pending")
        self.application_2 = Application.objects.create(user=self.applicant, vacancy=self.vacancy, status="accepted")

    def test_get_application_list(self):
        url = '/api/application/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_application_detail(self):
        url = f'/api/application/{self.application_1.id}/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.applicant.id)
        self.assertEqual(response.data['vacancy'], self.vacancy.id)
        self.assertEqual(response.data['status'], 'pending')

    def test_create_application(self):
        url = '/api/application/'
        data = {
            "user": self.applicant.id,
            "vacancy": self.vacancy.id,
            "status": "rejected"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 3)

    def test_update_application(self):
        url = f'/api/application/{self.application_1.id}/'
        data = {
            "user": self.applicant.id,
            "vacancy": self.vacancy.id,
            "status": "accepted"
        }

        response = self.client.put(url, data, format='json')
        updated_application = Application.objects.get(id=self.application_1.id)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_application(self):
        url = f'/api/application/{self.application_1.id}/'
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Application.objects.count(), 1)
