# 本番環境デプロイ手順書

## 概要

carepassアプリケーションのマルチテナントSaaSシステムを本番環境（Render）にデプロイし、サンプルデータを投入する手順を説明します。

## 前提条件

- GitHubリポジトリ: https://github.com/d68405394-lang/carepass.git
- Render: 自動デプロイが設定済み
- データベース: PostgreSQL (Neon)

## デプロイ状況

### ✅ 完了済み

1. **コードのプッシュ**: GitHubへのプッシュ完了
2. **マイグレーションファイル**: `billing_management/migrations/0001_initial.py`
3. **管理コマンド**: `billing_management/management/commands/load_sample_data.py`
4. **ドキュメント**:
   - MULTI_TENANT_IMPLEMENTATION.md
   - DEPLOYMENT_CHECKLIST.md
   - USER_GUIDE.md

### ⏳ 進行中

- Renderでの自動デプロイ（5〜10分）

## 本番環境でのサンプルデータ投入方法

### 方法1: Renderダッシュボードから実行（推奨）

1. Renderダッシュボードにログイン: https://dashboard.render.com/
2. carepassサービスを選択
3. 左メニューから「Manual Deploy」→「Deploy latest commit」をクリック
4. デプロイ完了後、「Console」タブを開く
5. 以下のコマンドを実行:

```bash
python manage.py load_sample_data
```

### 方法2: Render Web Serviceの「Run Command」機能を使用

1. Renderダッシュボードでcarepassサービスを選択
2. 「Settings」タブを開く
3. 「Build & Deploy」セクションで「Add Build Command」をクリック
4. 以下のコマンドを追加:

```bash
python manage.py migrate && python manage.py load_sample_data
```

5. 「Save Changes」をクリック
6. 「Manual Deploy」→「Deploy latest commit」で再デプロイ

### 方法3: 手動でユーザーを作成

管理画面から手動でユーザーと事業所を作成することもできます。

## サンプルデータ投入後の確認

### 1. 管理画面にアクセス

本番環境のURL + `/admin/` にアクセス

例: `https://carepass-xxxx.onrender.com/admin/`

### 2. スーパー管理者でログイン

- ユーザー名: `sample_superadmin`
- パスワード: `admin123`

### 3. データの確認

以下のデータが作成されていることを確認：

**事業所（3箇所）:**
- サンプル事業所A（東京） - SAMPLE01
- サンプル事業所B（大阪） - SAMPLE02
- サンプル事業所C（名古屋） - SAMPLE03

**ユーザー（8名）:**
- スーパー管理者: sample_superadmin / admin123
- 事業所管理者:
  - sample_admin_tokyo / admin123
  - sample_admin_osaka / admin123
  - sample_admin_nagoya / admin123
- スタッフ:
  - sample_staff_tokyo1 / staff123
  - sample_staff_tokyo2 / staff123
  - sample_staff_osaka1 / staff123
  - sample_staff_osaka2 / staff123

**利用者（5名）:**
- 東京: 田中 太郎、佐藤 花子
- 大阪: 鈴木 一郎、高橋 美咲
- 名古屋: 伊藤 健太

**職員（4名）:**
- 東京: 山田 太郎、山田 花子
- 大阪: 佐々木 次郎、佐々木 三郎

## テスト手順

### テスト1: スーパー管理者のテスト

1. `sample_superadmin` / `admin123` でログイン
2. 「利用者」をクリック
3. 全事業所の利用者（5名）が表示されることを確認

### テスト2: 事業所管理者のテスト（東京）

1. ログアウト
2. `sample_admin_tokyo` / `admin123` でログイン
3. 「利用者」をクリック
4. 東京の利用者のみ（2名）が表示されることを確認
5. 大阪・名古屋の利用者が表示されないことを確認

### テスト3: 事業所管理者のテスト（大阪）

1. ログアウト
2. `sample_admin_osaka` / `admin123` でログイン
3. 「利用者」をクリック
4. 大阪の利用者のみ（2名）が表示されることを確認

### テスト4: スタッフのテスト

1. ログアウト
2. `sample_staff_tokyo1` / `staff123` でログイン
3. 「利用者」をクリック
4. 東京の利用者のみ（2名）が表示されることを確認
5. 利用者の詳細ページで「削除」ボタンが表示されないことを確認

## トラブルシューティング

### 問題1: コマンドが見つからない

**症状:**
```
Unknown command: 'load_sample_data'
```

**原因:** マイグレーションが適用されていない、またはコードがデプロイされていない

**解決策:**
1. Renderダッシュボードで最新のデプロイを確認
2. ログを確認してエラーがないか確認
3. 手動で再デプロイを実行

### 問題2: データベース接続エラー

**症状:**
```
could not connect to server
```

**原因:** データベースの接続情報が正しくない

**解決策:**
1. Renderの環境変数を確認
2. `DATABASE_URL` が正しく設定されているか確認
3. Neonデータベースが起動しているか確認

### 問題3: パーミッションエラー

**症状:** ログイン後に「You don't have permission to view or edit anything.」と表示される

**原因:** ユーザーにパーミッションが付与されていない

**解決策:**
1. `load_sample_data` コマンドを再実行
2. または、スーパー管理者でログインして手動でパーミッションを付与

## 次のステップ

デプロイとテストが完了したら：

1. **パスワードの変更**: 本番環境では必ずパスワードを変更してください
2. **実際のデータ投入**: サンプルデータを削除して実際のデータを投入
3. **監視の設定**: Renderのログとメトリクスを定期的に確認
4. **バックアップの確認**: データベースのバックアップが正常に動作しているか確認

## 参考ドキュメント

- [MULTI_TENANT_IMPLEMENTATION.md](./MULTI_TENANT_IMPLEMENTATION.md): 実装の詳細
- [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md): デプロイチェックリスト
- [USER_GUIDE.md](./USER_GUIDE.md): ユーザーガイド

## サポート

問題が発生した場合は、以下の情報を含めて報告してください：

- エラーメッセージ
- 実行したコマンド
- Renderのログ
- ブラウザのコンソールログ（該当する場合）

---

**最終更新日:** 2025年12月27日
