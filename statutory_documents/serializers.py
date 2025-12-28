"""
法定書類管理のシリアライザー
"""
from rest_framework import serializers
from .models import StatutoryDocumentType


class StatutoryDocumentTypeSerializer(serializers.ModelSerializer):
    """
    法定書類種別マスターのシリアライザー
    """
    
    class Meta:
        model = StatutoryDocumentType
        fields = [
            'id',
            'name',
            'description',
            'frontend_path',
            'icon_name',
            'order',
            'is_active',
        ]
        read_only_fields = ['id']
