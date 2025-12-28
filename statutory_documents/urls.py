"""
法定書類管理のURLルーティング
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'types', views.StatutoryDocumentTypeViewSet, basename='statutory-document-type')

urlpatterns = [
    path('', include(router.urls)),
    path('list/', views.statutory_document_types_list, name='statutory-document-types-list'),
]
