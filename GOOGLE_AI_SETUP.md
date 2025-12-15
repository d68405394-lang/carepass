# Google AI (Gemini) セットアップガイド

## 🔄 変更内容

Care-pass v3.0のAI機能を**Google AI (Gemini)**に変更しました。

---

## 📋 変更されたファイル

### 1. `requirements.txt`
- **変更前**: `openai==2.9.0`
- **変更後**: `google-generativeai==0.8.3`

### 2. `billing_management/ai_utils.py` (新規作成)
Google AI (Gemini) APIとの統合を管理するユーティリティモジュール

**主な機能**:
- `analyze_sentiment()`: 感情分析・記録品質評価
- `generate_progress_record()`: AI記録自動生成
- `predict_churn_risk()`: 退所リスク予測

### 3. `billing_management/views.py`
- OpenAI APIの呼び出しをGoogle AI (Gemini)に置き換え
- `SentimentAnalysisView`: 感情分析API
- `AIRecordGenerationView`: AI記録生成API

---

## 🔑 Google AI Studio APIキー取得方法

### ステップ1: Google AI Studioにアクセス

1. **Google AI Studio**を開く: https://aistudio.google.com/
2. Googleアカウントでログイン

### ステップ2: APIキーを作成

1. 左側のメニューで **「Get API key」** をクリック
2. **「Create API key」** をクリック
3. プロジェクトを選択（または新規作成）
4. APIキーが表示されます（`AIza` で始まる文字列）
5. **コピー**してください

### ステップ3: 安全に保管

- APIキーは**一度しか表示されません**
- 安全な場所に保管してください
- GitHubなどにコミットしないでください

---

## ⚙️ Renderでの環境変数設定

Renderのデプロイ時に、以下の環境変数を設定してください：

| Key | Value |
|-----|-------|
| `GOOGLE_AI_API_KEY` | あなたのGoogle AI APIキー（`AIza`で始まる） |
| `SECRET_KEY` | `django-insecure-your-secret-key-here` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com` |
| `DATABASE_URL` | PostgreSQLの接続URL |

**注意**: `OPENAI_API_KEY`は不要になりました。

---

## 🚀 使用モデル

**Gemini 1.5 Flash**

- 高速で効率的
- 日本語対応
- JSON出力サポート
- 無料枠あり

---

## 💰 料金について

### Google AI Studio（Gemini API）

**無料枠**:
- 1分あたり15リクエスト
- 1日あたり1,500リクエスト
- 月間100万トークン

**有料プラン**:
- 従量課金制
- 詳細: https://ai.google.dev/pricing

### 比較（OpenAI vs Google AI）

| 項目 | OpenAI GPT-4 | Google Gemini |
|------|--------------|---------------|
| 無料枠 | なし | あり（1日1,500リクエスト） |
| 料金 | $0.03/1Kトークン | $0.00015/1Kトークン（約200倍安い） |
| 日本語 | 対応 | 対応 |
| JSON出力 | 対応 | 対応 |

---

## 🧪 テスト方法

### ローカルでテスト

```bash
# 環境変数を設定
export GOOGLE_AI_API_KEY="your-api-key-here"

# Djangoサーバーを起動
python manage.py runserver

# APIをテスト
curl -X POST http://localhost:8000/api/sentiment-analysis/1/
```

### Renderでテスト

デプロイ後、以下のエンドポイントをテスト：

1. **感情分析API**: `POST /api/sentiment-analysis/{assessment_id}/`
2. **AI記録生成API**: `POST /api/ai-record-generation/{client_id}/`

---

## ⚠️ トラブルシューティング

### エラー: "GOOGLE_AI_API_KEY environment variable is not set"

**原因**: 環境変数が設定されていない

**解決策**:
1. Renderの環境変数設定を確認
2. `GOOGLE_AI_API_KEY`が正しく設定されているか確認

### エラー: "API key not valid"

**原因**: APIキーが無効または期限切れ

**解決策**:
1. Google AI Studioで新しいAPIキーを作成
2. Renderの環境変数を更新

### エラー: "Rate limit exceeded"

**原因**: 無料枠の制限を超えた

**解決策**:
1. 少し待ってから再試行
2. 有料プランへのアップグレードを検討

---

## 📚 参考リンク

- **Google AI Studio**: https://aistudio.google.com/
- **Gemini API ドキュメント**: https://ai.google.dev/docs
- **料金**: https://ai.google.dev/pricing
- **Python SDK**: https://github.com/google/generative-ai-python

---

## ✅ 次のステップ

1. ✅ Google AI APIキーを取得
2. ✅ Renderで環境変数を設定
3. ✅ デプロイ
4. ✅ AI機能をテスト

---

**作成日**: 2024年12月16日  
**バージョン**: Care-pass v3.0 (Google AI対応版)
