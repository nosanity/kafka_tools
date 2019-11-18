from uuid import uuid4
from django.db import models


class KafkaGroup(models.Model):
    code = models.UUIDField(default=uuid4)
