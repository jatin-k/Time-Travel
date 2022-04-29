from django import forms
from .models import TravelDetail



class TravelForm(forms.ModelForm):

	class Meta:
		model = TravelDetail
		fields = ("subject", "message", "date",)