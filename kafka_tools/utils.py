"""
Creates the default KafkaGroup object.
"""

from django.apps import apps as global_apps
from django.db import DEFAULT_DB_ALIAS, connections, router


def create_default_kafka_group(app_config, using=DEFAULT_DB_ALIAS, apps=global_apps, **kwargs):
    try:
        KafkaGroup = apps.get_model('kafka_tools', 'KafkaGroup')
    except LookupError:
        return

    if not router.allow_migrate_model(using, KafkaGroup):
        return

    if not KafkaGroup.objects.using(using).exists():
        KafkaGroup().save(using=using)
