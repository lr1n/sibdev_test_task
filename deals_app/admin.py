from django.contrib import admin

from .models import DealsModel, DataFromDealsFiles


admin.site.register(DealsModel)
admin.site.register(DataFromDealsFiles)
