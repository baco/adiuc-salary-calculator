# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from forms import CargoUnivForm
import models

def calculate(request):

	if request.method == 'POST':
		form = CargoUnivForm(request.POST)

		if form.is_valid():
			context = {}
			
			cargo	   = form.cleaned_data['cargo']
			doctorado  = form.cleaned_data['doctorado']
			master	   = form.cleaned_data['master']
			antiguedad = form.cleaned_data['antiguedad']
			
	        cargo = Cargo.objects.get(nombre=tipo)
			#calcular el sueldo acorde.
			
#		else:
#			context = {'error':True}

		return render_to_response('salary_calculated.html', context)

	else:
		form = CargoUnivForm()
		return render_to_response('calculate.html', {'form': form})

