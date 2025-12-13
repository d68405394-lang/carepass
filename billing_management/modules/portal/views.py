"""
保護者向けポータルのAPIビュー
"""
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
import json

from .models import GuardianUser, ActivityLog
from billing_management.models import Client, ProgressAssessment
from billing_management.modules.email.models import EmailRecipient


@method_decorator(csrf_exempt, name='dispatch')
class GuardianLoginView(View):
    """保護者ログインAPI"""
    
    def post(self, request):
        """保護者ログイン"""
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return JsonResponse({
                    'success': False,
                    'error': 'メールアドレスとパスワードを入力してください'
                }, status=400)
            
            # ユーザー名としてメールアドレスを使用
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                # 保護者ユーザーかどうか確認
                try:
                    guardian = GuardianUser.objects.get(user=user)
                    login(request, user)
                    
                    # 最終ログイン日時を更新
                    guardian.last_login_at = timezone.now()
                    guardian.save()
                    
                    return JsonResponse({
                        'success': True,
                        'message': 'ログインしました',
                        'guardian_id': guardian.id,
                        'client_id': guardian.client.id,
                        'client_name': guardian.client.full_name
                    })
                except GuardianUser.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': '保護者アカウントが見つかりません'
                    }, status=403)
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'メールアドレスまたはパスワードが正しくありません'
                }, status=401)
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class GuardianLogoutView(View):
    """保護者ログアウトAPI"""
    
    def post(self, request):
        """保護者ログアウト"""
        try:
            logout(request)
            return JsonResponse({
                'success': True,
                'message': 'ログアウトしました'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ActivityLogView(View):
    """活動記録取得API"""
    
    def get(self, request, client_id):
        """利用者の活動記録を取得"""
        try:
            # 公開設定されている活動記録のみ取得
            logs = ActivityLog.objects.filter(
                client_id=client_id,
                is_published=True
            ).order_by('-date')[:30]  # 最新30件
            
            log_list = []
            for log in logs:
                log_list.append({
                    'id': log.id,
                    'date': log.date.isoformat(),
                    'activity_type': log.activity_type,
                    'description': log.description,
                    'staff_comment': log.staff_comment,
                    'has_photo': bool(log.photo),
                    'photo_url': log.photo.url if log.photo else None
                })
            
            return JsonResponse({
                'success': True,
                'count': len(log_list),
                'logs': log_list
            })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class GuardianDashboardView(View):
    """保護者ダッシュボードAPI"""
    
    def get(self, request, client_id):
        """保護者ダッシュボード情報を取得"""
        try:
            client = Client.objects.get(id=client_id)
            
            # 未読メッセージ数
            unread_messages = EmailRecipient.objects.filter(
                client_id=client_id,
                read_status='unread'
            ).count()
            
            # 最新の活動記録
            latest_activities = ActivityLog.objects.filter(
                client_id=client_id,
                is_published=True
            ).order_by('-date')[:5]
            
            activities = []
            for activity in latest_activities:
                activities.append({
                    'id': activity.id,
                    'date': activity.date.isoformat(),
                    'activity_type': activity.activity_type,
                    'description': activity.description[:100] + '...' if len(activity.description) > 100 else activity.description
                })
            
            # 最新のAI分析結果
            latest_assessment = ProgressAssessment.objects.filter(
                client_id=client_id
            ).order_by('-assessment_date').first()
            
            ai_analysis = None
            if latest_assessment and latest_assessment.ai_analysis_result:
                ai_analysis = {
                    'date': latest_assessment.assessment_date.isoformat(),
                    'sentiment': latest_assessment.ai_analysis_result.get('sentiment', 'N/A'),
                    'summary': latest_assessment.ai_analysis_result.get('summary', '')
                }
            
            return JsonResponse({
                'success': True,
                'data': {
                    'client_name': client.full_name,
                    'unread_messages': unread_messages,
                    'latest_activities': activities,
                    'ai_analysis': ai_analysis
                }
            })
        
        except Client.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': '利用者が見つかりません'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
