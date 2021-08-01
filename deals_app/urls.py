from django.urls import path

from .views import (
    add_deal,
    IndexView,
    # index
)


urlpatterns = [
    path('add_deal/', add_deal, name='add_deal'),
    path('', IndexView.as_view(), name='index'),
]
