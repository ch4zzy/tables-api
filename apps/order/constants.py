from django.db.models import TextChoices


class ShapeChoices(TextChoices):
    RECTANGLE = "rectangle", "Rectangle"
    CIRCLE = "circle", "Circle"
    TRIANGLE = "triangle", "Triangle"
