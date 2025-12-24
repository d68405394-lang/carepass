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

# 環境変数から管理者情報を取得（未設定の場合はランダム生成）
ADMIN_USERNAME="${ADMIN_USERNAME:-admin}"
ADMIN_EMAIL="${ADMIN_EMAIL:-admin@carepass.com}"
ADMIN_PASSWORD="${ADMIN_PASSWORD:-$(openssl rand -base64 24)}"

python manage.py shell -c "
from django.contrib.auth import get_user_model
import os
User = get_user_model()
admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
admin_email = os.environ.get('ADMIN_EMAIL', 'admin@carepass.com')
admin_password = os.environ.get('ADMIN_PASSWORD')

if not admin_password:
    print('⚠️ 警告: ADMIN_PASSWORD環境変数が設定されていません')
    print('⚠️ セキュリティのため、管理者ユーザーの作成をスキップします')
    print('⚠️ Renderダッシュボードで ADMIN_PASSWORD を設定してください')
else:
    if not User.objects.filter(username=admin_username).exists():
        User.objects.create_superuser(admin_username, admin_email, admin_password)
        print(f'✅ 管理者ユーザーが作成されました: {admin_username}')
        print('ℹ️ パスワードは環境変数 ADMIN_PASSWORD で設定されています')
    else:
        print(f'ℹ️ 管理者ユーザー {admin_username} は既に存在します')
"

echo "🎉 ビルドが正常に完了しました！"
echo "📱 アプリケーションにアクセス: https://your-app.onrender.com/"
echo "🔧 管理画面にアクセス: https://your-app.onrender.com/admin/"
