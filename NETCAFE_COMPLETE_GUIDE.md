# ネットカフェ完結ガイド（自宅PC不要）

**所要時間**: 40分  
**難易度**: ⭐（超簡単！）  
**必要なもの**: スマホだけ！

---

## 🎯 作業の流れ

### 今（Manusで）
1. GitHub Personal Access Token取得（5分）
2. GitHubにプッシュ（2分）

### ネットカフェで
1. Renderでデプロイ（25分）
2. SendGrid設定（10分）
3. 動作確認（3分）

**合計**: 約45分

---

## 📱 今すぐやること（Manusで・7分）

### ステップ1: GitHub Personal Access Token取得（5分）

#### 1-1: GitHubにログイン
1. [GitHub](https://github.com/)にアクセス
2. ログイン

#### 1-2: Personal Access Token作成
1. 右上のアイコン→「Settings」をクリック
2. 左メニューの一番下「Developer settings」をクリック
3. 「Personal access tokens」→「Tokens (classic)」をクリック
4. 「Generate new token」→「Generate new token (classic)」をクリック
5. 以下を入力：
   - **Note**: `carepass`
   - **Expiration**: 30 days
   - **Select scopes**: `repo`（すべてにチェック）
6. 「Generate token」をクリック
7. **トークンをコピー**（一度しか表示されない！）

**⚠️ 重要**: トークンは`ghp_`で始まる長い文字列です。必ずコピーしてください。

**✅ 完了**: Personal Access Tokenを取得できた

---

### ステップ2: GitHubリポジトリ作成（2分）

#### 2-1: 新しいリポジトリ作成
1. GitHubのトップページに戻る
2. 右上の「+」→「New repository」をクリック
3. 以下を入力：
   - **Repository name**: `carepass`
   - **Description**: 福祉事業所向け管理システム Care-pass v3.0
   - **Public**を選択
   - **Initialize this repository with**は全てチェックなし
4. 「Create repository」をクリック

**✅ 完了**: リポジトリができた

---

### ステップ3: Manusサンドボックスから直接プッシュ（2分）

**私（Manus）に以下を教えてください:**
1. GitHubのユーザー名
2. Personal Access Token（`ghp_`で始まる文字列）

**例:**
- ユーザー名: `your-username`
- トークン: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

教えていただければ、私が直接GitHubにプッシュします。

**✅ 完了**: GitHubにプッシュできた

---

## 🏪 ネットカフェでの作業（38分）

### 準備

**このガイドをスマホに送る:**
- メールで自分宛に送信
- または、スクショしてスマホに送る

---

### ステップ1: Renderでデプロイ（25分）

#### 1-1: Renderにログイン（1分）
1. [Render](https://render.com/)にアクセス
2. 「Sign in with GitHub」をクリック
3. GitHubアカウントでログイン

---

#### 1-2: PostgreSQL作成（4分）
1. 「New +」→「PostgreSQL」をクリック
2. 以下を入力：
   - **Name**: `carepass-db`
   - **Database**: `carepass`
   - **User**: `carepass`
   - **Region**: Singapore
   - **Plan**: Free
3. 「Create Database」をクリック
4. 作成完了後、「Info」タブを開く
5. **Internal Database URL**をコピー（後で使う）

**✅ 完了**: データベースができた

---

#### 1-3: Webサービス作成（20分）
1. Renderのトップページに戻る
2. 「New +」→「Web Service」をクリック
3. 「carepass」リポジトリを選択
4. 「Connect」をクリック
5. 以下を入力：

| 項目 | 値 |
|:---|:---|
| **Name** | `carepass` |
| **Region** | Singapore |
| **Branch** | main |
| **Root Directory** | （空欄） |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt && cd frontend && pnpm install && pnpm run build && cd .. && python manage.py collectstatic --noinput` |
| **Start Command** | `python manage.py migrate && gunicorn myproject.wsgi:application` |
| **Plan** | Free |

6. 「Advanced」をクリック
7. 「Add Environment Variable」をクリックして、以下を追加：

**環境変数:**

| Key | Value |
|:---|:---|
| `SECRET_KEY` | `django-insecure-care-pass-v3-production-secret-key-2025` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `carepass.onrender.com` |
| `DATABASE_URL` | （1-2でコピーしたInternal Database URL） |
| `OPENAI_API_KEY` | （あなたのOpenAI APIキー） |

8. 「Create Web Service」をクリック
9. **デプロイ開始**（10-15分待つ）

**✅ 完了**: デプロイできた！

---

### ステップ2: SendGrid設定（10分）

#### 2-1: SendGridにログイン（1分）
1. [SendGrid](https://sendgrid.com/)にアクセス
2. ログイン（アカウントがない場合は「Start for Free」で作成）

---

#### 2-2: 送信者認証（4分）
1. 「Settings」→「Sender Authentication」をクリック
2. 「Single Sender Verification」をクリック
3. 以下を入力：
   - **From Name**: あなたの事業所名（例: 〇〇放課後等デイサービス）
   - **From Email Address**: あなたのメールアドレス
   - **Reply To**: あなたのメールアドレス
   - **Company Address**: 事業所住所
   - **Nickname**: carepass
4. 「Create」をクリック
5. **メールを確認して認証リンクをクリック**

**✅ 完了**: 送信者認証できた

---

#### 2-3: APIキー作成（5分）
1. 「Settings」→「API Keys」をクリック
2. 「Create API Key」をクリック
3. 以下を入力：
   - **API Key Name**: carepass
   - **API Key Permissions**: Full Access
4. 「Create & View」をクリック
5. **APIキーをコピー**（`SG.`で始まる文字列）

6. **Renderに戻る**
7. careapassのWebサービスを選択
8. 「Environment」タブをクリック
9. 「Add Environment Variable」をクリックして、以下を追加：

| Key | Value |
|:---|:---|
| `SENDGRID_API_KEY` | （コピーしたAPIキー） |
| `FROM_EMAIL` | （あなたのメールアドレス） |

10. 「Save Changes」をクリック
11. **自動的に再デプロイ開始**（3-5分待つ）

**✅ 完了**: SendGrid設定できた！

---

### ステップ3: 動作確認（3分）

1. Renderで`carepass`のURLをクリック
2. ブラウザで開く
3. ダッシュボードが表示されることを確認

**例**: `https://carepass.onrender.com`

**✅ 完了**: すべて完了！

---

## 📋 超シンプルチェックリスト

### 今（Manusで）
- [ ] GitHub Personal Access Token取得
- [ ] GitHubリポジトリ作成
- [ ] Manusにユーザー名とトークンを伝える
- [ ] GitHubにプッシュ完了
- [ ] このガイドをスマホに送る

### ネットカフェで
- [ ] Renderにログイン（1分）
- [ ] PostgreSQL作成（4分）
- [ ] Webサービス作成（20分）
- [ ] SendGridログイン（1分）
- [ ] 送信者認証（4分）
- [ ] APIキー作成と設定（5分）
- [ ] 動作確認（3分）

---

## ⏱️ 時間配分

| 作業 | 場所 | 時間 |
|:---|:---|---:|
| Personal Access Token取得 | Manus | 5分 |
| GitHubリポジトリ作成 | Manus | 2分 |
| GitHubにプッシュ | Manus | 2分 |
| Renderログイン | ネットカフェ | 1分 |
| PostgreSQL作成 | ネットカフェ | 4分 |
| Webサービス作成 | ネットカフェ | 20分 |
| SendGridログイン | ネットカフェ | 1分 |
| 送信者認証 | ネットカフェ | 4分 |
| APIキー作成 | ネットカフェ | 5分 |
| 動作確認 | ネットカフェ | 3分 |
| **合計** | | **47分** |

---

## 🆘 トラブルシューティング

### エラー1: デプロイに失敗する
**解決策**: 
- Renderのログを確認
- 環境変数が正しいか確認
- Build Commandが正しいか確認

### エラー2: メールが送信できない
**解決策**:
- SendGridの送信者認証が完了しているか確認
- APIキーが正しいか確認
- 環境変数`SENDGRID_API_KEY`と`FROM_EMAIL`が設定されているか確認

### エラー3: データベースに接続できない
**解決策**:
- `DATABASE_URL`が正しいか確認
- PostgreSQLが起動しているか確認

---

## 💡 ポイント

1. **自宅PC不要**: Manusサンドボックスから直接GitHubにプッシュ
2. **ネットカフェで完結**: 40分で全て完了
3. **コピペだけ**: 複雑な操作なし
4. **スマホで見ながら**: このガイドをスマホで見ながら作業

---

**これで完了です！ネットカフェだけで全て完結します！** 🚀

**次のステップ:**
1. GitHub Personal Access Tokenを取得
2. GitHubリポジトリを作成
3. 私（Manus）にユーザー名とトークンを伝える
4. このガイドをスマホに送る
5. ネットカフェに行く

何か質問があれば、今のうちに聞いてください！
