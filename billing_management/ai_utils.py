"""
AI統合ユーティリティ（リファクタリング版）

新しいAI抽象化レイヤーを使用して、プロバイダーに依存しない実装を提供します。
既存のAPIとの互換性を維持しながら、将来のAGI統合に対応しています。
"""

import json
import re
from typing import Dict, Any, Optional

from .ai import get_ai_provider
from .ai.prompts import PromptManager
from .ai.logger import AILogger


def analyze_sentiment(assessment, user=None, location=None) -> Dict[str, Any]:
    """
    進捗記録の感情分析と品質評価
    
    Args:
        assessment: ProgressAssessment object
        user: ユーザー（ログ記録用）
        location: 事業所（ログ記録用）
        
    Returns:
        dict: 分析結果
            {
                'sentiment_score': float,
                'record_quality_score': int,
                'keywords': str,
                'feedback': str
            }
    """
    # AIプロバイダーを取得
    ai_provider = get_ai_provider()
    
    # プロンプトを取得してフォーマット
    system_prompt, user_prompt = PromptManager.format_prompt(
        'sentiment_analysis',
        client_name=assessment.client.full_name,
        assessment_date=assessment.assessment_date,
        progress_score=assessment.progress_score,
        comment=assessment.specialist_comment
    )
    
    # 入力データ（ログ記録用）
    input_data = {
        'client_id': assessment.client.id,
        'assessment_id': assessment.id,
        'client_name': assessment.client.full_name,
        'comment_length': len(assessment.specialist_comment)
    }
    
    # AI応答をログ記録しながら実行
    with AILogger.track_request(
        'sentiment_analysis',
        input_data,
        user=user or getattr(assessment, 'created_by', None),
        location=location or assessment.client.location
    ) as tracker:
        # AI生成
        response = ai_provider.generate_text(
            user_prompt,
            system_prompt=system_prompt,
            temperature=0.3
        )
        
        # ログに記録
        tracker.set_response(response)
    
    # JSONのパース
    try:
        # レスポンスからJSONを抽出
        json_match = re.search(r'\{[^}]+\}', response.text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = json.loads(response.text)
        
        return result
    except json.JSONDecodeError:
        # パースに失敗した場合はデフォルト値を返す
        return {
            'sentiment_score': 0.0,
            'record_quality_score': 3,
            'keywords': '',
            'feedback': 'AI応答のパースに失敗しました'
        }


def generate_progress_record(
    client,
    user_input: str,
    plan_context: str,
    user=None,
    location=None
) -> str:
    """
    進捗記録の自動生成
    
    Args:
        client: Client object
        user_input: 職員の簡単な入力
        plan_context: 個別支援計画のコンテキスト
        user: ユーザー（ログ記録用）
        location: 事業所（ログ記録用）
        
    Returns:
        str: 生成された進捗記録
    """
    # AIプロバイダーを取得
    ai_provider = get_ai_provider()
    
    # プロンプトを取得してフォーマット
    system_prompt, user_prompt = PromptManager.format_prompt(
        'progress_record_generation',
        client_name=client.full_name,
        date=client.created_at.strftime('%Y年%m月%d日'),
        memo=f"{plan_context}\n\n{user_input}"
    )
    
    # 入力データ（ログ記録用）
    input_data = {
        'client_id': client.id,
        'client_name': client.full_name,
        'user_input_length': len(user_input),
        'plan_context_length': len(plan_context)
    }
    
    # AI応答をログ記録しながら実行
    with AILogger.track_request(
        'progress_record_generation',
        input_data,
        user=user,
        location=location or client.location
    ) as tracker:
        # AI生成
        response = ai_provider.generate_text(
            user_prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=500
        )
        
        # ログに記録
        tracker.set_response(response)
    
    return response.text.strip()


def predict_churn_risk(
    client_data: Dict[str, Any],
    user=None,
    location=None
) -> Dict[str, Any]:
    """
    離脱リスク予測
    
    Args:
        client_data: 利用者データ
        user: ユーザー（ログ記録用）
        location: 事業所（ログ記録用）
        
    Returns:
        dict: 予測結果
            {
                'risk_score': float,
                'risk_level': str,
                'risk_factors': list,
                'recommendations': list
            }
    """
    # AIプロバイダーを取得
    ai_provider = get_ai_provider()
    
    # プロンプトを取得してフォーマット
    system_prompt, user_prompt = PromptManager.format_prompt(
        'churn_risk_prediction',
        client_name=client_data.get('name', '不明'),
        start_date=client_data.get('start_date', '不明'),
        last_visit_date=client_data.get('last_visit_date', '不明'),
        visit_frequency=client_data.get('visit_frequency', '不明'),
        avg_progress_score=client_data.get('avg_progress_score', '不明'),
        recent_comments=client_data.get('recent_comments', 'なし')
    )
    
    # 入力データ（ログ記録用）
    input_data = {
        'client_id': client_data.get('id'),
        'client_name': client_data.get('name'),
        'data_keys': list(client_data.keys())
    }
    
    # AI応答をログ記録しながら実行
    with AILogger.track_request(
        'churn_risk_prediction',
        input_data,
        user=user,
        location=location
    ) as tracker:
        # AI生成
        response = ai_provider.generate_text(
            user_prompt,
            system_prompt=system_prompt,
            temperature=0.3
        )
        
        # ログに記録
        tracker.set_response(response)
    
    # JSONのパース
    try:
        # レスポンスからJSONを抽出
        json_match = re.search(r'\{[^}]+\}', response.text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
        else:
            result = json.loads(response.text)
        
        return result
    except json.JSONDecodeError:
        # パースに失敗した場合はデフォルト値を返す
        return {
            'risk_score': 0.5,
            'risk_level': 'medium',
            'risk_factors': ['データ不足により正確な予測ができません'],
            'recommendations': ['より詳細なデータを収集してください']
        }


# 後方互換性のための関数（非推奨）
def initialize_gemini():
    """
    非推奨: 後方互換性のために残されています
    
    新しいコードでは get_ai_provider() を使用してください
    """
    import warnings
    warnings.warn(
        "initialize_gemini() は非推奨です。get_ai_provider() を使用してください。",
        DeprecationWarning,
        stacklevel=2
    )
    return get_ai_provider()
