# AI抽象化レイヤー実装ドキュメント

## 概要

carepassシステムに、将来のAGI統合を見据えたAI抽象化レイヤーを実装しました。これにより、AIプロバイダーに依存しない柔軟なシステム設計が実現されています。

## 実装日時

2025年12月28日

## 実装内容

### 1. AI抽象化レイヤーの設計

#### ディレクトリ構造

```
billing_management/
├── ai/
│   ├── __init__.py           # モジュール初期化
│   ├── base.py               # 抽象基底クラス
│   ├── factory.py            # プロバイダーファクトリー
│   ├── prompts.py            # プロンプト管理
│   ├── logger.py             # ログ記録
│   ├── models.py             # データベースモデル
│   └── providers/
│       ├── __init__.py
│       ├── google_ai.py      # Google AI実装
│       ├── openai_provider.py # OpenAI実装
│       └── anthropic_provider.py # Anthropic実装（スタブ）
└── ai_utils.py               # 既存APIのリファクタリング版
```

### 2. 主要コンポーネント

#### 2.1 AIProvider基底クラス

全てのAIプロバイダーが実装すべきインターフェースを定義：

```python
from billing_management.ai import get_ai_provider

# AIプロバイダーを取得（環境変数AI_PROVIDERで切り替え可能）
ai_provider = get_ai_provider()

# テキスト生成
response = ai_provider.generate_text(
    prompt="こんにちは",
    system_prompt="あなたは親切なアシスタントです",
    temperature=0.7
)

print(response.text)
print(f"使用トークン: {response.tokens_used}")
print(f"コスト: ${response.cost}")
```

#### 2.2 プロンプト管理システム

プロンプトをコードから分離し、データベースで管理：

```python
from billing_management.ai.prompts import PromptManager

# プロンプトを取得してフォーマット
system_prompt, user_prompt = PromptManager.format_prompt(
    'sentiment_analysis',
    client_name="山田太郎",
    assessment_date="2025-12-28",
    progress_score=4.5,
    comment="本日は積極的に参加していました"
)
```

#### 2.3 AI応答ログ記録

全てのAI応答を自動的にログに記録：

```python
from billing_management.ai.logger import AILogger

# コンテキストマネージャーで自動ログ記録
with AILogger.track_request('sentiment_analysis', input_data, user, location) as tracker:
    response = ai_provider.generate_text(prompt)
    tracker.set_response(response)
```

### 3. サポートするAIプロバイダー

#### 3.1 Google AI (Gemini)

- **モデル**: gemini-1.5-flash（デフォルト）
- **機能**: テキスト生成、感情分析、画像分析
- **環境変数**: `GOOGLE_AI_API_KEY` または `GEMINI_API_KEY`

#### 3.2 OpenAI (GPT)

- **モデル**: gpt-4.1-mini（デフォルト）
- **機能**: テキスト生成、感情分析、画像分析（GPT-4 Vision）
- **環境変数**: `OPENAI_API_KEY`

#### 3.3 Anthropic (Claude)

- **ステータス**: スタブ実装（将来実装用）
- **実装方法**: `billing_management/ai/providers/anthropic_provider.py`を完成させる

### 4. 環境変数設定

#### 4.1 AIプロバイダーの選択

```bash
# Google AIを使用（デフォルト）
export AI_PROVIDER=google
export GOOGLE_AI_API_KEY=your_api_key

# OpenAIを使用
export AI_PROVIDER=openai
export OPENAI_API_KEY=your_api_key

# Anthropicを使用（実装後）
export AI_PROVIDER=anthropic
export ANTHROPIC_API_KEY=your_api_key
```

#### 4.2 Renderでの設定

Renderダッシュボードで以下の環境変数を設定：

1. `AI_PROVIDER`: `google` または `openai`
2. `GOOGLE_AI_API_KEY`: Google AIのAPIキー
3. `OPENAI_API_KEY`: OpenAIのAPIキー（OpenAI使用時）

### 5. データベースモデル

#### 5.1 AIPrompt

プロンプトをデータベースで管理：

| フィールド | 型 | 説明 |
|----------|-----|------|
| name | CharField | プロンプト識別名 |
| display_name | CharField | 表示名 |
| system_prompt | TextField | システムプロンプト |
| user_template | TextField | ユーザープロンプトテンプレート |
| version | CharField | バージョン |
| is_active | BooleanField | 有効/無効 |

#### 5.2 AILog

AI応答を記録：

| フィールド | 型 | 説明 |
|----------|-----|------|
| provider | CharField | AIプロバイダー名 |
| model | CharField | モデル名 |
| task_type | CharField | タスクタイプ |
| input_data | JSONField | 入力データ |
| output_data | JSONField | 出力データ |
| tokens_used | IntegerField | 使用トークン数 |
| cost | DecimalField | コスト（USD） |
| response_time | FloatField | 応答時間（秒） |
| user | ForeignKey | ユーザー |
| location | ForeignKey | 事業所 |
| human_rating | IntegerField | 人間評価（1-5） |
| is_accurate | BooleanField | 正確性 |

### 6. 既存コードの互換性

既存の`ai_utils.py`の関数は、新しいAI抽象化レイヤーを使用するようにリファクタリングされましたが、**APIは完全に互換性を保っています**。

#### 使用例

```python
from billing_management.ai_utils import (
    analyze_sentiment,
    generate_progress_record,
    predict_churn_risk
)

# 既存コードはそのまま動作
result = analyze_sentiment(assessment, user=request.user, location=assessment.client.location)
```

### 7. コスト管理

#### 7.1 コストサマリーの取得

```python
from billing_management.ai.logger import AILogger
from datetime import datetime, timedelta

# 過去30日間のコストサマリー
start_date = datetime.now() - timedelta(days=30)
summary = AILogger.get_cost_summary(start_date=start_date)

print(f"総コスト: ${summary['total_cost']}")
print(f"総リクエスト数: {summary['total_requests']}")
print(f"平均応答時間: {summary['avg_response_time']}秒")

# プロバイダー別の内訳
for provider, stats in summary['provider_breakdown'].items():
    print(f"{provider}: ${stats['cost']} ({stats['requests']}リクエスト)")
```

#### 7.2 品質メトリクスの取得

```python
# 品質メトリクスを取得
metrics = AILogger.get_quality_metrics(start_date=start_date)

print(f"平均評価: {metrics['avg_rating']}/5")
print(f"正確性: {metrics['accuracy_rate']}%")
```

### 8. 将来のAGI統合手順

新しいAGIプロバイダーを統合する手順：

#### ステップ1: プロバイダークラスの作成

```python
# billing_management/ai/providers/agi_provider.py
from ..base import AIProvider, AIResponse

class AGIProvider(AIProvider):
    @property
    def provider_name(self) -> str:
        return "agi"
    
    @property
    def default_model(self) -> str:
        return "agi-model-v1"
    
    def generate_text(self, prompt, **kwargs) -> AIResponse:
        # AGI APIを呼び出す実装
        pass
    
    def analyze_sentiment(self, text):
        # 感情分析の実装
        pass
```

#### ステップ2: ファクトリーに登録

```python
# billing_management/ai/factory.py
def get_ai_provider(provider=None):
    # ...
    elif provider == 'agi':
        from .providers.agi_provider import AGIProvider
        return AGIProvider()
```

#### ステップ3: 環境変数を設定

```bash
export AI_PROVIDER=agi
export AGI_API_KEY=your_agi_api_key
```

**所要時間: 1〜2時間**

### 9. テスト方法

#### 9.1 ローカルテスト

```bash
cd /home/ubuntu
source venv/bin/activate

# Google AIでテスト
export AI_PROVIDER=google
export GOOGLE_AI_API_KEY=your_key
python manage.py shell

# Pythonシェルで
from billing_management.ai import get_ai_provider
ai = get_ai_provider()
response = ai.generate_text("こんにちは")
print(response.text)
```

#### 9.2 本番環境テスト

Renderで環境変数を設定後、管理画面から進捗記録のAI分析機能をテスト。

### 10. トラブルシューティング

#### 問題1: ImportError: No module named 'openai'

**解決方法**:
```bash
pip install openai
```

#### 問題2: AIプロバイダーが見つからない

**原因**: 環境変数`AI_PROVIDER`が正しく設定されていない

**解決方法**:
```bash
export AI_PROVIDER=google  # または openai
```

#### 問題3: APIキーエラー

**原因**: APIキーが設定されていない

**解決方法**:
```bash
export GOOGLE_AI_API_KEY=your_key
# または
export OPENAI_API_KEY=your_key
```

### 11. パフォーマンス最適化

#### 11.1 キャッシング

プロンプトは自動的にキャッシュされます（デフォルト: 1時間）。

#### 11.2 非同期処理（将来実装）

大量のAIリクエストを処理する場合は、Celeryを使用した非同期処理を推奨。

### 12. セキュリティ

- APIキーは環境変数で管理
- AI応答ログには個人情報の匿名化を推奨
- 本番環境では、AIプロバイダーのデータ保持ポリシーを確認

### 13. まとめ

✅ **実装完了項目**:
1. AI抽象化レイヤー（基底クラス）
2. Google AI プロバイダー
3. OpenAI プロバイダー
4. プロンプト管理システム
5. AI応答ログ記録システム
6. 既存コードのリファクタリング
7. データベースマイグレーション

✅ **メリット**:
- AIプロバイダーの切り替えが環境変数1つで可能
- 将来のAGI統合が1〜2時間で完了
- 全てのAI応答がログに記録され、コスト管理が可能
- プロンプトのA/Bテストとバージョン管理が可能

✅ **次のステップ**:
- 本番環境へのデプロイ
- AI機能の動作確認
- コスト監視ダッシュボードの作成（オプション）

## 連絡先

実装者: Manus AI
実装日: 2025年12月28日
