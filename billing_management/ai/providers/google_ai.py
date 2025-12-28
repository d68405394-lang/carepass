"""
Google AI (Gemini) プロバイダー実装
"""

import os
import json
import re
from typing import Dict, Any, Optional
import google.generativeai as genai

from ..base import AIProvider, AIResponse


class GoogleAIProvider(AIProvider):
    """Google AI (Gemini) プロバイダー"""
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        
        # APIキーの取得
        if self.api_key is None:
            self.api_key = os.environ.get('GOOGLE_AI_API_KEY') or os.environ.get('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Google AI APIキーが設定されていません。"
                "環境変数 GOOGLE_AI_API_KEY または GEMINI_API_KEY を設定してください。"
            )
        
        # Google AI の初期化
        genai.configure(api_key=self.api_key)
    
    @property
    def provider_name(self) -> str:
        return "google"
    
    @property
    def default_model(self) -> str:
        return "gemini-1.5-flash"
    
    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AIResponse:
        """テキスト生成"""
        if model is None:
            model = self.default_model
        
        # モデルの初期化
        generation_config = {
            'temperature': temperature,
        }
        if max_tokens:
            generation_config['max_output_tokens'] = max_tokens
        
        gemini_model = genai.GenerativeModel(
            model,
            generation_config=generation_config
        )
        
        # プロンプトの構築
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        # 生成
        response = gemini_model.generate_content(full_prompt)
        
        # トークン数の取得（利用可能な場合）
        tokens_used = None
        if hasattr(response, 'usage_metadata'):
            tokens_used = (
                response.usage_metadata.prompt_token_count +
                response.usage_metadata.candidates_token_count
            )
        
        return AIResponse(
            text=response.text,
            provider=self.provider_name,
            model=model,
            tokens_used=tokens_used,
            cost=self.estimate_cost(tokens_used or 0, model) if tokens_used else None,
            metadata={
                'finish_reason': response.candidates[0].finish_reason if response.candidates else None,
            }
        )
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """感情分析"""
        prompt = f"""
以下のテキストの感情を分析してください。

【テキスト】
{text}

以下の形式でJSON形式で回答してください：
{{
    "sentiment": "positive" または "negative" または "neutral",
    "score": -1.0から1.0の数値（ポジティブ=1.0、ネガティブ=-1.0、ニュートラル=0.0）,
    "confidence": 0.0から1.0の信頼度
}}

JSON形式のみで回答してください。
"""
        
        response = self.generate_text(prompt, temperature=0.3)
        
        # JSONの抽出
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
                'sentiment': 'neutral',
                'score': 0.0,
                'confidence': 0.0
            }
    
    def analyze_image(self, image_path: str, prompt: str) -> AIResponse:
        """画像分析（Gemini Vision対応）"""
        from PIL import Image
        
        # 画像の読み込み
        image = Image.open(image_path)
        
        # Gemini Pro Visionモデルを使用
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 画像とプロンプトを送信
        response = model.generate_content([prompt, image])
        
        return AIResponse(
            text=response.text,
            provider=self.provider_name,
            model='gemini-1.5-flash',
            metadata={'image_path': image_path}
        )
    
    def estimate_cost(self, tokens: int, model: Optional[str] = None) -> float:
        """
        コスト見積もり（Google AI の料金体系に基づく）
        
        Gemini 1.5 Flash:
        - Input: $0.075 / 1M tokens
        - Output: $0.30 / 1M tokens
        
        簡易計算のため、平均値を使用
        """
        if model is None:
            model = self.default_model
        
        # Gemini 1.5 Flash の平均コスト
        if 'flash' in model.lower():
            cost_per_million = 0.1875  # (0.075 + 0.30) / 2
        else:
            # その他のモデルは高めに見積もる
            cost_per_million = 0.5
        
        return (tokens / 1_000_000) * cost_per_million
