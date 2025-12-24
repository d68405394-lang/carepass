# 🚀 Render 環境変数設定ガイド

**重要:** デプロイ後、必ず以下の環境変数を設定してください。

---

## 📋 設定手順

### 1. Renderダッシュボードにアクセス

https://dashboard.render.com/

### 2. サービスを選択

`carepass` サービスをクリック

### 3. Environment タブを開く

左メニューから「Environment」を選択

### 4. 以下の環境変数を追加

---

## 🔑 必須の環境変数

### SECRET_KEY（必須）

**説明:** Djangoのセッション暗号化に使用される秘密鍵

**生成方法:**
```bash
openssl rand -base64 50
```

**設定例:**
```
Key: SECRET_KEY
Value: KAHvjm/K66CBDVnbAYWhyf/CNKuxDgi7/iqgX7uwnkJnGrZb9AgpDHhWrK5sPMiISWA=
```

⚠️ **注意:** 上記の値は例です。必ず新しい値を生成してください。

---

### ADMIN_PASSWORD（必須）

**説明:** 管理者アカウントのパスワード

**生成方法:**
```bash
openssl rand -base64 24
```

**設定例:**
```
Key: ADMIN_PASSWORD
Value: ywjmKDRoWazmdSz6j/F/xjwq/T3dZwfj
```

⚠️ **注意:** 
- 上記の値は例です。必ず新しい値を生成してください。
- このパスワードは安全な場所に保管してください。
- 管理画面ログイン時に使用します。

---

### ADMIN_USERNAME（オプション）

**説明:** 管理者アカウントのユーザー名

**デフォルト値:** `admin`

**設定例:**
```
Key: ADMIN_USERNAME
Value: admin
```

---

### ADMIN_EMAIL（オプション）

**説明:** 管理者アカウントのメールアドレス

**デフォルト値:** `admin@carepass.com`

**設定例:**
```
Key: ADMIN_EMAIL
Value: admin@carepass.com
```

---

### DEBUG（必須）

**説明:** デバッグモードの有効/無効

**本番環境では必ず `False` に設定**

**設定例:**
```
Key: DEBUG
Value: False
```

---

### ALLOWED_HOSTS（推奨）

**説明:** アクセスを許可するホスト名

**設定例:**
```
Key: ALLOWED_HOSTS
Value: carepass.onrender.com,localhost,127.0.0.1
```

---

## 🤖 Renderが自動設定する環境変数

以下の環境変数はRenderが自動的に設定するため、手動設定は不要です：

- `DATABASE_URL` - PostgreSQLデータベース接続URL
- `RENDER_EXTERNAL_URL` - アプリケーションの公開URL

---

## ✅ 設定完了後の確認

### 1. 環境変数が正しく設定されているか確認

Renderダッシュボードの「Environment」タブで以下を確認：

- [ ] `SECRET_KEY` が設定されている
- [ ] `ADMIN_PASSWORD` が設定されている
- [ ] `DEBUG` が `False` に設定されている

### 2. 再デプロイ

環境変数を追加/変更した後、「Manual Deploy」ボタンをクリックして再デプロイ

### 3. ビルドログを確認

デプロイ中のログで以下を確認：

```
✅ 管理者ユーザーが作成されました: admin
ℹ️ パスワードは環境変数 ADMIN_PASSWORD で設定されています
```

### 4. 管理画面にログイン

https://carepass.onrender.com/admin/

- **ユーザー名:** 環境変数 `ADMIN_USERNAME` の値（デフォルト: `admin`）
- **パスワード:** 環境変数 `ADMIN_PASSWORD` の値

---

## 🚨 トラブルシューティング

### エラー: "SECRET_KEY環境変数が設定されていません"

**原因:** `SECRET_KEY` 環境変数が設定されていない

**解決方法:**
1. Renderダッシュボードで `SECRET_KEY` を追加
2. 再デプロイを実行

---

### エラー: "管理者ユーザーの作成をスキップします"

**原因:** `ADMIN_PASSWORD` 環境変数が設定されていない

**解決方法:**
1. Renderダッシュボードで `ADMIN_PASSWORD` を追加
2. 再デプロイを実行

---

### 管理画面にログインできない

**原因1:** パスワードが間違っている

**解決方法:**
1. Renderダッシュボードで `ADMIN_PASSWORD` を確認
2. 正しいパスワードでログインを試行

**原因2:** 管理者ユーザーが作成されていない

**解決方法:**
1. `ADMIN_PASSWORD` 環境変数が設定されているか確認
2. 再デプロイを実行
3. ビルドログで管理者ユーザー作成を確認

---

## 📝 環境変数の管理

### セキュリティベストプラクティス

1. ✅ 環境変数は安全な場所に保管（パスワードマネージャーなど）
2. ✅ 定期的にパスワードを変更（3ヶ月ごと推奨）
3. ✅ 環境変数をGitHubにコミットしない
4. ✅ 開発環境と本番環境で異なる値を使用

### パスワード変更手順

1. 新しいパスワードを生成
   ```bash
   openssl rand -base64 24
   ```

2. Renderダッシュボードで `ADMIN_PASSWORD` を更新

3. 再デプロイを実行

4. 新しいパスワードでログイン確認

---

## 📞 サポート

問題が解決しない場合は、以下を確認してください：

- Renderのビルドログ
- アプリケーションログ
- データベース接続状態

---

**このガイドに従って環境変数を設定することで、セキュアなアプリケーション運用が可能になります。**
