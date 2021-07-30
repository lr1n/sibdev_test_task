from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from .forms import DealsForm


def add_deal(request):
    if request.method == 'POST':
        form = DealsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = DealsForm()
    return render(request, 'deals_app/add_deal.html', {'form': form})
