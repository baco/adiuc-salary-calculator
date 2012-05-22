# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from forms import CargoUnivForm, MesForm
import models

def calculate(request):

    if request.method == 'POST':

        mform = MesForm(request.POST)
        cform = CargoUnivForm(request.POST)
        context = {}
        
        if cform.is_valid() and mform.is_valid():
            cargo	   = cform.cleaned_data['cargo']
            doctorado  = cform.cleaned_data['doctorado']
            master	   = cform.cleaned_data['master']
            antiguedad = cform.cleaned_data['antiguedad']

            context['cform'] = cform

            aumento = fmes.cleaned_data['aumento']
            context['mform'] = mform

            
        #else: reportar error
            
        return render_to_response('salary_calculated.html',context)

    else:
        cform = CargoUnivForm()
        mform = MesForm()
        return render_to_response('calculate.html', {'cform':cform,'mform':mform})

