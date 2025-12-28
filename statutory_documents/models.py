"""
法定書類管理の基盤モデル

将来的に様々な法定書類を追加する際の拡張性を担保するため、
書類種別をマスターデータとして管理します。
"""
from django.db import models


class StatutoryDocumentType(models.Model):
    """
    法定書類種別マスター
    
    法定書類ハブ画面に表示される書類の種類を管理します。
    新しい法定書類を追加する際は、このテーブルにレコードを追加し、
    対応するフロントエンドのパスを指定するだけで、ハブ画面に自動的に表示されます。
    """
    
    name = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name="書類名",
        help_text="例: 事故・ヒヤリハット報告書"
    )
    
    description = models.TextField(
        blank=True, 
        verbose_name="説明",
        help_text="書類の目的や用途の説明"
    )
    
    frontend_path = models.CharField(
        max_length=200, 
        verbose_name="フロントエンドURLパス",
        help_text="例: /accident-reports"
    )
    
    icon_name = models.CharField(
        max_length=50, 
        blank=True, 
        verbose_name="アイコン名",
        help_text="UI表示用のアイコン名（例: ReportProblem）"
    )
    
    order = models.PositiveIntegerField(
        default=0, 
        verbose_name="表示順",
        help_text="ハブ画面での表示順序（小さい順）"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="有効",
        help_text="無効にするとハブ画面に表示されなくなります"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="作成日時"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="更新日時"
    )

    class Meta:
        verbose_name = "法定書類種別"
        verbose_name_plural = "法定書類種別"
        ordering = ["order", "name"]

    def __str__(self):
        return self.name
