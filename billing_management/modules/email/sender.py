"""
メール送信ロジック
"""
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from django.utils import timezone
from django.conf import settings
import base64


class EmailSender:
    """メール送信クラス"""
    
    def __init__(self):
        """SendGrid APIクライアントを初期化"""
        self.api_key = os.environ.get('SENDGRID_API_KEY')
        if not self.api_key:
            raise ValueError("SENDGRID_API_KEY environment variable is not set")
        self.client = SendGridAPIClient(self.api_key)
        self.from_email = settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@carepass.com'
    
    def send_individual_email(self, to_email, subject, body, attachment_path=None):
        """
        個別メールを送信
        
        Args:
            to_email (str): 送信先メールアドレス
            subject (str): 件名
            body (str): 本文
            attachment_path (str, optional): 添付ファイルのパス
        
        Returns:
            dict: 送信結果
        """
        try:
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=subject,
                html_content=body
            )
            
            # 添付ファイルがある場合
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as f:
                    data = f.read()
                encoded_file = base64.b64encode(data).decode()
                
                attached_file = Attachment(
                    FileContent(encoded_file),
                    FileName(os.path.basename(attachment_path)),
                    FileType('application/octet-stream'),
                    Disposition('attachment')
                )
                message.attachment = attached_file
            
            response = self.client.send(message)
            
            return {
                'success': True,
                'status_code': response.status_code,
                'message': '送信成功'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': '送信失敗'
            }
    
    def send_bulk_email(self, to_emails, subject, body, attachment_path=None):
        """
        一斉メールを送信（BCC使用）
        
        Args:
            to_emails (list): 送信先メールアドレスのリスト
            subject (str): 件名
            body (str): 本文
            attachment_path (str, optional): 添付ファイルのパス
        
        Returns:
            dict: 送信結果
        """
        success_count = 0
        failed_count = 0
        errors = []
        
        # BCCで一斉送信（プライバシー保護）
        # SendGridでは、一度に複数の宛先に送信する場合、各宛先に個別に送信することを推奨
        for to_email in to_emails:
            result = self.send_individual_email(to_email, subject, body, attachment_path)
            if result['success']:
                success_count += 1
            else:
                failed_count += 1
                errors.append({
                    'email': to_email,
                    'error': result['error']
                })
        
        return {
            'success': failed_count == 0,
            'success_count': success_count,
            'failed_count': failed_count,
            'errors': errors,
            'message': f'送信完了: 成功 {success_count}件, 失敗 {failed_count}件'
        }
    
    def send_notification(self, to_email, notification_type, data):
        """
        通知メールを送信（テンプレート使用）
        
        Args:
            to_email (str): 送信先メールアドレス
            notification_type (str): 通知タイプ
            data (dict): テンプレートに渡すデータ
        
        Returns:
            dict: 送信結果
        """
        templates = {
            'badge_earned': {
                'subject': '【Care-pass】バッジを獲得しました！',
                'body': '''
                    <h2>おめでとうございます！</h2>
                    <p>{child_name}さんが新しいバッジを獲得しました。</p>
                    <p><strong>バッジ名:</strong> {badge_name}</p>
                    <p><strong>獲得日:</strong> {earned_date}</p>
                    <p>Care-passをご利用いただき、ありがとうございます。</p>
                '''
            },
            'signature_request': {
                'subject': '【Care-pass】電子サインのお願い',
                'body': '''
                    <h2>電子サインのお願い</h2>
                    <p>{child_name}さんの{document_name}への電子サインをお願いいたします。</p>
                    <p>以下のリンクからサインページにアクセスしてください。</p>
                    <p><a href="{signature_url}">サインページへ</a></p>
                '''
            },
            'ai_report': {
                'subject': '【Care-pass】AI分析レポート',
                'body': '''
                    <h2>AI分析レポート</h2>
                    <p>{child_name}さんの{report_period}のAI分析レポートが完成しました。</p>
                    <p><strong>感情分析:</strong> {sentiment_summary}</p>
                    <p><strong>離脱リスク:</strong> {risk_level}</p>
                    <p>詳細はCare-passにログインしてご確認ください。</p>
                '''
            },
        }
        
        if notification_type not in templates:
            return {
                'success': False,
                'error': f'Unknown notification type: {notification_type}',
                'message': '送信失敗'
            }
        
        template = templates[notification_type]
        subject = template['subject']
        body = template['body'].format(**data)
        
        return self.send_individual_email(to_email, subject, body)
