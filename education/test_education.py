from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from rest_framework import status
from education.models import Course, Lesson, Subscription

User = get_user_model()


class LessonAndSubscriptionTests(APITestCase):
    def setUp(self):
        # Создание пользователей
        self.owner = User.objects.create_user(email="owner@example.com", password="pass123")
        self.other_user = User.objects.create_user(email="other@example.com", password="pass123")
        self.moderator = User.objects.create_user(email="moderator@example.com", password="pass123")

        # Создание группы "Модераторы"
        moderators_group = Group.objects.create(name="Модераторы")
        self.moderator.groups.add(moderators_group)

        # Создание курса и урока
        self.course = Course.objects.create(title="Тестовый курс", owner=self.owner)
        self.lesson = Lesson.objects.create(title="Тестовый урок", owner=self.owner, course=self.course)

    def test_create_lesson_owner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            "/education/lesson/create/",
            {
                "title": "Новый урок",
                "course": self.course.id,
                "description": "Описание нового урока",
                "video_url": "https://www.youtube.com/watch?v=example",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_lesson_moderator(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(
            "/education/lesson/create/", {"title": "Урок модератора", "course": self.course.id}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_lesson_owner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(f"/education/lesson/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_lesson_other_user(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(f"/education/lesson/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_lesson_owner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(f"/education/lesson/{self.lesson.id}/update/", {"title": "Обновлено владельцем"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_lesson_moderator(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(f"/education/lesson/{self.lesson.id}/update/", {"title": "Обновлено модератором"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson_owner(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(f"/education/lesson/{self.lesson.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_lesson_moderator(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(f"/education/lesson/{self.lesson.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post("/education/subscription/", {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.other_user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        self.client.force_authenticate(user=self.other_user)
        self.client.post("/education/subscription/", {"course_id": self.course.id})
        response = self.client.post("/education/subscription/", {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.other_user, course=self.course).exists())

    def test_subscribe_without_course_id(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post("/education/subscription/", {})
        print(f"Subscribe without course_id response: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
