# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.forms.formsets import formset_factory

from forms import CargoUnivForm, MesForm
import models

def calculate(request):

    # CargoUnivFormSet: Permite que aparezcan multiples formularios identicos.
    CargoUnivFormSet = formset_factory(CargoUnivForm, extra=2, max_num=5)

    if request.method == 'POST':
        univformset = CargoUnivFormSet(request.POST)

        if univformset.is_valid():

        mform = MesForm(request.POST)
        cform = CargoUnivForm(request.POST)
        context = {}
        
        if cform.is_valid() and mform.is_valid():
            cargo	   = cform.cleaned_data['cargo']
            doctorado  = cform.cleaned_data['doctorado']
            master	   = cform.cleaned_data['master']
            antiguedad = cform.cleaned_data['antiguedad']
            context['cform'] = cform
            return render_to_response('salary_calculated.html', context)

        else:
            aumento = fmes.cleaned_data['aumento']
            context['mform'] = mform
            return render_to_response('salary_calculated.html',context)

    else:
        univformset = CargoUnivFormSet()
        mform = MesForm()
        return render_to_response('calculate.html', {'univformset': univformset,'mform':mform})

