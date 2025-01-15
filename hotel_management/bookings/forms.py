from django import forms
from .models import Booking
from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['type', 'category', 'has_baby_cot',
                  'weekday_price', 'weekend_price']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Выберите тип номера'}),
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Выберите категорию'}),
            'has_baby_cot': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'weekday_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена в будни'}),
            'weekend_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена в выходные'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['room', 'check_in', 'check_out', 'guest_name', 'guest_phone',
                  'has_baby_cot', 'status', 'actual_check_in', 'actual_check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'actual_check_in': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'actual_check_out': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Скрываем поля actual_check_in и actual_check_out при создании бронирования
        if not self.instance.pk:  # Если это создание нового бронирования
            self.fields['actual_check_in'].widget = forms.HiddenInput()
            self.fields['actual_check_out'].widget = forms.HiddenInput()
            # Статус тоже скрываем, так как по умолчанию "Активен"
            self.fields['status'].widget = forms.HiddenInput()
        else:
            # Убедимся, что значения полей check_in, check_out, actual_check_in и actual_check_out передаются в правильном формате
            if self.instance.check_in:
                self.initial['check_in'] = self.instance.check_in.strftime(
                    '%Y-%m-%d')
            if self.instance.check_out:
                self.initial['check_out'] = self.instance.check_out.strftime(
                    '%Y-%m-%d')
            if self.instance.actual_check_in:
                self.initial['actual_check_in'] = self.instance.actual_check_in.strftime(
                    '%Y-%m-%d')
            if self.instance.actual_check_out:
                self.initial['actual_check_out'] = self.instance.actual_check_out.strftime(
                    '%Y-%m-%d')
