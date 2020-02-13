from django.shortcuts import render

# Create your views here.

def login_page(reqeust):
    return render(reqeust,"user/login.html")