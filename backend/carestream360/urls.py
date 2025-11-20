"""
URL configuration for carestream360 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import include
from apps.monitoring import views as monitoring_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.monitoring.urls")),
    # Root redirect to the frontend (helpful when opening port 8000 in a browser)
    path("", monitoring_views.root_redirect),
    # Lightweight dashboard accessible on the backend port (http://localhost:8000/dashboard/)
    path("dashboard/", monitoring_views.simple_dashboard),
]
