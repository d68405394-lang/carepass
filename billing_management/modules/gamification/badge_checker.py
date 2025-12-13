"""
バッジ獲得判定ロジック
"""
from django.utils import timezone
from datetime import timedelta
from .models import Badge, ClientBadge, ClientPoints
from billing_management.models import Client, WorkRecord
from billing_management.modules.email.sender import EmailSender


class BadgeChecker:
    """バッジ獲得判定クラス"""
    
    @staticmethod
    def check_and_award_badges(client_id):
        """
        利用者のバッジ獲得条件をチェックし、条件を満たしていれば授与
        
        Args:
            client_id (int): 利用者ID
        
        Returns:
            list: 新規獲得したバッジのリスト
        """
        client = Client.objects.get(id=client_id)
        newly_earned_badges = []
        
        # すべてのバッジをチェック
        badges = Badge.objects.all()
        
        for badge in badges:
            # すでに獲得済みかチェック
            if ClientBadge.objects.filter(client=client, badge=badge).exists():
                continue
            
            # 条件をチェック
            if BadgeChecker._check_badge_condition(client, badge):
                # バッジを授与
                client_badge = ClientBadge.objects.create(
                    client=client,
                    badge=badge
                )
                newly_earned_badges.append(badge)
                
                # メール通知を送信
                BadgeChecker._send_badge_notification(client, badge)
        
        return newly_earned_badges
    
    @staticmethod
    def _check_badge_condition(client, badge):
        """
        バッジの獲得条件をチェック
        
        Args:
            client (Client): 利用者
            badge (Badge): バッジ
        
        Returns:
            bool: 条件を満たしているかどうか
        """
        condition_type = badge.condition_type
        condition_value = badge.condition_value
        
        if condition_type == 'consecutive_attendance':
            # 連続出席日数
            return BadgeChecker._check_consecutive_attendance(client, condition_value)
        
        elif condition_type == 'total_attendance':
            # 累計出席日数
            return BadgeChecker._check_total_attendance(client, condition_value)
        
        elif condition_type == 'signature_count':
            # 電子サイン回数
            return BadgeChecker._check_signature_count(client, condition_value)
        
        elif condition_type == 'activity_participation':
            # 活動参加回数
            return BadgeChecker._check_activity_participation(client, condition_value)
        
        else:
            return False
    
    @staticmethod
    def _check_consecutive_attendance(client, required_days):
        """連続出席日数をチェック"""
        # 過去の出席記録を取得
        today = timezone.now().date()
        consecutive_days = 0
        
        for i in range(365):  # 最大365日前まで遡る
            check_date = today - timedelta(days=i)
            
            # その日の出席記録があるかチェック
            if WorkRecord.objects.filter(
                client=client,
                work_date=check_date
            ).exists():
                consecutive_days += 1
            else:
                break
        
        return consecutive_days >= required_days
    
    @staticmethod
    def _check_total_attendance(client, required_days):
        """累計出席日数をチェック"""
        total_days = WorkRecord.objects.filter(client=client).values('work_date').distinct().count()
        return total_days >= required_days
    
    @staticmethod
    def _check_signature_count(client, required_count):
        """電子サイン回数をチェック"""
        # signature_dateがNULLでないレコードをカウント
        signature_count = 1 if client.signature_date else 0
        return signature_count >= required_count
    
    @staticmethod
    def _check_activity_participation(client, required_count):
        """活動参加回数をチェック"""
        # ActivityLogがあればチェック（保護者ポータルの活動記録）
        try:
            from billing_management.modules.portal.models import ActivityLog
            activity_count = ActivityLog.objects.filter(client=client).count()
            return activity_count >= required_count
        except:
            return False
    
    @staticmethod
    def _send_badge_notification(client, badge):
        """バッジ獲得通知を送信"""
        if not client.guardian_email:
            return
        
        try:
            sender = EmailSender()
            sender.send_notification(
                to_email=client.guardian_email,
                notification_type='badge_earned',
                data={
                    'child_name': client.full_name,
                    'badge_name': badge.name,
                    'earned_date': timezone.now().strftime('%Y年%m月%d日')
                }
            )
        except Exception as e:
            print(f"Error sending badge notification: {e}")
    
    @staticmethod
    def award_points(client_id, points, category='activity'):
        """
        ポイントを付与
        
        Args:
            client_id (int): 利用者ID
            points (int): 付与するポイント
            category (str): カテゴリ（'attendance', 'activity', 'growth'）
        """
        client = Client.objects.get(id=client_id)
        
        # ポイントレコードを取得または作成
        client_points, created = ClientPoints.objects.get_or_create(
            client=client,
            defaults={
                'total_points': 0,
                'attendance_points': 0,
                'activity_points': 0,
                'growth_points': 0
            }
        )
        
        # ポイントを加算
        client_points.total_points += points
        
        if category == 'attendance':
            client_points.attendance_points += points
        elif category == 'activity':
            client_points.activity_points += points
        elif category == 'growth':
            client_points.growth_points += points
        
        client_points.save()
        
        return client_points
