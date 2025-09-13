from rest_framework import generics, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsNotModerator, IsOwner, IsOwnerOrModerator

from .models import Course, Lesson, Payment, Subscription
from .paginators import StandardPagination
from .serializer import CourseSerializer, CourseSubscriptionSerializer, LessonSerializer
from .services.strip_api import create_checkout_session, create_stripe_price, create_stripe_product
from .tasks import send_course_update_email


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
        if user.is_authenticated:
            if user.groups.filter(name="Модераторы").exists():
                return Course.objects.all()
            return Course.objects.filter(owner=user)

    def perform_update(self, serializer):
        course = serializer.save()
        subscriptions = Subscription.objects.filter(course=course)

        for subscription in subscriptions:
            send_course_update_email.delay(subscription.user.email, course.title)


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
        if user.is_authenticated:
            if user.groups.filter(name="Модераторы").exists():
                return Lesson.objects.all()
            return Lesson.objects.filter(owner=user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def get_queryset(self):
        """Фильтруем уроки: модераторы видят все, остальные - только свои"""
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name="Модераторы").exists():
                return Lesson.objects.all()
            return Lesson.objects.filter(owner=user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def get_queryset(self):
        """Фильтруем уроки: модераторы видят все, остальные - только свои"""
        user = self.request.user
        if user.is_authenticated:
            if user.groups.filter(name="Модераторы").exists():
                return Lesson.objects.all()
            return Lesson.objects.filter(owner=user)


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsNotModerator]

    def get_queryset(self):
        """Фильтруем уроки: показываем только свои"""
        user = self.request.user
        if user.is_authenticated:
            return Lesson.objects.filter(owner=user)
        return Lesson.objects.none()


class CourseSubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSubscriptionSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")

        if not course_id:
            return Response({"error": "course_id обязателен"}, status=400)

        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"

        return Response({"message": message})


class BuyCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)

        if not course.stripe_product_id:
            product = create_stripe_product(course.title)
            course.stripe_product_id = product.id

        if not course.stripe_price_id:
            price = create_stripe_price(course.stripe_product_id, int(course.price * 100))  # цену в копейках
            course.stripe_price_id = price.id

        course.save()

        session = create_checkout_session(
            course.stripe_price_id,
            success_url="https://example.com/success/",
            cancel_url="https://example.com/cancel/",
        )

        # Создание объекта Payment
        Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            stripe_session_id=session.id,
            payment_url=session.url,
        )

        return Response({"checkout_url": session.url})
