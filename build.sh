#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Copy frontend assets to static directory
mkdir -p staticfiles/assets
if [ -d "frontend/dist/assets" ]; then
    cp -r frontend/dist/assets/* staticfiles/assets/
fi

python manage.py collectstatic --no-input
python manage.py migrate
