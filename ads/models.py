import datetime

from django.db import models

from base.settings import MEDIA_ROOT
from users.models import User

# Create your models here.
class Ad(models.Model):
    class CategoryChoices(models.TextChoices):
        household_items = 'Вещи для дома'
        clothes = 'Одежда'
        transport = 'Транспорт'

    class ConditionChoices(models.TextChoices):
        new = 'новый'
        used = 'б/у'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    image_url = models.FilePathField(path=MEDIA_ROOT+'images/')
    category = models.CharField(choices=CategoryChoices)
    condition = models.CharField(choices=ConditionChoices)
    created_at = models.DateTimeField(auto_now_add=True)


class Proposal(models.Model):
    class StatusChoices(models.TextChoices):
        awaiting = 'ожидает'
        accepted = 'принято'
        rejected = 'отклонено'

    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='ad_sender')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='ad_receiver')
    comment = models.CharField(max_length=300)
    status = models.CharField(choices=StatusChoices, default=StatusChoices.awaiting)