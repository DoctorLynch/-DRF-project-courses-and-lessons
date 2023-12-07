from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from course.models import Course, Subscription, Lesson
from users.models import User


# Перед тестированием лучше закомментировать permission_classes во всех тестируемых контроллерах
class CourseTestCase(APITestCase):
    def setUp(self) -> None:
        pass

    def test_create_course(self):
        """Тестирование создания курса"""
        data = {
            'title': 'Test',
            'description': 'Test'
        }
        response = self.client.post(
            '/course/',
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {'title': 'Test', 'num_of_lesson': 0, 'lesson_this_course': []}
        )
        self.assertTrue(
            Course.objects.all().exists()
        )


class LessonTestCase(APITestCase):
    """Тестирование уроков"""

    def setUp(self):
        """Подготовка данных перед каждым тестом"""

        self.user = User.objects.create(email='test1@test.ru',
                                        first_name='test1',
                                        last_name='test2',
                                        is_staff=True,
                                        is_superuser=True,
                                        is_active=True)

        self.user.set_password('12345')
        self.user.save()

        self.course = Course.objects.create(title='Тестовый курс',
                                            description='Описание тестового курса',
                                            owner=self.user)

        self.lesson = Lesson.objects.create(title='тест 1',
                                            description='описание теста 1',
                                            video='https://www.youtube.com/',
                                            owner=self.user,
                                            course=self.course)

        response = self.client.post('/users/token/', data={'email': self.user.email, 'password': '12345'})

        self.access_token = response.data.get('access')

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

    def test_create_lesson(self):
        """Тестирование создания урока"""

        data = {
            'title': 'тест 1',
            "description": "описание теста 1",
            'course': self.course.pk,
            'video': 'https://www.youtube.com/',
        }

        response = self.client.post(reverse('course:lesson_create'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_list_lessons(self):
        """Тестирование списка уроков"""

        response = self.client.get(reverse('course:lesson_list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(),
                         [{'id': self.lesson.pk,
                           'title': self.lesson.title,
                           'description': self.lesson.description,
                           'preview': None,
                           'video': self.lesson.video,
                           'course': self.course.pk,
                           'owner': self.user.pk}]
                         )

    def test_update_lessons(self):
        """Тестирование обновления урока"""

        data = {
            'title': 'Урок 25.2 измененный',
            "description": "Описание урока 25.2 измененное",
            'preview': '',
            'video': 'https://www.youtube.com/',
            'course': self.course.pk,
            'owner': self.user.pk
        }

        response = self.client.put(reverse('course:lesson_update', args=[self.lesson.pk]), data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(),
                         {'id': self.lesson.pk,
                          'title': "Урок 25.2 измененный",
                          'description': 'Описание урока 25.2 измененное',
                          'preview': None,
                          'video': self.lesson.video,
                          'course': self.course.pk,
                          'owner': self.user.pk}
                         )

    def test_get_lessons_by_id(self):
        """Тестирование получения урока по id"""


        response = self.client.get(reverse('course:lesson_get', args=[self.lesson.pk]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {'id': self.lesson.pk,
                          'title': self.lesson.title,
                          'description': self.lesson.description,
                          'preview': None,
                          'video': self.lesson.video,
                          'course': self.course.pk,
                          'owner': self.user.pk}
                         )

    def test_destroy_lessons(self):
        """Тестирование удаления урока"""

        # Запрос на удаление урока
        response = self.client.delete(reverse('course:lesson_delete', args=[self.lesson.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Lesson.objects.all().count(), 0)


class SubscriptionTestCase(LessonTestCase):

    def test_subscribe_unsubscribe_course(self):
        """Тестирование подписки на урок"""

        data = {
            'user': self.user.pk,
        }

        response = self.client.post(reverse('course:subscribe', args=[self.course.pk]), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Subscription.objects.filter(user=self.user, course=self.course).exists(), True)

        response = self.client.delete(reverse('app_course:unsubscribe', args=[self.course.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Subscription.objects.filter(user=self.user, course=self.course).exists(), False)
