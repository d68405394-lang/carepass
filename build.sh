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
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@carepass.com', 'password123')
    print('✅ 管理者ユーザーが作成されました: admin/password123')
else:
    print('ℹ️ 管理者ユーザーは既に存在します')
"

echo "🎉 ビルドが正常に完了しました！"
echo "📱 アプリケーションにアクセス: https://your-app.onrender.com/"
echo "🔧 管理画面にアクセス: https://your-app.onrender.com/admin/"
