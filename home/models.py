from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f'Category: {self.name}'


class Institution(models.Model):
    class Types(models.TextChoices):
        FUNDATION = 'FUN', 'Fundacja'
        NGO = 'NGO', 'Organizacja Pozarządowa'
        LOCAL_COLLECTION = 'LOC', 'Zbiórka Lokalna'

    name = models.CharField(max_length=150)
    decription = models.TextField(max_length=1000)
    type = models.CharField(choices=Types.choices, default=Types.FUNDATION, max_length=25)
    categories = models.ManyToManyField('Category', related_name='instotution_categories')

    def __str__(self):
        return f'Institution: {self.name}'


class Donation(models.Model):
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField('Category', related_name='dontaion_categories')
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE, related_name='donations')
    address = models.CharField(max_length=300)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=150)
    zip_code = models.CharField(max_length=50)
    pick_up_date = models.DateTimeField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, null=True, blank=True, on_delete=models.CASCADE)
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return f'Donation: Address - {self.address}, City - {self.city}'
