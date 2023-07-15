docker-compose up 

celery -A upscale.celery worker --loglevel=info


python flask_app.py
