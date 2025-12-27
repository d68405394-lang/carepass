#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🔧 Care Pass デプロイメント開始..."

echo "📦 Python依存関係のインストール..."
pip install -r requirements.txt

echo "📁 静的ファイルディレクトリの作成..."
mkdir -p staticfiles/assets

echo "🎨 フロントエンドアセットのコピー..."
if [ -d "frontend/dist/assets" ]; then
    cp -r frontend/dist/assets/* staticfiles/assets/
    echo "✅ フロントエンドアセットがコピーされました"
else
    echo "ℹ️ フロントエンドアセットが見つからないため、プレースホルダーを作成..."
    mkdir -p staticfiles/assets
    echo "/* Placeholder CSS */" > staticfiles/assets/style.css
fi

echo "🗂️ 静的ファイルの収集..."
python manage.py collectstatic --no-input

echo "🗄️ データベースマイグレーションの実行..."
python manage.py migrate

echo "👤 管理者ユーザーの作成..."

# 環境変数の確認とデバッグ出力
echo "🔍 環境変数の確認:"
echo "ADMIN_USERNAME: ${ADMIN_USERNAME:-admin}"
echo "ADMIN_EMAIL: ${ADMIN_EMAIL:-admin@carepass.com}"
if [ -z "$ADMIN_PASSWORD" ]; then
    echo "⚠️ ADMIN_PASSWORD: 未設定"
else
    echo "✅ ADMIN_PASSWORD: 設定済み（長さ: ${#ADMIN_PASSWORD}文字）"
fi

# 管理者ユーザー作成スクリプト
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
import os

User = get_user_model()
admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
admin_email = os.environ.get('ADMIN_EMAIL', 'admin@carepass.com')
admin_password = os.environ.get('ADMIN_PASSWORD')

print(f"📝 管理者ユーザー作成処理開始...")
print(f"   ユーザー名: {admin_username}")
print(f"   メール: {admin_email}")

if not admin_password:
    print('❌ エラー: ADMIN_PASSWORD環境変数が設定されていません')
    print('⚠️ セキュリティのため、管理者ユーザーの作成をスキップします')
    print('⚠️ Renderダッシュボードで ADMIN_PASSWORD を設定してください')
else:
    print(f'✅ ADMIN_PASSWORD: 設定済み（長さ: {len(admin_password)}文字）')
    
    # 既存ユーザーの確認
    if User.objects.filter(username=admin_username).exists():
        print(f'ℹ️ 管理者ユーザー {admin_username} は既に存在します')
        # 既存ユーザーのパスワードを更新
        user = User.objects.get(username=admin_username)
        user.set_password(admin_password)
        user.save()
        print(f'✅ 管理者ユーザー {admin_username} のパスワードを更新しました')
    else:
        # 新規ユーザーを作成
        try:
            User.objects.create_superuser(admin_username, admin_email, admin_password)
            print(f'✅ 管理者ユーザーが作成されました: {admin_username}')
            print('ℹ️ パスワードは環境変数 ADMIN_PASSWORD で設定されています')
        except Exception as e:
            print(f'❌ エラー: 管理者ユーザーの作成に失敗しました: {e}')

print('👤 管理者ユーザー作成処理完了')
EOF

echo ""
echo "📊 サンプルデータの投入..."
python manage.py load_sample_data

echo "🎉 ビルドが正常に完了しました！"
echo "📱 アプリケーションにアクセス: https://carepass.onrender.com/"
echo "🔧 管理画面にアクセス: https://carepass.onrender.com/admin/"
