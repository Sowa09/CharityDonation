from django.db import models
from django.conf import settings


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

    def __str__(self):
        return f'{self.name} - {self.type} - {self.description}'


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=64)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=32)
    zip_code = models.IntegerField()
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)

