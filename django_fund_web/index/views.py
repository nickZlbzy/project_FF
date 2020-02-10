from django.shortcuts import render

# Create your views here.
from article.mappers import Article_mapper


def index_page(request):
    left_info=Article_mapper.query_by_type("art_info")

    return render(request, "main/index.html",locals())