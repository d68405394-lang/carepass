#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Creating frontend assets directory..."
mkdir -p staticfiles/assets

echo "Copying frontend assets if they exist..."
if [ -d "frontend/dist/assets" ]; then
    cp -r frontend/dist/assets/* staticfiles/assets/
    echo "Frontend assets copied successfully"
else
    echo "No frontend assets found, creating placeholder assets..."
    mkdir -p staticfiles/assets
    echo "/* Placeholder CSS */" > staticfiles/assets/style.css
fi

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate

echo "Creating superuser if it doesn't exist..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'password123')
    print('Superuser created: admin/password123')
else:
    print('Superuser already exists')
"

echo "Build completed successfully!"
