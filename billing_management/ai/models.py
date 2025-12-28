"""
AI関連のデータベースモデル

プロンプト管理とAI応答ログ記録のためのモデルを定義します。
"""

from django.db import models
from django.conf import settings


class AIPrompt(models.Model):
    """AIプロンプト管理モデル"""
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="プロンプト名",
        help_text="プロンプトの識別名（例: sentiment_analysis）"
    )
    
    display_name = models.CharField(
        max_length=200,
        verbose_name="表示名",
        help_text="管理画面での表示名"
    )
    
    description = models.TextField(
        blank=True,
        verbose_name="説明",
        help_text="プロンプトの目的や使用方法"
    )
    
    system_prompt = models.TextField(
        verbose_name="システムプロンプト",
        help_text="AIの役割や振る舞いを定義"
    )
    
    user_template = models.TextField(
        verbose_name="ユーザープロンプトテンプレート",
        help_text="変数を含むテンプレート（例: {client_name}）"
    )
    
    version = models.CharField(
        max_length=20,
        default="1.0",
        verbose_name="バージョン"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="有効",
        help_text="このプロンプトを使用するか"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="作成日時"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="更新日時"
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_prompts',
        verbose_name="作成者"
    )
    
    class Meta:
        verbose_name = "AIプロンプト"
        verbose_name_plural = "AIプロンプト"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.display_name} (v{self.version})"


class AILog(models.Model):
    """AI応答ログモデル"""
    
    TASK_TYPE_CHOICES = [
        ('sentiment_analysis', '感情分析'),
        ('progress_record_generation', '進捗記録生成'),
        ('churn_risk_prediction', '離脱リスク予測'),
        ('other', 'その他'),
    ]
    
    provider = models.CharField(
        max_length=50,
        verbose_name="AIプロバイダー",
        help_text="google, openai, anthropic等"
    )
    
    model = models.CharField(
        max_length=100,
        verbose_name="モデル名",
        help_text="gemini-1.5-flash, gpt-4.1-mini等"
    )
    
    task_type = models.CharField(
        max_length=50,
        choices=TASK_TYPE_CHOICES,
        verbose_name="タスクタイプ"
    )
    
    input_data = models.JSONField(
        verbose_name="入力データ",
        help_text="AIに送信したプロンプトとパラメータ"
    )
    
    output_data = models.JSONField(
        verbose_name="出力データ",
        help_text="AIから受信した応答"
    )
    
    tokens_used = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="使用トークン数"
    )
    
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name="コスト（USD）"
    )
    
    response_time = models.FloatField(
        null=True,
        blank=True,
        verbose_name="応答時間（秒）"
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ai_logs',
        verbose_name="ユーザー"
    )
    
    location = models.ForeignKey(
        'ServiceLocation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ai_logs',
        verbose_name="事業所"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="実行日時"
    )
    
    # 品質評価（人間によるフィードバック）
    human_rating = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="人間評価",
        help_text="1-5の評価（5が最高）"
    )
    
    is_accurate = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="正確性",
        help_text="AIの応答が正確だったか"
    )
    
    feedback = models.TextField(
        blank=True,
        verbose_name="フィードバック",
        help_text="AIの応答に対する人間のフィードバック"
    )
    
    class Meta:
        verbose_name = "AI応答ログ"
        verbose_name_plural = "AI応答ログ"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['provider', 'model']),
            models.Index(fields=['task_type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['location']),
        ]
    
    def __str__(self):
        return f"{self.provider}/{self.model} - {self.task_type} ({self.created_at})"
