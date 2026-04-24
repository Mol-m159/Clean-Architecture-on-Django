from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Админка Django
    path('django-admin/', admin.site.urls),
    
    
    # Веб-интерфейс
    path('', include('core.urls')), 
    
    # Перенаправление с корня на веб-интерфейс
    path('admin/', RedirectView.as_view(url='/', permanent=False)), 
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)