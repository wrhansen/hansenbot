web: gunicorn website.wsgi --log-file - --log-level info
worker: celery -A website worker -E
beat: celery -A website beat
