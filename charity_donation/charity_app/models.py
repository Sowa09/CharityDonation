from django.db import models

FUND_TYPE = [
    ('fundacja', 'fundacja'),
    ('organizacja pozarządowa', 'organizacja pozarządowa'),
    ('zbiórka lokalna', 'zbiórka lokalna'),
]


class Category(models.Model):
    name = models.CharField(max_length=32)


class Institution(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    type = models.CharField(max_length=63, choices=FUND_TYPE, default=FUND_TYPE[0][0])
    categories = models.ManyToManyField(Category)

