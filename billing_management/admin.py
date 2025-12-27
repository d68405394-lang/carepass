from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    CustomUser, ServiceLocation, Staff, StaffContract, WorkRecord, 
    Client, ProgressAssessment, FTESufficientStatus, StaffPeerReview
)


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """カスタムユーザーモデルの管理画面設定"""
    
    # リスト表示
    list_display = ('username', 'email', 'role', 'location', 'is_staff', 'is_active')
    list_filter = ('role', 'location', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('username',)
    
    # 詳細表示
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('個人情報', {'fields': ('email',)}),
        ('権限設定', {
            'fields': ('role', 'location', 'is_active', 'is_staff', 'is_superuser'),
            'description': 'ロールと事業所を設定してください。スーパー管理者は事業所を空欄にします。'
        }),
        ('グループとパーミッション', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
        ('重要な日付', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',),
        }),
    )
    
    # 新規作成時のフィールド
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'location', 'is_staff', 'is_active'),
        }),
    )


@admin.register(ServiceLocation)
class ServiceLocationAdmin(admin.ModelAdmin):
    """事業所の管理画面設定"""
    list_display = ('location_id', 'location_name')
    search_fields = ('location_id', 'location_name')
    ordering = ('location_id',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """利用者の管理画面設定"""
    list_display = ('client_code', 'full_name', 'location', 'birth_date', 'recipient_number')
    list_filter = ('location',)
    search_fields = ('client_code', 'full_name', 'recipient_number')
    ordering = ('client_code',)
    
    def get_queryset(self, request):
        """ユーザーのロールに応じてクエリセットをフィルタリング"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'super_admin':
            return qs
        if request.user.role in ['location_admin', 'staff']:
            return qs.filter(location=request.user.location)
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """事業所フィールドの選択肢を制限"""
        if db_field.name == 'location':
            if request.user.role in ['location_admin', 'staff']:
                kwargs['queryset'] = ServiceLocation.objects.filter(id=request.user.location.id)
                kwargs['initial'] = request.user.location
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    fieldsets = (
        ('基本情報', {
            'fields': ('client_code', 'full_name', 'birth_date', 'recipient_number', 'location')
        }),
        ('保護者情報', {
            'fields': ('guardian_name', 'guardian_email')
        }),
        ('支援計画', {
            'fields': ('long_term_goal', 'short_term_goal', 'support_content')
        }),
        ('署名', {
            'fields': ('guardian_signature', 'signature_date'),
            'classes': ('collapse',),
        }),
    )


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    """スタッフの管理画面設定"""
    list_display = ('staff_code', 'full_name', 'location', 'is_specialist')
    list_filter = ('location', 'is_specialist')
    search_fields = ('staff_code', 'full_name')
    ordering = ('staff_code',)
    
    def get_queryset(self, request):
        """ユーザーのロールに応じてクエリセットをフィルタリング"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'super_admin':
            return qs
        if request.user.role in ['location_admin', 'staff']:
            return qs.filter(location=request.user.location)
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """事業所フィールドの選択肢を制限"""
        if db_field.name == 'location':
            if request.user.role in ['location_admin', 'staff']:
                kwargs['queryset'] = ServiceLocation.objects.filter(id=request.user.location.id)
                kwargs['initial'] = request.user.location
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(WorkRecord)
class WorkRecordAdmin(admin.ModelAdmin):
    """勤務記録の管理画面設定"""
    list_display = ('staff', 'work_date', 'service_type', 'duration_minutes')
    list_filter = ('work_date', 'staff__location')
    search_fields = ('staff__full_name', 'staff__staff_code')
    date_hierarchy = 'work_date'
    ordering = ('-work_date', 'staff')
    
    def get_queryset(self, request):
        """ユーザーのロールに応じてクエリセットをフィルタリング"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'super_admin':
            return qs
        if request.user.role in ['location_admin', 'staff']:
            return qs.filter(staff__location=request.user.location)
        return qs.none()


@admin.register(ProgressAssessment)
class ProgressAssessmentAdmin(admin.ModelAdmin):
    """経過記録の管理画面設定"""
    list_display = ('client', 'assessment_date')
    list_filter = ('assessment_date', 'client__location')
    search_fields = ('client__full_name', 'assessor')
    date_hierarchy = 'assessment_date'
    ordering = ('-assessment_date',)
    
    def get_queryset(self, request):
        """ユーザーのロールに応じてクエリセットをフィルタリング"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.role == 'super_admin':
            return qs
        if request.user.role in ['location_admin', 'staff']:
            return qs.filter(client__location=request.user.location)
        return qs.none()


# その他のモデルを登録
admin.site.register(StaffContract)
admin.site.register(FTESufficientStatus)
admin.site.register(StaffPeerReview)
