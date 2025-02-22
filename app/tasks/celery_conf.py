import os
from dotenv import load_dotenv

from celery import Celery

load_dotenv()

broker = f"amqp://{os.getenv('BROKER_NAME')}:{os.getenv('BROKER_PASS')}@{os.getenv('BROKER_HOST')}:{os.getenv('BROKER_PORT')}//"

celery = Celery(
    'tasks',
    broker=broker,
    include=['app.tasks.tasks'],
    backend='rpc://'
)