from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from django.db import connection
from django.http import HttpResponseRedirect



def main(request):
    #return HttpResponse('about')
    return render(request,'main.html')
def main(request):
    #return HttpResponse('about')
    return render(request,'main.html')
    

    
