from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import pymongo
import requests

# Create your views here.
class IndexTemplateView(TemplateView):
    def get_template_names(self):
        if  settings.DEBUG:
            template_name = "index-dev.html"
        else:
            template_name = "index.html"
        return template_name

@csrf_exempt
def get_pharmacy(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)

    try:
        response = requests.get('https://www.google.com.tw/maps/place/{}'.format(data['raw_address']))
        res_text = response.text
        lat_lngs = res_text.split('ll=')[1].split(' ')[0].split(',')
        Y = float(lat_lngs[0].replace('"',''))
        X = float(lat_lngs[1].replace('"',''))
        client = pymongo.MongoClient("mongodb+srv://hughe:sk10041004@wuhan-pneumonia-xpc7e.mongodb.net/test?retryWrites=true&w=majority")
        db = client['wuhan']
        collection = db['pharmacy']
        query = {"loc":{"$near":{"$geometry":{"type":"Point","coordinates":[X,  Y]}, "$maxDistance": 500}}}
        pharmacys = list(collection.find(query, projection={'_id': False, 'name': True, 'phone': True, 'address':True, 'adult':True, 'child':True, 'update_time':True}).limit(10))

        print(pharmacys)
        return JsonResponse({ 'pharmacys' :pharmacys , 'inner_error': False}, safe=False)
    except:
        return JsonResponse({ 'pharmacys' :[], 'inner_error': True }, safe=False)
    
