# ネットカフェ作業 超シンプルガイド

**所要時間**: 約1時間  
**必要なもの**: USBメモリ、メールアドレス、パスワード

---

## 📋 事前準備（自宅で）

### 1. USBメモリにプロジェクトをコピー

```bash
# 自宅のPCで実行
cd /home/ubuntu
zip -r carepass.zip . -x "*.git/*" "venv/*" "node_modules/*"
# carepass.zipをUSBメモリにコピー
```

**または、このファイルだけをUSBにコピー:**
- `NETCAFE_SIMPLE_GUIDE.md`（このファイル）

---

## 🏪 ネットカフェでの作業（4ステップ）

### ステップ1: GitHubアカウント作成（5分）

1. [GitHub](https://github.com/)にアクセス
2. 「Sign up」をクリック
3. 以下を入力：
   - メールアドレス
   - パスワード
   - ユーザー名（例: your-name-123）
4. メール認証を完了

**✅ 完了**: GitHubアカウントができた

---

### ステップ2: GitHubにプロジェクトをアップロード（10分）

#### 方法A: Webブラウザから（簡単！）

1. GitHubにログイン
2. 右上の「+」→「New repository」をクリック
3. 以下を入力：
   - **Repository name**: `carepass`
   - **Description**: 福祉事業所向け管理システム
   - **Public**を選択
4. 「Create repository」をクリック
5. 「uploading an existing file」をクリック
6. USBメモリから`carepass.zip`をドラッグ＆ドロップ
7. 「Commit changes」をクリック

**✅ 完了**: GitHubにアップロードできた

#### 方法B: コマンドライン（上級者向け）

```bash
# ネットカフェのPCで実行
cd Desktop
unzip /path/to/carepass.zip
cd carepass

# Gitの設定
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"

# GitHubにプッシュ
git remote add origin https://github.com/your-username/carepass.git
git push -u origin main
```

**✅ 完了**: GitHubにアップロードできた

---

### ステップ3: Renderアカウント作成とデプロイ（30分）

#### 3-1: アカウント作成（5分）

1. [Render](https://render.com/)にアクセス
2. 「Get Started」をクリック
3. 「Sign up with GitHub」を選択
4. GitHubアカウントで認証

**✅ 完了**: Renderアカウントができた

#### 3-2: PostgreSQLデータベース作成（5分）

1. Renderダッシュボードで「New +」→「PostgreSQL」を選択
2. 以下を入力：
   - **Name**: `carepass-db`
   - **Database**: `carepass`
   - **User**: `carepass`
   - **Region**: Singapore（最も近い）
   - **Plan**: Free
3. 「Create Database」をクリック
4. **Internal Database URL**をコピーして保存（後で使う）

**✅ 完了**: データベースができた

#### 3-3: Webサービス作成（20分）

1. Renderダッシュボードで「New +」→「Web Service」を選択
2. 「Connect a repository」で`carepass`を選択
3. 以下を入力：
   - **Name**: `carepass`
   - **Region**: Singapore
   - **Branch**: main
   - **Root Directory**: （空欄）
   - **Runtime**: Python 3
   - **Build Command**: 
     ```
     pip install -r requirements.txt && cd frontend && pnpm install && pnpm run build && cd .. && python manage.py collectstatic --noinput
     ```
   - **Start Command**: 
     ```
     python manage.py migrate && gunicorn myproject.wsgi:application
     ```
   - **Plan**: Free

4. 「Advanced」をクリックして環境変数を追加：

| Key | Value |
|:---|:---|
| `SECRET_KEY` | `your-secret-key-here-make-it-long-and-random-50-chars` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `carepass.onrender.com` |
| `DATABASE_URL` | （ステップ3-2でコピーしたInternal Database URL） |
| `OPENAI_API_KEY` | （あなたのOpenAI APIキー） |

5. 「Create Web Service」をクリック
6. デプロイが完了するまで待つ（10-15分）

**✅ 完了**: デプロイできた！

---

### ステップ4: SendGrid設定（15分）

#### 4-1: SendGridアカウント作成（5分）

1. [SendGrid](https://sendgrid.com/)にアクセス
2. 「Start for Free」をクリック
3. 以下を入力：
   - メールアドレス
   - パスワード
   - 名前
4. メール認証を完了

**✅ 完了**: SendGridアカウントができた

#### 4-2: 送信者認証（5分）

1. SendGridダッシュボードで「Settings」→「Sender Authentication」を選択
2. 「Single Sender Verification」を選択
3. 以下を入力：
   - **From Name**: 事業所名
   - **From Email**: あなたのメールアドレス
   - **Reply To**: あなたのメールアドレス
   - **Company Address**: 事業所住所
4. 「Create」をクリック
5. メール認証を完了

**✅ 完了**: 送信者認証できた

#### 4-3: APIキー作成（5分）

1. SendGridダッシュボードで「Settings」→「API Keys」を選択
2. 「Create API Key」をクリック
3. 以下を入力：
   - **API Key Name**: carepass
   - **API Key Permissions**: Full Access
4. 「Create & View」をクリック
5. **APIキーをコピー**（一度しか表示されない！）

6. Renderダッシュボードに戻る
7. careapassのWebサービスを選択
8. 「Environment」タブを選択
9. 環境変数を追加：

| Key | Value |
|:---|:---|
| `SENDGRID_API_KEY` | （コピーしたAPIキー） |
| `FROM_EMAIL` | （ステップ4-2で設定したメールアドレス） |

10. 「Save Changes」をクリック

**✅ 完了**: SendGrid設定できた！

---

## 🎉 完了！

すべての作業が完了しました！

### アクセス方法

1. Renderダッシュボードで`carepass`のURLを確認
2. ブラウザでアクセス
3. ログインして動作確認

**例**: `https://carepass.onrender.com`

---

## 🆘 トラブルシューティング

### エラー1: デプロイに失敗する
**解決策**: 
- Renderのログを確認
- 環境変数が正しく設定されているか確認

### エラー2: メールが送信できない
**解決策**:
- SendGridのAPIキーが正しいか確認
- 送信者認証が完了しているか確認

### エラー3: データベースに接続できない
**解決策**:
- `DATABASE_URL`が正しいか確認
- PostgreSQLが起動しているか確認

---

## 📞 サポート

困ったときは：
- [Manusヘルプセンター](https://help.manus.im)

---

## ✅ 最終チェックリスト

- [ ] GitHubアカウント作成完了
- [ ] GitHubにプロジェクトアップロード完了
- [ ] Renderアカウント作成完了
- [ ] PostgreSQLデータベース作成完了
- [ ] Webサービスデプロイ完了
- [ ] SendGridアカウント作成完了
- [ ] 送信者認証完了
- [ ] APIキー作成完了
- [ ] Render環境変数設定完了
- [ ] 動作確認完了

---

**これで完了です！お疲れ様でした！** 🎉
