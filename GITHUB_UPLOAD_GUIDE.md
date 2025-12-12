# GitHubへのアップロード手順

このガイドは、ネットカフェなどの環境でGitHubにコードをアップロードする手順を説明します。

## 前提条件

- GitHubアカウントを持っていること
- インターネット接続があること

## 手順1: GitHubでリポジトリを作成

1. ブラウザで https://github.com にアクセス
2. ログイン（アカウントがない場合は新規作成）
3. 右上の「+」ボタンをクリック → 「New repository」を選択
4. リポジトリ情報を入力：
   - **Repository name**: `fukushi-management-system`（または任意の名前）
   - **Description**: 福祉事業所向け包括的管理システム
   - **Public** を選択（無料で使用可能）
   - **Initialize this repository with a README** は**チェックしない**（既にREADME.mdがあるため）
5. 「Create repository」をクリック

## 手順2: リモートリポジトリを追加

GitHubでリポジトリを作成すると、以下のようなコマンドが表示されます：

```bash
git remote add origin https://github.com/YOUR_USERNAME/fukushi-management-system.git
git branch -M main
git push -u origin main
```

**実際のコマンド実行:**

```bash
cd /home/ubuntu

# リモートリポジトリを追加（YOUR_USERNAMEを実際のユーザー名に置き換える）
git remote add origin https://github.com/YOUR_USERNAME/fukushi-management-system.git

# ブランチ名をmainに設定（既に設定済みの場合はスキップ可）
git branch -M main

# GitHubにプッシュ
git push -u origin main
```

## 手順3: 認証情報の入力

プッシュ時に認証情報を求められます：

### 方法1: Personal Access Token（推奨）

1. GitHubで Settings → Developer settings → Personal access tokens → Tokens (classic) に移動
2. 「Generate new token」をクリック
3. 以下の権限を選択：
   - `repo` (Full control of private repositories)
4. トークンを生成してコピー
5. コマンドラインで：
   - Username: GitHubのユーザー名
   - Password: 生成したトークン（パスワードではない）

### 方法2: GitHub CLI（オプション）

```bash
# GitHub CLIをインストール（既にインストール済み）
gh auth login

# ブラウザで認証
# または、トークンを直接入力
```

## 手順4: プッシュの確認

```bash
# プッシュが成功したか確認
git remote -v
git log --oneline

# GitHubのリポジトリページをブラウザで確認
# https://github.com/YOUR_USERNAME/fukushi-management-system
```

## トラブルシューティング

### エラー: "remote origin already exists"

```bash
# 既存のリモートを削除
git remote remove origin

# 再度追加
git remote add origin https://github.com/YOUR_USERNAME/fukushi-management-system.git
```

### エラー: "failed to push some refs"

```bash
# リモートの変更を取得してマージ
git pull origin main --allow-unrelated-histories

# 再度プッシュ
git push -u origin main
```

### エラー: "Authentication failed"

- Personal Access Tokenを使用していることを確認
- トークンの権限が正しいか確認（`repo`権限が必要）
- トークンの有効期限が切れていないか確認

## 次のステップ

GitHubへのアップロードが完了したら、`netcafe_deployment_guide.md`を参照してRenderへのデプロイを実行してください。

## 重要な注意事項

⚠️ **機密情報の管理**
- `.env`ファイルは`.gitignore`に含まれており、GitHubにはアップロードされません
- `SECRET_KEY`や`OPENAI_API_KEY`などの機密情報は、Renderの環境変数として設定してください
- `db.sqlite3`（開発用データベース）もGitHubにはアップロードされません

⚠️ **ネットカフェでの作業**
- 作業終了時は必ずログアウトしてください
- ブラウザの履歴とキャッシュをクリアしてください
- Personal Access Tokenは安全に保管してください（メモ帳などに保存しない）

## 参考リンク

- GitHub公式ドキュメント: https://docs.github.com/
- Personal Access Token作成手順: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token
- Git基本コマンド: https://git-scm.com/docs
