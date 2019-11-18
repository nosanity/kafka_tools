import json
import logging
from django.conf import settings
from jsonschema.exceptions import ValidationError
from kafka import KafkaProducer
from kafka_tools.message_format import validate_payload


def produce(topic, message):
    try:
        validate_payload(message)
        producer = KafkaProducer(bootstrap_servers=settings.KAFKA_TOOLS_BOOTSTRAP_SERVERS)
        sender = producer.send(topic, json.dumps(message).encode('utf8'))
        sender.get(timeout=getattr(settings, 'KAFKA_TOOLS_PRODUCER_TIMEOUT', 5))
        return True
    except ValidationError:
        logging.error('Invalid message structure')
    except Exception:
        logging.exception('Failed to send message to kafka: %s', message)
