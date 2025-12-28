"""
AI応答ログ記録システム

全てのAI応答を自動的にログに記録し、コスト管理と品質評価を可能にします。
"""

import time
from typing import Optional, Dict, Any
from contextlib import contextmanager

from .base import AIResponse


class AILogger:
    """AI応答ログ記録クラス"""
    
    @staticmethod
    def log_response(
        response: AIResponse,
        task_type: str,
        input_data: Dict[str, Any],
        response_time: Optional[float] = None,
        user=None,
        location=None
    ) -> 'AILog':
        """
        AI応答をログに記録
        
        Args:
            response: AI応答
            task_type: タスクタイプ
            input_data: 入力データ
            response_time: 応答時間（秒）
            user: ユーザー
            location: 事業所
            
        Returns:
            AILog: 作成されたログオブジェクト
        """
        from .models import AILog
        
        log = AILog.objects.create(
            provider=response.provider,
            model=response.model,
            task_type=task_type,
            input_data=input_data,
            output_data={
                'text': response.text,
                'metadata': response.metadata or {}
            },
            tokens_used=response.tokens_used,
            cost=response.cost,
            response_time=response_time,
            user=user,
            location=location
        )
        
        return log
    
    @staticmethod
    @contextmanager
    def track_request(
        task_type: str,
        input_data: Dict[str, Any],
        user=None,
        location=None
    ):
        """
        AI リクエストを追跡（コンテキストマネージャー）
        
        使用例:
            with AILogger.track_request('sentiment_analysis', {...}) as tracker:
                response = ai_provider.generate_text(prompt)
                tracker.set_response(response)
        
        Args:
            task_type: タスクタイプ
            input_data: 入力データ
            user: ユーザー
            location: 事業所
        """
        start_time = time.time()
        tracker = RequestTracker()
        
        try:
            yield tracker
        finally:
            if tracker.response:
                response_time = time.time() - start_time
                AILogger.log_response(
                    tracker.response,
                    task_type,
                    input_data,
                    response_time,
                    user,
                    location
                )
    
    @staticmethod
    def get_cost_summary(
        start_date=None,
        end_date=None,
        provider=None,
        location=None
    ) -> Dict[str, Any]:
        """
        コストサマリーを取得
        
        Args:
            start_date: 開始日
            end_date: 終了日
            provider: プロバイダー
            location: 事業所
            
        Returns:
            Dict: コストサマリー
        """
        from .models import AILog
        from django.db.models import Sum, Count, Avg
        
        queryset = AILog.objects.all()
        
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        if provider:
            queryset = queryset.filter(provider=provider)
        if location:
            queryset = queryset.filter(location=location)
        
        summary = queryset.aggregate(
            total_cost=Sum('cost'),
            total_tokens=Sum('tokens_used'),
            total_requests=Count('id'),
            avg_response_time=Avg('response_time')
        )
        
        # プロバイダー別の集計
        provider_breakdown = {}
        for log in queryset.values('provider').annotate(
            cost=Sum('cost'),
            tokens=Sum('tokens_used'),
            requests=Count('id')
        ):
            provider_breakdown[log['provider']] = {
                'cost': float(log['cost'] or 0),
                'tokens': log['tokens'] or 0,
                'requests': log['requests']
            }
        
        return {
            'total_cost': float(summary['total_cost'] or 0),
            'total_tokens': summary['total_tokens'] or 0,
            'total_requests': summary['total_requests'],
            'avg_response_time': float(summary['avg_response_time'] or 0),
            'provider_breakdown': provider_breakdown
        }
    
    @staticmethod
    def get_quality_metrics(
        start_date=None,
        end_date=None,
        task_type=None
    ) -> Dict[str, Any]:
        """
        品質メトリクスを取得
        
        Args:
            start_date: 開始日
            end_date: 終了日
            task_type: タスクタイプ
            
        Returns:
            Dict: 品質メトリクス
        """
        from .models import AILog
        from django.db.models import Avg, Count, Q
        
        queryset = AILog.objects.exclude(human_rating__isnull=True)
        
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        if task_type:
            queryset = queryset.filter(task_type=task_type)
        
        metrics = queryset.aggregate(
            avg_rating=Avg('human_rating'),
            total_rated=Count('id'),
            accurate_count=Count('id', filter=Q(is_accurate=True)),
            inaccurate_count=Count('id', filter=Q(is_accurate=False))
        )
        
        total_rated = metrics['total_rated']
        accuracy_rate = 0.0
        if total_rated > 0:
            accuracy_rate = (metrics['accurate_count'] / total_rated) * 100
        
        return {
            'avg_rating': float(metrics['avg_rating'] or 0),
            'total_rated': total_rated,
            'accuracy_rate': accuracy_rate,
            'accurate_count': metrics['accurate_count'],
            'inaccurate_count': metrics['inaccurate_count']
        }


class RequestTracker:
    """リクエスト追跡ヘルパークラス"""
    
    def __init__(self):
        self.response: Optional[AIResponse] = None
    
    def set_response(self, response: AIResponse):
        """応答を設定"""
        self.response = response
