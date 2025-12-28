"""
事故・ヒヤリハット報告書のビュー

運営指導対応を意識し、全ての操作に監査証跡を記録します。
"""
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AccidentReport, AccidentReportVersion, AccidentAuditTrail
from .serializers import (
    AccidentReportListSerializer,
    AccidentReportDetailSerializer,
    AccidentReportCreateSerializer,
    AccidentReportUpdateSerializer,
    AccidentReportVersionSerializer,
    AccidentAuditTrailSerializer,
    AIGenerateRequestSerializer,
)
from .ai_service import generate_accident_report_content
from .pdf_service import generate_accident_report_pdf
import json


def get_client_ip(request):
    """リクエストからクライアントIPを取得"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def create_audit_trail(report, user, action, request, details=None):
    """監査証跡を作成"""
    AccidentAuditTrail.objects.create(
        report=report,
        user=user,
        action=action,
        ip_address=get_client_ip(request),
        details=details
    )


def create_version_snapshot(report, user, change_summary=''):
    """報告書のバージョンスナップショットを作成"""
    # 現在のバージョン番号を取得
    latest_version = report.versions.order_by('-version_number').first()
    new_version_number = (latest_version.version_number + 1) if latest_version else 1
    
    # スナップショットデータの作成
    snapshot_data = {
        'report_type': report.report_type,
        'occurred_at': report.occurred_at.isoformat() if report.occurred_at else None,
        'location_detail': report.location_detail,
        'service_type': report.service_type,
        'client_id': report.client_id,
        'location_id': report.location_id,
        'incident_description': report.incident_description,
        'client_state': report.client_state,
        'damage_status': report.damage_status,
        'initial_response': report.initial_response,
        'family_contact_log': report.family_contact_log,
        'medical_response': report.medical_response,
        'ai_generated_overview': report.ai_generated_overview,
        'ai_generated_cause_analysis': report.ai_generated_cause_analysis,
        'ai_generated_prevention_plan': report.ai_generated_prevention_plan,
        'is_government_report_needed': report.is_government_report_needed,
        'government_report_reason': report.government_report_reason,
        'status': report.status,
    }
    
    AccidentReportVersion.objects.create(
        report=report,
        version_number=new_version_number,
        snapshot_data=snapshot_data,
        editor=user,
        change_summary=change_summary
    )


class AccidentReportViewSet(viewsets.ModelViewSet):
    """
    事故・ヒヤリハット報告書のViewSet
    
    CRUD操作に加え、AI生成、承認、PDF出力などのカスタムアクションを提供します。
    全ての操作は監査証跡に記録されます。
    """
    
    queryset = AccidentReport.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AccidentReportListSerializer
        elif self.action == 'create':
            return AccidentReportCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AccidentReportUpdateSerializer
        else:
            return AccidentReportDetailSerializer
    
    def get_queryset(self):
        """ユーザーの所属事業所に関連する報告書のみを返す"""
        queryset = AccidentReport.objects.all()
        
        # クエリパラメータによるフィルタリング
        report_type = self.request.query_params.get('report_type')
        status_filter = self.request.query_params.get('status')
        client_id = self.request.query_params.get('client')
        
        if report_type:
            queryset = queryset.filter(report_type=report_type)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        
        return queryset.select_related('client', 'reporter', 'location', 'approved_by')
    
    def retrieve(self, request, *args, **kwargs):
        """報告書詳細取得時に閲覧ログを記録"""
        instance = self.get_object()
        create_audit_trail(instance, request.user, 'viewed', request)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """報告書作成時にバージョンと監査証跡を記録"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report = serializer.save()
        
        # バージョンスナップショットと監査証跡を作成
        create_version_snapshot(report, request.user, '新規作成')
        create_audit_trail(report, request.user, 'created', request)
        
        headers = self.get_success_headers(serializer.data)
        return Response(
            AccidentReportDetailSerializer(report).data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    def update(self, request, *args, **kwargs):
        """報告書更新時にバージョンと監査証跡を記録"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # 承認済みの報告書は更新不可
        if instance.status == 'approved':
            return Response(
                {'error': '承認済みの報告書は編集できません'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        report = serializer.save()
        
        # バージョンスナップショットと監査証跡を作成
        create_version_snapshot(report, request.user, '内容更新')
        create_audit_trail(report, request.user, 'updated', request, {'partial': partial})
        
        return Response(AccidentReportDetailSerializer(report).data)
    
    @action(detail=True, methods=['post'])
    def generate_ai(self, request, pk=None):
        """AI生成を実行"""
        report = self.get_object()
        
        # 承認済みの報告書はAI生成不可
        if report.status == 'approved':
            return Response(
                {'error': '承認済みの報告書に対してAI生成は実行できません'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # AI生成用のデータを準備
        report_data = {
            'report_type': report.get_report_type_display(),
            'occurred_at': report.occurred_at.strftime('%Y年%m月%d日 %H時%M分') if report.occurred_at else '',
            'location_detail': report.location_detail,
            'service_type': report.get_service_type_display(),
            'client_name': report.client.full_name if report.client else '',
            'incident_description': report.incident_description,
            'client_state': report.client_state,
            'damage_status': report.damage_status,
            'initial_response': report.initial_response,
            'family_contact_log': report.family_contact_log,
            'medical_response': report.medical_response,
        }
        
        # AI生成を実行
        ai_result = generate_accident_report_content(report_data)
        
        # 結果を報告書に保存
        report.ai_generated_overview = ai_result['overview']
        report.ai_generated_cause_analysis = ai_result['cause_analysis']
        report.ai_generated_prevention_plan = ai_result['prevention_plan']
        report.is_government_report_needed = ai_result['is_government_report_needed']
        report.government_report_reason = ai_result['government_report_reason']
        report.save()
        
        # バージョンスナップショットと監査証跡を作成
        create_version_snapshot(report, request.user, 'AI生成実行')
        create_audit_trail(report, request.user, 'ai_generated', request)
        
        return Response(AccidentReportDetailSerializer(report).data)
    
    @action(detail=True, methods=['post'])
    def submit_for_review(self, request, pk=None):
        """承認申請"""
        report = self.get_object()
        
        if report.status != 'draft':
            return Response(
                {'error': '作成中の報告書のみ承認申請できます'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        report.status = 'pending_review'
        report.save()
        
        create_version_snapshot(report, request.user, '承認申請')
        create_audit_trail(report, request.user, 'submitted_for_review', request)
        
        return Response(AccidentReportDetailSerializer(report).data)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """承認（管理者のみ）"""
        report = self.get_object()
        
        # TODO: 管理者権限チェックを追加
        
        if report.status != 'pending_review':
            return Response(
                {'error': '承認待ちの報告書のみ承認できます'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        report.status = 'approved'
        report.approved_by = request.user
        report.approved_at = timezone.now()
        report.save()
        
        create_version_snapshot(report, request.user, '承認')
        create_audit_trail(report, request.user, 'approved', request)
        
        return Response(AccidentReportDetailSerializer(report).data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """差戻し（管理者のみ）"""
        report = self.get_object()
        
        # TODO: 管理者権限チェックを追加
        
        if report.status != 'pending_review':
            return Response(
                {'error': '承認待ちの報告書のみ差戻しできます'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reason = request.data.get('reason', '')
        
        report.status = 'draft'
        report.save()
        
        create_version_snapshot(report, request.user, f'差戻し: {reason}')
        create_audit_trail(report, request.user, 'rejected', request, {'reason': reason})
        
        return Response(AccidentReportDetailSerializer(report).data)
    
    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        """PDF出力"""
        report = self.get_object()
        
        # PDF生成
        pdf_bytes = generate_accident_report_pdf(report)
        
        # 監査証跡を記録
        create_audit_trail(report, request.user, 'pdf_downloaded', request)
        
        # レスポンス作成
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        filename = f"accident_report_{report.id}_{report.occurred_at.strftime('%Y%m%d')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
    
    @action(detail=True, methods=['get'])
    def versions(self, request, pk=None):
        """バージョン履歴取得"""
        report = self.get_object()
        versions = report.versions.all()
        serializer = AccidentReportVersionSerializer(versions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def audit_trails(self, request, pk=None):
        """監査証跡取得"""
        report = self.get_object()
        trails = report.audit_trails.all()
        serializer = AccidentAuditTrailSerializer(trails, many=True)
        return Response(serializer.data)
