
from django.contrib import admin
from django.urls import path,include
from login import views

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns


urlpatterns = [
path('admin/', admin.site.urls),
path('', include ('login.urls') ),
path('', include ('setup.urls') ),
path('', include ('account.urls') ),
path('', include ('report.urls') ),
path('', include ('control.urls') ),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
