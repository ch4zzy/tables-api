from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Table(models.Model):
    number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(2), MaxValueValidator(16)])


class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    customer_name = models.CharField(max_length=50)
    customer_email = models.EmailField()
