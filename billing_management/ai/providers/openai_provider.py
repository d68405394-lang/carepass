"""
OpenAI プロバイダー実装
"""

import os
import json
from typing import Dict, Any, Optional

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from ..base import AIProvider, AIResponse


class OpenAIProvider(AIProvider):
    """OpenAI (GPT) プロバイダー"""
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAIプロバイダーを使用するには、openaiパッケージが必要です。\n"
                "pip install openai でインストールしてください。"
            )
        
        super().__init__(api_key, **kwargs)
        
        # APIキーの取得
        if self.api_key is None:
            self.api_key = os.environ.get('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "OpenAI APIキーが設定されていません。"
                "環境変数 OPENAI_API_KEY を設定してください。"
            )
        
        # OpenAI クライアントの初期化
        self.client = OpenAI(api_key=self.api_key)
    
    @property
    def provider_name(self) -> str:
        return "openai"
    
    @property
    def default_model(self) -> str:
        return "gpt-4.1-mini"
    
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
        
        # メッセージの構築
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # API呼び出し
        completion_kwargs = {
            'model': model,
            'messages': messages,
            'temperature': temperature,
        }
        if max_tokens:
            completion_kwargs['max_tokens'] = max_tokens
        
        response = self.client.chat.completions.create(**completion_kwargs)
        
        # トークン数とコストの取得
        tokens_used = response.usage.total_tokens if response.usage else None
        
        return AIResponse(
            text=response.choices[0].message.content,
            provider=self.provider_name,
            model=model,
            tokens_used=tokens_used,
            cost=self.estimate_cost(tokens_used, model) if tokens_used else None,
            metadata={
                'finish_reason': response.choices[0].finish_reason,
                'prompt_tokens': response.usage.prompt_tokens if response.usage else None,
                'completion_tokens': response.usage.completion_tokens if response.usage else None,
            }
        )
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """感情分析"""
        system_prompt = """
あなたは感情分析の専門家です。
テキストの感情を分析し、以下のJSON形式で回答してください：

{
    "sentiment": "positive" または "negative" または "neutral",
    "score": -1.0から1.0の数値（ポジティブ=1.0、ネガティブ=-1.0、ニュートラル=0.0）,
    "confidence": 0.0から1.0の信頼度
}

JSON形式のみで回答してください。
"""
        
        prompt = f"以下のテキストの感情を分析してください：\n\n{text}"
        
        response = self.generate_text(
            prompt,
            system_prompt=system_prompt,
            temperature=0.3
        )
        
        # JSONのパース
        try:
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
        """画像分析（GPT-4 Vision対応）"""
        import base64
        
        # 画像をBase64エンコード
        with open(image_path, 'rb') as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # GPT-4 Visionモデルを使用
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        return AIResponse(
            text=response.choices[0].message.content,
            provider=self.provider_name,
            model="gpt-4-vision-preview",
            tokens_used=response.usage.total_tokens if response.usage else None,
            metadata={'image_path': image_path}
        )
    
    def estimate_cost(self, tokens: int, model: Optional[str] = None) -> float:
        """
        コスト見積もり（OpenAI の料金体系に基づく）
        
        GPT-4.1-mini:
        - Input: $0.15 / 1M tokens
        - Output: $0.60 / 1M tokens
        
        簡易計算のため、平均値を使用
        """
        if model is None:
            model = self.default_model
        
        # モデルごとのコスト（平均値）
        cost_map = {
            'gpt-4.1-mini': 0.375,  # (0.15 + 0.60) / 2
            'gpt-4.1-nano': 0.15,   # より安価なモデル
            'gpt-4': 15.0,          # GPT-4（高額）
        }
        
        # モデル名からコストを取得
        cost_per_million = cost_map.get(model, 1.0)
        
        return (tokens / 1_000_000) * cost_per_million
