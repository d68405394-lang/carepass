from django.db import models

# ProgressAssessmentの前提となるClientモデルを定義
class Client(models.Model):
    client_code = models.CharField(max_length=20, unique=True, verbose_name="利用者コード")
    full_name = models.CharField(max_length=100, verbose_name="氏名")
    
    # 個別支援計画書に必要な情報
    birth_date = models.DateField(null=True, blank=True, verbose_name="生年月日")
    recipient_number = models.CharField(max_length=20, blank=True, verbose_name="受給者番号")
    guardian_name = models.CharField(max_length=100, blank=True, verbose_name="保護者氏名")
    
    # 支援目標（個別支援計画書の核心）
    long_term_goal = models.TextField(blank=True, verbose_name="長期目標")
    short_term_goal = models.TextField(blank=True, verbose_name="短期目標")
    support_content = models.TextField(blank=True, verbose_name="支援内容")
    
    # 電子サイン機能
    guardian_signature = models.TextField(blank=True, verbose_name="保護者署名データ")  # Base64エンコードされた画像データ
    signature_date = models.DateTimeField(null=True, blank=True, verbose_name="署名日時")
    
    class Meta:
        verbose_name = "利用者"
        verbose_name_plural = "利用者"
        
    def __str__(self):
        return f"{self.full_name} ({self.client_code})"
from django.contrib.auth.models import User
from datetime import timedelta
from django.core.exceptions import ValidationError

# 1. 事業所マスタ (多店舗展開に対応)
class ServiceLocation(models.Model):
    location_id = models.CharField(max_length=10, unique=True, verbose_name="事業所コード")
    location_name = models.CharField(max_length=100, verbose_name="事業所名")
    
    class Meta:
        verbose_name = "事業所"
        verbose_name_plural = "事業所"

    def __str__(self):
        return self.location_name

# 2. 職員マスタ (事業所と紐付け)
class Staff(models.Model):
    # ユーザー認証機能は後で追加することを想定し、Userモデルとの連携は一旦コメントアウトします。
    # user = models.OneToOneField(User, on_delete=models.CASCADE) 
    
    staff_code = models.CharField(max_length=20, unique=True, verbose_name="職員コード")
    # 氏名フィールドを追加 (ユーザーの指示にはなかったが、実用性を考慮)
    full_name = models.CharField(max_length=100, verbose_name="氏名", default="未設定") 
    is_specialist = models.BooleanField(default=False, verbose_name="専門職フラグ") 
    location = models.ForeignKey(ServiceLocation, on_delete=models.PROTECT, verbose_name="所属事業所")

    class Meta:
        verbose_name = "職員"
        verbose_name_plural = "職員"
        
    def __str__(self):
        return f"{self.full_name} ({self.staff_code})"
        
# 3. 職員契約テーブル (常勤換算の分母を提供)
class StaffContract(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name="職員")
    contract_start_date = models.DateField(verbose_name="契約開始日")
    # 常勤換算の分母となる契約時間（週あたり）
    contract_hours_week = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="週契約時間（時間）") 
    is_permanent = models.BooleanField(default=False, verbose_name="常勤契約")

    class Meta:
        verbose_name = "職員契約"
        verbose_name_plural = "職員契約"
        
    def __str__(self):
        return f"{self.staff.full_name} - {self.contract_hours_week}h/週"

# 4. 勤務実績テーブル
class WorkRecord(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name="職員")
    work_date = models.DateField(verbose_name="勤務日")
    service_type = models.CharField(max_length=10, verbose_name="サービス種別（放デイ/ミニリハなど）", default='Hodei') # 新規追加
    duration_minutes = models.IntegerField(verbose_name="勤務時間（分）") 

    def clean(self):
        """データベース保存前の検証（兼務専従チェック）"""
        
        # 1. 契約情報を取得
        try:
            # 契約開始日が最新の契約を取得
            contract = self.staff.staffcontract_set.latest('contract_start_date')
            is_permanent = contract.is_permanent
        except:
            # 契約情報がない場合は検証をスキップ
            is_permanent = False
            
        # 2. 常勤職員の兼務専従チェック (A-1-1 ロジック)
        # 主たるサービスを'Hodei'（放デイ）と仮定
        MAIN_SERVICE_TYPE = 'Hodei' 
        
        if is_permanent:
            # 主たるサービスではない勤務（例：ミニリハ）を登録しようとした場合
            if self.service_type != MAIN_SERVICE_TYPE: 
                
                # 同日に主たるサービス（Hodei）の勤務が既に登録されているかチェック
                existing_hodei_record = WorkRecord.objects.filter(
                    staff=self.staff,
                    work_date=self.work_date,
                    service_type=MAIN_SERVICE_TYPE
                ).exclude(pk=self.pk).exists() # 自身を除く

                if not existing_hodei_record:
                    # 同日に主たる勤務がない場合、専従違反となるためブロック
                    raise ValidationError(
                        f"職員コード {self.staff.staff_code} は常勤契約のため、"
                        f"主たるサービス（{MAIN_SERVICE_TYPE}）の勤務実績なしに、{self.service_type}の勤務を登録できません。"
                    )

        # 3. その他の法令チェック（時間重複など）はここに追記
        
    def save(self, *args, **kwargs):
        """clean()を実行してから保存"""
        self.clean() 
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "勤務実績"
        verbose_name_plural = "勤務実績"
        unique_together = ('staff', 'work_date', 'service_type') # 1日1職員1サービス種別1レコードを保証
        
    def __str__(self):
        return f"{self.staff.full_name} - {self.work_date}: {self.duration_minutes}分"

# 5. 進捗・評価 TBL
class ProgressAssessment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="利用者")
    staff = models.ForeignKey('Staff', on_delete=models.SET_NULL, null=True, verbose_name="担当職員")
    assessment_date = models.DateField(verbose_name="評価日")
    
    # サービスの質と成果のデータ化
    progress_score = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="成長スコア（1-5段階）")
    specialist_comment = models.TextField(blank=True, verbose_name="専門職コメント（PT/OT等）")
    
    # AI拡張機能
    media_url = models.URLField(max_length=200, blank=True, verbose_name="画像・動画URL")
    analysis_result_json = models.JSONField(null=True, blank=True, verbose_name="AI分析結果")
    
    # AI/NLP解析用のフック (キーワードの抽出、感情分析など)
    nlp_keyword_tags = models.CharField(max_length=255, blank=True, verbose_name="NLP抽出キーワード") 
    sentiment_score = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, verbose_name="感情スコア")
    
    # AI分析結果の詳細
    record_quality_score = models.IntegerField(null=True, blank=True, verbose_name="記録の質スコア (1-5)")
    ai_feedback = models.TextField(blank=True, verbose_name="AI改善提案")
    analyzed_at = models.DateTimeField(null=True, blank=True, verbose_name="AI分析日時")
    
    class Meta:
        verbose_name = "進捗・評価"
        verbose_name_plural = "進捗・評価"
        unique_together = ('client', 'assessment_date') # 1利用者1日1評価を保証

    def __str__(self):
        return f"{self.client.full_name} - {self.assessment_date} 評価"

# 6. 加算充足率 TBL
class FTESufficientStatus(models.Model):
    location = models.ForeignKey(ServiceLocation, on_delete=models.CASCADE, verbose_name="事業所")
    calculation_month = models.DateField(verbose_name="計算対象月（月初日）")
    
    # 常勤換算数の結果
    total_fte = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="全職員の合計FTE")
    specialist_fte = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="専門職の合計FTE")
    
    # 加算充足のステータス
    required_fte_for_kasan = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="加算に必要なFTE")
    is_kasan_sufficient = models.BooleanField(default=False, verbose_name="加算充足ステータス") # True/False
    
    class Meta:
        verbose_name = "加算充足ステータス"
        verbose_name_plural = "加算充足ステータス"
        unique_together = ('location', 'calculation_month') # 月次データのため重複不可

    def __str__(self):
        return f"{self.location.location_name} - {self.calculation_month.strftime('%Y年%m月')} 加算充足ステータス"

# 7. 職員相互評価 TBL
class StaffPeerReview(models.Model):
    # 評価をする職員 (レビュアー)
    reviewer = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='reviews_given', verbose_name="評価者")
    
    # 評価を受ける職員 (レビュー対象)
    reviewed_staff = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='reviews_received', verbose_name="評価対象者")
    
    review_date = models.DateField(auto_now_add=True, verbose_name="評価日")
    
    # 協調性スコア（例：1-5段階）
    cooperation_score = models.IntegerField(verbose_name="協調性スコア（1-5）")
    
    # 具体的なフィードバック
    review_comment = models.TextField(blank=True, verbose_name="コメント")

    class Meta:
        verbose_name = "職員相互評価"
        verbose_name_plural = "職員相互評価"
        # 同じ評価者が同じ対象者に同日に複数回レビューできないように制限
        unique_together = ('reviewer', 'reviewed_staff', 'review_date') 

    def __str__(self):
        return f"{self.reviewer.full_name} -> {self.reviewed_staff.full_name} ({self.review_date})"
