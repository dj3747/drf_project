from rest_framework import generics, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsNotModerator, IsOwner, IsOwnerOrModerator

from .models import Course, Lesson, Subscription
from .paginators import StandardPagination
from .serializer import CourseSerializer, LessonSerializer, CourseSubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        """Определяем права доступа в зависимости от действия"""
        if self.action in ["create", "destroy"]:
            permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        else:  # list, retrieve
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Устанавливаем владельца при создании курса"""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Фильтруем курсы: модераторы видят все, остальные - только свои"""
        user = self.request.user
        if user.groups.filter(name="Модераторы").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        """Устанавливаем владельца при создании урока"""
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardPagination

    def get_queryset(self):
        """Фильтруем уроки: модераторы видят все, остальные - только свои"""
        user = self.request.user
        if user.groups.filter(name="Модераторы").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def get_queryset(self):
        """Фильтруем уроки: модераторы видят все, остальные - только свои"""
        user = self.request.user
        if user.groups.filter(name="Модераторы").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def get_queryset(self):
        """Фильтруем уроки: модераторы видят все, остальные - только свои"""
        user = self.request.user
        if user.groups.filter(name="Модераторы").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsNotModerator]

    def get_queryset(self):
        """Фильтруем уроки: показываем только свои"""
        return Lesson.objects.filter(owner=self.request.user)


class CourseSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSubscriptionSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        if not course_id:
            return Response({"error": "course_id обязателен"}, status=400)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})
