from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def homepage(request):
    # # print("works well------------------------")
    # return render(request, 'accounts/dashboard.html')
    return HttpResponse('yay, It works!')

