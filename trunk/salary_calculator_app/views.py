# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.forms.formsets import formset_factory

from forms import CargoUnivForm, MesForm
import models

def calculate(request):
#error = 1 : error einvformset
#error = 2 : error formularios invalidos


    # CargoUnivFormSet: Permite que aparezcan multiples formularios identicos.
    CargoUnivFormSet = formset_factory(CargoUnivForm, extra=1, max_num=5)

    if request.method == 'POST':
        univformset = CargoUnivFormSet(request.POST)
        context = {}
        mform = MesForm(request.POST)

        if univformset.is_valid():
            cform = CargoUnivForm(request.POST)
            context.update({'cform':cform,'mform':mform})       
        else:        
            error = 1
            print error            
            context['error'] = error
            return render_to_response('calculate.html',context)

        if cform.is_valid() and mform.is_valid():
            cargo	   = cform.cleaned_data['cargo']
            doctorado  = cform.cleaned_data['doctorado']
            master	   = cform.cleaned_data['master']
            antiguedad_obj = cform.cleaned_data['antiguedad']

            aumento_obj = mform.cleaned_data['aumento']

            antiguedad = 1 + float(antiguedad_obj.porcentaje)/100.0
            anios_antiguedad = antiguedad_obj_anio
            dedicacion = cargo_obj.dedicacion
            tipo_cargo = cargo_obj.tipo
            basico_unc = cargo_obj.basico_unc
            basico_nac = cargo_obj.basico_nac
            
            aumento = float(aumento_obj.porcentaje)/100.0
            mes = aumento_obj.mes
            anio = aumento_obj.anio

            ldescuentos = []      #lista de cosas a descontar, retencioens, etc.
            aumento2003   = 0
            descuentos    = 0.19  #calcularlo basadose en lista_descuentos
            
            context.update({'ldescuentos':ldescuentos,'aumento2003':aumento2003,'descuentos':descuentos})

            # ej: Sueldo*aumento_posg = sueldo_resultante
            if doctorado:
                aumento_posg = 1.15
            elif master:
                aumento_posg = 1.05
            else:
                aumento_posg = 1

            bruto_sep11 = bruto_nac * antiguedad
            neto_basico_sep11 = basico_nac - (basico_nac * descuentos)
            neto_sep11 = neto_basico_sep11 * antiguedad
            
            if mes == "SEP" and anio == "2011":
                
                context['bruto'] = bruto_sep11
                context['neto'] = neto_sep11

            if mes == "MAR" or mes == "JUN" or (mes == "SEP" and anio == "2012"):
                acum_mensual = basico_nac * aumento
                salario_basico = basico_unc + acum_mensual + aumento2003
                salario_bruto = salario_basico * antiguedad
                
                salario_bruto = salario_bruto * aumento_posg
            
                salario_neto = neto_sep11 + (neto_sep11 * aumento)

                context['bruto'] = salario_bruto
                context['neto'] = salario_neto
                
            return render_to_response('salary_calculated.html', context)

        else:
            error = 2 #error de validacion, indicar errores.
            context['error']= error
            return render_to_response('calculate.html',context)

    else:
        univformset = CargoUnivFormSet()
        mform = MesForm()
        return render_to_response('calculate.html', {'univformset': univformset,'mform':mform})

