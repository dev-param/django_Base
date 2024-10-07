from rest_framework import serializers
from .models import LogsModel
from django.db import models

class LogsSerializer(serializers.ModelSerializer):
    """
    _type_logs = TextChoices('_type', ['DEBUG', 'INFO'])
    _type = CharField(choices=_type_logs.choices)
    _tag = CharField(default="system")
    _info = JSONField(default=dict)
    _at = DateTimeField(auto_now_add=True)
    """
    class Meta:
        model = LogsModel
        fields = '__all__'
    
    