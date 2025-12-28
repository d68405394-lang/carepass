"""
Anthropic (Claude) プロバイダー実装（スタブ）

将来的にAnthropicのClaudeを使用する場合のために準備されたスタブです。
実装が必要になった際に、このファイルを完成させてください。
"""

import os
from typing import Dict, Any, Optional

from ..base import AIProvider, AIResponse


class AnthropicProvider(AIProvider):
    """Anthropic (Claude) プロバイダー（未実装）"""
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        
        raise NotImplementedError(
            "Anthropicプロバイダーはまだ実装されていません。\n"
            "実装が必要な場合は、anthropicパッケージをインストールし、\n"
            "このファイルを完成させてください。\n\n"
            "参考: pip install anthropic"
        )
    
    @property
    def provider_name(self) -> str:
        return "anthropic"
    
    @property
    def default_model(self) -> str:
        return "claude-3-sonnet-20240229"
    
    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AIResponse:
        raise NotImplementedError("Anthropicプロバイダーは未実装です")
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        raise NotImplementedError("Anthropicプロバイダーは未実装です")
