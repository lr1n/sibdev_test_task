from django.urls import path

from .views import add_deal


urlpatterns = [
    path('add_deal/', add_deal, name='add_deal'),
]
