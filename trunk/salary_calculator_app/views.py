# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.forms.formsets import formset_factory

from forms import CargoUnivForm, MesForm, CargoPreUnivForm
from models import *

#debugger
import pdb

##### Hardcoded
adic2003_code = '118'
adic2003_name = u'Adic. 8% RHCS 153/03'
antiguedad_code = '30'
antiguedad_name = u'Adicional Antigüedad'
doc_code = '51'
doc_preuniv_code = '53'
master_code = '52'
master_preuniv_code = '55'
garantia_code = '115'
garantia_name = u'Garantía Docentes Univ.'
garantia_preuniv_code = '107'
garantia_preuniv_name = u'Garantía Nivel Medio'

def calculate(request):
    """Vista principal"""

    # Permite que aparezcan multiples formularios identicos.
    CargoUnivFormSet = formset_factory(CargoUnivForm, extra=0, max_num=5, can_delete=True)
    CargoPreUnivFormSet = formset_factory(CargoPreUnivForm, extra=0, max_num=5, can_delete=True)

    context = {}
    if request.method == 'POST':

        # Sacamos la info del POST y bindeamos los forms.
        univformset = CargoUnivFormSet(request.POST, prefix='univcargo')
        preunivformset = CargoPreUnivFormSet(request.POST, prefix='preunivcargo')
        mform = MesForm(request.POST)

        pdb.set_trace()

        if univformset.is_valid() and preunivformset.is_valid() and mform.is_valid():

            aumento_obj = mform.cleaned_data['aumento']

            # Calculo para salarios de cargos universitarios.
            context_univ = processUnivFormSet(aumento_obj, univformset)
            context_preuniv = processPreUnivFormSet(aumento_obj, preunivformset)

            # Hago el merge de los dos contexts.
            context['total_rem'] = context_univ['total_rem'] + context_preuniv['total_rem']
            context['total_ret'] = context_univ['total_ret'] + context_preuniv['total_ret']
            context['total_bruto'] = context_univ['total_bruto'] + context_preuniv['total_bruto']
            context['total_neto'] = context_univ['total_neto'] + context_preuniv['total_neto']
            context['lista_res'] = context_univ['lista_res']
            context['lista_res'].extend(context_preuniv['lista_res'])
            context['aumento'] = aumento_obj

            return render_to_response('salary_calculated.html', context)

        else:
            context['univformset'] = univformset
            context['preunivformset'] = preunivformset
            context['mform'] = mform

    else:

        # Creamos formularios vacios (sin bindear) y los mandamos.
        univformset = CargoUnivFormSet(prefix='univcargo')
        preunivformset = CargoPreUnivFormSet(prefix='preunivcargo')
        mform = MesForm()
        context['univformset'] = univformset
        context['preunivformset'] = preunivformset
        context['mform'] = mform

    return render_to_response('calculate.html', context)


def processUnivFormSet(aumento_obj, univformset):
    """Procesa un formset con formularios de cargos universitarios. Retorna un context"""

    context = {}

    #guardo en esta lista un diccionario para cada formulario procesado
    #en cada una de estas, los resultados para renderizar luego.
    lista_res = list()

    # Itero sobre todos los cargos.
    total_rem = 0.0
    total_ret = 0.0
    total_bruto = 0.0
    total_neto = 0.0


    for univform in univformset:

        if univform in univformset.deleted_forms:
            continue

        cargo_obj = univform.cleaned_data['cargo']
        has_doctorado = univform.cleaned_data['doctorado']
        has_master = univform.cleaned_data['master']
        antiguedad_obj = univform.cleaned_data['antiguedad']

        ###### Salario Bruto.
        basico_unc = cargo_obj.basico_unc
        basico_nac = cargo_obj.basico_nac
        adic2003_obj = RemuneracionFija(nombre=adic2003_name, codigo=adic2003_code, valor=0.)
        if cargo_obj.adic2003:
            adic2003_obj.valor = cargo_obj.adic2003 # 118: Adicional 8% 2003
        aumento = basico_nac * aumento_obj.porcentaje / 100.0
        ##
        salario_bruto = basico_unc + aumento + adic2003_obj.valor

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
        rem_list.append( (adic2003_obj, adic2003_obj.valor) )
        rem_fijas = rem_fijas.exclude(codigo=adic2003_code)

        # 2: Adicional Antiguedad (cod 30).
        importe = salario_bruto * antiguedad_obj.porcentaje / 100.0
        acum_rem += importe
        rem_obj = RemuneracionPorcentual(nombre=antiguedad_name, codigo=antiguedad_code)
        if rem_porcentuales.filter(codigo=antiguedad_code).exists():
            rem_obj = rem_porcentuales.get(codigo=antiguedad_code)
        rem_obj.nombre = rem_obj.nombre + u' (' + unicode(antiguedad_obj.porcentaje) + u'%)'
        rem_list.append( (rem_obj, importe) )
        rem_porcentuales = rem_porcentuales.exclude(codigo=antiguedad_code)

        # 3: Adicional titulo doctorado (cod 51), Adicional titulo maestria (cod 52)
        if has_doctorado:
            rem_porcentuales = rem_porcentuales.exclude(codigo=master_code)
        elif has_master:
            rem_poscentuales = rem_porcentuales.exclude(codigo=doc_code)
        else:
            rem_porcentuales = rem_porcentuales.exclude(codigo=doc_code)
            rem_porcentuales = rem_porcentuales.exclude(codigo=master_code)

  
        ## Retenciones NO especiales:

        for ret in ret_porcentuales:
            importe = salario_bruto * ret.porcentaje / 100.
            acum_ret += importe
            ret_list.append( (ret, importe) )

        for ret in ret_fijas:
            acum_ret += ret.valor
            ret_list.append( (ret, ret.valor) )

        for rem in rem_porcentuales:
            importe = acum_rem + salario_bruto * rem.porcentaje / 100.
            acum_rem += importe
            rem_list.append( (rem, importe) )

        for rem in rem_fijas:
            acum_rem += rem.valor
            rem_list.append( (rem, rem.valor) )

        ###### Salario Neto.
        salario_neto = salario_bruto - acum_ret + acum_rem

        ## Garantia salarial.
        if cargo_obj.garantia_salarial.filter(mes=aumento_obj.mes, anio=aumento_obj.anio).exists():
            garantia_obj = cargo_obj.garantia_salarial.get(mes=aumento_obj.mes, anio=aumento_obj.anio)
            if salario_neto < garantia_obj.valor:
                garantia = garantia_obj.valor - salario_neto
                rem_obj = RemuneracionFija( codigo=garantia_code,
                                                            nombre= garantia_name + ' (' + unicode(garantia_obj) + ')',
                                                            aplicacion='U', valor=garantia)
                rem_list.append( (rem_obj, garantia) )
                acum_rem += garantia
                salario_neto += garantia

        # Calculo los acumulados de los salarios para todos los cargos.
        # y tambien los acumulados de las remuneraciones y retenciones.
        total_rem += acum_rem
        total_ret += acum_ret
        total_bruto += salario_bruto
        total_neto += salario_neto

        # Aqui iran los resultados del calculo para este cargo en particular.
        form_res = {
            'cargo': cargo_obj,
            'aumento': aumento,
            'retenciones': ret_list,
            'remuneraciones': rem_list,
            'acum_ret': acum_ret,
            'acum_rem': acum_rem,
            'salario_bruto': salario_bruto,
            'salario_neto': salario_neto
        }
        lista_res.append(form_res)

    context['total_rem'] = total_rem
    context['total_ret'] = total_ret
    context['total_bruto'] = total_bruto
    context['total_neto'] = total_neto
    context['lista_res'] = lista_res
    print context

    return context


def processPreUnivFormSet(aumento_obj, preunivformset):
    """Procesa un formset con formularios de cargos preuniversitarios. 
    Retorna un context."""

    context = {}

    #guardo en esta lista un diccionario para cada formulario procesado
    #en cada una de estas, los resultados para renderizar luego.
    lista_res = list()

    # Itero sobre todos los cargos.
    total_rem = 0.0
    total_ret = 0.0
    total_bruto = 0.0
    total_neto = 0.0


    for preunivform in preunivformset:

        if preunivform in preunivformset.deleted_forms:
            continue

        cargo_obj = preunivform.cleaned_data['cargo']
        has_doctorado = preunivform.cleaned_data['doctorado']
        has_master = preunivform.cleaned_data['master']
        antiguedad_obj = preunivform.cleaned_data['antiguedad']
        horas = preunivform.cleaned_data['horas']

        ###### Salario Bruto.
        basico_unc = cargo_obj.basico_unc
        basico_nac = cargo_obj.basico_nac
        aumento = basico_nac * aumento_obj.porcentaje / 100.0
        ##
        salario_bruto = basico_unc + aumento

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

        # 1: Adicional Antiguedad (cod 30).
        importe = salario_bruto * antiguedad_obj.porcentaje / 100.0
        acum_rem = acum_rem + importe
        rem_obj = RemuneracionPorcentual(nombre=antiguedad_name, codigo=antiguedad_code)
        if rem_porcentuales.filter(codigo=antiguedad_code).exists():
            rem_obj = rem_porcentuales.get(codigo=antiguedad_code)
        rem_obj.nombre = rem_obj.nombre + u' (' + unicode(antiguedad_obj.porcentaje) + u'%)'
        rem_list.append( (rem_obj, importe) )
        rem_porcentuales = rem_porcentuales.exclude(codigo=antiguedad_code)

        # 2: Adicional titulo doctorado nivel medio (cod 53), Adicional titulo maestria nivel medio (cod 55)
        if has_doctorado:
            rem_porcentuales = rem_porcentuales.exclude(codigo=master_preuniv_code)
        elif has_master:
            rem_poscentuales = rem_porcentuales.exclude(codigo=doc_preuniv_code)
        else:
            rem_porcentuales = rem_porcentuales.exclude(codigo=doc_preuniv_code)
            rem_porcentuales = rem_porcentuales.exclude(codigo=master_preuniv_code)

  
        ## Retenciones NO especiales:

        for ret in ret_porcentuales:
            importe = salario_bruto * ret.porcentaje / 100.
            acum_ret = acum_ret + importe
            ret_list.append( (ret, importe) )

        for ret in ret_fijas:
            acum_ret = acum_ret + ret.valor
            ret_list.append( (ret, ret.valor) )

        for rem in rem_porcentuales:
            importe = acum_rem + salario_bruto * rem.porcentaje / 100.
            acum_rem = acum_rem + importe
            rem_list.append( (rem, importe) )

        for rem in rem_fijas:
            acum_rem = acum_rem + rem.valor
            rem_list.append( (rem, rem.valor) )

        ###### Salario Neto.
        salario_neto = salario_bruto - acum_ret + acum_rem

        ## Garantia salarial.
        #pdb.set_trace()
        if cargo_obj.garantia_salarial.filter(mes=aumento_obj.mes, anio=aumento_obj.anio).exists():
            garantia_obj = cargo_obj.garantia_salarial.get(mes=aumento_obj.mes, anio=aumento_obj.anio)
            if salario_neto < garantia_obj.valor:
                garantia = garantia_obj.valor - salario_neto
                rem_obj = RemuneracionFija( codigo=garantia_preuniv_code,
                                                            nombre=garantia_preuniv_name + ' (' + unicode(garantia_obj) + ')',
                                                            aplicacion='P', valor=garantia)
                rem_list.append( (rem_obj, garantia) )
                acum_rem += garantia
                salario_neto += garantia

        # Calculo los acumulados de los salarios para todos los cargos.
        # y tambien los acumulados de las remuneraciones y retenciones.
        total_rem += acum_rem
        total_ret += acum_ret
        total_bruto += salario_bruto
        total_neto += salario_neto

        # Aqui iran los resultados del calculo para este cargo en particular.
        form_res = {
            'cargo': cargo_obj,
            'aumento': aumento,
            'retenciones': ret_list,
            'remuneraciones': rem_list,
            'acum_ret': acum_ret,
            'acum_rem': acum_rem,
            'salario_bruto': salario_bruto,
            'salario_neto': salario_neto
        }
        lista_res.append(form_res)

    context['total_rem'] = total_rem
    context['total_ret'] = total_ret
    context['total_bruto']= total_bruto
    context['total_neto'] = total_neto
    context['lista_res'] = lista_res
    print context

    return context
