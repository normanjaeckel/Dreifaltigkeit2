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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from . import views
from .feeds import AnnouncementFeed

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('gottesdienste/', views.Services.as_view(), name='services'),
    path('termine/', views.Events.as_view(), name='events'),
    path('termine/<int:pk>/', views.SingleEvent.as_view(), name='single_event'),
    path('impressum/', views.Imprint.as_view(), name='imprint'),
    path('ankuendigung/<int:pk>/', views.Announcements.as_view(), name='announcement'),
    path('ankuendigung/feed.rss', AnnouncementFeed(), name='announcement_feed'),  #TODO: Change URL (because the feed also contains events)
    path('admin/', admin.site.urls),
    path('<category>/<page>/', views.FlatPage.as_view(), name='flat_page'),
    path('<page>/', views.FlatPage.as_view(root=True), name='flat_page_root'),
]

# Pop URL pattern for "termine" because we do not want an event calender on
# kindergarten site.
if not settings.SITE_ID == 'parish':
    urlpatterns.pop(2)

# This line does only work during development (DEBUG = True)
# https://docs.djangoproject.com/en/2.0/howto/static-files/#serving-files-uploaded-by-a-user-during-development
urlpatterns[-2:-2] = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
