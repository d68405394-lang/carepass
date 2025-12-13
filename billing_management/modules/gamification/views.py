"""
ゲーミフィケーションのAPIビュー
"""
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .models import Badge, ClientBadge, ClientPoints
from .badge_checker import BadgeChecker
from billing_management.models import Client


@method_decorator(csrf_exempt, name='dispatch')
class ClientBadgesView(View):
    """利用者のバッジ取得API"""
    
    def get(self, request, client_id):
        """利用者が獲得したバッジを取得"""
        try:
            client = Client.objects.get(id=client_id)
            earned_badges = ClientBadge.objects.filter(client=client).select_related('badge')
            
            badges = []
            for client_badge in earned_badges:
                badges.append({
                    'id': client_badge.badge.id,
                    'name': client_badge.badge.name,
                    'description': client_badge.badge.description,
                    'category': client_badge.badge.category,
                    'icon': client_badge.badge.icon,
                    'earned_at': client_badge.earned_at.isoformat()
                })
            
            return JsonResponse({
                'success': True,
                'count': len(badges),
                'badges': badges
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


@method_decorator(csrf_exempt, name='dispatch')
class CheckBadgesView(View):
    """バッジ獲得チェックAPI"""
    
    def post(self, request, client_id):
        """利用者のバッジ獲得条件をチェック"""
        try:
            newly_earned = BadgeChecker.check_and_award_badges(client_id)
            
            badges = []
            for badge in newly_earned:
                badges.append({
                    'id': badge.id,
                    'name': badge.name,
                    'description': badge.description,
                    'icon': badge.icon
                })
            
            return JsonResponse({
                'success': True,
                'newly_earned_count': len(badges),
                'newly_earned_badges': badges
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


@method_decorator(csrf_exempt, name='dispatch')
class ClientPointsView(View):
    """利用者のポイント取得API"""
    
    def get(self, request, client_id):
        """利用者のポイントを取得"""
        try:
            client = Client.objects.get(id=client_id)
            
            try:
                points = ClientPoints.objects.get(client=client)
                return JsonResponse({
                    'success': True,
                    'data': {
                        'total_points': points.total_points,
                        'attendance_points': points.attendance_points,
                        'activity_points': points.activity_points,
                        'growth_points': points.growth_points
                    }
                })
            except ClientPoints.DoesNotExist:
                return JsonResponse({
                    'success': True,
                    'data': {
                        'total_points': 0,
                        'attendance_points': 0,
                        'activity_points': 0,
                        'growth_points': 0
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


@method_decorator(csrf_exempt, name='dispatch')
class AwardPointsView(View):
    """ポイント付与API"""
    
    def post(self, request, client_id):
        """利用者にポイントを付与"""
        try:
            data = json.loads(request.body)
            points = data.get('points', 0)
            category = data.get('category', 'activity')
            
            if points <= 0:
                return JsonResponse({
                    'success': False,
                    'error': 'ポイントは1以上を指定してください'
                }, status=400)
            
            client_points = BadgeChecker.award_points(client_id, points, category)
            
            return JsonResponse({
                'success': True,
                'message': f'{points}ポイントを付与しました',
                'data': {
                    'total_points': client_points.total_points,
                    'attendance_points': client_points.attendance_points,
                    'activity_points': client_points.activity_points,
                    'growth_points': client_points.growth_points
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


@method_decorator(csrf_exempt, name='dispatch')
class LeaderboardView(View):
    """ランキング取得API"""
    
    def get(self, request):
        """ポイントランキングを取得"""
        try:
            # 上位10名を取得
            top_clients = ClientPoints.objects.select_related('client').order_by('-total_points')[:10]
            
            ranking = []
            for rank, client_points in enumerate(top_clients, start=1):
                ranking.append({
                    'rank': rank,
                    'client_id': client_points.client.id,
                    'client_name': client_points.client.full_name,
                    'total_points': client_points.total_points,
                    'badge_count': ClientBadge.objects.filter(client=client_points.client).count()
                })
            
            return JsonResponse({
                'success': True,
                'ranking': ranking
            })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
