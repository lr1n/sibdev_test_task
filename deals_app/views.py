import csv
import io
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView

from .forms import DealsForm
from .models import DealsModel, DataFromDealsFiles


def process_csv(filename):
    customers = set()
    data = dict()

    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        reader = list(reader)

        for el in reader:
            customers.add(el[0])

        for el in customers:
            data[el] = [0, set()]

        for el in reader:
            data[el[0]][0] += int(el[2])
            data[el[0]][1].add(el[1])

    sorted_data = {
        k: v for k, v in sorted(data.items(), key=lambda x: x[1], reverse=True)
    }

    gems = []
    data_5_items = []
    for k, v in sorted_data.items():
        data_5_items.append([k, v[0], v[1]])
        gems.extend(list(v[1]))
        if len(data_5_items) > 4:
            break

    for el in data_5_items:
        for gem in gems:
            if gem in el[2] and gems.count(gem) < 2:
                el[2].remove(gem)

    return data_5_items


def add_deal(request):
    if request.method == 'POST':
        form = DealsForm(request.POST, request.FILES)
        file = request.FILES['upload_deal']
        if file.name.endswith('.csv'):
            data = file.read().decode('utf-8')
            io_str = io.StringIO(data)
            next(io_str)
            reader = csv.reader(io_str, delimiter=',')
            for el in reader:
                d = DataFromDealsFiles(
                    customer=el[0],
                    item=el[1],
                    total=el[2],
                    quantity=el[3],
                    date=el[4]
                )
                d.save()
            # for c in csv.reader(io_str, delimiter=','):
            #     _, created = DataFromDealsFiles.objects.update_or_create(
            #         customer=c[0],
            #         item=c[1],
            #         total=c[2],
            #         quantity=c[3],
            #         date=c[4]
            #     )

            # file = form.cleaned_data['upload_deal']
            # processed_csv_file = csv.reader(
            #     codecs.iterdecode(file, 'utf-8')
            # )
            # next(processed_csv_file)
            if form.is_valid():
                form.save()
        else:
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
