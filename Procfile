web:python manage.py runserver
web: gunicorn gemmeState.wsgi --log-file -
worker: python worker.py
heroku ps:scale web=1

