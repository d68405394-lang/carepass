# 最終チェックリスト - ネットカフェでの作業用

このチェックリストは、ネットカフェでGitHubへのアップロードとRenderへのデプロイを実行する際に使用してください。

## 事前準備

### 持参するもの

- [ ] GitHubアカウント情報（ユーザー名・パスワード）
- [ ] OpenAI APIキー（環境変数用）
- [ ] このチェックリストのコピー

### 必要な情報

- [ ] GitHubリポジトリ名: `fukushi-management-system`（または任意の名前）
- [ ] Renderアカウント（なければ作成）
- [ ] PostgreSQL接続情報（Renderで自動生成）

## Phase 1: GitHubへのアップロード

### 1.1 GitHubリポジトリの作成

- [ ] https://github.com にアクセス
- [ ] ログイン
- [ ] 「New repository」をクリック
- [ ] リポジトリ名を入力: `fukushi-management-system`
- [ ] Description: 福祉事業所向け包括的管理システム
- [ ] **Public**を選択
- [ ] **Initialize this repository with a README**は**チェックしない**
- [ ] 「Create repository」をクリック
- [ ] リポジトリURLをメモ: `https://github.com/YOUR_USERNAME/fukushi-management-system.git`

### 1.2 Personal Access Tokenの作成

- [ ] GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
- [ ] 「Generate new token」をクリック
- [ ] Note: `fukushi-system-deploy`
- [ ] Expiration: 90 days（または任意）
- [ ] Select scopes: `repo`（Full control of private repositories）にチェック
- [ ] 「Generate token」をクリック
- [ ] **トークンをコピーして安全に保管**（後で使用）

### 1.3 コマンド実行

```bash
# プロジェクトディレクトリに移動
cd /home/ubuntu

# リモートリポジトリを追加（YOUR_USERNAMEを実際のユーザー名に置き換える）
git remote add origin https://github.com/YOUR_USERNAME/fukushi-management-system.git

# プッシュ
git push -u origin main
```

- [ ] Username: GitHubのユーザー名を入力
- [ ] Password: **Personal Access Token**を入力（パスワードではない）
- [ ] プッシュ成功を確認

### 1.4 確認

- [ ] ブラウザでGitHubリポジトリを開く
- [ ] ファイルが正しくアップロードされているか確認
- [ ] README.mdが表示されているか確認

## Phase 2: Renderへのデプロイ

### 2.1 Renderアカウントの作成

- [ ] https://render.com にアクセス
- [ ] 「Get Started」をクリック
- [ ] GitHubアカウントで認証（推奨）
- [ ] アカウント作成完了

### 2.2 PostgreSQLデータベースの作成

- [ ] Renderダッシュボードで「New +」→「PostgreSQL」を選択
- [ ] Name: `fukushi-system-db`
- [ ] Database: `fukushi_db`
- [ ] User: `fukushi_user`
- [ ] Region: Singapore（日本に最も近い）
- [ ] PostgreSQL Version: 15
- [ ] Plan: Free
- [ ] 「Create Database」をクリック
- [ ] **Internal Database URL**をコピー（後で使用）

### 2.3 Webサービスの作成

- [ ] Renderダッシュボードで「New +」→「Web Service」を選択
- [ ] 「Connect a repository」→GitHubリポジトリを選択
- [ ] Name: `fukushi-management-system`
- [ ] Region: Singapore
- [ ] Branch: `main`
- [ ] Root Directory: （空欄のまま）
- [ ] Runtime: Python 3
- [ ] Build Command: `pip install -r requirements.txt && cd frontend && pnpm install && pnpm run build && cd .. && python manage.py collectstatic --noinput && python manage.py migrate`
- [ ] Start Command: `gunicorn myproject.wsgi:application`
- [ ] Plan: Free

### 2.4 環境変数の設定

- [ ] 「Advanced」→「Add Environment Variable」をクリック
- [ ] 以下の環境変数を追加:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | ランダムな文字列（50文字以上推奨） |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` |
| `DATABASE_URL` | PostgreSQLのInternal Database URL |
| `OPENAI_API_KEY` | OpenAI APIキー |

**SECRET_KEYの生成方法:**
```python
import secrets
print(secrets.token_urlsafe(50))
```

- [ ] 全ての環境変数を入力完了
- [ ] 「Create Web Service」をクリック

### 2.5 デプロイの監視

- [ ] デプロイログを確認
- [ ] ビルドが成功するまで待機（5-10分程度）
- [ ] デプロイ完了を確認

### 2.6 動作確認

- [ ] Renderが提供するURLにアクセス: `https://your-app-name.onrender.com`
- [ ] フロントエンドが正しく表示されるか確認
- [ ] 以下のAPIエンドポイントにアクセスして動作確認:
  - [ ] `/api/clients/` - 利用者一覧
  - [ ] `/api/dashboard/fte/` - FTEステータス
  - [ ] `/api/export/kokuhoren_csv/` - 国保連CSV（ダウンロード確認）

## Phase 3: 最終確認

### 3.1 全機能のテスト

- [ ] 勤務実績の登録
- [ ] 進捗評価の登録
- [ ] CSV出力（国保連、給与、会計）
- [ ] PDF出力（個別支援計画書）
- [ ] 電子サイン機能
- [ ] AI感情分析
- [ ] 離脱リスク予測
- [ ] AI記録自動生成

### 3.2 レスポンシブデザインの確認

- [ ] スマホ表示（Chrome DevTools）
- [ ] タブレット表示（Chrome DevTools）
- [ ] PC表示

### 3.3 パフォーマンスの確認

- [ ] ページ読み込み速度
- [ ] API応答速度
- [ ] エラーログの確認

## Phase 4: ドキュメント更新

### 4.1 README.mdの更新

- [ ] デプロイURLを追加
- [ ] 環境変数の設定方法を更新
- [ ] スクリーンショットを追加（オプション）

### 4.2 GitHubリポジトリの整理

- [ ] リポジトリの説明を追加
- [ ] トピックを追加（django, react, welfare, ai）
- [ ] Licenseを設定（MIT推奨）

## トラブルシューティング

### GitHubプッシュ失敗

**エラー: "Authentication failed"**
- Personal Access Tokenを使用しているか確認
- トークンの権限が正しいか確認（`repo`権限）

**エラー: "remote origin already exists"**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/fukushi-management-system.git
```

### Renderデプロイ失敗

**エラー: "Build failed"**
- ビルドログを確認
- requirements.txtが正しいか確認
- pnpmがインストールされているか確認

**エラー: "Database connection failed"**
- DATABASE_URLが正しいか確認
- PostgreSQLデータベースが起動しているか確認

**エラー: "Static files not found"**
- collectstaticが実行されているか確認
- STATIC_ROOTが正しく設定されているか確認

## 完了後の作業

### セキュリティ対策

- [ ] ブラウザの履歴をクリア
- [ ] ブラウザのキャッシュをクリア
- [ ] GitHubからログアウト
- [ ] Renderからログアウト
- [ ] Personal Access Tokenを安全に保管

### 次のステップ

- [ ] ユーザーテストの実施
- [ ] フィードバックの収集
- [ ] 改善点のリストアップ
- [ ] 次期バージョンの計画

## 参考ドキュメント

- `README.md`: プロジェクト概要
- `GITHUB_UPLOAD_GUIDE.md`: GitHubアップロード詳細手順
- `netcafe_deployment_guide.md`: Renderデプロイ詳細手順
- `PROJECT_COMPLETION_REPORT.md`: プロジェクト完成レポート

## 緊急連絡先

- GitHub公式サポート: https://support.github.com/
- Render公式サポート: https://render.com/docs/support
- OpenAI公式サポート: https://help.openai.com/

---

**作成日**: 2025年12月13日  
**バージョン**: 1.0.0  
**最終更新**: デプロイ前

**重要**: このチェックリストは、作業の進捗を確認するためのものです。各項目を確実にチェックしながら進めてください。
