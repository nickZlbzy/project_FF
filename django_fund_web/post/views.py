from django.shortcuts import render




def postHome(request):
    if request.method == "GET":
        return render(request,"post/postHome.html")
