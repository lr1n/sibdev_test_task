from django.db import models


class DealsModel(models.Model):
    upload_deal = models.FileField(upload_to='uploads/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Deal from {self.created_at}'

    class Meta:
        verbose_name = 'Deal'
        verbose_name_plural = 'Deals'
        # ordering = ('created_at',)


class DataFromDealsFiles(models.Model):
    # deal_id = models.ForeignKey(DealsModel)
    customer = models.CharField(max_length=256)
    item = models.CharField(max_length=256)
    total = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.customer} -- {self.item}'
