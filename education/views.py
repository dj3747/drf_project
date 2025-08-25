from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson
from .serializer import CourseSerializer, LessonSerializer
from users.permissions import IsOwnerOrModerator, IsNotModerator, IsOwner

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """Определяем права доступа в зависимости от действия"""
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated, IsNotModerator]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwnerOrModerator]
        else:  # list, retrieve
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Устанавливаем владельца при создании курса"""
        serializer.save(owner=self.request.user)


class LessonCreateApiView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsNotModerator]  # Только не-модераторы могут создавать

    def perform_create(self, serializer):
        """Устанавливаем владельца при создании урока"""
        serializer.save(owner=self.request.user)


class LessonListApiView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Фильтруем уроки: модераторы видят все, остальные - только свои"""
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveApiView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]  # Владелец или модератор

    def get_queryset(self):
        """Фильтруем уроки: модераторы видят все, остальные - только свои"""
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonUpdateApiView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]  # Владелец или модератор

    def get_queryset(self):
        """Фильтруем уроки: модераторы видят все, остальные - только свои"""
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonDestroyApiView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsNotModerator, IsOwner]  # Только владелец и не модератор

    def get_queryset(self):
        """Фильтруем уроки: показываем только свои"""
        return Lesson.objects.filter(owner=self.request.user)
