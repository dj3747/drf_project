from django.urls import path
from rest_framework.routers import DefaultRouter

from education.views import (BuyCourseView,
                             CourseSubscriptionAPIView,
                             CourseViewSet,
                             LessonCreateAPIView,
                             LessonDestroyAPIView,
                             LessonListAPIView,
                             LessonRetrieveAPIView,
                             LessonUpdateAPIView)

router = DefaultRouter()
router.register(r"courses", CourseViewSet)

urlpatterns = [
    path("lesson/", LessonListAPIView.as_view(), name="lesson-list"),
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson-create"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson-detail"),
    path("lesson/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson-update"),
    path("lesson/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson-delete"),
    path("subscription/", CourseSubscriptionAPIView.as_view(), name="course-subscription"),
    path("courses/<int:pk>/buy/", BuyCourseView.as_view(), name="course-buy"),
] + router.urls
