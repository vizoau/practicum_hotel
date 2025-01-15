from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Room, Booking
from .forms import BookingForm, RoomForm


class RoomListView(ListView):
    model = Room
    template_name = 'bookings/room_list.html'
    context_object_name = 'rooms'
    paginate_by = 9


class RoomCreateView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = 'bookings/room_form.html'
    success_url = reverse_lazy('bookings:room_list')

    def form_valid(self, form):
        messages.success(self.request, 'Номер успешно добавлен!')
        return super().form_valid(form)


class RoomDetailView(DetailView):
    model = Room
    template_name = 'bookings/room_detail.html'
    context_object_name = 'room'
    pk_url_kwarg = 'room_id'


class RoomUpdateView(UpdateView):
    model = Room
    form_class = RoomForm
    template_name = 'bookings/room_form.html'
    pk_url_kwarg = 'room_id'
    success_url = reverse_lazy('bookings:room_list')

    def form_valid(self, form):
        messages.success(self.request, 'Номер успешно обновлён!')
        return super().form_valid(form)


class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'bookings/room_confirm_delete.html'
    pk_url_kwarg = 'room_id'
    success_url = reverse_lazy('bookings:room_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Номер успешно удалён!')
        return super().delete(request, *args, **kwargs)


class BookingListView(ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 12

    def get_queryset(self):
        # Поля, по которым можно сортировать
        valid_sort_fields = [
            'room', 'guest_name', 'check_in',
            'check_out', 'total_price', 'status'
        ]

        # Получаем параметр сортировки из запроса
        # По умолчанию сортируем по дате заезда
        sort_field = self.request.GET.get('sort', 'check_in')

        # Проверяем, что поле для сортировки допустимо
        if sort_field.lstrip('-') not in valid_sort_fields:
            sort_field = 'check_in'

        # Получаем параметр фильтрации по номеру
        room_id = self.request.GET.get('room')

        # Фильтруем бронирования по номеру, если указан room_id
        queryset = Booking.objects.all()
        if room_id:
            room = get_object_or_404(Room, id=room_id)
            queryset = room.bookings.all()

        self.sort_field = sort_field
        self.sort_direction = 'desc' if sort_field.startswith('-') else 'asc'

        return queryset.order_by(sort_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем параметры сортировки в контекст
        context['sort_field'] = self.sort_field.lstrip('-')
        context['sort_direction'] = self.sort_direction

        # Добавляем список номеров для фильтрации
        context['rooms'] = Room.objects.all()

        # Добавляем выбранный номер (если есть)
        room_id = self.request.GET.get('room')
        if room_id:
            context['selected_room'] = get_object_or_404(Room, id=room_id)

        return context


class BookingDetailView(DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'
    pk_url_kwarg = 'booking_id'


class BookingCreateView(CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    success_url = reverse_lazy('bookings:booking_list')

    def get_initial(self):
        initial = super().get_initial()
        room_id = self.request.GET.get('room')
        if room_id:
            room = get_object_or_404(Room, id=room_id)
            initial['room'] = room
        return initial

    def form_valid(self, form):
        messages.success(self.request, 'Бронирование успешно создано!')
        return super().form_valid(form)


class BookingUpdateView(UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'
    pk_url_kwarg = 'booking_id'
    success_url = reverse_lazy('bookings:booking_list')

    def form_valid(self, form):
        messages.success(self.request, 'Бронирование успешно обновлено!')
        return super().form_valid(form)


class BookingDeleteView(DeleteView):
    model = Booking
    template_name = 'bookings/booking_confirm_delete.html'
    pk_url_kwarg = 'booking_id'
    success_url = reverse_lazy('bookings:booking_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Бронирование успешно удалено!')
        return super().delete(request, *args, **kwargs)
