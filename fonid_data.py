#para correr sobre el shell
#python manage.py shell
#from salary_calculator_app import RemuneracionFija, RemuneracionRetencion

fonid_values = [
    '430',
    '189.26',
    '215',
    '257.88',
    '129',
    '430',
    '178.49',
    '184.53',
    '17.92',
    '14.33',
    '171.92',
    '161.25',
    '429.84',
    '343.84',
    '208.71',
    '215',
    '161.25',
    '213.63',
    '14.33',
    '107.50'
]

for v in fonid_values:
    r = RemuneracionFija(codigo="122",nombre="FONID",aplicacion='P',valor=v)
    r.save()
