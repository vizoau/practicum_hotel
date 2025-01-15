# Generated by Django 3.2.16 on 2025-01-14 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minimum_nights', models.IntegerField(verbose_name='Минимальное количество ночей')),
                ('discount_percent', models.IntegerField(verbose_name='Процент скидки')),
            ],
            options={
                'verbose_name': 'Скидка',
                'verbose_name_plural': 'Скидки',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, '1-местный'), (2, '2-местный'), (3, '3-местный')], verbose_name='Тип номера')),
                ('category', models.CharField(choices=[('standard', 'Стандарт'), ('comfort', 'Комфорт'), ('lux', 'Люкс')], max_length=10, verbose_name='Категория номера')),
                ('has_baby_cot', models.BooleanField(default=False, verbose_name='Детская кровать')),
                ('weekday_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена в будни')),
                ('weekend_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена в выходные')),
            ],
            options={
                'verbose_name': 'Номер',
                'verbose_name_plural': 'Номера',
            },
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateField(verbose_name='Дата заезда')),
                ('check_out', models.DateField(verbose_name='Дата выезда')),
                ('guest_name', models.CharField(max_length=100, verbose_name='Имя гостя')),
                ('guest_phone', models.CharField(max_length=20, verbose_name='Телефон гостя')),
                ('has_baby_cot', models.BooleanField(default=False, verbose_name='Детская кровать')),
                ('status', models.CharField(choices=[('active', 'Активен'), ('cancelled', 'Отменён'), ('checked_in', 'Заселен'), ('checked_out', 'Выселен')], default='active', max_length=20, verbose_name='Статус')),
                ('actual_check_in', models.DateField(blank=True, null=True, verbose_name='Фактическая дата заезда')),
                ('actual_check_out', models.DateField(blank=True, null=True, verbose_name='Фактическая дата выезда')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookings.room', verbose_name='Номер')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирования',
            },
        ),
    ]
