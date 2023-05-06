from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.order.constants import ShapeChoices


class Table(models.Model):
    number = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(2), MaxValueValidator(16)])
    shape = models.CharField(choices=ShapeChoices.choices, max_length=10, default=ShapeChoices.RECTANGLE)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    length = models.DecimalField(max_digits=5, decimal_places=2)


class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    customer_name = models.CharField(max_length=50)
    customer_email = models.EmailField()
