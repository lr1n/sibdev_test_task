from django.db import models


class DealsModel(models.Model):
    upload_deal = models.FileField(upload_to='uploads/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.upload_deal.name[19:]}'

    class Meta:
        verbose_name = 'Deal'
        verbose_name_plural = 'Deals'


class DataFromDealsFiles(models.Model):
    customer = models.CharField(max_length=256)
    item = models.CharField(max_length=256)
    total = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.customer} -- {self.item}'
