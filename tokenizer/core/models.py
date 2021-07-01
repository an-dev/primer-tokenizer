from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.db import models


class Card(models.Model):
    number = models.CharField(max_length=16, unique=True, validators=[MinLengthValidator(16)])
    expiry_month = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    expiry_year = models.PositiveSmallIntegerField(validators=[MinValueValidator(2021)])

    def __str__(self):
        return f'Card {self.number} (expires on {self.expiry_month}/{self.expiry_year})'
