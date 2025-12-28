"""
AIプロバイダーファクトリー

環境変数に基づいて適切なAIプロバイダーを返すファクトリー関数を提供します。
"""

import os
from typing import Optional
from .base import AIProvider


def get_ai_provider(provider: Optional[str] = None) -> AIProvider:
    """
    AIプロバイダーを取得
    
    Args:
        provider: プロバイダー名（Noneの場合は環境変数AI_PROVIDERから取得）
            - 'google': Google AI (Gemini)
            - 'openai': OpenAI (GPT)
            - 'anthropic': Anthropic (Claude)
            - 'agi': 将来のAGI
            
    Returns:
        AIProvider: AIプロバイダーインスタンス
        
    Raises:
        ValueError: サポートされていないプロバイダーが指定された場合
    """
    if provider is None:
        provider = os.getenv('AI_PROVIDER', 'google').lower()
    
    provider = provider.lower()
    
    if provider == 'google':
        from .providers.google_ai import GoogleAIProvider
        return GoogleAIProvider()
    
    elif provider == 'openai':
        from .providers.openai_provider import OpenAIProvider
        return OpenAIProvider()
    
    elif provider == 'anthropic':
        from .providers.anthropic_provider import AnthropicProvider
        return AnthropicProvider()
    
    elif provider == 'agi':
        # 将来のAGI統合用（現在は未実装）
        raise NotImplementedError(
            "AGIプロバイダーはまだ実装されていません。"
            "実装準備は完了しているため、AGIが利用可能になり次第、"
            "providers/agi_provider.pyを作成して統合できます。"
        )
    
    else:
        raise ValueError(
            f"サポートされていないAIプロバイダー: {provider}\n"
            f"利用可能なプロバイダー: google, openai, anthropic"
        )


def get_available_providers() -> list:
    """
    利用可能なAIプロバイダーのリストを返す
    
    Returns:
        list: プロバイダー名のリスト
    """
    return ['google', 'openai', 'anthropic']
