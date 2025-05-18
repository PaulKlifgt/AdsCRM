import datetime

from django.db import models

from base.settings import MEDIA_ROOT
from users.models import User

# Create your models here.
class Ad(models.Model):
    category_choices = {
        'вещи для дома': 'вещи для дома',
        'одежда': 'одежда',
        'транспорт': 'транспорт',
    }

    condition_choices = {
        'новый': 'новый',
        'б/у': 'б/у',
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    category = models.CharField(choices=category_choices)
    condition = models.CharField(choices=condition_choices)
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