web: gunicorn ai_chatbot.wsgi

#!/bin/bash

python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn ai_chatbot.wsgi:application --bind 0.0.0.0:$PORT

