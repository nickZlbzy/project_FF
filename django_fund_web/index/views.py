from django.shortcuts import render

# Create your views here.
from article.mappers import Article_mapper


def index_page(request):

    left_info=Article_mapper.query_by_type("art_info")
    courses = Article_mapper.query_article_list2('cls')
    return render(request, "main/index.html",locals())