from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import pymongo
import requests
import os

# Create your views here.
class IndexTemplateView(TemplateView):
    def get_template_names(self):
        if  settings.DEBUG:
            template_name = "index-dev.html"
        else:
            template_name = "index.html"
        return template_name

@csrf_exempt
def get_google_location(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    try:
        response = requests.get('https://www.google.com.tw/maps/place/{}'.format(data['raw_address']))
        res_text = response.text
        if 'markers' in res_text:
            lat_lngs = res_text.split('center=')[1].split('&amp')[0].split('%2C')
            Y = float(lat_lngs[0])
            X = float(lat_lngs[1])
        else:
            lat_lngs = res_text.split('ll=')[1].split(' ')[0].split(',')
            Y = float(lat_lngs[0].replace('"',''))
            X = float(lat_lngs[1].replace('"',''))
        return JsonResponse({ 'X' : X , 'Y': Y, 'inner_error': False})
    except:
        return JsonResponse({ 'X' : None , 'Y': None, 'inner_error': True })

@csrf_exempt
def get_pharmacy(request):
    body_unicode = request.body.decode('utf-8')
    data = json.loads(body_unicode)
    print(data)
    try:
        X = data['X']
        Y = data['Y']
        client = pymongo.MongoClient(os.environ['MONGODB_URI'])
        db = client['wuhan']
        collection = db['pharmacy']
        query = {"loc":{"$near":{"$geometry":{"type":"Point","coordinates":[X,  Y]}, "$maxDistance": 1000}}}
        pharmacys = list(collection.find(query, projection={'_id': False, 'name': True, 'phone': True, 'address':True, 'adult':True, 'child':True, 'update_time':True}).limit(10))

        if len(pharmacys) == 0:
            return JsonResponse({ 'pharmacys' :pharmacys , 'inner_error': False, 'message': '地址週邊1公里沒有口罩販賣點'}, safe=False)
        return JsonResponse({ 'pharmacys' :pharmacys , 'inner_error': False, 'message': None}, safe=False)
    except:
        return JsonResponse({ 'pharmacys' :[], 'inner_error': True, 'message': None }, safe=False)
    
