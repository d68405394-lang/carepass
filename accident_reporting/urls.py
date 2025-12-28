"""
事故・ヒヤリハット報告書のURLルーティング
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.AccidentReportViewSet, basename='accident-report')

urlpatterns = [
    path('', include(router.urls)),
]
