# ネットカフェ作業 最短30分ガイド

**所要時間**: 最短30分  
**難易度**: ⭐（超簡単！）  
**必要なもの**: スマホだけ！

---

## 📱 今すぐやること（自宅で・5分）

### ステップ1: GitHubにプッシュ

```bash
# 自宅のPCで実行（コピー＆ペーストするだけ）
cd /home/ubuntu
git remote add origin https://github.com/あなたのユーザー名/carepass.git
git push -u origin main
```

**⚠️ エラーが出た場合:**
```bash
# リモートが既に存在する場合
git remote remove origin
git remote add origin https://github.com/あなたのユーザー名/carepass.git
git push -u origin main
```

**✅ 完了**: GitHubにアップロードできた

---

### ステップ2: このガイドをスマホに送る

**方法A: メールで送信**
1. このファイルをメールで自分宛に送信
2. スマホで開く

**方法B: スクショ**
1. この画面をスクショ
2. スマホに送る

**✅ 完了**: スマホで見られる

---

## 🏪 ネットカフェでの作業（25分）

### 🎯 作業の流れ（3ステップだけ！）

1. **Renderでデプロイ**（15分）
2. **SendGrid設定**（10分）
3. **動作確認**（5分）

---

## ステップ1: Renderでデプロイ（15分）

### 1-1: Renderにログイン（1分）

1. [Render](https://render.com/)にアクセス
2. 「Sign in with GitHub」をクリック
3. GitHubアカウントでログイン

---

### 1-2: PostgreSQL作成（3分）

1. 「New +」→「PostgreSQL」をクリック
2. 以下をコピペ：
   - **Name**: `carepass-db`
   - **Region**: Singapore
   - **Plan**: Free
3. 「Create Database」をクリック
4. **Internal Database URL**をコピー（後で使う）

**✅ 完了**: データベースができた

---

### 1-3: Webサービス作成（11分）

1. 「New +」→「Web Service」をクリック
2. 「carepass」リポジトリを選択
3. 以下をコピペ：

| 項目 | 値 |
|:---|:---|
| **Name** | `carepass` |
| **Region** | Singapore |
| **Branch** | main |
| **Build Command** | `pip install -r requirements.txt && cd frontend && pnpm install && pnpm run build && cd .. && python manage.py collectstatic --noinput` |
| **Start Command** | `python manage.py migrate && gunicorn myproject.wsgi:application` |

4. 「Advanced」をクリック
5. 環境変数を追加（以下をコピペ）:

```
SECRET_KEY=django-insecure-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEBUG=False
ALLOWED_HOSTS=carepass.onrender.com
DATABASE_URL=（1-2でコピーしたURL）
OPENAI_API_KEY=（あなたのOpenAI APIキー）
```

6. 「Create Web Service」をクリック
7. **待つ**（10-15分）

**✅ 完了**: デプロイできた！

---

## ステップ2: SendGrid設定（10分）

### 2-1: SendGridにログイン（1分）

1. [SendGrid](https://sendgrid.com/)にアクセス
2. ログイン（アカウントがない場合は作成）

---

### 2-2: 送信者認証（4分）

1. 「Settings」→「Sender Authentication」
2. 「Single Sender Verification」
3. 以下を入力：
   - **From Name**: あなたの事業所名
   - **From Email**: あなたのメールアドレス
   - **Reply To**: あなたのメールアドレス
4. 「Create」をクリック
5. **メールを確認して認証リンクをクリック**

**✅ 完了**: 送信者認証できた

---

### 2-3: APIキー作成（5分）

1. 「Settings」→「API Keys」
2. 「Create API Key」をクリック
3. 以下を入力：
   - **Name**: carepass
   - **Permissions**: Full Access
4. 「Create & View」をクリック
5. **APIキーをコピー**

6. **Renderに戻る**
7. careapassのWebサービスを選択
8. 「Environment」タブ
9. 環境変数を追加：

```
SENDGRID_API_KEY=（コピーしたAPIキー）
FROM_EMAIL=（あなたのメールアドレス）
```

10. 「Save Changes」をクリック

**✅ 完了**: SendGrid設定できた！

---

## ステップ3: 動作確認（5分）

1. Renderで`carepass`のURLをクリック
2. ブラウザで開く
3. ログインして確認

**例**: `https://carepass.onrender.com`

**✅ 完了**: すべて完了！

---

## 📋 超シンプルチェックリスト

### 自宅で（5分）
- [ ] GitHubにプッシュ完了
- [ ] このガイドをスマホで見られる

### ネットカフェで（25分）
- [ ] Renderにログイン（1分）
- [ ] PostgreSQL作成（3分）
- [ ] Webサービス作成（11分）
- [ ] SendGridログイン（1分）
- [ ] 送信者認証（4分）
- [ ] APIキー作成と設定（5分）
- [ ] 動作確認（5分）

---

## 🆘 エラーが出たら

### エラー1: GitHubにプッシュできない
**解決策**: 
```bash
git remote remove origin
git remote add origin https://github.com/あなたのユーザー名/carepass.git
git push -u origin main
```

### エラー2: デプロイに失敗する
**解決策**: 
- Renderのログを確認
- 環境変数が正しいか確認

### エラー3: メールが送信できない
**解決策**:
- SendGridの送信者認証を確認
- APIキーが正しいか確認

---

## 💡 時短テクニック

### 1. 環境変数をメモ帳に準備
自宅で以下をメモ帳にコピペしておく：

```
SECRET_KEY=django-insecure-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEBUG=False
ALLOWED_HOSTS=carepass.onrender.com
DATABASE_URL=（後で入力）
OPENAI_API_KEY=（あなたのAPIキー）
SENDGRID_API_KEY=（後で入力）
FROM_EMAIL=（あなたのメールアドレス）
```

### 2. スマホでこのガイドを開いておく
- ネットカフェでPCとスマホの両方を使う
- スマホで手順を見ながら、PCで作業

### 3. デプロイ中に次の作業
- Renderのデプロイ中（10-15分）にSendGridの設定を進める

---

## ⏱️ 時間配分

| 作業 | 時間 | 累計 |
|:---|---:|---:|
| Renderログイン | 1分 | 1分 |
| PostgreSQL作成 | 3分 | 4分 |
| Webサービス作成 | 11分 | 15分 |
| SendGridログイン | 1分 | 16分 |
| 送信者認証 | 4分 | 20分 |
| APIキー作成 | 5分 | 25分 |
| 動作確認 | 5分 | **30分** |

---

**これで完了です！最短30分でデプロイできます！** 🚀

**ポイント**: 
- コピペだけ
- 3ステップだけ
- スマホで見ながら作業

何か質問があれば、今のうちに聞いてください！
