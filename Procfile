web: gunicorn FB_WebApp_Project.wsgi
release: |
  python manage.py collectstatic --noinput
  playwright install chromium
  python scripts/test_browser.py
