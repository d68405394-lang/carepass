# 🔒 Care Pass - セキュリティ運用ガイド

**最終更新:** 2025年12月22日  
**対象:** Care Pass 福祉管理システム

---

## 📋 目次

1. [セキュリティ概要](#セキュリティ概要)
2. [環境変数の設定](#環境変数の設定)
3. [管理者アカウント管理](#管理者アカウント管理)
4. [デプロイ手順](#デプロイ手順)
5. [セキュリティチェックリスト](#セキュリティチェックリスト)
6. [インシデント対応](#インシデント対応)
7. [定期メンテナンス](#定期メンテナンス)

---

## 🛡️ セキュリティ概要

### 実装されたセキュリティ対策

#### 1. 秘密情報の保護
- ✅ 全ての機密情報を環境変数で管理
- ✅ `.gitignore`で`.env`ファイルを除外
- ✅ ハードコードされたパスワードを削除

#### 2. 認証・認可
- ✅ Django標準の認証システム
- ✅ 強力なパスワードポリシー（最小12文字）
- ✅ セッションタイムアウト（1時間）

#### 3. 通信の暗号化
- ✅ HTTPS強制リダイレクト（本番環境）
- ✅ HSTS（HTTP Strict Transport Security）
- ✅ セキュアCookie設定

#### 4. 脆弱性対策
- ✅ SQLインジェクション対策（Django ORM）
- ✅ XSS対策（テンプレート自動エスケープ）
- ✅ CSRF対策（Django標準機能）
- ✅ セキュリティヘッダー設定

---

## 🔐 環境変数の設定

### Renderダッシュボードでの設定手順

1. **Renderダッシュボードにログイン**
   - https://dashboard.render.com/

2. **サービスを選択**
   - `carepass` サービスをクリック

3. **Environment タブを開く**
   - 左メニューから「Environment」を選択

4. **以下の環境変数を追加**

#### 必須の環境変数

```bash
# Django SECRET_KEY（必須）
SECRET_KEY=<強力なランダム文字列>
# 生成方法: openssl rand -base64 50

# 管理者パスワード（必須）
ADMIN_PASSWORD=<強力なランダムパスワード>
# 生成方法: openssl rand -base64 24

# 管理者ユーザー名（オプション、デフォルト: admin）
ADMIN_USERNAME=admin

# 管理者メールアドレス（オプション）
ADMIN_EMAIL=admin@carepass.com

# DEBUG設定（本番環境では必ずFalse）
DEBUG=False

# 許可するホスト名
ALLOWED_HOSTS=carepass.onrender.com,localhost,127.0.0.1
```

#### Renderが自動設定する環境変数

```bash
# データベースURL（Renderが自動設定）
DATABASE_URL=postgresql://...

# 外部URL（Renderが自動設定）
RENDER_EXTERNAL_URL=https://carepass.onrender.com
```

---

## 👤 管理者アカウント管理

### 初回セットアップ

1. **環境変数を設定**
   ```bash
   ADMIN_USERNAME=admin
   ADMIN_EMAIL=admin@carepass.com
   ADMIN_PASSWORD=<強力なランダムパスワード>
   ```

2. **デプロイ実行**
   - GitHubにプッシュすると自動デプロイ
   - ビルドログで管理者ユーザー作成を確認

3. **管理画面にログイン**
   - URL: https://carepass.onrender.com/admin/
   - ユーザー名: `admin`（または設定した値）
   - パスワード: 環境変数で設定した値

### パスワード変更

#### 方法1: 管理画面から変更
1. https://carepass.onrender.com/admin/ にログイン
2. 右上の「パスワード変更」をクリック
3. 新しいパスワードを設定

#### 方法2: コマンドラインから変更
```bash
# Renderのシェルにアクセス
python manage.py changepassword admin
```

### パスワードポリシー

- ✅ 最小12文字
- ✅ 英数字と記号を含む
- ✅ 一般的なパスワードは使用不可
- ✅ ユーザー名と類似したパスワードは使用不可

---

## 🚀 デプロイ手順

### 1. ローカルでの変更

```bash
# コードを修正
git add .
git commit -m "機能追加またはバグ修正"
git push origin main
```

### 2. Renderでの自動デプロイ

- GitHubにプッシュすると自動的にデプロイが開始
- ビルドログを確認: https://dashboard.render.com/

### 3. デプロイ後の確認

```bash
# ヘルスチェック
curl https://carepass.onrender.com/api/clients/

# 管理画面アクセス確認
curl -I https://carepass.onrender.com/admin/
```

---

## ✅ セキュリティチェックリスト

### デプロイ前

- [ ] 環境変数`SECRET_KEY`が設定されている
- [ ] 環境変数`ADMIN_PASSWORD`が設定されている
- [ ] `DEBUG=False`に設定されている
- [ ] `.env`ファイルが`.gitignore`に含まれている
- [ ] ハードコードされた機密情報がない

### デプロイ後

- [ ] HTTPS接続が有効
- [ ] 管理画面にログインできる
- [ ] APIエンドポイントが正常に動作
- [ ] セキュリティヘッダーが設定されている
- [ ] エラーログを確認

### 定期チェック（月次）

- [ ] 依存パッケージの更新確認
- [ ] セキュリティパッチの適用
- [ ] アクセスログの確認
- [ ] 不審なアクティビティの確認

---

## 🚨 インシデント対応

### 不正アクセスが疑われる場合

#### 即座に実施

1. **管理者パスワードの変更**
   ```bash
   # Renderダッシュボードで環境変数を更新
   ADMIN_PASSWORD=<新しい強力なパスワード>
   ```

2. **SECRET_KEYの変更**
   ```bash
   # 新しいSECRET_KEYを生成
   openssl rand -base64 50
   
   # Renderダッシュボードで環境変数を更新
   SECRET_KEY=<新しいキー>
   ```

3. **全セッションの無効化**
   - SECRET_KEY変更により自動的に全セッションが無効化

4. **アクセスログの確認**
   - Renderダッシュボードでログを確認
   - 不審なIPアドレスを特定

#### 事後対応

1. **インシデントレポート作成**
   - 発生日時
   - 影響範囲
   - 対応内容
   - 再発防止策

2. **セキュリティ監査の実施**
   - コードレビュー
   - 脆弱性スキャン
   - ペネトレーションテスト

---

## 🔧 定期メンテナンス

### 週次タスク

- [ ] アプリケーションの動作確認
- [ ] エラーログの確認
- [ ] データベースバックアップの確認

### 月次タスク

- [ ] 依存パッケージの更新
  ```bash
  pip list --outdated
  pip install --upgrade <package>
  ```

- [ ] セキュリティパッチの適用
  ```bash
  pip install --upgrade django
  ```

- [ ] アクセスログの分析
- [ ] パフォーマンスモニタリング

### 四半期タスク

- [ ] 包括的なセキュリティ監査
- [ ] ペネトレーションテスト
- [ ] ディザスタリカバリテスト
- [ ] セキュリティポリシーの見直し

---

## 📞 サポート情報

### 緊急連絡先

- **技術サポート:** [メールアドレス]
- **セキュリティインシデント:** [メールアドレス]

### 参考資料

- [Django セキュリティドキュメント](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Render セキュリティベストプラクティス](https://render.com/docs/security)

---

## 📝 変更履歴

| 日付 | バージョン | 変更内容 |
|------|-----------|---------|
| 2025-12-22 | 1.0.0 | 初版作成 - セキュリティ強化実施 |

---

**このドキュメントは機密情報を含みます。適切に管理してください。**
