"""
ゲーミフィケーションのデータモデル
"""
from django.db import models
from billing_management.models import Client


class Badge(models.Model):
    """バッジマスタ"""
    
    BADGE_CATEGORY_CHOICES = [
        ('attendance', '出席'),
        ('signature', '電子サイン'),
        ('activity', '活動'),
        ('growth', '成長'),
        ('special', '特別'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='バッジ名')
    description = models.TextField(verbose_name='説明')
    category = models.CharField(max_length=20, choices=BADGE_CATEGORY_CHOICES, verbose_name='カテゴリ')
    icon = models.CharField(max_length=50, default='🏆', verbose_name='アイコン')
    
    # 獲得条件
    condition_type = models.CharField(max_length=50, verbose_name='条件タイプ')
    condition_value = models.IntegerField(verbose_name='条件値')
    
    # 表示順
    display_order = models.IntegerField(default=0, verbose_name='表示順')
    
    class Meta:
        db_table = 'badges'
        verbose_name = 'バッジ'
        verbose_name_plural = 'バッジ'
        ordering = ['display_order', 'id']
    
    def __str__(self):
        return f"{self.icon} {self.name}"


class ClientBadge(models.Model):
    """利用者が獲得したバッジ"""
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='earned_badges', verbose_name='利用者')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='earned_by', verbose_name='バッジ')
    earned_at = models.DateTimeField(auto_now_add=True, verbose_name='獲得日時')
    
    # 通知済みフラグ
    notification_sent = models.BooleanField(default=False, verbose_name='通知送信済み')
    
    class Meta:
        db_table = 'client_badges'
        verbose_name = '獲得バッジ'
        verbose_name_plural = '獲得バッジ'
        unique_together = ['client', 'badge']
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.client.full_name} - {self.badge.name}"


class ClientPoints(models.Model):
    """利用者のポイント"""
    
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='points', verbose_name='利用者')
    total_points = models.IntegerField(default=0, verbose_name='合計ポイント')
    
    # カテゴリ別ポイント
    attendance_points = models.IntegerField(default=0, verbose_name='出席ポイント')
    activity_points = models.IntegerField(default=0, verbose_name='活動ポイント')
    growth_points = models.IntegerField(default=0, verbose_name='成長ポイント')
    
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')
    
    class Meta:
        db_table = 'client_points'
        verbose_name = 'ポイント'
        verbose_name_plural = 'ポイント'
    
    def __str__(self):
        return f"{self.client.full_name} - {self.total_points}pt"
