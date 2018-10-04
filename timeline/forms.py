from django import forms
from django.contrib.admin import widgets 
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

class filter_form(forms.Form):

	def __init__(self,launchsite_list, *args,**kwargs):
		# self.launchsite_list = kwargs.pop('launchsite_list')
		self.launchsite_list = launchsite_list
		super(filter_form,self).__init__(*args,**kwargs)
		self.fields['launchsite'].widget = forms.Select(choices=self.launchsite_list)

	
	launchsite = forms.CharField(label="Launch Site", required = False,widget = forms.Select(choices = [('Select','Select')]))
	mission_types = [(0,'Select'),(1,'Unmanned'),(2,'Manned')]
	typeofmission = forms.IntegerField(label = 'Type of Mission',widget =forms.Select(choices=[(0,'Select'),(1,'Unmanned'),(2,'Manned')]), required = False)
	launchdate_from = forms.DateField(label = 'From ',widget = widgets.AdminDateWidget(), required = False)
	launchdate_to = forms.DateField(label = 'To ',widget = widgets.AdminDateWidget(), required = False)
	mission_duration_min = forms.IntegerField(label = 'Minimum: ', required = False)
	mission_duration_max = forms.IntegerField(label = 'Maximum: ', required = False)

	def clean_mission_duration_min(self):
		data = self.cleaned_data['mission_duration_min']
		if data is not None and data < 0:
			raise ValidationError(_('Invalid entry - negative months'))
		return data

	def clean_mission_duration_max(self):
		data = self.cleaned_data['mission_duration_max']
		if data is not None and data<0:
			raise ValidationError(_('Invalid entry - negative months'))
		return data

	def clean(self):
		super().clean()
		duration_min = self.cleaned_data.get('mission_duration_min')
		duration_max = self.cleaned_data.get('mission_duration_max')
		if duration_min is not None and duration_min < 0:
			raise ValidationError(_('Invalid entry - negative months'))
		if duration_max is not None and duration_max < 0:
			raise ValidationError(_('Invalid entry - negative months'))
		if duration_min is not None and duration_max is not None and duration_min > duration_max:
			raise ValidationError(_('Invalid entry - negative duration'))
