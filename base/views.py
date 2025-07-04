from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def service_detail(request, id):
    return render(request, 'service-detail.html')