import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from education.models import Course
from users.models import Payment, User


class Command(BaseCommand):
    help = "Заполняет модель оплаты случайными данными"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Начинаем заполнять платёжные данные"))

        users = User.objects.all()
        courses = Course.objects.all()  # Получаем курсы

        if not users:
            self.stdout.write(self.style.WARNING("Пользователи не найдены. Сначала создайте несколько пользователей."))
            return

        if not courses:
            self.stdout.write(self.style.WARNING("Курсы не найдены. Создайте сначала несколько курсов"))
            return

        num_payments = 10

        for i in range(num_payments):
            user = random.choice(users)
            course = courses.first()  # Берем первый курс из списка
            amount = Decimal(random.randrange(100, 10000)) / 100
            payment_method = random.choice([Payment.PAYMENT_METHOD_CASH, Payment.PAYMENT_METHOD_TRANSFER])

            payment = Payment(
                user=user,
                date=timezone.now().date(),
                course=course,  # Связываем с курсом
                amount=amount,
                payment_method=payment_method,
            )
            payment.save()
            self.stdout.write(self.style.SUCCESS(f"Созданный платёж {i+1}: {payment}"))

        self.stdout.write(self.style.SUCCESS("Успешно заполненные платёжные данные."))
