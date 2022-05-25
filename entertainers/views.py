from django.shortcuts import render

# Create your views here.


def entertainers(request):
    return render(request, 'pages/entertainers/index.html')


def entertainer(request, entertainer_id):
    return render(request, 'pages/entertainers/index.html')
