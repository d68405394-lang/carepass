"""
事故・ヒヤリハット報告書モデル

運営指導・実地指導で指摘されない設計を最優先とし、
改ざん防止・履歴保持・監査証跡を徹底した構造です。
"""
from django.db import models
from django.conf import settings


class AccidentReport(models.Model):
    """
    事故・ヒヤリハット報告書（最新状態を保持）
    
    このテーブルは報告書の「現在の状態」を保持します。
    変更履歴はAccidentReportVersionテーブルで管理されます。
    """
    
    REPORT_TYPE_CHOICES = [
        ('accident', '事故'),
        ('hiyari_hatto', 'ヒヤリハット'),
    ]
    
    STATUS_CHOICES = [
        ('draft', '作成中'),
        ('pending_review', '承認待ち'),
        ('approved', '承認済み'),
    ]
    
    SERVICE_TYPE_CHOICES = [
        ('houmon_kaigo', '訪問介護'),
        ('houmon_kango', '訪問看護'),
        ('day_service', '通所介護（デイサービス）'),
        ('day_care', '通所リハビリテーション（デイケア）'),
        ('short_stay', '短期入所生活介護（ショートステイ）'),
        ('group_home', '認知症対応型共同生活介護（グループホーム）'),
        ('houdehi', '放課後等デイサービス'),
        ('jihatsu', '児童発達支援'),
        ('other', 'その他'),
    ]
    
    # 基本情報
    report_type = models.CharField(
        max_length=20, 
        choices=REPORT_TYPE_CHOICES, 
        verbose_name="区分"
    )
    
    occurred_at = models.DateTimeField(
        verbose_name="発生日時"
    )
    
    location_detail = models.CharField(
        max_length=255, 
        verbose_name="発生場所（詳細）",
        help_text="例: 居室内、廊下、トイレ、食堂、送迎車内"
    )
    
    service_type = models.CharField(
        max_length=50, 
        choices=SERVICE_TYPE_CHOICES, 
        verbose_name="サービス種別"
    )
    
    # リレーション（既存モデルとの連携）
    client = models.ForeignKey(
        'billing_management.Client', 
        on_delete=models.PROTECT, 
        verbose_name="利用者",
        related_name='accident_reports'
    )
    
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        verbose_name="報告者（起案者）",
        related_name='reported_accidents'
    )
    
    location = models.ForeignKey(
        'billing_management.ServiceLocation', 
        on_delete=models.PROTECT, 
        verbose_name="発生場所（事業所）",
        related_name='accident_reports'
    )
    
    involved_staff = models.ManyToManyField(
        'billing_management.Staff',
        blank=True,
        verbose_name="関係職員",
        related_name='involved_accidents'
    )
    
    # 事実情報（職員による一次入力）
    incident_description = models.TextField(
        verbose_name="事実経過",
        help_text="発生時の状況を時系列で客観的に記載"
    )
    
    client_state = models.TextField(
        blank=True,
        verbose_name="利用者の状態",
        help_text="発生時・発生後の利用者の状態"
    )
    
    damage_status = models.TextField(
        blank=True,
        verbose_name="被害の状況",
        help_text="怪我の有無、程度、部位など"
    )
    
    initial_response = models.TextField(
        blank=True,
        verbose_name="初期対応",
        help_text="発生直後に行った対応"
    )
    
    family_contact_log = models.TextField(
        blank=True,
        verbose_name="家族等への連絡状況",
        help_text="連絡日時、連絡先、連絡内容"
    )
    
    medical_response = models.TextField(
        blank=True,
        verbose_name="医療機関への対応",
        help_text="受診の有無、医療機関名、診断内容"
    )
    
    # AI生成フィールド
    ai_generated_overview = models.TextField(
        blank=True,
        verbose_name="事故の状況（AI生成）"
    )
    
    ai_generated_cause_analysis = models.TextField(
        blank=True,
        verbose_name="原因分析（AI生成）"
    )
    
    ai_generated_prevention_plan = models.TextField(
        blank=True,
        verbose_name="再発防止策（AI生成）"
    )
    
    # 行政報告判定
    is_government_report_needed = models.BooleanField(
        default=False,
        verbose_name="行政報告要否"
    )
    
    government_report_reason = models.TextField(
        blank=True,
        verbose_name="行政報告要否の判定理由"
    )
    
    # ステータス管理
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft', 
        verbose_name="ステータス"
    )
    
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="承認者",
        related_name='approved_accidents'
    )
    
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="承認日時"
    )
    
    # タイムスタンプ
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="作成日時"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="最終更新日時"
    )

    class Meta:
        verbose_name = "事故・ヒヤリハット報告書"
        verbose_name_plural = "事故・ヒヤリハット報告書"
        ordering = ["-occurred_at"]

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.client.full_name} ({self.occurred_at.strftime('%Y/%m/%d %H:%M')})"


class AccidentReportVersion(models.Model):
    """
    報告書バージョン管理（改ざん防止・履歴保持）
    
    報告書が作成・更新されるたびに、その時点の全データを
    JSON形式でスナップショットとして保存します。
    これにより、過去のどのバージョンも完全に復元可能となり、
    改ざんをシステム的に防止します。
    """
    
    report = models.ForeignKey(
        AccidentReport, 
        on_delete=models.CASCADE, 
        related_name='versions', 
        verbose_name="関連報告書"
    )
    
    version_number = models.PositiveIntegerField(
        verbose_name="バージョン番号"
    )
    
    snapshot_data = models.JSONField(
        verbose_name="スナップショットデータ",
        help_text="その時点の報告書データの完全なスナップショット（JSON形式）"
    )
    
    editor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        verbose_name="編集者"
    )
    
    edited_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="編集日時"
    )
    
    change_summary = models.TextField(
        blank=True,
        verbose_name="変更概要",
        help_text="このバージョンでの主な変更点"
    )

    class Meta:
        verbose_name = "報告書バージョン"
        verbose_name_plural = "報告書バージョン"
        unique_together = ('report', 'version_number')
        ordering = ["-version_number"]

    def __str__(self):
        return f"{self.report} - Ver.{self.version_number}"


class AccidentAuditTrail(models.Model):
    """
    監査証跡
    
    報告書に対する全ての操作（閲覧、AI生成、承認、PDF出力など）を記録します。
    これにより、運営指導で「誰がいつ、この記録に何をしたか」を完全に証明できます。
    """
    
    ACTION_CHOICES = [
        ('created', '作成'),
        ('viewed', '閲覧'),
        ('updated', '更新'),
        ('ai_generated', 'AI生成実行'),
        ('submitted_for_review', '承認申請'),
        ('approved', '承認'),
        ('rejected', '差戻し'),
        ('pdf_generated', 'PDF出力'),
        ('pdf_downloaded', 'PDFダウンロード'),
    ]
    
    report = models.ForeignKey(
        AccidentReport, 
        on_delete=models.CASCADE, 
        related_name='audit_trails', 
        verbose_name="関連報告書"
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.PROTECT, 
        verbose_name="操作ユーザー"
    )
    
    action = models.CharField(
        max_length=50, 
        choices=ACTION_CHOICES,
        verbose_name="操作内容"
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="操作日時"
    )
    
    details = models.JSONField(
        null=True,
        blank=True,
        verbose_name="操作詳細",
        help_text="操作に関する追加情報（例: 変更前後の値）"
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="IPアドレス"
    )

    class Meta:
        verbose_name = "監査証跡"
        verbose_name_plural = "監査証跡"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.report} - {self.get_action_display()} by {self.user} ({self.timestamp.strftime('%Y/%m/%d %H:%M')})"
