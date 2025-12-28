"""
法定書類管理のビュー
"""
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import StatutoryDocumentType
from .serializers import StatutoryDocumentTypeSerializer


class StatutoryDocumentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    法定書類種別マスターのViewSet
    
    法定書類ハブ画面に表示する書類一覧を取得するためのAPIです。
    読み取り専用（一覧取得・詳細取得のみ）で、
    有効な書類のみを表示順でソートして返します。
    """
    
    queryset = StatutoryDocumentType.objects.filter(is_active=True)
    serializer_class = StatutoryDocumentTypeSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def statutory_document_types_list(request):
    """
    法定書類種別一覧を取得するシンプルなAPIビュー
    
    法定書類ハブ画面で使用します。
    """
    document_types = StatutoryDocumentType.objects.filter(is_active=True).order_by('order')
    serializer = StatutoryDocumentTypeSerializer(document_types, many=True)
    return Response(serializer.data)
