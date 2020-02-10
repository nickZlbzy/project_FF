import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from system.mappers import Title_url_mapper


def queryBox(request):
    select_name = request.GET.get("selName")
    re_json=Title_url_mapper.query_box(select_name)
    return HttpResponse(json.dumps(re_json))
