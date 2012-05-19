from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, Template

from models import *

def calculate(request):
	req = request.POST.get()

	return render_to_response('salary_calculated.html', context)
