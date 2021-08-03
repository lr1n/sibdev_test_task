import csv
import io

from django.http import JsonResponse
from django.shortcuts import render

from .forms import DealsForm
from .models import DataFromDealsFiles


def process_csv(reader):
    """This function takes a csv reader and handle it with our needs

    Returns: a list with dicts
    """
    customers = set()
    data = dict()

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

    for el in data_5_items:
        el[2] = list(el[2])

    res_data = []
    for el in data_5_items:
        res_data.append({'username': el[0], 'spent_money': el[1], 'gems': el[2]})

    return res_data


def add_deal(request):
    if request.method == 'POST':
        form = DealsForm(request.POST, request.FILES)
        file = request.FILES['upload_deal']
        if file.name.endswith('.csv'):
            d = file.read().decode('utf-8')
            io_str = io.StringIO(d)
            # skip header
            headers = next(io_str).split(',')
            needed_headers = [
                'customer', 'item', 'total', 'quantity', 'date\r\n'
            ]
            # check if structure of csv file matches our needs
            for el in needed_headers:
                if el not in headers:
                    return JsonResponse(
                        {
                            'Status': 'Error',
                            'Desc': 'You\'ve uploaded a .csv file with wrong headers'
                        }
                    )
            reader = csv.reader(io_str, delimiter=',')
            reader = list(reader)
            for el in reader:
                d = DataFromDealsFiles(
                    customer=el[0],
                    item=el[1],
                    total=el[2],
                    quantity=el[3],
                    date=el[4]
                )
                d.save()
            processed_data = process_csv(reader)
            if form.is_valid():
                form.save()
                return JsonResponse(
                    {'Response': processed_data},
                    json_dumps_params={'ensure_ascii': False}
                )
        else:
            if form.is_valid():
                response = {
                    'Status': 'Error',
                    'Desc': 'Please upload a .csv file'
                }
                return JsonResponse(response)
    else:
        form = DealsForm()
    return render(request, 'deals_app/add_deal.html', {'form': form})


# class IndexView(ListView):
#     model = DealsModel
#     template_name = 'deals_app/index.html'
#     context_object_name = 'deals'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context
