# 福祉事業所向け包括的管理システム

## 概要

このシステムは、福祉事業所（児童発達支援、放課後等デイサービスなど）向けの包括的な管理システムです。既存システム（カイポケ、かべなし）に劣る部分をゼロにし、AI連携などで圧倒的な優位性を確立することを目標としています。

## 主な機能

### 基本機能
- **勤務実績管理**: 職員の勤務時間を記録し、常勤換算（FTE）を自動計算
- **進捗評価管理**: 利用者の成長スコアを記録・評価
- **加算充足ステータス**: 加算要件の充足状況をリアルタイムで確認
- **職員相互評価**: 職員間の協調性を評価し、総合評価を算出

### CSV出力機能
- **国保連請求CSV**: 国保連への請求データを自動生成
- **給与計算CSV**: 給与計算システムとの連携用データを出力
- **会計CSV**: 会計システムとの連携用データを出力

### PDF出力機能
- **個別支援計画書PDF**: 法定帳票を自動生成（指導監査対応）
- **電子サイン機能**: タブレットで保護者の署名を取得（ペーパーレス化）

### AI機能
- **感情分析**: 専門職コメントから利用者の感情状態を分析
- **離脱リスク予測**: 利用者の離脱リスクを予測し、早期対応を支援
- **AI記録自動生成**: 職員の断片的な入力から法定形式の記録を自動生成

### レスポンシブデザイン
- スマホ（〜768px）: 1列表示
- タブレット（769-1024px）: 2列表示
- PC（1025px〜）: 3列表示
- タッチ操作最適化済み（ボタン44px以上、フォント16px以上）

## 技術スタック

### バックエンド
- Django 5.1.4
- Django REST Framework 3.15.2
- PostgreSQL（本番環境）
- SQLite（開発環境）
- OpenAI API（GPT-4.1-mini）
- ReportLab（PDF生成）

### フロントエンド
- React 18.3.1
- Vite 6.0.3
- Recharts（グラフ表示）
- react-signature-canvas（電子サイン）

### デプロイ
- Render（本番環境）
- Gunicorn（WSGIサーバー）
- WhiteNoise（静的ファイル配信）

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/YOUR_USERNAME/fukushi-management-system.git
cd fukushi-management-system
```

### 2. バックエンドのセットアップ

```bash
# 仮想環境の作成と有効化
python3 -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# データベースのマイグレーション
python manage.py migrate

# テストデータの投入（オプション）
python manage.py loaddata test_data.json

# 開発サーバーの起動
python manage.py runserver
```

### 3. フロントエンドのセットアップ

```bash
cd frontend

# 依存関係のインストール
pnpm install

# 開発サーバーの起動
pnpm run dev

# ビルド（本番環境用）
pnpm run build
```

### 4. 環境変数の設定

`.env`ファイルを作成し、以下の環境変数を設定してください：

```
# Django設定
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com

# データベース設定（本番環境）
DATABASE_URL=postgresql://user:password@host:port/dbname

# OpenAI API設定
OPENAI_API_KEY=your-openai-api-key-here
```

## API エンドポイント一覧

| エンドポイント | メソッド | 説明 |
|--------------|---------|------|
| `/api/workrecords/` | GET, POST | 勤務実績の登録・一覧取得 |
| `/api/progress/` | GET, POST | 進捗評価の登録・一覧取得 |
| `/api/dashboard/fte/` | GET | 加算充足ステータスの取得 |
| `/api/peerreview/` | GET, POST | 職員相互評価の登録・一覧取得 |
| `/api/evaluation/summary/` | GET | 職員評価サマリーの取得 |
| `/api/export/kokuhoren_csv/` | GET | 国保連請求CSV出力 |
| `/api/export/payroll_csv/` | GET | 給与計算CSV出力 |
| `/api/export/accounting_csv/` | GET | 会計CSV出力 |
| `/api/export/support_plan_pdf/<client_id>/` | GET | 個別支援計画書PDF出力 |
| `/api/clients/` | GET | 利用者一覧の取得 |
| `/api/analyze_sentiment/<assessment_id>/` | POST | AI感情分析 |
| `/api/analysis_results/` | GET | AI分析結果一覧の取得 |
| `/api/churn_prediction/` | GET | 離脱リスク予測（全利用者） |
| `/api/churn_prediction/<client_id>/` | GET | 離脱リスク予測（個別） |
| `/api/ai_record_generation/` | POST | AI記録自動生成 |
| `/api/save_signature/<client_id>/` | POST | 電子サイン保存 |

## デプロイ手順（Render）

詳細な手順は`netcafe_deployment_guide.md`を参照してください。

### 概要
1. GitHubリポジトリにコードをプッシュ
2. Renderでアカウント作成
3. 新しいWebサービスを作成
4. GitHubリポジトリを連携
5. 環境変数を設定
6. PostgreSQLデータベースを作成
7. デプロイを実行

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 開発者

開発者: Manus AI Agent
プロジェクト開始日: 2025年12月

## サポート

問題が発生した場合は、GitHubのIssuesセクションで報告してください。
