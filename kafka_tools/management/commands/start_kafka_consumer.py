import asyncio
import importlib
import json
import logging
import time
from django.conf import settings
from django.core.management.base import BaseCommand
from aiokafka import AIOKafkaConsumer
from jsonschema.exceptions import ValidationError
from kafka.errors import KafkaError, ConnectionError, NodeNotReadyError
from kafka_tools.message_format import validate_payload
from kafka_tools.models import KafkaGroup


loop = asyncio.get_event_loop()


class Command(BaseCommand):
    help = 'Запуск прослушивания указанных топиков в кафке'

    def handle(self, *args, **options):
        if not getattr(settings, 'KAFKA_TOOLS_MESSAGES_HANDLER', None):
            logging.error('KAFKA_TOOLS_MESSAGES_HANDLER is not specified')
            return
        try:
            module, name = settings.KAFKA_TOOLS_MESSAGES_HANDLER.rsplit('.', 1)
            handler = getattr(importlib.import_module(module), name)
        except (ImportError, AttributeError):
            logging.exception('Failed to import KAFKA_TOOLS_MESSAGES_HANDLER')
            return
        if not getattr(settings, 'KAFKA_TOOLS_BOOTSTRAP_SERVERS', None):
            logging.error('KAFKA_TOOLS_BOOTSTRAP_SERVERS is not specified')
            return
        if not getattr(settings, 'KAFKA_TOOLS_LISTEN_TOPICS', None):
            logging.error('kafka_tools has no topics to listen')
            return
        start(handler)


def start(handler):
    while True:
        try:
            loop.run_until_complete(consume(handler))
        except (ConnectionError, NodeNotReadyError):
            logging.exception('Failed to connect to kafka')
            time.sleep(getattr(settings, 'KAFKA_TOOLS_CONNECTION_RETRY_TIMEOUT', 60))
        except KafkaError:
            logging.exception('Kafka consumer error')


async def consume(handler):
    consumer = AIOKafkaConsumer(
        *tuple(settings.KAFKA_TOOLS_LISTEN_TOPICS),
        loop=loop,
        bootstrap_servers=settings.KAFKA_TOOLS_BOOTSTRAP_SERVERS,
        group_id=str(KafkaGroup.objects.first().code)
    )
    try:
        await consumer.start()
        # Consume messages
        async for msg in consumer:
            try:
                message = json.loads(msg.value.decode('utf8'))
                validate_payload(message)
                handler(msg.topic, message)
            except (json.JSONDecodeError, ValidationError):
                logging.error('Got invalid message from kafka: %s', msg.value)
            except Exception:
                logging.exception('Failed to process message from kafka')
    finally:
        # Will leave consumer group; perform autocommit if enabled.
        await consumer.stop()
