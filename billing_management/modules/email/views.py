"""
メール機能のAPIビュー
"""
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import json

from .models import EmailMessage, EmailRecipient
from .sender import EmailSender
from .tracker import EmailTracker
from billing_management.models import Client


@method_decorator(csrf_exempt, name='dispatch')
class SendEmailView(View):
    """メール送信API"""
    
    def post(self, request):
        """メールを送信"""
        try:
            data = json.loads(request.body)
            
            # 必須フィールドの確認
            subject = data.get('subject')
            body = data.get('body')
            message_type = data.get('message_type', 'individual')
            client_ids = data.get('client_ids', [])
            
            if not subject or not body:
                return JsonResponse({
                    'success': False,
                    'error': '件名と本文は必須です'
                }, status=400)
            
            if not client_ids:
                return JsonResponse({
                    'success': False,
                    'error': '送信先を選択してください'
                }, status=400)
            
            # メールメッセージを作成
            # Note: 本番環境ではrequest.userを使用
            from django.contrib.auth.models import User
            sender = User.objects.first()  # テスト用
            
            email_message = EmailMessage.objects.create(
                sender=sender,
                subject=subject,
                body=body,
                message_type=message_type,
                status='draft'
            )
            
            # 受信者を取得
            clients = Client.objects.filter(id__in=client_ids)
            
            if not clients.exists():
                return JsonResponse({
                    'success': False,
                    'error': '有効な送信先が見つかりません'
                }, status=400)
            
            # メール送信
            sender_instance = EmailSender()
            to_emails = []
            
            for client in clients:
                # 保護者のメールアドレスを取得（guardian_emailフィールドがあると仮定）
                # 実際のフィールド名に応じて調整が必要
                guardian_email = getattr(client, 'guardian_email', None)
                
                if not guardian_email:
                    # メールアドレスがない場合はスキップ
                    continue
                
                # 受信者レコードを作成
                EmailRecipient.objects.create(
                    message=email_message,
                    client=client,
                    guardian_email=guardian_email,
                    read_status='unread'
                )
                
                to_emails.append(guardian_email)
            
            if not to_emails:
                return JsonResponse({
                    'success': False,
                    'error': '有効なメールアドレスが見つかりません'
                }, status=400)
            
            # メール送信
            if message_type == 'individual' and len(to_emails) == 1:
                result = sender_instance.send_individual_email(
                    to_emails[0],
                    subject,
                    body
                )
            else:
                result = sender_instance.send_bulk_email(
                    to_emails,
                    subject,
                    body
                )
            
            if result['success']:
                email_message.status = 'sent'
                email_message.sent_at = timezone.now()
                email_message.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'メールを送信しました',
                    'message_id': email_message.id,
                    'sent_count': result.get('success_count', 1)
                })
            else:
                email_message.status = 'failed'
                email_message.save()
                
                return JsonResponse({
                    'success': False,
                    'error': result.get('error', '送信に失敗しました')
                }, status=500)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class MarkAsReadView(View):
    """メール既読API"""
    
    def post(self, request, recipient_id):
        """メールを既読にする"""
        try:
            result = EmailTracker.mark_as_read(recipient_id)
            
            if result['success']:
                return JsonResponse(result)
            else:
                return JsonResponse(result, status=404)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ReadStatusView(View):
    """メール既読状況API"""
    
    def get(self, request, message_id):
        """メッセージの既読状況を取得"""
        try:
            status = EmailTracker.get_read_status(message_id)
            return JsonResponse({
                'success': True,
                'data': status
            })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class UnreadMessagesView(View):
    """未読メッセージ取得API"""
    
    def get(self, request, client_id):
        """利用者の未読メッセージを取得"""
        try:
            messages = EmailTracker.get_unread_messages(client_id)
            return JsonResponse({
                'success': True,
                'count': len(messages),
                'messages': messages
            })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class MessageHistoryView(View):
    """メッセージ履歴API"""
    
    def get(self, request):
        """メッセージ履歴を取得"""
        try:
            messages = EmailMessage.objects.filter(status='sent').order_by('-sent_at')[:50]
            
            message_list = []
            for message in messages:
                recipients_count = message.recipients.count()
                read_count = message.recipients.filter(read_status='read').count()
                
                message_list.append({
                    'id': message.id,
                    'subject': message.subject,
                    'body': message.body[:100] + '...' if len(message.body) > 100 else message.body,
                    'message_type': message.message_type,
                    'sender': message.sender.username,
                    'sent_at': message.sent_at.isoformat() if message.sent_at else None,
                    'recipients_count': recipients_count,
                    'read_count': read_count,
                    'read_rate': round((read_count / recipients_count * 100), 2) if recipients_count > 0 else 0
                })
            
            return JsonResponse({
                'success': True,
                'count': len(message_list),
                'messages': message_list
            })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
