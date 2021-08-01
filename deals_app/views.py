import csv
import io
import codecs
from django.http.response import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import ListView

from .forms import DealsForm
from .models import DealsModel, DataFromDealsFiles


def add_deal(request):
    if request.method == 'POST':
        csv_file = request.FILES['upload_deal']
        data = csv_file.read().decode('utf-8')
        io_string = io.StringIO(data)
        next(io_string)
        for c in csv.reader(io_string, delimiter=','):
            _, created = DataFromDealsFiles.objects.update_or_create(
                customer=c[0],
                item=c[1],
                total=c[2],
                quantity=c[3],
                date=c[4]
            )
        # file = form.cleaned_data['upload_deal']
        # processed_csv_file = csv.reader(
        #     codecs.iterdecode(file, 'utf-8')
        # )
        # next(processed_csv_file)
        form = DealsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('index/')
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
