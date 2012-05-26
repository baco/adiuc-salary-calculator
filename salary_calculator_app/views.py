# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.forms.formsets import formset_factory

from forms import CargoUnivForm, MesForm
import models

# debugger
#import pdb

def calculate(request):
#    pdb.set_trace()

    # CargoUnivFormSet: Permite que aparezcan multiples formularios identicos.
    CargoUnivFormSet = formset_factory(CargoUnivForm, extra=1, max_num=5)

    context = {}
    if request.method == 'POST':

        # Sacamos la info del POST y bindeamos los forms.
        univformset = CargoUnivFormSet(request.POST, prefix='univcargo')
        mform = MesForm(request.POST)

        if univformset.is_valid() and mform.is_valid():

            aumento_obj = mform.cleaned_data['aumento']

            #guardo en esta lista un diccionario para cada formulario procesado
            #en cada una de estas, los resultados para renderizar luego.
            lista_res = list()
            for univform in univformset:
                lista_res.append(dict())

            # Itero sobre todos los cargos.
            i = 0
            total_bruto = 0.0
            total_neto = 0.0 

            for univform in univformset:                
                form_res = lista_res[i] #i-esimo diccionario de la lista. 
                                        #para guardar los res del cargo i esimo                
                salario_bruto = 0
                salario_neto = 0

                cargo_obj = univform.cleaned_data['cargo']
                has_doctorado = univform.cleaned_data['doctorado']
                has_master = univform.cleaned_data['master']
                antiguedad_obj = univform.cleaned_data['antiguedad']

                antiguedad = 1. + float(antiguedad_obj.porcentaje)/100.0
                anios_antiguedad = antiguedad_obj.anio
                dedicacion = cargo_obj.dedicacion
                tipo_cargo = cargo_obj.tipo
                dedicacion = cargo_obj.dedicacion

                basico_unc = cargo_obj.basico_unc
                basico_nac = cargo_obj.basico_nac

                aumento = float(aumento_obj.porcentaje)/100.0
                mes = aumento_obj.mes
                anio = aumento_obj.anio

                ldescuentos = []      #lista de cosas a descontar, retencioens, etc.
                aumento2003 = 0
                descuentos  = 0.19  #calcularlo basadose en lista_descuentos

                tipo_cargo = str(tipo_cargo) + " " + str(dedicacion)
                form_res.update({
                                 'Tipo de Cargo':tipo_cargo,
                                 'Aaumento desde 2003':aumento2003,
                                 'Total Descuentos':descuentos,
                                 'ldescuentos':ldescuentos                             
                                })

                if has_doctorado:
                    aumento_posg = 1.15
                elif has_master:
                    aumento_posg = 1.05
                else:
                    aumento_posg = 1.

                bruto_sep11 = basico_nac * antiguedad
                neto_basico_sep11 = basico_nac - (basico_nac * descuentos)
                neto_sep11 = neto_basico_sep11 * antiguedad
            
                if mes == "SEP" and anio == "2011":
                    salario_bruto = bruto_sep11
                    salario_neto = neto_sep11

                if mes == "MAR" or mes == "JUN" or (mes == "SEP" and anio == "2012"):
                    acum_mensual = basico_nac * aumento
                    salario_basico = basico_unc + acum_mensual + aumento2003
                   
                    salario_bruto = salario_basico * antiguedad                    
                    salario_bruto = salario_bruto * aumento_posg
                
                    salario_neto = neto_sep11 + (neto_sep11 * aumento)

                form_res.update({'Sueldo Bruto':salario_bruto,'Sueldo Neto':salario_neto})                    
                total_bruto += salario_bruto
                total_neto += salario_neto
                i = i+1

            context['total_bruto']=total_bruto
            context['total_neto'] = total_neto
            context['lista_res'] = lista_res
            print context
            return render_to_response('salary_calculated.html', context)

    else:

        # Creamos formularios vacios (sin bindear) y los mandamos.
        univformset = CargoUnivFormSet(prefix='univcargo')
        mform = MesForm()
        context['univformset'] = univformset
        context['mform'] = mform

    return render_to_response('calculate.html', context)

