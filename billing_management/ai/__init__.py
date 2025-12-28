"""
AI抽象化レイヤー

このモジュールは、複数のAIプロバイダー（Google AI、OpenAI、Anthropic等）を
統一されたインターフェースで利用できるようにする抽象化レイヤーを提供します。

将来的なAGI統合に向けて、プロバイダーに依存しない設計を実現しています。
"""

from .factory import get_ai_provider
from .base import AIProvider

__all__ = ['get_ai_provider', 'AIProvider']
