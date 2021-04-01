from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from django.db import connection
from django.http import HttpResponseRedirect



def main(request):
    #return HttpResponse('about')
    print("pony")
    return render(request,'main.html')
    
