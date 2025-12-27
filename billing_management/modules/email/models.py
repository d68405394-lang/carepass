"""
メール機能のデータモデル
"""
from django.db import models
from django.conf import settings
from billing_management.models import Client


class EmailMessage(models.Model):
    """メールメッセージモデル"""
    
    MESSAGE_TYPE_CHOICES = [
        ('individual', '個別'),
        ('bulk', '一斉配信'),
    ]
    
    STATUS_CHOICES = [
        ('draft', '下書き'),
        ('sent', '送信済み'),
        ('failed', '送信失敗'),
    ]
    
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_emails', verbose_name='送信者')
    subject = models.CharField(max_length=200, verbose_name='件名')
    body = models.TextField(verbose_name='本文')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='individual', verbose_name='メッセージタイプ')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='ステータス')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name='送信日時')
    
    # ファイル添付（オプション）
    attachment = models.FileField(upload_to='email_attachments/', null=True, blank=True, verbose_name='添付ファイル')
    
    class Meta:
        db_table = 'email_messages'
        verbose_name = 'メールメッセージ'
        verbose_name_plural = 'メールメッセージ'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.sender.username}"


class EmailRecipient(models.Model):
    """メール受信者モデル"""
    
    READ_STATUS_CHOICES = [
        ('unread', '未読'),
        ('read', '既読'),
    ]
    
    message = models.ForeignKey(EmailMessage, on_delete=models.CASCADE, related_name='recipients', verbose_name='メッセージ')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='received_emails', verbose_name='受信者（利用者）')
    guardian_email = models.EmailField(verbose_name='保護者メールアドレス')
    read_status = models.CharField(max_length=20, choices=READ_STATUS_CHOICES, default='unread', verbose_name='既読ステータス')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='既読日時')
    
    class Meta:
        db_table = 'email_recipients'
        verbose_name = 'メール受信者'
        verbose_name_plural = 'メール受信者'
        unique_together = ['message', 'client']
    
    def __str__(self):
        return f"{self.client.name} - {self.message.subject}"
