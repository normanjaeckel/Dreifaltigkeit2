"""dreifaltigkeit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('gottesdienste/', views.Services.as_view(), name='services'),
    path('termine/', views.Events.as_view(), name='events'),
    path('<category>/<page>/', views.Flatpage.as_view(), name='flatpage'),
    path('spenden/', views.Imprint.as_view(), name='donation'),  # TODO: Change view.
    path('links/', views.Imprint.as_view(), name='links'),  # TODO: Change view.
    path('impressum/', views.Imprint.as_view(), name='imprint'),
    path('ankuendigung/<int:pk>/', views.Announcements.as_view(), name='announcement'),
    path('admin/', admin.site.urls),
]
