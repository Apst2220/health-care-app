from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.health_dashboard_stats, name="health_dashboard_stats"),
    path("", views.health_dashboard_map, name="health_dashboard_map")] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
