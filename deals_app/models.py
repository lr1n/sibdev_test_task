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
