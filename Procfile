web: gunicorn website.wsgi --log-file -
worker: celery -A website worker -E
