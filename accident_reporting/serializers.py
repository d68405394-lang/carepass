"""
事故・ヒヤリハット報告書のシリアライザー
"""
from rest_framework import serializers
from .models import AccidentReport, AccidentReportVersion, AccidentAuditTrail
from billing_management.models import Client, Staff, ServiceLocation


class AccidentReportListSerializer(serializers.ModelSerializer):
    """
    事故報告書一覧用のシリアライザー（軽量版）
    """
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    reporter_name = serializers.CharField(source='reporter.username', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = AccidentReport
        fields = [
            'id',
            'report_type',
            'report_type_display',
            'occurred_at',
            'client',
            'client_name',
            'reporter',
            'reporter_name',
            'location',
            'location_name',
            'status',
            'status_display',
            'is_government_report_needed',
            'created_at',
            'updated_at',
        ]


class AccidentReportDetailSerializer(serializers.ModelSerializer):
    """
    事故報告書詳細用のシリアライザー（全フィールド）
    """
    client_name = serializers.CharField(source='client.full_name', read_only=True)
    reporter_name = serializers.CharField(source='reporter.username', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.username', read_only=True)
    report_type_display = serializers.CharField(source='get_report_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)
    involved_staff_names = serializers.SerializerMethodField()
    
    class Meta:
        model = AccidentReport
        fields = '__all__'
    
    def get_involved_staff_names(self, obj):
        return [staff.name for staff in obj.involved_staff.all()]


class AccidentReportCreateSerializer(serializers.ModelSerializer):
    """
    事故報告書作成用のシリアライザー
    """
    
    class Meta:
        model = AccidentReport
        fields = [
            'report_type',
            'occurred_at',
            'location_detail',
            'service_type',
            'client',
            'location',
            'involved_staff',
            'incident_description',
            'client_state',
            'damage_status',
            'initial_response',
            'family_contact_log',
            'medical_response',
        ]
    
    def create(self, validated_data):
        # 報告者は現在のユーザーを自動設定
        validated_data['reporter'] = self.context['request'].user
        involved_staff = validated_data.pop('involved_staff', [])
        report = AccidentReport.objects.create(**validated_data)
        report.involved_staff.set(involved_staff)
        return report


class AccidentReportUpdateSerializer(serializers.ModelSerializer):
    """
    事故報告書更新用のシリアライザー
    """
    
    class Meta:
        model = AccidentReport
        fields = [
            'report_type',
            'occurred_at',
            'location_detail',
            'service_type',
            'client',
            'location',
            'involved_staff',
            'incident_description',
            'client_state',
            'damage_status',
            'initial_response',
            'family_contact_log',
            'medical_response',
            'ai_generated_overview',
            'ai_generated_cause_analysis',
            'ai_generated_prevention_plan',
        ]


class AccidentReportVersionSerializer(serializers.ModelSerializer):
    """
    報告書バージョン履歴のシリアライザー
    """
    editor_name = serializers.CharField(source='editor.username', read_only=True)
    
    class Meta:
        model = AccidentReportVersion
        fields = [
            'id',
            'version_number',
            'snapshot_data',
            'editor',
            'editor_name',
            'edited_at',
            'change_summary',
        ]


class AccidentAuditTrailSerializer(serializers.ModelSerializer):
    """
    監査証跡のシリアライザー
    """
    user_name = serializers.CharField(source='user.username', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = AccidentAuditTrail
        fields = [
            'id',
            'user',
            'user_name',
            'action',
            'action_display',
            'timestamp',
            'details',
            'ip_address',
        ]


class AIGenerateRequestSerializer(serializers.Serializer):
    """
    AI生成リクエスト用のシリアライザー
    """
    regenerate = serializers.BooleanField(default=False, help_text="既存のAI生成結果を再生成するかどうか")
