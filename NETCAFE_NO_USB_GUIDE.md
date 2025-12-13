# ネットカフェ作業ガイド（USB不要版）

**所要時間**: 約1時間  
**必要なもの**: メールアドレス、パスワード（USBは不要！）

---

## 🌐 方法1: GitHub経由（最も簡単！推奨）

### 自宅での準備（5分）

#### ステップ1: GitHubアカウント作成

1. [GitHub](https://github.com/)にアクセス
2. 「Sign up」をクリック
3. 以下を入力：
   - メールアドレス
   - パスワード
   - ユーザー名（例: your-name-123）
4. メール認証を完了

**✅ 完了**: GitHubアカウントができた

#### ステップ2: プロジェクトをGitHubにアップロード

```bash
# 自宅のPCで実行
cd /home/ubuntu

# Gitの設定（初回のみ）
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"

# GitHubにリモートリポジトリを作成
# （GitHubのWebサイトで「New repository」→「carepass」を作成）

# リモートリポジトリを追加
git remote add origin https://github.com/your-username/carepass.git

# プッシュ
git push -u origin main
```

**GitHub Personal Access Token（PAT）が必要な場合:**

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 「Generate new token (classic)」をクリック
3. Note: `carepass`
4. Expiration: 30 days
5. Select scopes: `repo`（すべてにチェック）
6. 「Generate token」をクリック
7. **トークンをコピーして保存**（パスワードの代わりに使用）

**✅ 完了**: GitHubにアップロードできた

---

### ネットカフェでの作業（55分）

#### ステップ1: プロジェクトをダウンロード（5分）

```bash
# ネットカフェのPCで実行
cd Desktop
git clone https://github.com/your-username/carepass.git
cd carepass
```

**または、Webブラウザから:**
1. `https://github.com/your-username/carepass`にアクセス
2. 「Code」→「Download ZIP」をクリック
3. ZIPを解凍

**✅ 完了**: プロジェクトをダウンロードできた

#### ステップ2: Renderでデプロイ（50分）

以降は`NETCAFE_SIMPLE_GUIDE.md`の**ステップ3**と**ステップ4**を実行してください。

---

## 📧 方法2: メール経由（バックアップ）

### 自宅での準備（10分）

#### ステップ1: プロジェクトをZIPに圧縮

```bash
cd /home/ubuntu
zip -r carepass.zip . -x "*.git/*" "venv/*" "node_modules/*" "__pycache__/*"
```

#### ステップ2: Google Driveにアップロード

1. [Google Drive](https://drive.google.com/)にアクセス
2. 「新規」→「ファイルのアップロード」をクリック
3. `carepass.zip`を選択
4. アップロード完了後、右クリック→「共有」→「リンクを取得」
5. 「リンクを知っている全員」に変更
6. リンクをコピーして保存

**または、メールで送信:**
1. 自分宛にメールを送信
2. `carepass.zip`を添付（25MB以下）
3. 25MBを超える場合は、Google Drive等を使用

**✅ 完了**: クラウドにアップロードできた

---

### ネットカフェでの作業（55分）

#### ステップ1: プロジェクトをダウンロード（5分）

**Google Driveから:**
1. [Google Drive](https://drive.google.com/)にログイン
2. `carepass.zip`をダウンロード
3. 解凍

**メールから:**
1. メールを開く
2. 添付ファイルをダウンロード
3. 解凍

**✅ 完了**: プロジェクトをダウンロードできた

#### ステップ2: GitHubにアップロード（10分）

```bash
cd Desktop/carepass

# Gitの設定
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"

# GitHubにプッシュ
git init
git add -A
git commit -m "初回コミット"
git branch -m main
git remote add origin https://github.com/your-username/carepass.git
git push -u origin main
```

**✅ 完了**: GitHubにアップロードできた

#### ステップ3: Renderでデプロイ（40分）

以降は`NETCAFE_SIMPLE_GUIDE.md`の**ステップ3**と**ステップ4**を実行してください。

---

## 🌟 方法3: 完全Webブラウザのみ（最も簡単！）

### 自宅での準備（10分）

#### ステップ1: GitHubアカウント作成

1. [GitHub](https://github.com/)にアクセス
2. アカウント作成（方法1と同じ）

#### ステップ2: リポジトリ作成

1. GitHubにログイン
2. 右上の「+」→「New repository」をクリック
3. 以下を入力：
   - **Repository name**: `carepass`
   - **Description**: 福祉事業所向け管理システム
   - **Public**を選択
4. 「Create repository」をクリック

#### ステップ3: ファイルをアップロード

1. 「uploading an existing file」をクリック
2. 以下のファイルをドラッグ＆ドロップ：
   - `manage.py`
   - `requirements.txt`
   - `myproject/`フォルダ
   - `billing_management/`フォルダ
   - `frontend/`フォルダ
   - `staticfiles/`フォルダ
   - `README.md`
   - その他必要なファイル

**⚠️ 注意**: 
- `.git/`フォルダはアップロードしない
- `venv/`フォルダはアップロードしない
- `node_modules/`フォルダはアップロードしない

3. 「Commit changes」をクリック

**✅ 完了**: GitHubにアップロードできた

---

### ネットカフェでの作業（50分）

#### ステップ1: Renderでデプロイ（50分）

以降は`NETCAFE_SIMPLE_GUIDE.md`の**ステップ3**と**ステップ4**を実行してください。

---

## 🎯 推奨方法の比較

| 方法 | 難易度 | 所要時間 | メリット | デメリット |
|:---|:---:|:---:|:---|:---|
| **方法1: GitHub経由** | ⭐⭐ | 1時間 | 最も確実、Git履歴が残る | コマンドライン必要 |
| **方法2: メール経由** | ⭐⭐⭐ | 1時間5分 | バックアップになる | 手順が多い |
| **方法3: Webのみ** | ⭐ | 1時間 | **最も簡単！** | 大量ファイルのアップロードが面倒 |

### 推奨

**初心者**: 方法3（完全Webブラウザのみ）  
**中級者**: 方法1（GitHub経由）  
**バックアップ**: 方法2（メール経由）

---

## 📱 スマホで見る方法

### このガイドをスマホで見る

1. **方法A**: このファイルをメールで自分宛に送信
2. **方法B**: Google Driveにアップロードして、スマホで開く
3. **方法C**: LINEの「Keep」に保存

### ネットカフェで

1. スマホでガイドを開く
2. PCで作業しながら、スマホで手順を確認

---

## ✅ 最終チェックリスト

### 自宅で
- [ ] GitHubアカウント作成完了
- [ ] プロジェクトをGitHubにアップロード完了
- [ ] このガイドをスマホで見られる状態にした

### ネットカフェで
- [ ] GitHubからプロジェクトをダウンロード完了
- [ ] Renderアカウント作成完了
- [ ] PostgreSQLデータベース作成完了
- [ ] Webサービスデプロイ完了
- [ ] SendGridアカウント作成完了
- [ ] 送信者認証完了
- [ ] APIキー作成完了
- [ ] Render環境変数設定完了
- [ ] 動作確認完了

---

## 🆘 トラブルシューティング

### エラー1: GitHubにプッシュできない
**解決策**:
- Personal Access Token（PAT）を使用
- パスワードの代わりにPATを入力

### エラー2: ファイルが大きすぎる
**解決策**:
- `.git/`、`venv/`、`node_modules/`を除外
- ZIPファイルを分割

### エラー3: ネットカフェでGitが使えない
**解決策**:
- 方法3（完全Webブラウザのみ）を使用

---

**これで準備完了です！USBなしでネットカフェでの作業ができます！** 🚀

何か質問があれば、今のうちに聞いてください！
