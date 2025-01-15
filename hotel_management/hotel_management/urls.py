"""hotel_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.conf.urls import handler404, handler403, handler500
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

handler404 = 'pages.views.custom_404'
handler403 = 'pages.views.custom_403_csrf'
handler500 = 'pages.views.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bookings.urls')),
    path(
        'auth/signup/',
        CreateView.as_view(
            template_name='registration/signup.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('login'),
        ),
        name='registration',
    ),
    path('auth/', include('django.contrib.auth.urls')),
]
