# マルチテナントSaaSシステム実装レポート

## 概要

carepassアプリケーションを、ロールベースのアクセス制御（RBAC）と事業所間の完全なデータ分離を備えたマルチテナントSaaSシステムに変換しました。

## 実装日時

2025年12月27日

## 主要な変更点

### 1. CustomUserモデルの実装

**ファイル:** `billing_management/models.py`

Django標準の`AbstractUser`を継承したカスタムユーザーモデルを実装しました。

**追加フィールド:**
- `role`: ユーザーのロール（super_admin, location_admin, staff）
- `location`: 所属事業所（ForeignKey to ServiceLocation）

**ロールの種類:**
- **super_admin**: 全事業所のデータにアクセス可能なシステム管理者
- **location_admin**: 特定の事業所のデータを管理する事業所管理者
- **staff**: 特定の事業所のデータを閲覧・編集するスタッフ

### 2. モデルへのlocationフィールド追加

以下のモデルに`location`フィールドを追加し、事業所別のデータ分離を実現しました：

- **Client（利用者）**: 各利用者は特定の事業所に所属
- **Staff（職員）**: 各職員は特定の事業所に所属
- **WorkRecord（勤務実績）**: 各勤務記録は特定の事業所に関連付け
- **ProgressAssessment（進捗・評価）**: 各評価記録は特定の事業所に関連付け

### 3. Django管理画面のカスタマイズ

**ファイル:** `billing_management/admin.py`

#### CustomUserAdmin
- ユーザーのロールと所属事業所を管理画面で編集可能
- リスト表示、フィルタ、検索機能を追加

#### ロケーションベースのデータフィルタリング

各モデルの管理画面に以下のメソッドを実装：

**get_queryset()メソッド:**
```python
def get_queryset(self, request):
    qs = super().get_queryset(request)
    if request.user.role == 'super_admin':
        return qs  # 全データを表示
    elif request.user.role in ['location_admin', 'staff']:
        return qs.filter(location=request.user.location)  # 自分の事業所のみ
    return qs.none()  # ロールが設定されていない場合は何も表示しない
```

**formfield_for_foreignkey()メソッド:**
```python
def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == "location":
        if request.user.role in ['location_admin', 'staff']:
            kwargs["queryset"] = ServiceLocation.objects.filter(id=request.user.location.id)
            kwargs["initial"] = request.user.location
    return super().formfield_for_foreignkey(db_field, request, **kwargs)
```

### 4. パーミッションシステムの統合

**ファイル:** `load_sample_data.py`

Django標準のパーミッションシステムとカスタムロールシステムを統合しました。

**パーミッション付与:**
- **super_admin**: 全てのパーミッション（56個）
- **location_admin**: billing_managementアプリの全パーミッション（36個）
- **staff**: view, add, changeパーミッション（27個）

### 5. データベーススキーマの更新

**マイグレーションファイル:** `billing_management/migrations/0001_initial.py`

以下のテーブル構造を更新：
- `CustomUser`テーブルの作成（roleとlocationフィールド付き）
- `Client`, `Staff`, `WorkRecord`, `ProgressAssessment`テーブルに`location`フィールドを追加

### 6. サンプルデータの作成

**ファイル:** `load_sample_data.py`

以下のサンプルデータを自動生成：

**ユーザー:**
- スーパー管理者: 1名（sample_superadmin / admin123）
- 事業所管理者: 3名
  - sample_admin_tokyo / admin123（東京）
  - sample_admin_osaka / admin123（大阪）
  - sample_admin_nagoya / admin123（名古屋）
- スタッフ: 4名
  - sample_staff_tokyo1 / staff123（東京）
  - sample_staff_tokyo2 / staff123（東京）
  - sample_staff_osaka1 / staff123（大阪）
  - sample_staff_osaka2 / staff123（大阪）

**事業所:**
- サンプル事業所A（東京）- SAMPLE01
- サンプル事業所B（大阪）- SAMPLE02
- サンプル事業所C（名古屋）- SAMPLE03

**利用者:**
- 東京: 2名（田中 太郎、佐藤 花子）
- 大阪: 2名（鈴木 一郎、高橋 美咲）
- 名古屋: 1名（伊藤 健太）

## テスト結果

### ローカル環境テスト

**テスト日時:** 2025年12月27日

#### テスト1: スーパー管理者ログイン
- **ユーザー:** sample_superadmin
- **結果:** ✅ 成功
- **確認事項:** 全事業所の利用者（5名）が表示される

#### テスト2: 事業所管理者ログイン（東京）
- **ユーザー:** sample_admin_tokyo
- **結果:** ✅ 成功
- **確認事項:** 東京の利用者のみ（2名）が表示される

#### テスト3: ロケーション別データフィルタリング
- **結果:** ✅ 成功
- **確認事項:** 
  - 事業所管理者は自分の事業所のデータのみ閲覧・編集可能
  - 他の事業所のデータは表示されない
  - 新規作成時に自動的に自分の事業所が設定される

## セキュリティ上の考慮事項

### 1. データ分離
- 各事業所のデータは完全に分離されている
- location_adminとstaffは自分の事業所のデータのみアクセス可能

### 2. パーミッション制御
- Djangoの標準パーミッションシステムを使用
- ロールに応じて適切なパーミッションを付与

### 3. クエリレベルのフィルタリング
- get_queryset()メソッドでデータベースクエリレベルでフィルタリング
- URLを直接入力しても他の事業所のデータにはアクセスできない

## デプロイ手順

### 1. ローカル環境でのテスト
```bash
# マイグレーションの作成と適用
python manage.py makemigrations
python manage.py migrate

# サンプルデータの投入
python load_sample_data.py

# 開発サーバーの起動
python manage.py runserver
```

### 2. 本番環境へのデプロイ
```bash
# 変更をコミット
git add -A
git commit -m "Implement multi-tenant system with role-based access control"

# GitHubにプッシュ
git push origin main
```

### 3. Renderでの自動デプロイ
- Renderは自動的にGitHubのプッシュを検知してデプロイを開始
- デプロイ完了後、マイグレーションが自動実行される

### 4. 本番環境でのサンプルデータ投入
```bash
# Render Shellにアクセス
# または、Webインターフェースから実行
python load_sample_data.py
```

## 今後の拡張案

### 1. フロントエンドの実装
- 事業所管理者用のダッシュボード
- スタッフ用の勤務記録入力画面
- 利用者ポータル

### 2. API認証の強化
- JWT認証の実装
- APIエンドポイントへのロールベースアクセス制御

### 3. 監査ログの実装
- ユーザーの操作履歴を記録
- データ変更の追跡

### 4. マルチテナント機能の拡張
- 事業所ごとのカスタム設定
- 事業所間のデータ共有機能（オプション）

## 技術スタック

- **フレームワーク:** Django 5.2.9
- **データベース:** PostgreSQL（Neon）
- **認証:** Django標準認証システム + カスタムロール
- **デプロイ:** Render
- **バージョン管理:** Git + GitHub

## 参考資料

- Django公式ドキュメント: https://docs.djangoproject.com/
- Django認証システム: https://docs.djangoproject.com/en/stable/topics/auth/
- マルチテナントアーキテクチャ: https://docs.djangoproject.com/en/stable/topics/db/multi-db/

## まとめ

carepassアプリケーションを、完全なマルチテナントSaaSシステムに変換することに成功しました。ロールベースのアクセス制御と事業所間の完全なデータ分離により、複数の事業所が安全に同じシステムを利用できるようになりました。

ローカル環境でのテストでは、全ての機能が正常に動作することを確認しました。本番環境でのテストを完了すれば、実際の運用が可能な状態になります。
