from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
import notifications.urls

urlpatterns = [
     path('admin/', admin.site.urls),
     path("", include("main_app.urls")),
     path("accounts/", include("accounts.urls")),
     path("", include("chats.urls")),
     path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
