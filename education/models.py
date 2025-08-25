from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to="course_previews/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses',
                              verbose_name='Владелец')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=255)
    description = models.TextField()
    preview = models.ImageField(upload_to="lesson_previews/", blank=True, null=True)
    video_url = models.URLField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='lessons',
                              verbose_name='Владелец')

    def __str__(self):
        return f"{self.title} ({self.course.title})"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
