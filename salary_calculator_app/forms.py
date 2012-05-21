from django import forms

year_choices = (
('0','0'),
('1','1'),
('2','2'),
('5','5'),
('7','7'),
('10','10'),
('12','12'),
('15','15'),
('17','17'),
('20','20'),
('22','22'),
('24','24'),

)

class CargoForm(forms.Form):
	tipo 		= forms.CharField(max_length=50)
	antiguedad 	= forms.ChoiceField(choices=year_choices)
	master 		= forms.BooleanField(required=False)
	doctorado 	= forms.BooleanField(required=False)
