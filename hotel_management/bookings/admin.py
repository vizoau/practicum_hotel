from django.contrib import admin
from .models import Room, Discount, Booking


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'category', 'has_baby_cot',
                    'weekday_price', 'weekend_price')
    list_filter = ('type', 'category', 'has_baby_cot')
    search_fields = ('id', 'type', 'category')
    ordering = ('id',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'minimum_nights', 'discount_percent')
    list_filter = ('minimum_nights', 'discount_percent')
    search_fields = ('id', 'minimum_nights')
    ordering = ('id',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'room', 'guest_name', 'check_in',
                    'check_out', 'status', 'total_price')
    list_filter = ('room', 'status', 'check_in', 'check_out')
    search_fields = ('guest_name', 'room__id', 'status')
    ordering = ('-check_in',)
