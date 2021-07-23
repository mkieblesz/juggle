from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers

from juggle import views

router = routers.DefaultRouter()
router.register(r"jobs", views.JobViewSet)
router.register(r"job-applications", views.JobApplicationViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
