from django.contrib import admin

from . import models


admin.site.register(models.Donation)
admin.site.register(models.Category)
admin.site.register(models.Institution)