# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.forms.formsets import formset_factory

from forms import CargoUnivForm, MesForm
import models

# debugger
import pdb

def calculate(request):
    #pdb.set_trace()

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

            # Itero sobre todos los cargos.
            i = 0
            total_bruto = 0.0
            total_neto = 0.0 

            for univform in univformset:

                cargo_obj = univform.cleaned_data['cargo']
                has_doctorado = univform.cleaned_data['doctorado']
                has_master = univform.cleaned_data['master']
                antiguedad_obj = univform.cleaned_data['antiguedad']

                ###### Salario Bruto.
                basico_unc = cargo_obj.basico_unc
                basico_nac = cargo_obj.basico_nac
                adic2003 = 0.
                if cargo_obj.rem_fijas.exists(codigo=u'118'):
                    adic2003 = cargo_obj.rem_fijas.get(codigo='118').valor # 118: Adicional 8% 2003
                aumento = basico_nac * aumento_obj.porcentaje / 100.0
                #
                salario_bruto = basico_unc + aumento + adic2003

                ###### El Neto se calcula del basico restando las retenciones y sumando las remuneraciones.
                ret_porcentuales = cargo_obj.ret_porcentuales.all()
                ret_fijas = cargo_obj.ret_fijas.all()
                rem_porcentuales = cargo_obj.rem_porcentuales.all()
                rem_fijas = cargo_obj.rem_fijas.all()

                ret_list = list()   # Aqui iran tuplas de la forma (obj retencion, importe) para mostrar esta info en el template
                rem_list = list()  # De forma similar, va a tener tuplas (obj remuneracion, importe)

                acum_ret = 0.   # El acumulado de todo lo que hay que descontarle al bruto.
                acum_rem = 0. # El acumulado de todo lo que hay que sumarle.

                ## Remuneraciones Especiales:

                # 1: Adicional 8% 2003 (cod 118).
                if rem_fijas.exists(codigo=u'118'):
                    rem_list.append( (rem_fijas.get(codigo='118'), adic2003) )
                    rem_fijas = rem_fijas.exclude(codigo='118')

                # 2: Adicional Antiguedad (cod 30).
                #importe = salario_bruto * antiguedad_obj.porcentaje / 100.0
                #acum_rem = acum_rem + importe
                #rem_obj = rem_porcentuales.get(codigo='30')
                #rem_obj.nombre = rem_obj.nombre + u' (' + unicode(antiguedad_obj.porcentaje) + u'%)'
                #rem_list.append( (rem_obj, importe) )
                #rem_porcentuales = rem_porcentuales.exclude(codigo='30')

                # 3: Adicional titulo doctorado (cod 51), Adicional titulo maestria (cod 52)
                if has_doctorado:
                    rem_porcentuales = rem_porcentuales.exclude(codigo='52')
                elif has_master:
                    rem_poscentuales = rem_porcentuales.exclude(codigo='51')
                else:
                    rem_porcentuales = rem_porcentuales.exclude(codigo='51')
                    rem_porcentuales = rem_porcentuales.exclude(codigo='52')

          
                ## Retenciones NO especiales:

                for ret in ret_porcentuales:
                    importe = salario_bruto * ret.porcentage / 100.
                    acum_ret = acum_ret + importe
                    ret_list.append( (ret, importe) )

                for ret in ret_fijas:
                    acum_ret = acum_ret + ret.valor
                    ret_list.append( (ret, ret.valor) )

                for rem in rem_porcentuales:
                    importe = salario_bruto * rem.porcentaje / 100.
                    acum_ret = acum_ret + importe
                    rem_list.append( (rem, importe) )

                for rem in rem_fijas:
                    acum_ret = acum_ret + rem.valor
                    rem_list.append( (rem, rem.valor) )

                ###### Salario Neto.
                salario_neto = salario_bruto - acum_ret + acum_rem

                #salario_bruto = round(salario_bruto, 2)
                #salario_neto = round(salario_neto, 2)

                # Calculo los acumulados de los salarios para todos los cargos.
                total_bruto += salario_bruto
                total_neto += salario_neto

                # Aqui iran los resultados del calculo para este cargo en particular.
                form_res = {
                    'cargo': cargo_obj,
                    'aumento': aumento,
                    'retenciones': ret_list,
                    'remuneraciones': rem_list,
                    'salario_bruto': salario_bruto,
                    'salario_neto': salario_neto
                }
                lista_res.append(form_res)

            context['total_bruto']= round(total_bruto, 2)
            context['total_neto'] = round(total_neto, 2)
            context['lista_res'] = lista_res
            context['aumento'] = aumento_obj
            print context

            return render_to_response('salary_calculated.html', context)

    else:

        # Creamos formularios vacios (sin bindear) y los mandamos.
        univformset = CargoUnivFormSet(prefix='univcargo')
        mform = MesForm()
        context['univformset'] = univformset
        context['mform'] = mform

    return render_to_response('calculate.html', context)

