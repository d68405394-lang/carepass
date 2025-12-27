"""
保護者向けポータルのデータモデル
"""
from django.db import models
from django.conf import settings
from billing_management.models import Client


class GuardianUser(models.Model):
    """保護者ユーザーモデル"""
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guardian_profile', verbose_name='ユーザー')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='guardians', verbose_name='利用者')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='電話番号')
    relationship = models.CharField(max_length=50, default='保護者', verbose_name='続柄')
    
    # アカウント設定
    email_notifications = models.BooleanField(default=True, verbose_name='メール通知を受け取る')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='登録日時')
    last_login_at = models.DateTimeField(null=True, blank=True, verbose_name='最終ログイン日時')
    
    class Meta:
        db_table = 'guardian_users'
        verbose_name = '保護者ユーザー'
        verbose_name_plural = '保護者ユーザー'
    
    def __str__(self):
        return f"{self.user.username} - {self.client.full_name}の保護者"


class ActivityLog(models.Model):
    """活動記録モデル（保護者向け表示用）"""
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='activity_logs', verbose_name='利用者')
    date = models.DateField(verbose_name='日付')
    activity_type = models.CharField(max_length=50, verbose_name='活動種別')
    description = models.TextField(verbose_name='活動内容')
    staff_comment = models.TextField(blank=True, verbose_name='職員コメント')
    
    # 写真（オプション）
    photo = models.ImageField(upload_to='activity_photos/', null=True, blank=True, verbose_name='活動写真')
    
    # 公開設定
    is_published = models.BooleanField(default=True, verbose_name='保護者に公開')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')
    
    class Meta:
        db_table = 'activity_logs'
        verbose_name = '活動記録'
        verbose_name_plural = '活動記録'
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.client.full_name} - {self.date} - {self.activity_type}"
