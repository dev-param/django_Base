from django.db import models


class PendingTaskModel(models.Model):
    task_name = models.CharField(max_length=255)