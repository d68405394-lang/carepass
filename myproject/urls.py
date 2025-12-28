"""
URL configuration for myproject project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("progress/", views.progress, name='progress'),
    path("progress/input/", views.progress_input, name='progress_input'),
    path("work-record/input/", views.work_record_input, name='work_record_input'),
    path("ai-analysis/", views.ai_analysis, name='ai_analysis'),
    path("billing/", views.billing, name='billing'),
    path("guardian/", views.guardian, name='guardian'),
    path("statutory-documents/", views.statutory_documents, name='statutory_documents'),
    path("accident-reports/", views.accident_reports, name='accident_reports'),
    path("api/", include("billing_management.urls")),
    path("api/statutory-documents/", include("statutory_documents.urls")),
    path("api/accident-reports/", include("accident_reporting.urls")),
    path('admin/', admin.site.urls),
]

# Serve static files in production
if settings.DEBUG is False:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
