from django.apps import AppConfig
from django.db.models.signals import post_migrate

from .utils import create_default_kafka_group


class KafkaToolsConfig(AppConfig):
    name = 'kafka_tools'

    def ready(self):
        post_migrate.connect(create_default_kafka_group, sender=self)
