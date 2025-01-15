from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # URL для номеров
    path('rooms/', views.RoomListView.as_view(), name='room_list'),
    path('rooms/<int:room_id>/', views.RoomDetailView.as_view(), name='room_detail'),
    path('rooms/create/', views.RoomCreateView.as_view(), name='room_create'),
    path('rooms/<int:room_id>/update/', views.RoomUpdateView.as_view(),
         name='room_update'),
    path('rooms/<int:room_id>/delete/', views.RoomDeleteView.as_view(),
         name='room_delete'),


    # URL для бронирований
    path('bookings/', views.BookingListView.as_view(), name='booking_list'),
    path('bookings/<int:booking_id>/', views.BookingDetailView.as_view(),
         name='booking_detail'),
    path('bookings/create/', views.BookingCreateView.as_view(),
         name='booking_create'),
    path('bookings/<int:booking_id>/update/',
         views.BookingUpdateView.as_view(), name='booking_update'),
    path('bookings/<int:booking_id>/delete/',
         views.BookingDeleteView.as_view(), name='booking_delete'),

]
