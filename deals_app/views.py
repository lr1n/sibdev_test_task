import csv
import io
import codecs
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView

from .forms import DealsForm
from .models import DealsModel, DataFromDealsFiles


def add_deal(request):
    if request.method == 'POST':
        form = DealsForm(request.POST, request.FILES)
        if form.is_valid():
            # csv_file = form.cleaned_data['upload_deal']
            # processed_csv_file = csv.reader(
            #     codecs.iterdecode(csv_file, 'utf-8')
            # )
            # for el in processed_csv_file:
            #     print(el)
            # form.save()
            csv_file = request.FILES['upload_deal']
            data = csv_file.read().decode('utf-8')
            print(type(data))
            return HttpResponseRedirect('/')
    else:
        form = DealsForm()
    return render(request, 'deals_app/add_deal.html', {'form': form})


class IndexView(ListView):
    model = DealsModel
    template_name = 'deals_app/index.html'
    context_object_name = 'deals'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
