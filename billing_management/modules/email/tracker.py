"""
メール既読管理ロジック
"""
from django.utils import timezone
from .models import EmailRecipient


class EmailTracker:
    """メール既読管理クラス"""
    
    @staticmethod
    def mark_as_read(recipient_id):
        """
        メールを既読にする
        
        Args:
            recipient_id (int): 受信者ID
        
        Returns:
            dict: 処理結果
        """
        try:
            recipient = EmailRecipient.objects.get(id=recipient_id)
            if recipient.read_status == 'unread':
                recipient.read_status = 'read'
                recipient.read_at = timezone.now()
                recipient.save()
                return {
                    'success': True,
                    'message': '既読にしました'
                }
            else:
                return {
                    'success': True,
                    'message': 'すでに既読です'
                }
        except EmailRecipient.DoesNotExist:
            return {
                'success': False,
                'error': '受信者が見つかりません'
            }
    
    @staticmethod
    def get_read_status(message_id):
        """
        メッセージの既読状況を取得
        
        Args:
            message_id (int): メッセージID
        
        Returns:
            dict: 既読状況
        """
        recipients = EmailRecipient.objects.filter(message_id=message_id)
        total_count = recipients.count()
        read_count = recipients.filter(read_status='read').count()
        unread_count = total_count - read_count
        
        read_recipients = []
        unread_recipients = []
        
        for recipient in recipients:
            recipient_data = {
                'id': recipient.id,
                'client_name': recipient.client.name,
                'guardian_email': recipient.guardian_email,
                'read_at': recipient.read_at.isoformat() if recipient.read_at else None
            }
            
            if recipient.read_status == 'read':
                read_recipients.append(recipient_data)
            else:
                unread_recipients.append(recipient_data)
        
        return {
            'total_count': total_count,
            'read_count': read_count,
            'unread_count': unread_count,
            'read_rate': round((read_count / total_count * 100), 2) if total_count > 0 else 0,
            'read_recipients': read_recipients,
            'unread_recipients': unread_recipients
        }
    
    @staticmethod
    def get_unread_messages(client_id):
        """
        利用者の未読メッセージを取得
        
        Args:
            client_id (int): 利用者ID
        
        Returns:
            list: 未読メッセージのリスト
        """
        unread_recipients = EmailRecipient.objects.filter(
            client_id=client_id,
            read_status='unread'
        ).select_related('message', 'message__sender')
        
        messages = []
        for recipient in unread_recipients:
            messages.append({
                'recipient_id': recipient.id,
                'message_id': recipient.message.id,
                'subject': recipient.message.subject,
                'body': recipient.message.body,
                'sender': recipient.message.sender.username,
                'sent_at': recipient.message.sent_at.isoformat() if recipient.message.sent_at else None,
                'has_attachment': bool(recipient.message.attachment)
            })
        
        return messages
