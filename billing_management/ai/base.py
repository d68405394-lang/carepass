"""
AI基底クラス

全てのAIプロバイダーが実装すべき抽象基底クラスを定義します。
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass


@dataclass
class AIResponse:
    """AI応答の標準フォーマット"""
    text: str
    provider: str
    model: str
    tokens_used: Optional[int] = None
    cost: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class AIProvider(ABC):
    """
    AIプロバイダーの抽象基底クラス
    
    全てのAIプロバイダー（Google AI、OpenAI、Anthropic等）は
    このクラスを継承して実装する必要があります。
    """
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """
        Args:
            api_key: APIキー（環境変数から取得する場合はNone）
            **kwargs: プロバイダー固有の設定
        """
        self.api_key = api_key
        self.config = kwargs
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """プロバイダー名を返す"""
        pass
    
    @property
    @abstractmethod
    def default_model(self) -> str:
        """デフォルトモデル名を返す"""
        pass
    
    @abstractmethod
    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AIResponse:
        """
        テキスト生成
        
        Args:
            prompt: ユーザープロンプト
            system_prompt: システムプロンプト
            model: 使用するモデル（Noneの場合はdefault_modelを使用）
            temperature: 生成の多様性（0.0-1.0）
            max_tokens: 最大トークン数
            **kwargs: プロバイダー固有のパラメータ
            
        Returns:
            AIResponse: AI応答
        """
        pass
    
    @abstractmethod
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        感情分析
        
        Args:
            text: 分析対象のテキスト
            
        Returns:
            Dict: 感情分析結果
                {
                    'sentiment': 'positive' | 'negative' | 'neutral',
                    'score': float,  # -1.0 to 1.0
                    'confidence': float  # 0.0 to 1.0
                }
        """
        pass
    
    def analyze_image(self, image_path: str, prompt: str) -> AIResponse:
        """
        画像分析（マルチモーダルAI対応）
        
        Args:
            image_path: 画像ファイルのパス
            prompt: 分析の指示
            
        Returns:
            AIResponse: 分析結果
            
        Raises:
            NotImplementedError: プロバイダーが画像分析に対応していない場合
        """
        raise NotImplementedError(
            f"{self.provider_name}は画像分析に対応していません"
        )
    
    def generate_speech(self, text: str) -> bytes:
        """
        音声生成（将来実装）
        
        Args:
            text: 音声化するテキスト
            
        Returns:
            bytes: 音声データ
            
        Raises:
            NotImplementedError: プロバイダーが音声生成に対応していない場合
        """
        raise NotImplementedError(
            f"{self.provider_name}は音声生成に対応していません"
        )
    
    def transcribe_audio(self, audio_path: str) -> str:
        """
        音声認識（将来実装）
        
        Args:
            audio_path: 音声ファイルのパス
            
        Returns:
            str: 認識されたテキスト
            
        Raises:
            NotImplementedError: プロバイダーが音声認識に対応していない場合
        """
        raise NotImplementedError(
            f"{self.provider_name}は音声認識に対応していません"
        )
    
    def estimate_cost(self, tokens: int, model: Optional[str] = None) -> float:
        """
        コスト見積もり
        
        Args:
            tokens: トークン数
            model: モデル名
            
        Returns:
            float: 推定コスト（USD）
        """
        # デフォルト実装（各プロバイダーでオーバーライド推奨）
        return 0.0
