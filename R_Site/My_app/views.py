from django.shortcuts import render
from django.http import HttpResponse
import pandas as pan
import json
from .models import Data 

# Create your views here.
def hello(request):
    if (request.method == 'POST'):
        previous_data = Data.objects.all()
        previous_data.delete()
       #  print('This is a post request')
       # name = request.POST.get('name')
        file = request.FILES['file']
        df = pan.read_csv(file)
        json_records = df.reset_index().to_json(orient='records')
        data = []
        data = json.loads(json_records)
        for d in data:
            name = d['property_name']
            price = d['property_price']
            rent = d['property_rent']
            emi = d['emi']
            tax = d['tax']
            exp = d['other_exp']
            expenses_monthly = emi+tax+exp
            income_monthly = rent-expenses_monthly
            dt = Data(name=name , price=price,rent=rent,emi=emi,tax=tax,exp=exp, expenses_monthly=expenses_monthly, income_monthly=income_monthly)
            dt.save()

        data_objects = Data.objects.all()
        context ={'data_objects': data_objects}
        return render(request, 'My_app/index.html', context)

    else:
        print('This is a get request')
  #  name = 'Ray'
  #  price = 200
  #  movies = ['Deadpool','ironman','spiderman','Notebook']
  #  context = {
    #   'name':name  # can only pass one context at a time#
    #   'price':price
  #   'movies': movies
   # }
    return render(request,'My_app/index.html')  #,context) 