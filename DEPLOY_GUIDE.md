# 福祉事業所向け請求管理システム - デプロイ手順書

このガイドでは、開発したシステムをRender（無料ステージング環境）にデプロイする手順を、分かりやすく説明します。

---

## 📋 事前準備

### 必要なもの

1.  **GitHubアカウント** (作成済み: `d68405394-lang`)
2.  **Renderアカウント** (これから作成します)
3.  **デプロイ用ファイル** (`fukushi-system-deploy.zip`)

---

## ステップ 1: GitHubにリポジトリを作成する

### 1-1. GitHubにログイン

1.  ブラウザで [https://github.com](https://github.com) にアクセスします。
2.  Googleアカウントでログインします。

### 1-2. 新しいリポジトリを作成

3.  画面右上の **「+」アイコン** をクリックし、**「New repository」** を選択します。
4.  以下の情報を入力します。

| 項目 | 入力内容 |
|------|---------|
| **Repository name** | `fukushi-system-backend` |
| **Description** | `福祉事業所向け請求管理システム（バックエンド）` |
| **Public / Private** | **Private**（非公開）を選択 |
| **Initialize this repository with:** | **何もチェックしない** |

5.  **「Create repository」** ボタンをクリックします。

### 1-3. リポジトリのURLを確認

6.  リポジトリが作成されると、以下のようなURLが表示されます。

```
https://github.com/d68405394-lang/fukushi-system-backend
```

このURLを**メモ**しておいてください。

---

## ステップ 2: デプロイ用ファイルをGitHubにアップロードする

### 2-1. ファイルを解凍

1.  ダウンロードした **`fukushi-system-deploy.zip`** を、パソコンの任意のフォルダに解凍します。
    *   例: `C:\fukushi-system-deploy\` (Windows)
    *   例: `/Users/あなたの名前/fukushi-system-deploy/` (Mac)

### 2-2. GitHubのWebインターフェースからアップロード

2.  先ほど作成したリポジトリのページ（`https://github.com/d68405394-lang/fukushi-system-backend`）にアクセスします。
3.  **「uploading an existing file」** というリンクをクリックします。
4.  解凍したフォルダ内の**すべてのファイルとフォルダ**を、ドラッグ&ドロップでアップロードします。

**アップロードするファイル一覧:**
*   `myproject/` (フォルダ)
*   `billing_management/` (フォルダ)
*   `manage.py`
*   `requirements.txt`
*   `build.sh`
*   `render.yaml`

5.  アップロードが完了したら、画面下部の **「Commit changes」** ボタンをクリックします。

---

## ステップ 3: Renderアカウントを作成する

### 3-1. Renderにアクセス

1.  ブラウザで [https://render.com](https://render.com) にアクセスします。

### 3-2. GitHubアカウントでサインアップ

2.  **「Get Started for Free」** または **「Sign Up」** ボタンをクリックします。
3.  **「Sign up with GitHub」** を選択します。
4.  GitHubの認証画面が表示されるので、**「Authorize Render」** をクリックします。

### 3-3. Renderアカウントの作成完了

5.  これで、Renderアカウントが作成されました！

---

## ステップ 4: RenderにGitHubリポジトリを連携する

### 4-1. 新しいWebサービスを作成

1.  Renderのダッシュボード画面で、**「New +」** ボタンをクリックします。
2.  **「Blueprint」** を選択します。

### 4-2. GitHubリポジトリを選択

3.  **「Connect a repository」** セクションで、先ほど作成した **`fukushi-system-backend`** リポジトリを選択します。
4.  **「Connect」** ボタンをクリックします。

### 4-3. Blueprintの設定を確認

5.  Renderが自動的に `render.yaml` ファイルを読み込み、以下のサービスが表示されます。

*   **Web Service**: `fukushi-system-backend`
*   **Database**: `fukushi-system-db`

6.  **「Apply」** ボタンをクリックします。

---

## ステップ 5: デプロイの完了を待つ

### 5-1. デプロイの進行状況を確認

1.  Renderが自動的にデプロイを開始します。
2.  画面に **「Building...」** → **「Deploying...」** → **「Live」** と表示されるのを待ちます。

**所要時間:** 約5〜10分

### 5-2. 公開URLを確認

3.  デプロイが完了すると、画面上部に **公開URL** が表示されます。

```
https://fukushi-system-backend.onrender.com
```

このURLが、**ステージング環境のバックエンドURL**です。

---

## ステップ 6: 動作確認

### 6-1. APIの動作確認

1.  ブラウザで以下のURLにアクセスします。

```
https://fukushi-system-backend.onrender.com/api/dashboard/fte/
```

2.  以下のようなJSON形式のデータが表示されれば、**デプロイ成功**です！

```json
[]
```

（データがまだ登録されていないため、空のリストが返ってきます）

---

## ステップ 7: フロントエンド（React）のデプロイ

バックエンドのデプロイが完了したら、次はフロントエンド（React）をデプロイします。

**別途、フロントエンド用の手順書をお渡しします。**

---

## トラブルシューティング

### エラー1: 「Build failed」と表示される

**原因:** `requirements.txt` や `build.sh` に問題がある可能性があります。

**解決策:**
1.  Renderのログを確認し、エラーメッセージをコピーしてください。
2.  エラーメッセージを私にお知らせください。修正いたします。

### エラー2: 「Database connection failed」と表示される

**原因:** データベースの接続設定に問題がある可能性があります。

**解決策:**
1.  Renderのダッシュボードで、**Environment Variables**（環境変数）を確認してください。
2.  `DATABASE_URL` が正しく設定されているか確認してください。

---

## まとめ

これで、バックエンド（Django）のデプロイが完了しました！

次のステップとして、フロントエンド（React）をデプロイし、スマートフォンでもテストできる環境を構築します。

ご不明な点がございましたら、いつでもお気軽にお尋ねください。
