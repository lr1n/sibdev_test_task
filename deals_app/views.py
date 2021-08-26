import csv
import io
from django.http import JsonResponse
from django.shortcuts import render
from .forms import DealsForm
from .models import DataFromDealsFiles
from .utils import process_csv


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
