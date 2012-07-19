# -*- coding: utf-8 -*-

#=============================================
#
# Copyright 2012 David Racca and Matias Molina.
#
# This file is part of ADIUC Salary Calculator.
#
# ADIUC Salary Calculator is free software: you can redistribute it and/or 
# modify it under the terms of the GNU General Public License as published 
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ADIUC Salary Calculator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ADIUC Salary Calculator.  If not, see 
# <http://www.gnu.org/licenses/>.
#
#=============================================

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.forms.formsets import formset_factory

from forms import *
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

fondo_becas_code = '770'
fondo_becas_name = u'Fondo de Becas'

afiliacion_code = '640'
afiliacion_name = u'ADIUC - Afiliacion'

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
        commonform = CommonForm(request.POST)

        if univformset.is_valid() and preunivformset.is_valid() and commonform.is_valid():

            #aumento_obj = commonform.cleaned_data['aumento']
            fecha = commonform.cleaned_data['fecha']
            antiguedad = commonform.cleaned_data['antiguedad']
            es_afiliado = commonform.cleaned_data['afiliado']

            # Calculo para salarios de cargos universitarios.

            context_univ = processUnivFormSet(fecha, antiguedad, univformset)
            context_preuniv = processPreUnivFormSet(fecha, antiguedad, preunivformset)

            #quito los duplicados, si hay, entre univ y preuniv para las ret/rem por persona
            rfp_univ = list()
            rfp_preuniv = list()
            if context_univ.has_key('ret_fijas_persona'):
                rfp_univ = list(context_univ['ret_fijas_persona'])
            if context_preuniv.has_key('ret_fijas_persona'):
                rfp_preuniv = list(context_preuniv['ret_fijas_persona'])
            ret_fijas_persona = list(set(rfp_univ + rfp_preuniv))

            rpp_univ = list()
            rpp_preuniv = list()
            if context_univ.has_key('ret_porc_persona'):
                rpp_univ = list(context_univ['ret_porc_persona'])
            if context_preuniv.has_key('ret_porc_persona'):
                rpp_preuniv = list(context_preuniv['ret_porc_persona'])
            ret_porc_persona = list(set(rpp_univ + rpp_preuniv))

            #calculo las retenciones/remuneracioens que son por persona.

            total_rem = context_univ['total_rem'] + context_preuniv['total_rem']
            total_ret = context_univ['total_ret'] + context_preuniv['total_ret']
            total_bruto = context_univ['total_bruto'] + context_preuniv['total_bruto']
            total_neto = context_univ['total_neto'] + context_preuniv['total_neto']
 
            #acumulacion de retenciones y remuneraciones por persona.
            acum_ret = 0.0
            acum_rem = 0.0
            for ret in ret_porc_persona:
                importe = (total_bruto * ret.porcentaje / 100)
                acum_ret += importe

            for ret in ret_fijas_persona:
                acum_ret += ret.valor
  
            #for rem in rem_porc_persona:
                #importe = (total_bruto * ret.porcentaje / 100)
                #acum_rem += importe

            #for rem in rem_fijas_persona:
                #importe = rem.valor
                #acum_rem += importe

            #calculo de afiliacion.
            af_importe = 0.0
            if es_afiliado:
                afiliacion_objs = RetencionPorcentual.objects.filter(retencion__codigo=afiliacion_code, vigencia_desde__lte=fecha, vigencia_hasta__gte=fecha)
                if not afiliacion_objs.exists():
                    context["error_msg"] = "No existe informacion sobre afiliaciones."
                    return render_to_response('salary_calculated.html', context)
                afiliacion_obj = afiliacion_objs.order_by('vigencia_hasta')[afiliacion_objs.count()-1]
                af_importe = total_bruto * afiliacion_obj.porcentaje / 100.0 
                # en caso de exisitr, los guardo en el context.
                context['afiliacion'] = afiliacion_obj
                context['afiliacion_importe'] = af_importe

            acum_ret += af_importe
            total_neto = total_neto - acum_ret + acum_rem

            # Hago el merge de los dos contexts.
            context['total_rem'] = total_rem + acum_rem
            context['total_ret'] = total_ret + acum_ret
            context['total_bruto'] = total_bruto
            context['total_neto'] = total_neto
            context['lista_res'] = context_univ['lista_res']
            context['lista_res'].extend(context_preuniv['lista_res'])
            context['fecha'] = fecha
            context['ret_fijas_persona'] = ret_fijas_persona
            context['ret_porc_persona'] = ret_porc_persona

            return render_to_response('salary_calculated.html', context)

        else:
            context['univformset'] = univformset
            context['preunivformset'] = preunivformset
            context['commonform'] = commonform

    else:

        # Creamos formularios vacios (sin bindear) y los mandamos.
        univformset = CargoUnivFormSet(prefix='univcargo')
        preunivformset = CargoPreUnivFormSet(prefix='preunivcargo')
        commonform = CommonForm()

        context['univformset'] = univformset
        context['preunivformset'] = preunivformset
        context['commonform'] = commonform

    return render_to_response('calculate.html', context)


def processUnivFormSet(fecha, antiguedad, univformset):
    """Procesa un formset con formularios de cargos universitarios. Retorna un context"""

    #NOTA: Sobre el cálculo, según las tablas:
    # importe = basico_sep11 + aumento2003 + acum (= basicoREFerencia*12% o 18%)
    # sueldo_bruto = importe*antiguedad%

    context = {}

    #guardo en esta lista un diccionario para cada formulario procesado
    #en cada una de estas, los resultados para renderizar luego.
    lista_res = list()

    # Itero sobre todos los cargos.
    total_rem = 0.0
    total_ret = 0.0
    total_bruto = 0.0
    total_neto = 0.0

    # Retenciones / Remuneraciones que son por persona (no por cargo).
    ret_fijas_persona = RetencionFija.objects.filter(
        retencion__aplicacion='U',
        retencion__modo='P',
        vigencia_desde__lte=fecha,
        vigencia_hasta__gte=fecha
    )
    ret_porc_persona  = RetencionPorcentual.objects.filter(
        retencion__aplicacion='U',
        retencion__modo='P',
        vigencia_desde__lte=fecha,
        vigencia_hasta__gte=fecha
    )
    rem_fijas_persona = RemuneracionFija.objects.filter(
        remuneracion__aplicacion='U',
        remuneracion__modo='P',
        vigencia_desde__lte=fecha,
        vigencia_hasta__gte=fecha
    )
    rem_porc_persona  = RemuneracionPorcentual.objects.filter(
        remuneracion__aplicacion='U',
        remuneracion__modo='P',
        vigencia_desde__lte=fecha,
        vigencia_hasta__gte=fecha
    )


    for univform in univformset:

        # No analizamos los forms que fueron borrados por el usuario.
        if univform in univformset.deleted_forms:
            continue

        cargo_obj = univform.cleaned_data['cargo']
        has_doctorado = univform.cleaned_data['doctorado']
        has_master = univform.cleaned_data['master']

        # Retenciones / Remuneraciones que son por cargo.
        ret_porcentuales = RetencionPorcentual.objects.filter(
            retencion__aplicacion='U',
            retencion__modo='C',
            vigencia_desde__lte=fecha,
            vigencia_hasta__gte=fecha
        )
        ret_fijas = RetencionFija.objects.filter(
            retencion__aplicacion='U',
            retencion__modo='C',
            vigencia_desde__lte=fecha,
            vigencia_hasta__gte=fecha
        )
        rem_porcentuales = RemuneracionPorcentual.objects.filter(
            remuneracion__aplicacion='U',
            remuneracion__modo='C',
            vigencia_desde__lte=fecha,
            vigencia_hasta__gte=fecha
        )
        rem_fijas = RemuneracionFija.objects.filter(
            remuneracion__aplicacion='U',
            remuneracion__modo='C',
            vigencia_desde__lte=fecha,
            vigencia_hasta__gte=fecha
        )

        # Obtengo la Antiguedad
        antiguedades = AntiguedadUniversitaria.objects.filter(anio=antiguedad, vigencia_desde__lte=fecha, vigencia_hasta__gte=fecha)
        antiguedad = None
        if not antiguedades.exists():
            context['error_msg'] = u'No existe información de Antigüedad para los datos ingresados. Por favor introduzca otros datos.'
            return context
        else:
            antiguedad = antiguedades.order_by('vigencia_hasta')[antiguedades.count()-1]
            for ant in antiguedades:
                rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo = ant.remuneracion.codigo)

        ###### Salario Bruto.
        basicos = SalarioBasico.objects.filter(cargo=cargo_obj, vigencia_desde__lte=fecha, vigencia_hasta__gte=fecha)
        basico = None
        if not basicos.exists():
            context['error_msg'] = u'No existe información de Salarios Básicos para los datos ingresados. Por favor introduzca otros datos.'
            return context
        else:
            basico = basicos.order_by('vigencia_hasta')[basicos.count()-1]
            for bas in basicos:
                rem_fijas = rem_fijas.exclude(remuneracion__codigo = bas.remuneracion.codigo)
        antiguedad_importe = basico.valor * antiguedad.porcentaje / 100.0
        salario_bruto = basico.valor + antiguedad_importe


        ###### El Neto se calcula del bruto restando las retenciones y sumando las remuneraciones.

        ret_list = list()   # Aqui iran tuplas de la forma (obj retencion, importe) para mostrar esta info en el template.
        rem_list = list()  # De forma similar, tendra tuplas (obj remuneracion, importe)

        acum_ret = 0.   # El acumulado de todo lo que hay que descontarle al bruto.
        acum_rem = 0. # El acumulado de todo lo que hay que sumarle.

        #Adicional titulo doctorado (cod 51), Adicional titulo maestria (cod 52)
        if has_doctorado:
            rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo=master_code)
        elif has_master:
            rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo=doc_code)
        else:
            rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo=doc_code)
            rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo=master_code)

        ## Retenciones / Remuneraciones NO especiales:

        for ret in ret_porcentuales:
            importe = salario_bruto * ret.porcentaje / 100.
            acum_ret += importe
            ret_list.append( (ret, importe) )

        for ret in ret_fijas:
                acum_ret += ret.valor
                ret_list.append( (ret, ret.valor) )

        for rem in rem_porcentuales:
            importe = salario_bruto * rem.porcentaje / 100.
            acum_rem += importe
            rem_list.append( (rem, importe) )

        for rem in rem_fijas:
            acum_rem += rem.valor
            rem_list.append( (rem, rem.valor) )

        ###### Salario Neto.
        salario_neto = salario_bruto - acum_ret + acum_rem

        ## Garantia salarial.
        garantias_salariales = GarantiaSalarial.objects.filter(cargo=cargo_obj, vigencia_desde__lte=fecha, vigencia_hasta__gte=fecha)
        
        if garantias_salariales.exists():

            garantia_obj = garantias_salariales.order_by('vigencia_hasta')[garantias_salariales.count()-1]
            valor_minimo = garantia_obj.valor_minimo

            if salario_neto < valor_minimo:
  
                if garantia_obj.antiguedad_min <= antiguedad.anios and antiguedad.anios < garantia_obj.antiguedad_max:

                    if has_doctorado:
                        valor = garantia_obj.valor_doctorado
                    elif has_master:
                        valor = garantia_obj.valor_master
                    else:
                        valor = garantia_obj.valor_st

                    #el neto + garantia no puede superar la cota de garantia.
                    total = max(valor_minimo, salario_neto+valor)

                    garantia = total - salario_neto

                    rem_obj = RemuneracionFija(
                        codigo=garantia_code,
                        nombre= garantia_name + ' (' + unicode(garantia_obj) + ')',
                        aplicacion='U', valor=garantia
                    )
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
            'basico': basico.valor,
            'retenciones': ret_list,
            'remuneraciones': rem_list,
            'acum_ret': acum_ret,
            'acum_rem': acum_rem,
            'salario_bruto': salario_bruto,
            'salario_neto': salario_neto,
            'antiguedad': antiguedad,
            'antiguedad_importe':antiguedad.porcentaje
        }
        lista_res.append(form_res)

    context['total_rem'] = total_rem
    context['total_ret'] = total_ret
    context['total_bruto'] = total_bruto
    context['total_neto'] = total_neto
    context['lista_res'] = lista_res
    context['ret_fijas_persona'] = ret_fijas_persona
    context['ret_porc_persona'] = ret_porc_persona

    return context



def processPreUnivFormSet(fecha, antiguedad, preunivformset):
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

    # Retenciones / Remuneraciones que son por persona (no por cargo).
    ret_fijas_persona = RetencionFija.objects.filter(
        retencion__aplicacion='U',
        retencion__modo='P',
        vigencia_desde__lte=fecha,
        vigencia_hasta__gte=fecha
    )
    ret_porc_persona  = RetencionPorcentual.objects.filter(
        retencion__aplicacion='U',
        retencion__modo='P',
        vigencia_desde__lte=fecha,
        vigencia_hasta__gte=fecha
    )
    rem_fijas_persona = RemuneracionFija.objects.filter(
        remuneracion__aplicacion='U',
        remuneracion__modo='P',
        vigencia_desde__lte=fecha,
        vigencia_hasta__gte=fecha
    )
    rem_porc_persona  = RemuneracionPorcentual.objects.filter(
        remuneracion__aplicacion='U',
        remuneracion__modo='P',
        vigencia_desde__lte=fecha,
        vigencia_hasta__gte=fecha
    )

    for preunivform in preunivformset:

        if preunivform in preunivformset.deleted_forms:
            continue
		
        cargo_obj = preunivform.cleaned_data['cargo']
        has_doctorado = preunivform.cleaned_data['doctorado']
        has_master = preunivform.cleaned_data['master']
        horas = preunivform.cleaned_data['horas']

        # Obtengo la Antiguedad
        antiguedades = AntiguedadPreUniversitaria.objects.filter(anio=antiguedad, vigencia_desde__lte=fecha, vigencia_hasta__gte=fecha)
        antiguedad = None
        if not antiguedades.exists():
            context['error_msg'] = u'No existe información de Antigüedad para los datos ingresados. Por favor introduzca otros datos.'
            return context
        else:
            antiguedad = antiguedades.order_by('vigencia_hasta')[antiguedades.count()-1]
            for ant in antiguedades:
                rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo = ant.remuneracion.codigo)

        ###### Salario Bruto.
        basicos = SalarioBasico.objects.filter(cargo=cargo_obj, vigencia_desde__lte=fecha, vigencia_hasta__gte=fecha)
        basico = None
        antiguedad_importe = 0.0
        salario_bruto = 0.0
        if not basicos.exists():
            context['error_msg'] = u'No existe información de Salarios Básicos para los datos ingresados. Por favor introduzca otros datos.'
            return context
        else:
            basico = basicos.order_by('vigencia_hasta')[basicos.count()-1]
            for bas in basicos:
                rem_fijas = rem_fijas.exclude(remuneracion__codigo = bas.remuneracion.codigo)

        if cargo_obj.pago_por_hora:
            antiguedad_importe = basico.valor * horas * antiguedad.porcentaje / 100.0
            salario_bruto = basico.valor * horas + antiguedad_importe
        else:
            antiguedad_importe = basico.valor * antiguedad.porcentaje / 100.0
            salario_bruto = basico.valor + antiguedad_importe
        

        ###### El Neto se calcula del bruto restando las retenciones y sumando las remuneraciones.

        ret_list = list()   # Aqui iran tuplas de la forma (obj retencion, importe) para mostrar esta info en el template
        rem_list = list()  # De forma similar, va a tener tuplas (obj remuneracion, importe)

        acum_ret = 0.   # El acumulado de todo lo que hay que descontarle al bruto.
        acum_rem = 0. # El acumulado de todo lo que hay que sumarle.


        ## Remuneraciones Especiales:        

        # Adicional titulo doctorado nivel medio (cod 53), Adicional titulo maestria nivel medio (cod 55)
        if has_doctorado:
            rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo=master_preuniv_code)
        elif has_master:
            rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo=doc_preuniv_code)
        else:
            rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo=doc_preuniv_code)
            rem_porcentuales = rem_porcentuales.exclude(remuneracion__codigo=master_preuniv_code)


        ## Retenciones NO especiales:

        for ret in ret_porcentuales:
                importe = salario_bruto * ret.porcentaje / 100.
                acum_ret = acum_ret + importe
                ret_list.append( (ret, importe) )

        for ret in ret_fijas:
                acum_ret = acum_ret + ret.valor
                ret_list.append( (ret, ret.valor) )

        for rem in rem_porcentuales:
                importe = salario_bruto * rem.porcentaje / 100.
                acum_rem = acum_rem + importe
                rem_list.append( (rem, importe) )


        ## FONID
        fonid = 0.0
        for rem in rem_fijas:
            if rem.remuneracion.codigo == '122': #fonid
                fonid = float(rem.valor)
            else:
                acum_rem = acum_rem + rem.valor
            rem_list.append( (rem, rem.valor) )


        ###### Salario Neto.
        salario_neto = salario_bruto - acum_ret + acum_rem + fonid

        ## Garantia salarial.
        garantias_salariales = GarantiaSalarial.objects.filter(cargo=cargo_obj, vigencia_desde__lte=fecha, vigencia_hasta__gte=fecha)

        if garantiaes_salariales.exists():

            garantia_obj = garantia_salarial_objs.order_by('vigencia_hasta')[garantia_salarial_objs.count()-1]
            valor_minimo = garantia_obj.valor_minimo

            if salario_neto < valor_minimo:

                if garantia_obj.antiguedad_min <= antiguedad.anios and antiguedad.anios < garantia_obj.antiguedad_max:
  
                    if has_doctorado:
                        valor = garantia_obj.valor_doctorado
                    elif has_master:
                        valor = garantia_obj.valor_master
                    else:
                        valor = garantia_obj.valor_st

                    #el neto + garantia no puede superar la cota de garantia.
                    total = max(valor_minimo,salario_neto+valor)

                    garantia = total - salario_neto

                    rem_obj = RemuneracionFija(
                        codigo=garantia_code,
                        nombre= garantia_name + ' (' + unicode(garantia_obj) + ')',
                        aplicacion='U',
                        valor=garantia
                    )
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
            'basico': basico.valor,
            'retenciones': ret_list,
            'remuneraciones': rem_list,
            'acum_ret': acum_ret,
            'acum_rem': acum_rem,
            'salario_bruto': salario_bruto,
            'salario_neto': salario_neto,
            'antiguedad': antiguedad,
            'antiguedad_importe': antiguedad_importe
        }
        lista_res.append(form_res)

    context['total_rem'] = total_rem
    context['total_ret'] = total_ret
    context['total_bruto']= total_bruto
    context['total_neto'] = total_neto
    context['lista_res'] = lista_res

    return context
