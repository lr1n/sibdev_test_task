from django.urls import path

from .views import (
    add_deal,
    # IndexView,
    # index
)


urlpatterns = [
    path('', add_deal, name='add_deal'),
    # path('index/', IndexView.as_view(), name='index'),
]
