"""
プロンプト管理システム

AIプロンプトをコードから分離し、データベースまたは設定ファイルで管理します。
これにより、プロンプトのA/Bテスト、バージョン管理、動的な最適化が可能になります。
"""

from typing import Optional, Dict
from django.core.cache import cache


# デフォルトプロンプト（データベースに登録されていない場合のフォールバック）
DEFAULT_PROMPTS = {
    'sentiment_analysis': {
        'system': """
あなたは福祉事業所の専門家です。
職員による利用者の進捗記録を分析し、記録の質を評価してください。
""",
        'user_template': """
【利用者情報】
- 氏名: {client_name}
- 評価日: {assessment_date}
- 成長スコア: {progress_score} / 5.0

【職員のコメント】
{comment}

以下の項目について分析し、JSON形式で回答してください：

1. sentiment_score: 感情スコア（-1.0〜1.0、ポジティブ=1.0、ネガティブ=-1.0、ニュートラル=0.0）
2. record_quality_score: 記録の質スコア（1〜5、5が最高）
   - 具体性: 具体的な行動や状況が記録されているか
   - 客観性: 主観的な表現ではなく、客観的な観察が記録されているか
   - 専門性: 専門的な視点や用語が適切に使用されているか
3. keywords: 重要なキーワード（最大5個、カンマ区切り）
4. feedback: 改善提案（具体的なフィードバック、100文字以内）

回答例：
{{
    "sentiment_score": 0.8,
    "record_quality_score": 4,
    "keywords": "コミュニケーション向上, 積極的参加, 社会性",
    "feedback": "具体的な行動が記録されており良好です。今後は数値や頻度を追加するとより客観的になります。"
}}

JSON形式のみで回答してください。
""",
        'version': '1.0',
    },
    
    'progress_record_generation': {
        'system': """
あなたは福祉事業所の記録作成支援AIです。
職員が入力した簡単なメモから、専門的で詳細な進捗記録を生成してください。
""",
        'user_template': """
以下の情報から、利用者の進捗記録を作成してください。

【利用者情報】
- 氏名: {client_name}
- 日付: {date}

【職員のメモ】
{memo}

【要件】
- 200〜300文字程度
- 具体的な行動や状況を記述
- 客観的な表現を使用
- 専門的な視点を含める
- 今後の支援方針を示唆

進捗記録のみを出力してください（説明や前置きは不要）。
""",
        'version': '1.0',
    },
    
    'churn_risk_prediction': {
        'system': """
あなたはデータ分析の専門家です。
利用者の行動パターンから、離脱リスクを予測してください。
""",
        'user_template': """
以下の利用者データから、離脱リスクを予測してください。

【利用者情報】
- 氏名: {client_name}
- 利用開始日: {start_date}
- 最終利用日: {last_visit_date}
- 利用頻度: {visit_frequency}
- 進捗スコア平均: {avg_progress_score}
- 最近のコメント: {recent_comments}

以下の形式でJSON形式で回答してください：
{{
    "risk_level": "high" または "medium" または "low",
    "risk_score": 0.0から1.0の数値（1.0=高リスク）,
    "reasons": ["理由1", "理由2", "理由3"],
    "recommendations": ["推奨アクション1", "推奨アクション2"]
}}

JSON形式のみで回答してください。
""",
        'version': '1.0',
    },
}


class PromptManager:
    """プロンプト管理クラス"""
    
    @staticmethod
    def get_prompt(
        prompt_name: str,
        use_cache: bool = True,
        cache_ttl: int = 3600
    ) -> Optional[Dict]:
        """
        プロンプトを取得
        
        Args:
            prompt_name: プロンプト名
            use_cache: キャッシュを使用するか
            cache_ttl: キャッシュの有効期限（秒）
            
        Returns:
            Dict: プロンプト情報
                {
                    'system': システムプロンプト,
                    'user_template': ユーザープロンプトテンプレート,
                    'version': バージョン
                }
        """
        # キャッシュから取得を試みる
        if use_cache:
            cache_key = f"ai_prompt:{prompt_name}"
            cached_prompt = cache.get(cache_key)
            if cached_prompt:
                return cached_prompt
        
        # データベースから取得を試みる
        try:
            from .models import AIPrompt
            db_prompt = AIPrompt.objects.filter(
                name=prompt_name,
                is_active=True
            ).first()
            
            if db_prompt:
                prompt_data = {
                    'system': db_prompt.system_prompt,
                    'user_template': db_prompt.user_template,
                    'version': db_prompt.version,
                }
                
                # キャッシュに保存
                if use_cache:
                    cache.set(cache_key, prompt_data, cache_ttl)
                
                return prompt_data
        except Exception:
            # データベーステーブルが存在しない場合はスキップ
            pass
        
        # デフォルトプロンプトを返す
        prompt_data = DEFAULT_PROMPTS.get(prompt_name)
        
        if prompt_data and use_cache:
            cache.set(cache_key, prompt_data, cache_ttl)
        
        return prompt_data
    
    @staticmethod
    def format_prompt(
        prompt_name: str,
        **kwargs
    ) -> tuple[Optional[str], Optional[str]]:
        """
        プロンプトをフォーマット
        
        Args:
            prompt_name: プロンプト名
            **kwargs: テンプレート変数
            
        Returns:
            tuple: (system_prompt, user_prompt)
        """
        prompt_data = PromptManager.get_prompt(prompt_name)
        
        if not prompt_data:
            return None, None
        
        system_prompt = prompt_data['system'].strip()
        user_prompt = prompt_data['user_template'].format(**kwargs).strip()
        
        return system_prompt, user_prompt
    
    @staticmethod
    def clear_cache(prompt_name: Optional[str] = None):
        """
        プロンプトキャッシュをクリア
        
        Args:
            prompt_name: プロンプト名（Noneの場合は全てクリア）
        """
        if prompt_name:
            cache_key = f"ai_prompt:{prompt_name}"
            cache.delete(cache_key)
        else:
            # 全てのプロンプトキャッシュをクリア
            for name in DEFAULT_PROMPTS.keys():
                cache_key = f"ai_prompt:{name}"
                cache.delete(cache_key)
