from django.core.exceptions import ValidationError
from django.db import models
from datetime import timedelta
from decimal import Decimal


class Room(models.Model):
    # Тип номера
    TYPE_CHOICES = [
        (1, '1-местный'),
        (2, '2-местный'),
        (3, '3-местный'),
    ]

    # Категория номера
    CATEGORY_CHOICES = [
        ('стандарт', 'Стандарт'),
        ('комфорт', 'Комфорт'),
        ('люкс', 'Люкс'),
    ]

    type = models.IntegerField(choices=TYPE_CHOICES, verbose_name='Тип номера')
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        verbose_name='Категория номера'
    )
    has_baby_cot = models.BooleanField(
        default=False,
        verbose_name='Детская кровать'
    )
    weekday_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена в будни'
    )
    weekend_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена в выходные'
    )

    def __str__(self):
        return (
            f"Номер {self.id} "
            f"({self.get_type_display()}, "
            f"{self.get_category_display()})"
        )

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'


class Discount(models.Model):
    minimum_nights = models.IntegerField(
        verbose_name='Минимальное количество ночей')
    discount_percent = models.IntegerField(verbose_name='Процент скидки')

    def __str__(self):
        return f"Скидка {self.discount_percent}% за {self.minimum_nights}+ ночей"

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Booking(models.Model):
    # Статусы бронирования
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('checked_in', 'Заселен'),
        ('checked_out', 'Выселен'),
    ]

    def calculate_total_price(self):
        """
        Рассчитывает итоговую стоимость бронирования.
        """
        # Определяем цену за ночь (будни/выходные)
        total_price = Decimal('0')
        current_date = self.check_in
        while current_date < self.check_out:
            if current_date.weekday() < 5:  # Будни
                total_price += Decimal(str(self.room.weekday_price))
            else:  # Выходные (5-6 - суббота, воскресенье)
                total_price += Decimal(str(self.room.weekend_price))
            current_date += timedelta(days=1)

        # Применяем скидку за длительное пребывание
        nights = (self.check_out - self.check_in).days
        discount = Discount.objects.filter(
            minimum_nights__lte=nights).order_by('-minimum_nights').first()
        if discount:
            # Вычисляем скидку
            discount_percent = Decimal(str(discount.discount_percent))
            total_price *= (Decimal('1') - discount_percent / Decimal('100'))

        return total_price

    def save(self, *args, **kwargs):
        # Рассчитываем стоимость перед сохранением
        self.total_price = self.calculate_total_price()

        # Автоматическое обновление статуса
        if self.actual_check_in and not self.actual_check_out:
            self.status = 'checked_in'  # Гость заселился
        elif self.actual_check_in and self.actual_check_out:
            self.status = 'checked_out'  # Гость выселился
        elif not self.actual_check_in and not self.actual_check_out:
            self.status = 'active'  # Бронирование активно

        super().save(*args, **kwargs)

    def clean(self):
        # Проверяем, что дата выезда позже даты заезда
        if self.check_in and self.check_out and self.check_out <= self.check_in:
            raise ValidationError(
                {'check_out': 'Дата выезда должна быть позже даты заезда.'}
            )

        # Проверяем, можно ли добавить детскую кровать
        if self.has_baby_cot and not self.room.has_baby_cot:
            raise ValidationError(
                {'has_baby_cot': 'В этом номере нет возможности добавить детскую кровать.'}
            )

        # Проверяем, что в номере нет других бронирований на заданный период
        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            check_in__lt=self.check_out,  # Начало нового бронирования раньше конца существующего
            check_out__gt=self.check_in,  # Конец нового бронирования позже начала существующего
            # Исключаем текущее бронирование (при редактировании)
        ).exclude(id=self.id)

        if overlapping_bookings.exists():
            raise ValidationError(
                {'check_in': 'Номер уже забронирован на выбранные даты.'}
            )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name='Номер',
        related_name='bookings'
    )
    check_in = models.DateField(verbose_name='Дата заезда')
    check_out = models.DateField(verbose_name='Дата выезда')
    guest_name = models.CharField(max_length=100, verbose_name='Имя гостя')
    guest_phone = models.CharField(max_length=20, verbose_name='Телефон гостя')
    has_baby_cot = models.BooleanField(
        default=False,
        verbose_name='Детская кровать'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='Статус'
    )
    actual_check_in = models.DateField(
        null=True, blank=True,
        verbose_name='Фактическая дата заезда'
    )
    actual_check_out = models.DateField(
        null=True,
        blank=True,
        verbose_name='Фактическая дата выезда'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Итоговая стоимость',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Бронирование {self.id} ({self.guest_name}, {self.room})"

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
